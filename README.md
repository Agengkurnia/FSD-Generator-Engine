# FSD Generator Engine

Toolkit untuk menghasilkan **Functional Specification Document (FSD)** dalam format Markdown dan Word (DOCX) dengan standar visual Kalbe Nutritionals — cover resmi, tabel hijau, diagram Kroki, dan pipeline build otomatis.

**Target pengguna:** Technical Writer, BA, developer, dan **AI IDE** (Cursor, Antigravity, dll.).

> **AI Agent baru?** Baca **[docs/AI-START-HERE.md](docs/AI-START-HERE.md)** dulu — urutan baca, aturan anti-halusinasi, tutorial modul baru (~15 menit).

---

## Quick Start

```powershell
cd "D:\Work\Source\FSD Generator Engine"
py -m pip install -r requirements.txt
# Pastikan pandoc terinstall: https://pandoc.org/installing.html

# Build Item Spec RM v1.2
cd modules\item-spec
py build.py

# Build New RM Sample v3.1
cd ..\new-rm-sample
py build.py
```

Setelah generate: buka DOCX → tekan **F9** untuk update Table of Contents.

---

## Dokumentasi Standar (AI-Ready)

| Dokumen | Isi |
|---------|-----|
| **[docs/AI-START-HERE.md](docs/AI-START-HERE.md)** | **Mulai di sini** — orientasi AI, anti-halusinasi, tutorial |
| [docs/STANDARD-FSD-GENERATION.md](docs/STANDARD-FSD-GENERATION.md) | **Master** — standar § A–M, prompt eksekusi, pipeline, checklist |
| [docs/MODULE-INDEX.md](docs/MODULE-INDEX.md) | Katalog modul + perintah build |
| [docs/FOLDER-STRUCTURE.md](docs/FOLDER-STRUCTURE.md) | Aturan penempatan file |
| [docs/COVER-STANDARD.md](docs/COVER-STANDARD.md) | Cover + revision/approval (2 halaman pertama) |
| [modules/_template/](modules/_template/) | Skeleton modul baru — salin & edit |

Salin `docs/AI-START-HERE.md` + `docs/STANDARD-FSD-GENERATION.md` ke AI IDE lain sebagai konteks proyek.

---

## Struktur Repo

```
lib/          → fsd_cover_merge.py, fsd_build.py (shared Python)
templates/    → FSD_Cover_Template.docx, logo.png, reference.docx
modules/      → Satu folder per modul FSD (source, output, build.py)
docs/         → Standar dokumentasi
scripts/      → Utility capture/render/legacy
archive/      → File obsolete (review sebelum hapus)
```

Detail: [docs/FOLDER-STRUCTURE.md](docs/FOLDER-STRUCTURE.md)

---

## Modul Aktif

| Modul | Build |
|-------|-------|
| Item Spec RM v1.2 | `cd modules\item-spec && py build.py` |
| New RM Sample v3.1 | `cd modules\new-rm-sample && py build.py` |
| Item Registration | `cd modules\item-registration && py build.py` |
| Oracle Registration | `cd modules\oracle-registration && py build.py` |
| Item Code Trial | `cd modules\item-code-trial && py build.py` |
| Lab Formula | `cd modules\formulation-lab && py build.py` |

Daftar lengkap: [docs/MODULE-INDEX.md](docs/MODULE-INDEX.md)

---

## Dokumen Legacy (Deprecated)

| File | Ganti dengan |
|------|--------------|
| `QUICK_START.md` | README ini (workflow HTML→DOCX sudah legacy) |
| `README_Conversion.md` | [docs/STANDARD-FSD-GENERATION.md](docs/STANDARD-FSD-GENERATION.md) |
| `PANDUAN_SCREENSHOT.md` | [docs/PANDUAN_SCREENSHOT.md](docs/PANDUAN_SCREENSHOT.md) |
| `COVER_STANDARD.md` (root) | [docs/COVER-STANDARD.md](docs/COVER-STANDARD.md) |

---

*PT. Sanghiang Perkasa · Kalbe Nutritionals · FSD Generator Engine*
