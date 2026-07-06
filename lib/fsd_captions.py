"""Auto-number figures/tables and inject Daftar Gambar / Daftar Tabel sections."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

FIG_CAPTION_RE = re.compile(r'^\*?Gambar\s+(\d+(?:\.\d+)*)\s*[—–-]\s*(.+?)\*?$')
TBL_CAPTION_RE = re.compile(r'^\*?Tabel\s+(\d+(?:\.\d+)*)\s*[—–-]\s*(.+?)\*?$')
CHAPTER_RE = re.compile(r'^##\s+(\d+)\.\s+')
SUBSECTION_RE = re.compile(r'^###\s+(\d+)\.(\d+)\s+')
IMAGE_RE = re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$')
TABLE_ROW_RE = re.compile(r'^\|.+\|$')
TABLE_SEP_RE = re.compile(r'^\|[\s|:\-]+\|$')
BOLD_LINE_RE = re.compile(r'^\*\*(.+?)\*\*\s*$')
LANE_TABLE_MARKERS = ('| # | Lane ID |', '| # | Lane ID|', 'Lane ID | Label')


@dataclass
class CaptionEntry:
    kind: str
    number: str
    title: str
    bookmark: str


@dataclass
class CaptionRegistry:
    figures: list[CaptionEntry] = field(default_factory=list)
    tables: list[CaptionEntry] = field(default_factory=list)


def _bookmark_id(kind: str, number: str) -> str:
    parts = number.split('.')
    prefix = 'fig' if kind == 'fig' else 'tbl'
    return f'{prefix}_' + '_'.join(parts)


def _is_lane_table(lines: list[str], start: int) -> bool:
    block = '\n'.join(lines[start:min(start + 4, len(lines))])
    return any(m in block for m in LANE_TABLE_MARKERS)


def _is_daftar_table_header(lines: list[str], start: int) -> bool:
    line = lines[start].strip().lower()
    return '| no.' in line and 'judul' in line and 'halaman' in line


def _is_separator_row(line: str) -> bool:
    return bool(TABLE_SEP_RE.match(line.strip()))


def _extract_table_block(lines: list[str], start: int) -> tuple[int, list[str]]:
    end = start
    while end < len(lines) and TABLE_ROW_RE.match(lines[end].strip()):
        end += 1
    return end, lines[start:end]


def _table_title(lines: list[str], table_start: int) -> str:
    idx = table_start - 1
    while idx >= 0:
        line = lines[idx].strip()
        if not line:
            idx -= 1
            continue
        if TBL_CAPTION_RE.match(line):
            return ''
        m = BOLD_LINE_RE.match(line)
        if m:
            return m.group(1).strip()
        if line.startswith('#'):
            break
        idx -= 1
    _, table_lines = _extract_table_block(lines, table_start)
    if table_lines:
        header_cells = [c.strip() for c in table_lines[0].strip('|').split('|')]
        if header_cells:
            return header_cells[0]
    return 'Tabel'


def _format_caption(kind: str, number: str, title: str) -> str:
    label = 'Gambar' if kind == 'fig' else 'Tabel'
    return f'*{label} {number} — {title}*'


def _build_daftar_sections(registry: CaptionRegistry) -> str:
    parts: list[str] = []

    if registry.figures:
        parts.append('## Daftar Gambar\n')
        parts.append('| No. | Judul | Halaman |')
        parts.append('|-----|-------|---------|')
        for e in registry.figures:
            parts.append(
                f'| Gambar {e.number} | {e.title} | {{PAGEREF:{e.bookmark}}} |'
            )
        parts.append('')

    if registry.tables:
        parts.append('## Daftar Tabel\n')
        parts.append('| No. | Judul | Halaman |')
        parts.append('|-----|-------|---------|')
        for e in registry.tables:
            parts.append(
                f'| Tabel {e.number} | {e.title} | {{PAGEREF:{e.bookmark}}} |'
            )
        parts.append('')

    if parts:
        parts.append('')
    return '\n'.join(parts)


def preprocess_captions(md_text: str) -> tuple[str, CaptionRegistry]:
    """Number images/tables, add captions, inject Daftar sections before chapter 1."""
    registry = CaptionRegistry()
    lines = md_text.splitlines()
    out: list[str] = []

    chapter: int | None = None
    subsection: int | None = None
    fig_counter = 0
    tbl_counter = 0
    in_code = False
    in_table = False
    prev_line = ''

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code = not in_code
            out.append(line)
            i += 1
            prev_line = stripped
            continue

        if in_code:
            out.append(line)
            i += 1
            prev_line = stripped
            continue

        m_ch = CHAPTER_RE.match(stripped)
        if m_ch:
            chapter = int(m_ch.group(1))
            subsection = None
            fig_counter = 0
            tbl_counter = 0

        m_sub = SUBSECTION_RE.match(stripped)
        if m_sub:
            subsection = int(m_sub.group(2))
            tbl_counter = 0

        if stripped.startswith('## Daftar Gambar') or stripped.startswith('## Daftar Tabel'):
            while i < len(lines) and not CHAPTER_RE.match(lines[i].strip()):
                i += 1
            continue

        img = IMAGE_RE.match(stripped)
        if img and chapter is not None:
            alt = img.group(1).strip()
            path = img.group(2)
            next_stripped = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if not FIG_CAPTION_RE.match(next_stripped):
                fig_counter += 1
                number = f'{chapter}.{fig_counter}'
                title = alt or f'Gambar {number}'
                bookmark = _bookmark_id('fig', number)
                registry.figures.append(CaptionEntry('fig', number, title, bookmark))
                out.append(line)
                out.append('')
                out.append(_format_caption('fig', number, title))
                i += 1
                prev_line = _format_caption('fig', number, title)
                continue

        if TABLE_ROW_RE.match(stripped) and chapter is not None:
            if in_table or _is_separator_row(stripped):
                out.append(line)
                i += 1
                prev_line = stripped
                continue
            if _is_lane_table(lines, i) or _is_daftar_table_header(lines, i):
                in_table = True
                out.append(line)
                i += 1
                prev_line = stripped
                continue
            prev_stripped = prev_line.strip()
            if not TBL_CAPTION_RE.match(prev_stripped):
                tbl_counter += 1
                if subsection is not None:
                    number = f'{chapter}.{subsection}.{tbl_counter}'
                else:
                    number = f'{chapter}.{tbl_counter}'
                title = _table_title(lines, i)
                bookmark = _bookmark_id('tbl', number)
                registry.tables.append(CaptionEntry('tbl', number, title, bookmark))
                out.append(_format_caption('tbl', number, title))
                out.append('')
            in_table = True
            out.append(line)
            i += 1
            prev_line = stripped
            continue

        in_table = False

        out.append(line)
        i += 1
        prev_line = stripped

    body = '\n'.join(out)
    daftar = _build_daftar_sections(registry)
    m = re.search(r'^##\s+1\.\s+Pendahuluan', body, re.M)
    if m and daftar:
        body = daftar + body[m.start():]
    elif daftar:
        body = daftar + body

    return body, registry


def caption_number_from_text(text: str) -> tuple[str, str] | None:
    """Return (kind, bookmark_id) from caption paragraph text."""
    text = text.strip().strip('*')
    m = FIG_CAPTION_RE.match(text)
    if m:
        return 'fig', _bookmark_id('fig', m.group(1))
    m = TBL_CAPTION_RE.match(text)
    if m:
        return 'tbl', _bookmark_id('tbl', m.group(1))
    return None
