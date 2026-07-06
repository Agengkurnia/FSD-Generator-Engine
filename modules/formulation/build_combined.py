
content = r"""# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
## Modul: Formulation Management System
### Sistem: IDC System – New Formulation Management
### (Premix · DryBlend · Liquid · Baking · Drying · Packaging)

---

| Atribut          | Keterangan                                        |
|------------------|---------------------------------------------------|
| **Nama Dokumen** | FSD Modul Formulation Management System (Gabungan)|
| **Versi**        | 1.0                                               |
| **Tanggal**      | April 2026                                        |
| **Divisi**       | R&D / ICT                                         |
| **Status**       | Draft                                             |
| **Dibuat oleh**  | Tim ICT – IDC System                              |

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Sistem **Formulation Management** pada IDC System terdiri dari **6 modul** yang saling berkaitan secara hierarkis dalam proses pembuatan formula produk. Modul-modul ini merupakan migrasi dari sistem legacy **KN2017_FORMULATION**.

### 1.2 Hierarki Formula (3 Layer)

```
LAYER 1 – Base Calculation
├── Premix Formula   → Hitung komposisi campuran bahan (premix)
└── DryBlend Formula → Hitung komposisi pencampuran kering (base)

LAYER 2 – Product Formula  (menggunakan output Layer 1 sebagai ingredient)
├── Liquid Formula   → Formula produk cair
├── Baking Formula   → Formula produk panggang
└── Drying Formula   → Formula produk kering (dapat digunakan kembali di Layer 1)

LAYER 3 – Packaging Formula  (menarik data dari Layer 2)
└── Packaging Formula → Formula kemasan produk
```

---

## 2. Business Flow (End-to-End)

```mermaid
flowchart TD
    subgraph L1["LAYER 1 - Base Calculation"]
        direction LR
        PX["Premix Formula"]
        DB["DryBlend Formula"]
    end

    subgraph L2["LAYER 2 - Product Formula"]
        direction LR
        LQ["Liquid Formula"]
        BK["Baking Formula"]
        DR["Drying Formula"]
    end

    subgraph L3["LAYER 3 - Packaging"]
        PK["Packaging Formula"]
    end

    Start(["Mulai RnD Project"]) --> L1
    PX -->|"Item Code Premix"| L2
    DB -->|"Item Code Base"| L2
    DR -->|"Cross: Drying ke Layer 1"| L1
    L2 -->|"Formula No ke Packaging"| L3
    L3 --> End(["Formula Kemasan Selesai"])
```

---

## 3. Flow Per Layer

### 3.1 Layer 1 – Premix & DryBlend Formula

```mermaid
flowchart TD
    P1["Pilih Project No"] --> P2["Isi Header Formula"]
    P2 --> P3["Input Bahan Baku di Grid"]
    P3 --> P4["BatchSize = sum Dosage Conv"]
    P4 --> P5{Validasi?}
    P5 -->|Gagal| P6["Tampilkan Error"]
    P5 -->|OK| P7{Pilih Aksi}
    P7 -->|SAVE| P8["Status DRAFT 10"]
    P7 -->|SUBMIT| P9["Cek item code Oracle"]
    P9 -->|Belum approved| P10["Blokir Submit"]
    P9 -->|Semua OK| P11["Kalkulasi dan Approval K2"]
    P11 --> P12(["Item Code siap di Layer 2"])
```

**DryBlend tambahan validasi**: Country Name, Food Category, OD Regulation wajib diisi.

---

### 3.2 Layer 2 – Product Formula

```mermaid
flowchart TD
    L2Start["Pilih Project No"] --> L2A["Input Header Formula"]
    L2A --> L2B["Input Grid Bahan Baku dari Layer 1"]
    L2B --> L2C{Tipe Formula?}
    L2C -->|Liquid| LQ1["ServingSize g = mL x Density\nWater = BatchSize - TotalMaterial"]
    L2C -->|Baking| BK1["Min 1 Main Ingredient\nInput Water Manual"]
    L2C -->|Drying| DR1["Dosage in FG pct\nBase Item Code"]
    LQ1 --> L2D{Validasi OK?}
    BK1 --> L2D
    DR1 --> L2D
    L2D -->|OK| L2E["SAVE atau SUBMIT ke K2"]
    L2E --> L2End(["Formula No Layer 2 siap"])
```

---

### 3.3 Layer 3 – Packaging Formula

```mermaid
flowchart TD
    PK1["Pilih Project No"] --> PK2["Pilih Formula No dari Layer 2"]
    PK2 --> PK3["Isi Header: Desc, BatchSize, Netto"]
    PK3 --> PK4["Isi Grid Detail Kemasan"]
    PK4 --> PK5["Isi Grid Parameter"]
    PK5 --> PK6["calculateQty otomatis"]
    PK6 --> PK7{Cek Duplikat?}
    PK7 -->|Duplikat| PK8["Blokir Save"]
    PK7 -->|OK| PK9{Pilih Aksi}
    PK9 -->|DRAFT| PK10["SaveData type 1 - Status 10"]
    PK9 -->|SUBMIT| PK11["SaveData type 2 - Status 20"]
    PK11 --> PK12(["Packaging Formula Selesai"])
```

---

## 4. Struktur Database & ERD

### 4.1 Tabel-Tabel Per Modul

| Layer | Modul        | Header Table          | Detail Table(s)                                    |
|-------|--------------|-----------------------|----------------------------------------------------|
| 1     | Premix       | `trPremixHeader`      | `trPremixDetail`                                   |
| 1     | DryBlend     | `trDryBlendHeader`    | `trDryBlendDetail`                                 |
| 2     | Liquid       | `trLiquidHeader`      | `trLiquidDetail`                                   |
| 2     | Baking       | `trBakingHeader`      | `trBakingDetail`                                   |
| 2     | Drying       | `trDryingHeader`      | `trDryingDetail`                                   |
| 3     | Packaging    | `trPackagingHeader`   | `trPackagingDetail` + `trPackagingParameter`        |

### 4.2 ERD – Relasi Antar Modul (Cross-Layer)

```mermaid
erDiagram
    trProjectRegistration {
        int intProjectRegistrationID PK
        varchar txtProjectNo
        varchar txtProjectType
        varchar txtProductType
        varchar txtSubbrandDesc
        varchar txtProductVariant
    }

    trPremixHeader {
        int intPremixHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        varchar txtPremixItemCode
        decimal decProductBatchSize
        varchar txtAppParamID
    }

    trPremixDetail {
        int intPremixDetailId PK
        int intPremixHeaderId FK
        varchar txtItemCode
        decimal decDosage
        decimal decDosageConv
        varchar txtUOM
        varchar txtUOMConv
    }

    trDryBlendHeader {
        int intDryBlendHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decProductBatchSize
        varchar txtCountry
        varchar txtFoodCategory
        int intODRegulationID FK
        varchar txtAppParamID
    }

    trDryBlendDetail {
        int intDryBlendDetailId PK
        int intDryBlendHeaderId FK
        varchar txtItemCode
        decimal decDosage
        decimal decDosageConv
    }

    trDryingHeader {
        int intDryingHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        varchar txtBaseItemCode
        decimal decProductBatchSize
        decimal decDosageinFG
        decimal decTotalSolid
        decimal decTargetMaxMoisture
        varchar txtAppParamID
    }

    trDryingDetail {
        int intDryingDetailId PK
        int intDryingHeaderId FK
        varchar txtItemCode
        decimal decDosage
        decimal decDosageConv
    }

    trLiquidHeader {
        int intLiquidHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decProductBatchSize
        decimal decDensity
        decimal decNettoServingSizeML
        decimal decServingSize
        varchar txtCountry
        varchar txtFoodCategory
        int intODRegulationID FK
        varchar txtAppParamID
    }

    trLiquidDetail {
        int intLiquidDetailId PK
        int intLiquidHeaderId FK
        varchar txtItemCode
        decimal decDosage
        decimal decDosageConv
    }

    trBakingHeader {
        int intBakingHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decProductBatchSize
        decimal decWater
        decimal decTargetMaxMoisture
        varchar txtCountry
        varchar txtFoodCategory
        int intODRegulationID FK
        varchar txtAppParamID
    }

    trBakingDetail {
        int intBakingDetailId PK
        int intBakingHeaderId FK
        varchar txtItemCode
        decimal decDosage
        decimal decDosageConv
        bit bolMainIngredient
    }

    trPackagingHeader {
        int intPHeaderId PK
        varchar txtFormulaNo
        varchar txtProjectNo
        decimal decBatchSize
        decimal decNetto
        varchar txtRMFormulaNo
        varchar txtDocStatus
    }

    trPackagingDetail {
        int intPDetailId PK
        int intPHeaderId FK
        int intPMId FK
        varchar txtOraItemCode
        decimal decQty
        decimal decQtyAdjustment
    }

    trPackagingParameter {
        int intPParameterId PK
        int intPHeaderId FK
        int intPPId FK
        decimal decValue
    }

    mODRegulation {
        int intODRegulationID PK
        varchar txtODRegulationName
    }

    mPackagingMaterial {
        int intPMId PK
        varchar txtPMName
    }

    trProjectRegistration ||--o{ trPremixHeader : "has Premix"
    trProjectRegistration ||--o{ trDryBlendHeader : "has DryBlend"
    trProjectRegistration ||--o{ trLiquidHeader : "has Liquid"
    trProjectRegistration ||--o{ trBakingHeader : "has Baking"
    trProjectRegistration ||--o{ trDryingHeader : "has Drying"

    trPremixHeader ||--o{ trPremixDetail : "ingredient"
    trDryBlendHeader ||--o{ trDryBlendDetail : "ingredient"
    trLiquidHeader ||--o{ trLiquidDetail : "ingredient"
    trBakingHeader ||--o{ trBakingDetail : "ingredient"
    trDryingHeader ||--o{ trDryingDetail : "ingredient"

    trPackagingHeader ||--o{ trPackagingDetail : "bahan kemasan"
    trPackagingHeader ||--o{ trPackagingParameter : "parameter"
    mPackagingMaterial ||--o{ trPackagingDetail : "jenis material"
    mODRegulation ||--o{ trDryBlendHeader : "regulasi"
    mODRegulation ||--o{ trLiquidHeader : "regulasi"
    mODRegulation ||--o{ trBakingHeader : "regulasi"
    mODRegulation ||--o{ trDryingHeader : "regulasi"
```

---

## 5. Relasi Cross-Layer (Item Code Flow)

| From (Source)       | To (Consumer)        | Mekanisme                                                   |
|---------------------|----------------------|-------------------------------------------------------------|
| `trPremixHeader.txtPremixItemCode` | `trPremixDetail.txtItemCode` | Self-reference: premix bisa pakai premix lain |
| `trPremixHeader.txtPremixItemCode` | `trDryBlendDetail.txtItemCode` | DryBlend pakai hasil premix sebagai ingredient |
| `trPremixHeader.txtPremixItemCode` | `trLiquidDetail.txtItemCode` | Liquid pakai hasil premix |
| `trPremixHeader.txtPremixItemCode` | `trBakingDetail.txtItemCode` | Baking pakai hasil premix |
| `trDryingHeader.txtFormulaNo`      | `trPremixDetail.txtItemCode` | Drying dipakai di Premix (cross-layer) |
| `trDryingHeader.txtFormulaNo`      | `trDryBlendDetail.txtItemCode` | Drying dipakai di DryBlend |
| `trLiquidHeader.txtFormulaNo`      | `trPackagingHeader.txtRMFormulaNo` | Packaging referensi ke Liquid |
| `trBakingHeader.txtFormulaNo`      | `trPackagingHeader.txtRMFormulaNo` | Packaging referensi ke Baking |
| `trDryingHeader.txtFormulaNo`      | `trPackagingHeader.txtRMFormulaNo` | Packaging referensi ke Drying |

---

## 6. Spesifikasi Per Modul

### 6.1 Premix Formula (Layer 1)

#### Header Fields

| Field                   | DB Column               | Mandatory | Keterangan                               |
|-------------------------|-------------------------|-----------|------------------------------------------|
| Formula No.             | `txtFormulaNo`          | Auto      | Auto-generate                            |
| Formula Name            | `txtFormulaName`        | Ya        | Nama formula                             |
| Premix Item Code        | `txtPremixItemCode`     | Ya        | Item code di Oracle                      |
| Product Batch Size (Kg) | `decProductBatchSize`   | Ya        | Auto-update dari sum grid                |
| Project No.             | via FK                  | Ya        | LOV Project Registration                 |
| Remarks                 | `remarks`               | Tidak     | Catatan bebas                            |

#### Detail Grid Columns

| Kolom       | DB Column       | Keterangan                                    |
|-------------|-----------------|-----------------------------------------------|
| Item Code   | `txtItemCode`   | Oracle + Premix + Drying (lookup berantai)    |
| UOM         | `txtUOM`        | Dropdown dari mAppParam LOVUom                |
| Dosage (Kg) | `decDosage`     | Nilai dalam Kg                                |
| UOM Conv    | `txtUOMConv`    | UOM sebelum konversi                          |
| Dosage Conv | `decDosageConv` | Input user; auto-konversi ke Kg               |

#### Business Rules

| Rule  | Deskripsi |
|-------|-----------|
| BR-P1 | Semua item code harus approved Oracle sebelum Submit |
| BR-P2 | `decProductBatchSize` = sum(`decDosageConv`) |
| BR-P3 | Lookup item code: Oracle → Premix → Drying → RMMaster0 |

---

### 6.2 DryBlend Formula (Layer 1)

Sama dengan Premix dengan tambahan:

#### Tambahan Header Fields

| Field              | DB Column          | Mandatory | Keterangan                        |
|--------------------|--------------------|-----------|-----------------------------------|
| Country Name       | `txtCountry`       | Ya        | Autocomplete dari Oracle          |
| Netto/Serving Size | `decServingSize`   | Ya        | Serving size dalam gram           |
| Packing Netto (g)  | `decPackingNetto`  | Ya        | Netto kemasan                     |
| Food Category      | `txtFoodCategory`  | Ya        | Autocomplete master               |
| OD Regulation      | `intODRegulationID`| Ya        | Dropdown                          |

#### Business Rules Tambahan

| Rule   | Deskripsi |
|--------|-----------|
| BR-DB1 | Country wajib dipilih dari autocomplete (isValidCountry = true) |
| BR-DB2 | Food Category wajib dari autocomplete |
| BR-DB3 | OD Regulation tidak boleh bernilai -1 |

---

### 6.3 Liquid Formula (Layer 2)

#### Tambahan Header Fields

| Field                   | DB Column              | Mandatory | Keterangan                                       |
|-------------------------|------------------------|-----------|--------------------------------------------------|
| Density (g/mL)          | `decDensity`           | Ya        | Densitas produk; trigger kalkulasi Serving Size  |
| Serving Size (mL)       | `decNettoServingSizeML`| Ya        | Input dalam mL                                   |
| Serving Size (g)        | `decServingSize`       | Auto      | = `decNettoServingSizeML × decDensity` (readonly)|
| Total Qty Product       | `decTotalQuantityProduct`| Auto    | = `decProductBatchSize`                          |

#### Business Rules

| Rule   | Deskripsi |
|--------|-----------|
| BR-LQ1 | `decServingSize(g) = decNettoServingSizeML × decDensity` (client-side JS) |
| BR-LQ2 | Water = `decProductBatchSize - dblTotalQuantityMaterial` (auto-kalkulasi) |
| BR-LQ3 | Jika Water negatif → warning, total bahan melebihi batch size |

---

### 6.4 Baking Formula (Layer 2)

#### Tambahan Header Fields

| Field                 | DB Column              | Mandatory | Keterangan                                    |
|-----------------------|------------------------|-----------|-----------------------------------------------|
| Water (Kg)            | `decWater`             | Tidak     | Input manual (bukan kalkulasi otomatis)        |
| Target Moisture (%)   | `decTargetMaxMoisture` | Tidak     | Target kadar air produk jadi                  |

#### Detail Grid — Kolom Tambahan

| Kolom           | DB Column          | Keterangan                                            |
|-----------------|--------------------|-------------------------------------------------------|
| Main Ingredient | `bolMainIngredient`| Checkbox — tandai bahan utama                         |

#### Business Rules

| Rule   | Deskripsi |
|--------|-----------|
| BR-BK1 | Minimal 1 baris harus `bolMainIngredient = true` |
| BR-BK2 | `dblTotalQuantityMaterial` = sum(`decDosageConv`) **hanya** dari baris `bolMainIngredient = true` |
| BR-BK3 | `decProductBatchSize` diinput manual (tidak auto dari grid) |

---

### 6.5 Drying Formula (Layer 2 & Cross-Layer 1)

#### Tambahan Header Fields

| Field                  | DB Column              | Mandatory | Keterangan                                    |
|------------------------|------------------------|-----------|-----------------------------------------------|
| Base Item Code         | `txtBaseItemCode`      | Tidak     | Referensi item kode dasar; readonly setelah simpan |
| Base Description       | `txtBaseDescription`   | Auto      | Deskripsi base item; readonly                 |
| Dosage in FG (%)       | `decDosageinFG`        | Ya        | % dosage dalam produk jadi (0-100)            |
| Total Solid (%)        | `decTotalSolid`        | Tidak     | % padatan dalam formula                       |
| Target Max Moisture (%)| `decTargetMaxMoisture` | Tidak     | Batas maksimal kadar air setelah drying       |

#### Business Rules

| Rule   | Deskripsi |
|--------|-----------|
| BR-DR1 | `decDosageinFG` harus bernilai 0–100 |
| BR-DR2 | Drying Header dapat digunakan sebagai item code di Premix dan DryBlend (cross-layer) |

---

### 6.6 Packaging Formula (Layer 3)

#### Header Fields

| Field           | DB Column           | Mandatory | Keterangan                                         |
|-----------------|---------------------|-----------|----------------------------------------------------|
| Project No.     | `txtProjectNo`      | Ya        | LOV Project Registration                           |
| Formula No.     | `txtFormulaNo`      | Ya        | LOV — filter dari Layer 2 (Liquid/Baking/Drying)   |
| Formula Desc    | `txtFormulaDesc`    | Ya        | Deskripsi formula kemasan                          |
| Batch Size      | `decBatchSize`      | Ya        | Ukuran batch                                       |
| Netto           | `decNetto`          | Ya        | Netto produk untuk kalkulasi qty                   |
| RM Formula No.  | `txtRMFormulaNo`    | Tidak     | Link ke formula Layer 2 (Liquid/Baking/Drying)     |

#### Grid Detail Kemasan

| Kolom            | DB Column         | Keterangan                                          |
|------------------|-------------------|-----------------------------------------------------|
| Packaging Mat.   | `intPMId`         | LOV dari `mPackagingMaterial`                       |
| Oracle Item Code | `txtOraItemCode`  | LOV Oracle PM Item Code                             |
| Qty              | `decQty`          | Auto-kalkulasi via `calculateQty`                   |
| Qty Adjustment   | `decQtyAdjustment`| Penyesuaian manual                                  |

#### Grid Parameter Kemasan

| Kolom      | DB Column   | Keterangan                         |
|------------|-------------|------------------------------------|
| Parameter  | `intPPId`   | LOV dari `mPackagingParamMaster`   |
| Value      | `decValue`  | Nilai parameter                    |

#### Business Rules

| Rule   | Deskripsi |
|--------|-----------|
| BR-PK1 | Kombinasi `intPMId + txtOraItemCode` tidak boleh duplikat per header |
| BR-PK2 | `decQty` dihitung via `calculateQty(listDetail, batchsize, netto, param)` |
| BR-PK3 | Perubahan `gridParam` mempengaruhi `gridDetail` via `reloadParamByDetail` |
| BR-PK4 | Submit (type=2) → `insertMApprove` dipanggil → `txtDocStatus = '20'` |

---

## 7. Status Dokumen (Semua Modul)

| Kode     | Label            | Layer 1 (Premix/DB) | Layer 2 (Liq/Bk/Dr) | Layer 3 (Pkg) |
|----------|------------------|---------------------|----------------------|---------------|
| null/00  | New              | Ya                  | Ya                   | —             |
| 10       | Draft            | Ya                  | Ya                   | Ya            |
| 20       | Waiting Approval | Ya                  | Ya                   | Ya (Submitted)|
| 30       | Approved         | Ya                  | Ya                   | Ya            |

---

## 8. Shared Components (Dipakai Semua Modul)

| Komponen              | Endpoint                            | Digunakan Oleh               |
|-----------------------|-------------------------------------|------------------------------|
| Item Code Lookup      | `POST /PremixFormula/getItemDesc`   | Semua Layer 1 & 2            |
| KgConversion          | `GET /PremixFormula/KgConversion`   | Semua Layer 1 & 2            |
| Item Code Autocomplete| `GET /PremixFormula/getItemCodeRMPM`| Semua Layer 1 & 2            |
| Country Autocomplete  | `POST /{Module}/CountriesAutoComplete` | DryBlend, Liquid, Baking, Drying |
| Food Category         | `POST /{Module}/getFoodCategory`    | DryBlend, Liquid, Baking, Drying |
| OD Regulation         | `cont.getODRegulation()`            | DryBlend, Liquid, Baking, Drying |
| UOM List              | `mAppParam` var=LOVUom              | Semua Layer 1 & 2            |

---

## 9. Hak Akses

| Peran           | Buat Formula | Edit Draft | Submit | Delete | Packaging Submit |
|-----------------|-------------|------------|--------|--------|------------------|
| R&D Formulator  | Ya*         | Ya         | Ya     | Ya     | Ya               |
| Supervisor R&D  | Ya*         | Ya         | Ya     | Tidak  | Ya               |
| ICT Admin       | Ya          | Ya         | Ya     | Ya     | Ya               |
| View Only       | Tidak       | Tidak      | Tidak  | Tidak  | Tidak            |

*) Hanya jika `IntDepartmentID == 101` untuk Layer 1 & 2.

---

## 10. Appendix – Ringkasan Endpoint

### Layer 1

| Modul    | Index | Detail | Save | Delete | Calculate |
|----------|-------|--------|------|--------|-----------|
| Premix   | `/PremixFormula/Index` | `/PremixFormula/Detail` | `POST SavePremix` | `POST DeletePremix` | `POST Calculate` |
| DryBlend | `/DryBlendFormula/Index` | `/DryBlendFormula/Detail` | `POST SaveDryBlend` | `POST DeleteDryBlend` | `POST Calculate` |

### Layer 2

| Modul   | Index | Detail | Save | Delete |
|---------|-------|--------|------|--------|
| Liquid  | `/LiquidFormula/Index` | `/LiquidFormula/Detail` | `POST SaveLiquid` | `POST DeleteLiquid` |
| Baking  | `/BakingFormula/Index` | `/BakingFormula/Detail` | `POST SaveBaking` | `POST DeleteBaking` |
| Drying  | `/DryingFormula/Index` | `/DryingFormula/Detail` | `POST SaveDrying` | `POST DeleteDrying` |

### Layer 3

| Endpoint | Fungsi |
|----------|--------|
| `POST ReadAlltrPackagingHeader` | List header (AJAX) |
| `POST SaveData` | Save/Submit (type=1/2) |
| `POST calculateQty` | Kalkulasi Qty otomatis |
| `POST reloadParamByDetail` | Sync param ke detail |
"""

with open("FSD_FormulationModules_v1.0.md", "w", encoding="utf-8") as f:
    f.write(content)

print("FSD gabungan berhasil dibuat!")
print(f"Size: {len(content):,} chars")
