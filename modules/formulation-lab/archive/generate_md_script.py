import os
import datetime

def generate_fsd():
    today = datetime.datetime.now().strftime('%d %B %Y')
    md = f"""---
title: FSD Laboratory Formula Modules
version: 1.0
date: {today}
author: IDC System Team
---

# 1. Document Information

| Attribute | Detail |
| :--- | :--- |
| **Document Name** | Functional Specification Document - Laboratory Formula |
| **Module** | Formulation (Premix, Blending, Liquid, Baking, Drying, Packaging) |
| **System** | IDC System |
| **Version** | 1.0 |
| **Status** | Final |

---

# 2. Module Overview
Modul **Laboratory Formula** adalah ekosistem penyusunan resep (formulasi) yang saling terintegrasi dalam sistem R&D. Proses formulasi berjenjang (3-Layer) memastikan standarisasi mulai dari pembuatan premix bahan baku, pembentukan base liquid/powder, hingga finalisasi produk beserta kemasannya.

## 2.1. Hierarchical Flow (3-Layer)
```mermaid
flowchart TD
    subgraph L1 [Layer 1: Base & Premix]
        P(Premix Formula)
        B(Dry Blend Formula)
    end
    subgraph L2 [Layer 2: Product Formulation]
        L(Liquid Formula)
        BA(Baking Formula)
        D(Drying Formula)
    end
    subgraph L3 [Layer 3: Finishing]
        PKG(Packaging Formula)
    end

    P -->|Used as RM| L2
    B -->|Used as RM| L2
    L2 -->|Reference for| PKG
```

---

# 3. Detailed Form Specifications

Setiap modul di bawah ini dilengkapi dengan pembahasan detail terkait input form, struktur tab, dan mekanisme operasional.

"""

    modules = [
        ("Premix Formula", "premixformula", "Premix Formula digunakan untuk menghitung bahan-bahan pra-campuran mikronutrien (Premix).", "Batch Size dihitung otomatis berdasarkan akumulasi bahan penyusun.", False),
        ("Blending Formula (Dry Blend)", "blendingformula", "Blending Formula digunakan untuk pencampuran bahan kering (powder base).", "Modul ini memiliki keterkaitan dengan Food Category dan memuat regulasi khusus OD Regulation.", False),
        ("Liquid Formula", "liquidformula", "Liquid Formula untuk produk berbasis cairan.", "Kalkulasi modul ini sangat spesifik, karena sisa formula otomatis dikonversi menjadi kandungan Water (Air).", False),
        ("Baking Formula", "bakingformula", "Baking Formula digunakan untuk produk panggang/snack bar.", "Dilengkapi mekanisme penentuan Main Ingredient sebagai basis acuan formulasi.", False),
        ("Drying Formula", "dryingformula", "Drying Formula digunakan untuk menghitung penyusutan bobot bahan cair setelah pengeringan.", "Terdapat perhitungan Yield dan Solid percentage.", False),
        ("Packaging Formula", "packagingformula", "Tahap akhir penentuan spesifikasi dan material kemasan.", "Modul ini harus merujuk ke RM Formula No (kode output dari layer 1/2) untuk mendefinisikan packaging.", True)
    ]

    for title, prefix, desc1, desc2, is_pkg in modules:
        tab3_name = "Packaging Parameters" if is_pkg else "Ingredient Detail"
        tab3_id = "params" if is_pkg else "ingredients"
        tab4_name = "Packaging Materials" if is_pkg else "Calculation Result"
        tab4_id = "materials" if is_pkg else "result"
        
        md += f"""
## 3.{modules.index((title, prefix, desc1, desc2, is_pkg)) + 1}. {title}

**{desc1}** {desc2}

### A. Index Page
Halaman Index berfungsi untuk mencari, menyaring, dan menampilkan daftar {title} yang sudah tersimpan di sistem.

![Screenshot: {title} Index](screenshots/{prefix}_index.png)

**1. Pencarian & Filter:**
| Field Name | Type | Mandatory | Description |
| :--- | :--- | :--- | :--- |
| Keyword | Text | No | Pencarian multi-kriteria berdasarkan Project No, Formula No, atau Description |
| Status | Dropdown | No | Filter status (DRAFT, REJECTED, APPROVED) |

**2. Aksi Grid:**
- **Add New**: Membuka form {title} kosong untuk pembuatan baru.
- **Edit**: Mengakses halaman detail untuk memodifikasi formula yang berstatus DRAFT.
- **View**: Membuka form dalam mode *read-only*.

---

### B. Detail Page
Form ini terbagi menjadi 4 tab utama untuk memfasilitasi pembuatan formulasi.

#### Tab 1: Project Information
Tab ini bersifat otomatis terisi (read-only). Informasi ditarik saat user melakukan *lookup* Project No.

![Screenshot: {title} - Tab Project](screenshots/{prefix}_tab_project.png)

**Data Definition:**
| Field Name | Type | Mandatory | Source / Behavior |
| :--- | :--- | :--- | :--- |
| Date | Date | Yes | Auto-generated saat pembuatan dokumen |
| Project No | LOV | Yes | Diambil dari modul Project Header via Pop-up LOV |
| Project Type | Text | Yes | Terisi otomatis berdasarkan tipe Project |
| Product Type | Text | Yes | Terisi otomatis berdasarkan Project (contoh: POWDER/LIQUID) |
| Brand | Text | No | Brand payung produk |
| Variant | Text | No | Varian spesifik produk |

#### Tab 2: Formulation Setup
Pengaturan parameter inti formula, termasuk nomor unik, ukuran *batch*, dan referensi target.

![Screenshot: {title} - Tab Formula](screenshots/{prefix}_tab_formula.png)

**Data Definition:**
| Field Name | Type | Mandatory | Source / Behavior |
| :--- | :--- | :--- | :--- |
| Formula No | Text | Yes | Digenerate otomatis oleh sistem saat pertama kali *Save* |
| Batch Size (Kg) | Numeric | Yes | Kapasitas produksi per batch. Pada Premix, nilai ini *read-only* (hasil rekap ingredients) |
| Item Code | LOV | Yes | Kode material luaran (Output RM) yang akan dihasilkan formula ini |
| Formula Name | Text | Yes | Deskripsi naratif dari formulasi |
| Serving Size | Numeric | Yes | Takaran saji dalam ukuran gram/ml |
| Remarks | Text Area | No | Catatan tambahan |

"""
        if is_pkg:
            md += f"""
> [!NOTE]
> Pada Packaging Formula, terdapat field krusial **RM Formula No** yang harus diisi via LOV. Field ini merelasikan spesifikasi kemasan dengan formulasi produk jadinya.

#### Tab 3: {tab3_name}
Area input grid parameter spesifikasi kemasan (misal: dimensi, berat kotor, jenis segel).

![Screenshot: {title} - Tab {tab3_name}](screenshots/{prefix}_tab_{tab3_id}.png)

**Fitur Operasional:**
- Menggunakan komponen PQ Grid.
- User dapat menambahkan baris baru untuk setiap jenis parameter.
- Terdapat tombol **Copy From Packing** untuk menduplikasi template parameter dari dokumen terdahulu.

#### Tab 4: {tab4_name}
Area input grid material komponen (Can, Lid, Carton, Label).

![Screenshot: {title} - Tab {tab4_name}](screenshots/{prefix}_tab_{tab4_id}.png)

**Fitur Operasional:**
- Menyertakan mekanisme kalkulasi (Stored Procedure `spTrPackagingCalculateQty`) untuk menghitung otomatis jumlah PCS material berbanding dengan kapasitas Batch Size produk cair/kering yang akan dikemas.
- Grid menggunakan PQ Grid terintegrasi penuh.

"""
        else:
            md += f"""
#### Tab 3: {tab3_name}
Fasilitas input grid bahan penyusun (*bill of materials*).

![Screenshot: {title} - Tab {tab3_name}](screenshots/{prefix}_tab_{tab3_id}.png)

**Fitur Operasional:**
- **Add Row**: Menambahkan baris bahan baru.
- **LOV Item Code**: Pencarian material bahan baku.
- **Dosage (%)**: Input utama komposisi. *Dosage Konv (Kg)* akan terkalkulasi seiring dengan *Batch Size*.
- **Copy From Oracle / Copy From Lab Formula**: Fitur kloning komposisi.

#### Tab 4: {tab4_name}
Representasi analitik hasil perhitungan nutrisi/kandungan dari racikan.

![Screenshot: {title} - Tab {tab4_name}](screenshots/{prefix}_tab_{tab4_id}.png)

**Fitur Operasional:**
- Tombol **Calculate** akan memicu prosedur kalkulasi pada database untuk memproses setiap bahan baku di Tab 3 dengan faktor *Specific Gravity*, takaran *Serving*, dan *OD Regulation*.
- Grid Result (read-only) menampilkan kolom Target Value, % AKG, hingga komparasi batas Max/Min.

"""

    md += """
---

# 4. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    TR_PROJECT ||--o{ TR_FORMULA_HEADER : "has"
    TR_FORMULA_HEADER ||--|{ TR_FORMULA_DETAIL : "contains"
    TR_FORMULA_HEADER {
        int intFormulaID PK
        varchar ProjectNo FK
        varchar FormulaNo
        decimal BatchSize
        varchar ItemCode
    }
    TR_FORMULA_DETAIL {
        int intDetailID PK
        int intFormulaID FK
        varchar MaterialCode
        decimal Dosage
    }
    TR_PACKAGING_HEADER ||--o{ TR_PACKAGING_MATERIAL : "contains"
    TR_PACKAGING_HEADER ||--o{ TR_PACKAGING_PARAM : "defines"
```

"""
    out_path = os.path.join(os.path.dirname(__file__), "gen_lab_formula_fsd.py")
    script = f'''import os
import datetime

MARKDOWN_CONTENT = """{md.replace('"""', '\\"\\"\\"')}"""

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "FSD_LaboratoryFormula_v1.0.md")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(MARKDOWN_CONTENT)
        
    print("FSD Laboratory Formula berhasil dibuat!")
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(script)

if __name__ == "__main__":
    generate_fsd()
