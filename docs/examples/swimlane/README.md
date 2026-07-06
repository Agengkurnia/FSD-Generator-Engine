# Library Template Swimlane (Cross-Functional Flowchart)

Template siap salin untuk Bab **Business Flow**, **Integrasi**, dan **Approval Workflow**.

## Format standar (disarankan)

**Mermaid** — lane menyamping, alur turun:

```
flowchart LR          ← lane = kolom (Customer | Clerk | Sistem | …)
  subgraph L1["Role"]
    direction TB      ← langkah turun di dalam lane
```

**PlantUML** — alternatif jika ingin tampilan activity swimlane klasik:

```plantuml
|Role A|
:Langkah;
|Role B|
:Langkah lain;
```

## File di folder ini

| File | Kegunaan |
|------|----------|
| `restaurant-poc-mermaid.mmd` | Golden reference visual (4 lane) — Mermaid |
| `restaurant-poc-plantuml.puml` | Golden reference — PlantUML |
| `swimlane-4-role-template.mmd` | Template 4 role generik |
| `swimlane-approval-template.mmd` | Template approval |
| `swimlane-integration-template.mmd` | Template integrasi Master→Transaksi |

## Render PoC (bandingkan Mermaid vs PlantUML)

```powershell
cd "D:\Work\Source\FSD Generator Engine"
py scripts/render_swimlane_poc.py
```

Output: `docs/examples/swimlane/output/poc_mermaid.png`, `poc_plantuml.png`

**Hasil PoC (Juli 2026):**

| Renderer | Layout lane | Rekomendasi |
|----------|-------------|-------------|
| **PlantUML** | Kolom vertikal (Customer \| Clerk \| …) — **mirip gambar referensi** | **Utama** untuk Bab 2/9 baru |
| Mermaid | Kadang baris horizontal per role | Tetap untuk modul existing (Item Spec) |

## Palet warna lane

| Tipe | Fill | Stroke |
|------|------|--------|
| User / bisnis | `#FFF9C4` | `#FBC02D` |
| Sistem aplikasi | `#E3F2FD` | `#1976D2` |
| Approval | `#E8F5E9` | `#388E3C` |
| ERP / integrasi | `#FCE4EC` | `#C62828` |
| Eksternal | `#F3E5F5` | `#7B1FA2` |
| Start | `#C8E6C9` | `#388E3C` |
| End | `#B2DFDB` | `#00796B` |
| Decision | `#FFE0B2` | `#F57C00` |

## Aturan wajib (ringkas)

1. Tabel **Lane** di MD sebelum diagram (sumber: RBAC/spec)
2. Setiap node di dalam satu lane (`subgraph` atau `|Role|`)
3. Maks 4–5 lane; pecah jika lebih
4. Hand-off antar lane dijelaskan di narasi

Detail: `docs/STANDARD-FSD-GENERATION.md` §F
