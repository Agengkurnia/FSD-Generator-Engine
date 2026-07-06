"""Shared build helpers for FSD Generator Engine modules."""
import base64
import os
import re
import subprocess
import urllib.request
import zlib

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from fsd_cover_merge import content_start_index, COVER_TABLE_COUNT
from fsd_captions import caption_number_from_text
from fsd_paths import REFERENCE_DOCX

HEADER_BG = 'D9EAD3'
BORDER_COLOR = '000000'
FONT_NAME = 'Calibri'
FONT_SIZE_BODY = 11
FONT_SIZE_TABLE = 9


def render_kroki(mermaid_code: str, output_path: str, label: str) -> bool:
    return _render_kroki(mermaid_code, output_path, label, 'mermaid')


def render_kroki_plantuml(plantuml_code: str, output_path: str, label: str) -> bool:
    return _render_kroki(plantuml_code, output_path, label, 'plantuml')


def _render_kroki(code: str, output_path: str, label: str, engine: str) -> bool:
    try:
        compressed = zlib.compress(code.strip().encode('utf-8'), 9)
        b64 = base64.urlsafe_b64encode(compressed).decode('ascii')
        url = f'https://kroki.io/{engine}/png/{b64}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(data)
        print(f'   [{label}] OK {len(data):,} bytes -> {os.path.basename(output_path)}')
        return True
    except Exception as e:
        print(f'   [{label}] FAIL: {e}')
        return False


def is_swimlane_mermaid(code: str) -> bool:
    """True if Mermaid code uses 2+ subgraph lanes (cross-functional swimlane)."""
    return len(re.findall(r'^\s*subgraph\s+', code, flags=re.MULTILINE)) >= 2


def is_swimlane_plantuml(code: str) -> bool:
    """True if PlantUML activity diagram uses swimlane separators (|Role|)."""
    return len(re.findall(r'^\s*\|[^|]+\|\s*$', code, flags=re.MULTILINE)) >= 2


PLANTUML_SWIMLANE_SKINPARAM = """
skinparam partition {
  BackgroundColor #D9EAD3
  BorderColor #000000
  FontStyle bold
  BorderThickness 2
}
skinparam activity {
  BackgroundColor #FFFFFF
  BorderColor #000000
  StartColor #C8E6C9
  EndColor #B2DFDB
}
""".strip()


def inject_plantuml_swimlane_style(code: str) -> str:
    """Inject standard swimlane skinparam after @startuml when missing."""
    if not is_swimlane_plantuml(code):
        return code
    if re.search(r'skinparam\s+partition\b', code, flags=re.I):
        return code
    m = re.search(r'(@startuml[^\n]*\n)', code, flags=re.I)
    if not m:
        return code
    insert_at = m.end()
    return code[:insert_at] + PLANTUML_SWIMLANE_SKINPARAM + '\n' + code[insert_at:]


def body_content_start_index(doc, marker: str = '1. Pendahuluan') -> int:
    """First body paragraph: Daftar Gambar (if any) else chapter 1."""
    for i, p in enumerate(doc.paragraphs):
        t = (p.text or '').strip()
        if t == 'Daftar Gambar':
            return i
    return content_start_index(doc, marker)


def run_pandoc(md_tmp: str, docx_out: str, resource_dirs: list[str], cwd: str):
    paths = ';'.join(resource_dirs)
    cmd = [
        'pandoc', md_tmp, '-o', docx_out,
        '--from=markdown+pipe_tables',
        f'--resource-path={paths}',
    ]
    if os.path.exists(REFERENCE_DOCX):
        cmd.append(f'--reference-doc={REFERENCE_DOCX}')
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:800])


def _set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        if edge in kwargs:
            tag = f'w:{edge}'
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for k, v in kwargs[edge].items():
                element.set(qn(f'w:{k}'), str(v))


def _set_cell_bg(cell, color: str):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcPr = cell._tc.get_or_add_tcPr()
    existing = tcPr.find(qn('w:shd'))
    if existing is not None:
        tcPr.remove(existing)
    tcPr.append(shd)


