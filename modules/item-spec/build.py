"""
Build FSD Item Spec RM v1.2 → DOCX (Kalbe cover standard).

Run:
    py build.py
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import base64
import os
import re
import subprocess
import urllib.request
import zlib

from docx import Document
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_cover_merge import (
    parse_md_cover_meta,
    strip_md_for_body,
    merge_cover_and_content,
    content_start_index,
    COVER_TABLE_COUNT,
)
from fsd_paths import (
    COVER_TEMPLATE,
    LOGO_PATH,
    REFERENCE_DOCX,
    TMP_DIR,
    engine_root_from_script,
)

ENGINE_ROOT = engine_root_from_script(__file__)
MODULE_SLUG = 'item-spec'
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, 'output'), exist_ok=True)

MD_SRC = os.path.join(SCRIPT_DIR, 'source', 'FSD_ItemSpec_RM_v1.2.md')
MD_TMP = os.path.join(TMP_DIR, f'{MODULE_SLUG}_processed.md')
DOCX_CONTENT_TMP = os.path.join(TMP_DIR, f'{MODULE_SLUG}_content.docx')
DOCX_OUT = os.path.join(SCRIPT_DIR, 'output', 'FSD_ItemSpec_RM_v1.2.docx')
SCREENSHOTS = os.path.join(SCRIPT_DIR, 'screenshots')
COVER_META = {}

FLOW_MAIN_PNG = os.path.join(SCREENSHOTS, 'itemspec_rm_flow_main.png')
FLOW_APPROVAL_PNG = os.path.join(SCREENSHOTS, 'itemspec_rm_flow_approval.png')
ERD_PNG = os.path.join(SCREENSHOTS, 'itemspec_rm_erd.png')

HEADER_BG = 'D9EAD3'
BORDER_COLOR = '000000'
FONT_NAME = 'Calibri'
FONT_SIZE_BODY = 11
FONT_SIZE_TABLE = 9

os.makedirs(SCREENSHOTS, exist_ok=True)


def render_kroki(mermaid_code: str, output_path: str, label: str) -> bool:
    try:
        compressed = zlib.compress(mermaid_code.strip().encode('utf-8'), 9)
        b64 = base64.urlsafe_b64encode(compressed).decode('ascii')
        url = f'https://kroki.io/mermaid/png/{b64}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
        with open(output_path, 'wb') as f:
            f.write(data)
        print(f'   [{label}] OK {len(data):,} bytes -> {os.path.basename(output_path)}')
        return True
    except Exception as e:
        print(f'   [{label}] FAIL: {e}')
        return False


def step1_render_diagrams(md_content: str):
    print('\n[STEP 1] Render diagram Mermaid via Kroki.io...')
    blocks = list(re.finditer(r'```mermaid\s*\n(.*?)```', md_content, flags=re.DOTALL))
    print(f'   Blok Mermaid: {len(blocks)}')
    for i, match in enumerate(blocks):
        code = match.group(1).strip()
        if 'flowchart LR' in code and 'subgraph PDV' in code and 'subgraph QAQS' in code:
            render_kroki(code, FLOW_MAIN_PNG, 'Flow-Main-Swimlane')
        elif 'flowchart LR' in code and 'Creator' in code and 'WaitApproval' in code:
            render_kroki(code, FLOW_APPROVAL_PNG, 'Flow-Approval')
        elif 'erDiagram' in code and 'TrItemSpecRM_Header' in code:
            render_kroki(code, ERD_PNG, 'ERD-Main')
        else:
            render_kroki(code, os.path.join(SCREENSHOTS, f'itemspec_rm_diagram_{i + 1}.png'), f'Diagram-{i + 1}')


def _rel(path: str) -> str:
    return os.path.relpath(path, SCRIPT_DIR).replace('\\', '/')


def step2_preprocess():
    global COVER_META
    print('\n[STEP 2] Pre-processing Markdown...')
    with open(MD_SRC, 'r', encoding='utf-8') as f:
        raw = f.read()
    COVER_META = parse_md_cover_meta(raw)
    text = strip_md_for_body(raw)
    step1_render_diagrams(text)

    counter = [0]

    def replace_mermaid(m):
        code = m.group(1).strip()
        counter[0] += 1
        i = counter[0]
        if 'flowchart LR' in code and 'subgraph PDV' in code and 'subgraph QAQS' in code:
            png, caption = FLOW_MAIN_PNG, 'Business Flow Diagram Swimlane – Item Spec RM'
        elif 'flowchart LR' in code and 'Creator' in code and 'WaitApproval' in code:
            png, caption = FLOW_APPROVAL_PNG, 'Approval Flow – Item Spec RM'
        elif 'erDiagram' in code and 'TrItemSpecRM_Header' in code:
            png, caption = ERD_PNG, 'ERD – Entity Relationship Diagram Item Spec RM'
        else:
            png = os.path.join(SCREENSHOTS, f'itemspec_rm_diagram_{i}.png')
            caption = f'Diagram {i}'
        if os.path.exists(png):
            return f'\n![{caption}]({_rel(png)})\n'
        return f'\n> *[{caption} – diagram tidak dapat di-render]*\n'

    text = re.sub(r'```mermaid\s*\n(.*?)```', replace_mermaid, text, flags=re.DOTALL)
    with open(MD_TMP, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'   OK -> {os.path.basename(MD_TMP)}')


def step3_pandoc():
    print('\n[STEP 3] Pandoc MD -> DOCX (isi bab)...')
    cmd = [
        'pandoc', MD_TMP,
        '-o', DOCX_CONTENT_TMP,
        '--from=markdown+pipe_tables',
        f'--resource-path={SCRIPT_DIR};{SCREENSHOTS}',
    ]
    if os.path.exists(REFERENCE_DOCX):
        cmd.append(f'--reference-doc={REFERENCE_DOCX}')
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRIPT_DIR)
    if result.returncode != 0:
        print(result.stderr[:800])
        raise RuntimeError('pandoc failed')
    print(f'   OK -> {os.path.basename(DOCX_CONTENT_TMP)}')


def step3b_merge_cover():
    print('\n[STEP 3b] Gabung cover + revision template...')
    merge_cover_and_content(DOCX_CONTENT_TMP, DOCX_OUT, COVER_META)
    print(f'   OK -> {os.path.basename(DOCX_OUT)}')


def set_cell_border(cell, **kwargs):
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


def set_cell_bg(cell, color: str):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcPr = cell._tc.get_or_add_tcPr()
    existing = tcPr.find(qn('w:shd'))
    if existing is not None:
        tcPr.remove(existing)
    tcPr.append(shd)


def apply_font(run, size_pt: int, bold=None):
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


def step4_postprocess():
    print('\n[STEP 4] Post-process DOCX...')
    from fsd_build import postprocess_docx
    postprocess_docx(DOCX_OUT)
    print(f'   OK -> {DOCX_OUT}')


if __name__ == '__main__':
    print('=' * 65)
    print('  BUILD: FSD Item Spec RM v1.2')
    print('=' * 65)
    if not os.path.exists(MD_SRC):
        print(f'ERROR: {MD_SRC} tidak ditemukan')
        sys.exit(1)
    step2_preprocess()
    step3_pandoc()
    step3b_merge_cover()
    step4_postprocess()
    for tmp in (MD_TMP, DOCX_CONTENT_TMP):
        if os.path.exists(tmp):
            os.remove(tmp)
    print(f'\nSELESAI: {DOCX_OUT}')
