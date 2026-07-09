# Struktur Folder — FSD Generator Engine

> Peta resmi penempatan file. Gunakan dokumen ini saat menambah modul baru atau bekerja dengan AI IDE.

---

## Diagram

```
FSD Generator Engine/
├── README.md                 # Entry point
├── requirements.txt
├── .gitignore
│
├── docs/                     # Dokumentasi standar (AI-ready)
│   ├── AI-START-HERE.md      ← entry point AI
│   ├── STANDARD-FSD-GENERATION.md
│   ├── MODULE-INDEX.md
│   ├── FOLDER-STRUCTURE.md   ← file ini
│   ├── COVER-STANDARD.md
│   ├── PANDUAN_SCREENSHOT.md
│   ├── deliverables/         # DOCX terbaru per proyek (tanpa timestamp)
│   └── examples/swimlane/    ← template cross-functional swimlane
│
├── lib/                      # Python shared
│   ├── fsd_paths.py
│   ├── fsd_cover_merge.py
│   ├── fsd_build.py          # postprocess DOCX (+ page break antar bab)
│   ├── fsd_captions.py
│   ├── fsd_crud.py           # format tabel CRUD (omit opsi tidak tersedia)
│   ├── fsd_ui_section.py     # standar penulisan section UI (Markdown)
│   ├── fsd_deliver.py        # Project Log + salinan repo terbaru
│   └── fsd_module_runner.py
│
├── templates/                # Aset Word global
│   ├── FSD_Cover_Template.docx
│   ├── logo.png
│   └── reference.docx
│
├── modules/                  # Satu folder per produk FSD
│   ├── _template/            ← skeleton modul baru (salin, jangan build langsung)
│   ├── new-rm-sample/
│   ├── item-spec/
│   ├── item-registration/
│   ├── item-code-trial/
│   ├── formulation-lab/
│   ├── master-data/
│   └── seal/
│
├── scripts/                  # Utility bersama
│   ├── capture/
│   ├── render/
│   ├── postprocess/
│   └── legacy/
│
├── archive/                  # File obsolete (review sebelum hapus)
├── reference/                # PDF referensi eksternal
└── _tmp/                     # Build intermediate (gitignored)
```

---

## Konvensi per Modul (`modules/{slug}/`)

| Subfolder | Isi |
|-----------|-----|
| `source/` | `FSD_*.md` canonical — **satu versi aktif** |
| `output/` | `.docx` / `.pdf` hasil build terbaru |
| `screenshots/` | Capture UI modul ini |
| `diagrams/` | PNG dari Mermaid (opsional; bisa di `screenshots/`) |
| `build.py` | Satu entry point build |
| `archive/` | Versi lama modul ini saja |
| `README.md` | Ringkasan modul + perintah build |

### Penamaan slug

- Lowercase, hyphen: `new-rm-sample`, `item-spec`, `item-code-trial`
- Tanpa spasi (hindari `Item Code Trial`)

---

## Aturan Penempatan

| Jenis file | Lokasi | Jangan taruh di |
|------------|--------|-----------------|
| MD FSD aktif | `modules/{slug}/source/` | Root repo |
| Build script modul | `modules/{slug}/build.py` | Root (kecuali orchestrator) |
| Root `screenshots/` | `modules/{slug}/screenshots/` (folder root dihapus) |
| Cover template | `templates/` | Per modul |
| Build obsolete | `archive/` | Root |
| PDF referensi AKS | `reference/` | Root |
| Temp `_tmp_*` | `_tmp/` | Sebarang folder modul |

---

## Menambah Modul Baru

1. Salin `modules/_template/` → `modules/{slug}/`
2. Edit `build.py` (slug, md_filename, output_filename)
3. Rename & isi `source/FSD_TEMPLATE.md`
4. Tambah screenshot di `screenshots/`
5. `py build.py` → verifikasi DOCX
6. Update `docs/MODULE-INDEX.md` + tulis `modules/{slug}/README.md`

Tutorial lengkap: [AI-START-HERE.md](AI-START-HERE.md) · Standar: [STANDARD-FSD-GENERATION.md](STANDARD-FSD-GENERATION.md)

---

## Lokasi Lama (Deprecated)

Folder lama masih bisa ada stub `README.md` yang mengarah ke `modules/`:

| Lama | Baru |
|------|------|
| `ItemSpec/` | `modules/item-spec/` |
| `Item_Registration/` | `modules/item-registration/` |
| `Item Code Trial/` | `modules/item-code-trial/` |
| `Formulation/` | `modules/formulation-lab/` + `modules/formulation/` |
| Root `FSD_New_RM_Sample_*` | `modules/new-rm-sample/` |