def _apply_font(run, size_pt: int, bold=None):
    run.font.name = FONT_NAME
    run.font.size = Pt(size_pt)
    rPr = run._r.get_or_add_rPr()
    el = rPr.find(qn('w:rFonts'))
    if el is None:
        el = OxmlElement('w:rFonts')
        rPr.insert(0, el)
    el.set(qn('w:ascii'), FONT_NAME)
    el.set(qn('w:hAnsi'), FONT_NAME)
    el.set(qn('w:cs'), FONT_NAME)
    if bold is not None:
        run.bold = bold


def _add_bookmark(para, bookmark_name: str, bookmark_id: int):
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(bookmark_id))
    start.set(qn('w:name'), bookmark_name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), str(bookmark_id))
    para._p.insert(0, start)
    para._p.append(end)


def _set_paragraph_pageref(para, bookmark_name: str):
    for child in list(para._p):
        para._p.remove(child)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), f'PAGEREF {bookmark_name} \\h')
    run = OxmlElement('w:r')
    t = OxmlElement('w:t')
    t.text = '?'
    run.append(t)
    fld.append(run)
    para._p.append(fld)


def _is_daftar_table(table) -> bool:
    if not table.rows:
        return False
    cells = [c.text.strip().lower() for c in table.rows[0].cells]
    return len(cells) >= 3 and cells[0] == 'no.' and 'judul' in cells[1] and 'halaman' in cells[2]


def postprocess_captions(doc, content_start: int):
    bookmark_id = 1
    pageref_re = re.compile(r'\{PAGEREF:([a-zA-Z0-9_]+)\}')

    for i, para in enumerate(doc.paragraphs):
        if i < content_start:
            continue
        raw = (para.text or '').strip()
        if not raw:
            continue
        info = caption_number_from_text(raw)
        if not info:
            continue
        _, bookmark_name = info
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.italic = True
            _apply_font(run, FONT_SIZE_BODY)
        _add_bookmark(para, bookmark_name, bookmark_id)
        bookmark_id += 1

    for table in doc.tables:
        if not _is_daftar_table(table):
            continue
        for row in table.rows[1:]:
            if len(row.cells) < 3:
                continue
            cell = row.cells[2]
            m = pageref_re.search(cell.text or '')
            if not m:
                continue
            bookmark_name = m.group(1)
            para = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
            _set_paragraph_pageref(para, bookmark_name)


def postprocess_docx(docx_path: str, max_width_cm: float = 15.0):
    doc = Document(docx_path)
    content_start = body_content_start_index(doc)
    try:
        doc.styles['Normal'].font.name = FONT_NAME
        doc.styles['Normal'].font.size = Pt(FONT_SIZE_BODY)
    except Exception:
        pass
    for i, para in enumerate(doc.paragraphs):
        if i < content_start:
            continue
        for run in para.runs:
            _apply_font(run, FONT_SIZE_BODY)
    border_spec = {"sz": "8", "val": "single", "color": BORDER_COLOR}
    bdr_all = dict(top=border_spec, bottom=border_spec, start=border_spec, end=border_spec,
                   insideH=border_spec, insideV=border_spec)
    for ti, table in enumerate(doc.tables):
        if ti < COVER_TABLE_COUNT:
            continue
        try:
            table.style = 'Table Grid'
        except Exception:
            pass
        for row_idx, row in enumerate(table.rows):
            is_header = row_idx == 0
            for cell in row.cells:
                _set_cell_border(cell, **bdr_all)
                if is_header:
                    _set_cell_bg(cell, HEADER_BG)
                for para in cell.paragraphs:
                    for run in para.runs:
                        _apply_font(run, FONT_SIZE_TABLE, bold=True if is_header else None)
    max_w = Cm(max_width_cm)
    ns = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
    for para in doc.paragraphs:
        for run in para.runs:
            for drawing in run._r.findall(f'.//{ns}inline'):
                extent = drawing.find(f'{ns}extent')
                if extent is not None:
                    cx = int(extent.get('cx', 0))
                    if cx > max_w.emu:
                        ratio = max_w.emu / cx
                        cy = int(int(extent.get('cy', 0)) * ratio)
                        extent.set('cx', str(max_w.emu))
                        extent.set('cy', str(cy))
    postprocess_captions(doc, content_start)
    doc.save(docx_path)
