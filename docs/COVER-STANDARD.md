# Standar Cover FSD — Kalbe Nutritionals

Dokumen ini menjelaskan standar **2 halaman pertama** FSD (cover + revision history & document approval) untuk seluruh **FSD Generator Engine**.

Layout mengacu pada template resmi Kalbe (`templates/FSD_Cover_Template.docx`).

> Dokumen terkait: [STANDARD-FSD-GENERATION.md](STANDARD-FSD-GENERATION.md) · [FOLDER-STRUCTURE.md](FOLDER-STRUCTURE.md)

---

## Aset Template

| File | Lokasi | Keterangan |
|------|--------|------------|
| `FSD_Cover_Template.docx` | `templates/` | Layout Word: cover, revision, approval, TOC field |
| `logo.png` | `templates/` | Logo Kalbe Nutritionals (6.51 × 3.93 cm) |
| `reference.docx` | `templates/` | Pandoc style reference (body Calibri) |

---

## Modul Python (`lib/`)

| Modul | Fungsi |
|-------|--------|
| `fsd_paths.py` | `ENGINE_ROOT`, `COVER_TEMPLATE`, `LOGO_PATH`, `REFERENCE_DOCX` |
| `fsd_cover_merge.py` | `parse_md_cover_meta`, `strip_md_for_body`, `merge_cover_and_content`, `content_start_index` |
| `fsd_build.py` | Helper Kroki, post-process tabel/gambar (shared) |

### Dependency

```powershell
cd "D:\Work\Source\FSD Generator Engine"
py -m pip install -r requirements.txt
```

Butuh: `python-docx`, `docxcompose`, `pandoc` di PATH.

---

## Pipeline Build (dengan Cover)

```
MD sumber (full, dengan metadata)
    │
    ├─ parse_md_cover_meta()  → dict metadata cover
    └─ strip_md_for_body()    → MD mulai ## 1. Pendahuluan
    │
    ▼
Render Mermaid + preprocess lainnya
    │
    ▼
Pandoc → _tmp/*_content.docx   (TANPA --toc)
    │
    ▼
merge_cover_and_content()        (STEP cover)
    │
    ▼
Post-process python-docx         (skip 2 tabel cover + paragraf sebelum "1. Pendahuluan")
    │
    ▼
output/*.docx final
```

**Penting:** Jangan kirim front matter MD (cover, riwayat revisi, daftar isi manual) ke Pandoc — ditangani template Word.

---

## Metadata dari Markdown

| Sumber MD | Field cover |
|-----------|-------------|
| `\| **Proyek** \|` atau `\| **Project** \|` | Judul proyek (biru, 26pt) |
| `### Sistem:` | Fallback judul proyek |
| `## Modul:` | Nama modul (singkat di cover) |
| `\| **Versi** \|` | Version `[x.x.x]` |
| `\| **Tanggal** \|` | Date `[dd/mm/yyyy]` |
| `\| **Dibuat oleh** \|` | Prepared By |
| `## Riwayat Revisi` (baris match versi / terakhir) | Tabel revision history |

### Override per proyek

```python
COVER_META = parse_md_cover_meta(raw, defaults={
    'project': 'KICAO KDS',
    'brd_no': '2026.SHP-FSD.0040',
    'pid_no': '2026.SHP-PID.0040',
})
```

---

## Integrasi ke `modules/*/build.py`

```python
import sys, os
ENGINE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ENGINE_ROOT, 'lib'))

from fsd_cover_merge import (
    parse_md_cover_meta, strip_md_for_body, merge_cover_and_content,
    content_start_index, COVER_TABLE_COUNT,
)
from fsd_paths import COVER_TEMPLATE, LOGO_PATH, REFERENCE_DOCX, TMP_DIR
```

Lihat [STANDARD-FSD-GENERATION.md § Build Pipeline](STANDARD-FSD-GENERATION.md#build-pipeline) untuk langkah lengkap.

---

## Spesifikasi Visual

### Halaman 1 (Cover)

- Logo kiri atas (`templates/logo.png`)
- Font **Arial**, teks cover **right-aligned**
- Warna biru variabel: `#548DD4`
- Judul FSD: 36pt bold | Version: 18pt | Project: 26pt biru italic | Modul: 16pt biru italic
- PT. Sanghiang Perkasa: 18pt bold | Date: 18pt biru italic `[dd/mm/yyyy]`

### Halaman 2

- BRD No / PID Ref. No (header biru muda)
- Revision history + **Document Approval** (header abu-abu, border hitam)

#### Document Approval (standar Falcon FPRS / SHP)

Diisi otomatis oleh `update_document_approval()` di `lib/fsd_cover_merge.py` saat merge cover:

| Full name | Job Title |
|-----------|-----------|
| Muhammad Rafi | SHP Channel & Customer Development |
| Silvester Mario Nian Destrada | SHP Channel & Customer Development |
| Aldira Rahmania | SHP Channel & Customer Development |
| Ageng Kurniawan Sugianto | IT Product |
| Albet | IT Product |

Kolom **Signature** dan **Signature Date** dikosongkan untuk ditandatangani manual di Word.

Override per proyek via metadata build:

```python
COVER_META = parse_md_cover_meta(raw, defaults={
    'document_approval': [
        {'name': '...', 'title': '...'},
    ],
})
```

### Setelah Generate

1. Buka DOCX di Microsoft Word
2. Tekan **F9** untuk update field TOC
3. Verifikasi halaman 1–2 sesuai template
