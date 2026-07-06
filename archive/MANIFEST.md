# Archive Manifest — FSD Generator Engine

File di folder ini **diarsipkan** untuk review manual sebelum penghapusan permanen.

**Tanggal arsip:** Juli 2026  
**Kebijakan:** Archive dulu → review → hapus jika tidak diperlukan

---

## archive/builds-obsolete/

Build script digantikan `modules/*/build.py` + `lib/fsd_cover_merge.py`.

| File | Digantikan oleh |
|------|-----------------|
| `build_fsd_v2.py`, `v21`, `v3` | `modules/new-rm-sample/build.py` |
| `build_fsd_docx.py`, `build_new_rm_sample_docx.py` | sama |
| `generate_fsd_docx.py` | sama |
| `embed_*.py`, `enhance_fsd_complete.py`, `add_diagrams.py`, `merge_fsd.py` | Pipeline MD modern |

---

## archive/new-rm-sample/

Versi FSD New RM Sample sebelum v3.1 (MD/DOCX/PDF/HTML).

**Canonical:** `modules/new-rm-sample/source/FSD_New_RM_Sample_v3.1.md`

---

## archive/html-legacy/

Workflow HTML → DOCX (`convert_to_docx.bat`, `FSD_*.html`).

**Canonical:** Pipeline MD → Pandoc → cover merge.

---

## archive/scripts-experimental/

Varian `render_*.py` — diagram sekarang via Kroki di `build.py` masing-masing modul.

---

## archive/duplicates/

| File | Alasan |
|------|--------|
| `logo_root.png` | Duplikat `templates/logo.png` |
| `reference_root.docx` | Duplikat `templates/reference.docx` |
| `extracted_*.txt/md` | Artefak ekstraksi sementara |

---

## reference/

PDF referensi eksternal / signed AKS — bukan input build otomatis.

---

## archive/root-cleanup/ (Juli 2026 — Tahap B)

File dipindah dari **root** saat pembersihan folder:

| Jenis | Contoh | Destinasi aktif |
|-------|--------|-----------------|
| Diagram sumber lama | `erd_master_data.mmd`, `flow_diagram.mmd` | Kroki di `modules/*/build.py` |
| Screenshot tidak terklasifikasi | misc dari root `screenshots/` | Review manual |
| Duplikat folder lama | `ItemSpec_screenshots/` | `modules/item-spec/screenshots/` |

**DOCX/MD aktif** sekarang di `modules/{slug}/output/` dan `source/`.

---

## scripts/legacy/

`generate_erd_and_embed.py`, `update_erd_in_md.py` — utility lama pra-pipeline standar.

