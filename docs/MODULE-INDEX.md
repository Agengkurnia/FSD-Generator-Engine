# Indeks Modul FSD

Katalog modul FSD Generator Engine. **Perbarui** saat menambah modul baru.

---

## Modul Aktif (cover lib + `modules/{slug}/build.py`)

| Slug | Path | Source | Build | Status |
|------|------|--------|-------|--------|
| `new-rm-sample` | `modules/new-rm-sample/` | `source/FSD_New_RM_Sample_v3.1.md` | `py build.py` | active |
| `item-spec` | `modules/item-spec/` | `source/FSD_ItemSpec_RM_v1.2.md` | `py build.py` | active |
| `item-registration` | `modules/item-registration/` | `source/FSD_Item_Registration_v1.0.md` | `py build.py` | active |
| `oracle-registration` | `modules/oracle-registration/` | `source/FSD_Oracle_Registration_v1.1.md` | `py build.py` | active |
| `item-code-trial` | `modules/item-code-trial/` | `source/FSD_ItemCodeTrial_v3.0.md` | `py build.py` | active |
| `formulation-lab` | `modules/formulation-lab/` | `source/FSD_LaboratoryFormula_v1.1.md` | `py build.py` | active |

---

## Template & Modul Khusus

| Slug | Path | Catatan |
|------|------|---------|
| **`_template`** | `modules/_template/` | **Skeleton modul baru** — salin ke `modules/{slug}/`, jangan build langsung |
| `formulation` | `modules/formulation/` | `build_combined.py` — FSD gabungan (legacy embedded MD) |
| `master-data` | `modules/master-data/` | `source/`, `output/`, `screenshots/` (`no-build`) |
| `seal` | `modules/seal/` | `source/`, `output/`, `screenshots/` (`no-build`) |

---

## Perintah Build

```powershell
cd "D:\Work\Source\FSD Generator Engine\modules\item-spec"
py build.py
```

Ganti `item-spec` dengan slug modul di tabel atas.

---

## Shared Library

| Modul | Fungsi |
|-------|--------|
| `lib/fsd_cover_merge.py` | Cover Kalbe 2 halaman |
| `lib/fsd_build.py` | Kroki, Pandoc, post-process |
| `lib/fsd_module_runner.py` | Runner generik; deteksi swimlane + PlantUML |
| `lib/fsd_paths.py` | Path template & engine root |

---

## Dokumentasi

- [AI-START-HERE.md](AI-START-HERE.md) — entry point AI
- [STANDARD-FSD-GENERATION.md](STANDARD-FSD-GENERATION.md)
- [FOLDER-STRUCTURE.md](FOLDER-STRUCTURE.md)
- [COVER-STANDARD.md](COVER-STANDARD.md)

---

## Proyek Eksternal

| Proyek | Acuan engine |
|--------|--------------|
| KICAO KDS Enhancement | `modules/item-spec/` + `docs/STANDARD-FSD-GENERATION.md` |
| **Falcon FPRS Web Admin** | `Comsup/falcon/Prototype/wwwroot/document/FSD/FalconWebPortal/` — FSD Web v1.0 |
| **Falcon FPRS Mobile SFA** | `Comsup/falcon/Prototype/wwwroot/document/FSD/FalconMobile/` — FSD Mobile v1.0 |
