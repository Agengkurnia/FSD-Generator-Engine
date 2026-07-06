import os
import datetime

def generate_fsd():
    today = datetime.datetime.now().strftime('%d %B %Y')
    md = f"""---
title: FSD Laboratory Formula Modules
version: 1.1
date: {today}
author: IDC System Team
---

# 1. Document Information

| Attribute | Detail |
| :--- | :--- |
| **Document Name** | Functional Specification Document - Laboratory Formula |
| **Module** | Formulation (Premix, Blending, Liquid, Baking, Drying, Packaging) |
| **System** | IDC System |
| **Version** | 1.1 |
| **Status** | Final |

## 1.1. Revision History
- **v1.0**: Pembuatan struktur awal dokumen FSD Laboratory Formula dengan layout UI baru.
- **v1.1**: Perubahan format *Data Definition* menjadi naratif dan penambahan informasi *Stored Procedures (SP)* dari sistem *legacy* KN2017 untuk keperluan migrasi logika *backend*.

---

# 2. Module Overview
Modul **Laboratory Formula** adalah ekosistem penyusunan resep (formulasi) yang saling terintegrasi dalam sistem R&D. Proses formulasi berjenjang (3-Layer) memastikan standarisasi mulai dari pembuatan premix bahan baku, pembentukan base liquid/powder, hingga finalisasi produk beserta kemasannya. Tujuan utama proyek ini adalah memigrasikan tampilan ke arsitektur SPA IDC System, sedangkan struktur *database* dan *Business Logic* tetap mempertahankan sistem KN2017.

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

Setiap modul di bawah ini dilengkapi dengan pembahasan detail terkait form, tabulasi antarmuka, serta daftar *Stored Procedure (SP)* yang mendasari proses transaksi database.

"""

    modules = [
        ("Premix Formula", "premixformula", 
         "Premix Formula digunakan untuk menghitung bahan-bahan pra-campuran mikronutrien (Premix).", 
         "Batch Size dihitung otomatis berdasarkan akumulasi bahan penyusun.", 
         False,
         ["spTrPremixFormulaSelectAll (Read Index)", "spTrPremixFormulaByID (Read Detail)", "spTrCalculatePremix (Proses Kalkulasi Parameter)", "spTrPremixFormulationPushApproval (Submit Approval)", "spTrPushToPremixTemp (Simpan ke Temp sebelum dihitung)", "trCreateFormulationNo (Generate Nomor Formula)"]),
        
        ("Blending Formula (Dry Blend)", "blendingformula", 
         "Blending Formula digunakan untuk pencampuran bahan kering (powder base).", 
         "Modul ini memiliki keterkaitan dengan Food Category dan memuat regulasi khusus OD Regulation.", 
         False,
         ["spTrFormulaSelectAll dengan parameter 'DR' (Read Index)", "spTrFormulaByID dengan parameter 'DR' (Read Detail)", "spGetDataDryBlendForFixedCalculate (Kalkulasi Fixed)", "spTrGetCategoryFood & spTrGetCategoryFoodById (Pencarian Kategori Makanan)", "spTrDryBlendFormulationPushApproval (Submit Approval)", "trCreateFormulationNo (Generate Nomor Formula)"]),
        
        ("Liquid Formula", "liquidformula", 
         "Liquid Formula untuk produk berbasis cairan.", 
         "Kalkulasi modul ini sangat spesifik, karena sisa formula otomatis dikonversi menjadi kandungan Water (Air = Batch Size - Total Ingredients).", 
         False,
         ["spTrFormulaSelectAll dengan parameter 'LQ' (Read Index)", "spTrFormulaByID dengan parameter 'LQ' (Read Detail)", "spTrCalculateLiquid (Proses Kalkulasi dengan pengecekan Overdosage, Max, Min)", "spTrGetCategoryFood & spTrGetCategoryFoodById (Pencarian Kategori Makanan)", "spTrLiquidFormulationPushApproval (Submit Approval)", "trCreateFormulationNo (Generate Nomor Formula)"]),
        
        ("Baking Formula", "bakingformula", 
         "Baking Formula digunakan untuk produk panggang/snack bar.", 
         "Dilengkapi mekanisme penentuan Main Ingredient sebagai basis acuan formulasi.", 
         False,
         ["spTrFormulaSelectAll dengan parameter 'BK' (Read Index)", "spTrFormulaByID dengan parameter 'BK' (Read Detail)", "spTrCalculateBaking (Proses Kalkulasi Parameter & Nutrisi)", "spTrGetCategoryFood & spTrGetCategoryFoodById", "spTrBakingFormulationPushApproval (Submit Approval)", "trCreateFormulationNo (Generate Nomor Formula)"]),
        
        ("Drying Formula", "dryingformula", 
         "Drying Formula digunakan untuk menghitung penyusutan bobot bahan cair setelah pengeringan.", 
         "Terdapat perhitungan persentase Solid dan Yield.", 
         False,
         ["spTrFormulaSelectAll dengan parameter 'DY' (Read Index)", "spTrFormulaByID dengan parameter 'DY' (Read Detail)", "spTrCalculateDrying (Perhitungan Yield & Solid Percentage)", "spTrDryingFormulationPushApproval (Submit Approval)", "trCreateFormulationNo (Generate Nomor Formula)"]),
        
        ("Packaging Formula", "packagingformula", 
         "Tahap akhir penentuan spesifikasi dan material kemasan.", 
         "Modul ini harus merujuk ke RM Formula No (kode output dari layer 1/2) untuk mendefinisikan packaging.", 
         True,
         ["spTrPackagingSelectAll (Read Index)", "spTrPackagingGetProjectInfo & spTrPackagingGetFormulaNo (Informasi Referensi)", "spTrPackagingDetailByID & spTrPackagingParameterByID (Load Grid)", "spTrPackagingCalculateQty (Hitung otomatis quantity material misal Can/Lid per batch)", "spTrPackagingPushApproval (Submit Approval)", "spTrPackagingDeleteAllDetailByID & spTrPackagingDeleteAllParameterByID (Reset Grid)", "trCreateFormulationNo (Generate Nomor Formula)"])
    ]

    for i, (title, prefix, desc1, desc2, is_pkg, sp_list) in enumerate(modules):
        tab3_name = "Packaging Parameters" if is_pkg else "Ingredient Detail"
        tab3_id = "params" if is_pkg else "ingredients"
        tab4_name = "Packaging Materials" if is_pkg else "Calculation Result"
        tab4_id = "materials" if is_pkg else "result"
        
        sp_table = "| Stored Procedure Name | Description |\n| :--- | :--- |\n"
        for sp in sp_list:
            parts = sp.split(" (", 1)
            sp_name = parts[0]
            sp_desc = parts[1].replace(")", "") if len(parts) > 1 else ""
            sp_table += f"| `{sp_name}` | {sp_desc} |\n"

        md += f"""
## 3.{i + 1}. {title}

**{desc1}** {desc2}

### A. Backend Stored Procedures (Migration Target)
Proses bisnis {title} di *backend* menggunakan *Stored Procedures (SP)* bawaan sistem KN2017 berikut. UI baru harus melakukan *binding* data ke API yang memanggil SP ini:

{sp_table}

### B. Index Page
Halaman Index berfungsi untuk mencari, menyaring, dan menampilkan daftar {title} yang sudah tersimpan di sistem.

![Screenshot: {title} Index](screenshots/{prefix}_index.png)

**Data Definition & Behavior:**
- **Keyword (Text)**: Bersifat opsional. Digunakan untuk pencarian multi-kriteria (berdasarkan Project No, Formula No, atau Description).
- **Status (Dropdown)**: Bersifat opsional. Menyaring formula berdasarkan status dokumen (DRAFT, IN REVIEW, APPROVED, REJECTED).
- **Add New**: Membuka form {title} kosong untuk pembuatan baru.
- **Edit / View**: Mengakses halaman detail untuk memodifikasi formula (jika DRAFT) atau sekadar melihat rekapitulasi data.

---

### C. Detail Page
Form detail {title} terbagi menjadi 4 tab yang harus dilalui secara berurutan.

#### Tab 1: Project Information
Tab ini bersifat informatif (*read-only*) paska user memilih rujukan Project.

![Screenshot: {title} - Tab Project](screenshots/{prefix}_tab_project.png)

**Data Definition & Behavior:**
- **Date (Date)**: Wajib. Diisi otomatis dengan tanggal hari ini saat *form* dibuat (Creation Date).
- **Project No (LOV)**: Wajib. Merupakan pintu gerbang pembuatan formula. Pengguna memilih ID proyek melalui pop-up LOV yang membaca data dari `Project Header`.
- **Project Type, Product Type, Brand, Variant (Text)**: Wajib/Opsional tergantung ketersediaan data. Seluruhnya akan otomatis terisi (auto-fill) begitu Project No dipilih. Kolom ini bersifat *read-only*.

#### Tab 2: Formulation Setup
Pengaturan parameter inti formula, termasuk ukuran produksi (*batch*) dan material keluaran.

![Screenshot: {title} - Tab Formula](screenshots/{prefix}_tab_formula.png)

**Data Definition & Behavior:**
- **Formula No (Text)**: Wajib. Field *read-only* yang akan otomatis di-*generate* (melalui `trCreateFormulationNo`) ketika pengguna menekan tombol *Save* untuk pertama kali.
- **Batch Size (Kg) (Numeric)**: Wajib. Mengatur kapasitas total produksi. 
  - *Note Khusus*: Pada modul Premix, nilai ini terkalkulasi otomatis secara *bottom-up* dari total konversi material bahan, sehingga *field* di-*disable*. Pada modul lain, nilai ini harus di-input manual.
- **Item Code & Description (LOV)**: Wajib. Mengidentifikasi barang/material apa yang secara sistematis dihasilkan (*output*) oleh formula ini.
- **Formula Name (Text)**: Wajib. Judul naratif dari formulasi (contoh: *Base Vanilla Liquid X*).
- **Serving Size (Numeric)**: Wajib. Satuan gram/ml dari satu takaran saji produk jadi.
"""

        if is_pkg:
            md += f"""
> [!NOTE]
> Pada Packaging Formula, terdapat *field* wajib **RM Formula No** yang harus diisi via LOV. Fungsi *field* ini adalah menghubungkan spesifikasi kemasan dengan "isi"-nya, yakni produk yang dihasilkan dari proses Premix/Blending/Liquid/Baking di tahap sebelumnya.

#### Tab 3: {tab3_name}
Area input grid parameter spesifikasi kemasan (misal: dimensi kardus, berat kotor, tipe tutup kaleng).

![Screenshot: {title} - Tab {tab3_name}](screenshots/{prefix}_tab_{tab3_id}.png)

**Fitur Operasional:**
- **Implementasi Grid**: Wajib menggunakan komponen **PQ Grid** (seperti standar *IDC System*) untuk memungkinkan edit di dalam sel (*inline editing*).
- **Add / Delete Parameter**: Menambah jenis parameter secara leluasa.
- **Copy From Packing**: Fungsi utilitas untuk menduplikasi seluruh parameter dari spesifikasi kemasan lama, memotong waktu *data entry*.

#### Tab 4: {tab4_name}
Area input grid material penyusun fisik kemasan (contoh: kaleng, tutup, sendok ukur, label bungkus).

![Screenshot: {title} - Tab {tab4_name}](screenshots/{prefix}_tab_{tab4_id}.png)

**Fitur Operasional:**
- **Integrasi Kalkulasi Otomatis**: Setiap kali ada perubahan *Batch Size* atau isi kemasan (*Netto*), sistem wajib mengeksekusi fungsi `spTrPackagingCalculateQty` per baris material. Tujuannya adalah menghitung pasti kebutuhan jumlah PCS kaleng/sendok per proses produksi.
- Pengguna cukup mengisi rasio kemasan, dan nilai final kuantitas (Qty per Batch) bersifat statis (*calculated*).

"""
        else:
            md += f"""
#### Tab 3: {tab3_name}
Fasilitas input grid bahan penyusun racikan (*bill of materials*).

![Screenshot: {title} - Tab {tab3_name}](screenshots/{prefix}_tab_{tab3_id}.png)

**Fitur Operasional:**
- **Implementasi Grid**: Menggunakan komponen **PQ Grid** untuk memfasilitasi penambahan puluhan bahan dengan mudah.
- **Dosage (%)**: Input utama persentase komposisi per bahan. Sistem akan melakukan fungsi matematika dasar untuk menampilkan estimasi satuan Kg pada kolom *Dosage Konv* (dikalikan dengan Batch Size).
- **Copy From Oracle / Lab Formula**: Untuk mempercepat pekerjaan R&D, grid bahan bisa diisi massal hasil kloning dari formula sebelumnya, atau integrasi spesifikasi dari sistem Oracle.

#### Tab 4: {tab4_name}
Representasi analitik hasil perhitungan nutrisi/kandungan aktif dari racikan formula yang divalidasi.

![Screenshot: {title} - Tab {tab4_name}](screenshots/{prefix}_tab_{tab4_id}.png)

**Fitur Operasional:**
- Tombol **Calculate** memegang peranan vital. Saat diklik, sistem mengeksekusi SP kalkulasi kompleks (misal `spTrCalculateLiquid` atau `spTrCalculateBaking`).
- SP ini akan mengurai nilai *Specific Gravity*, mengalikan setiap takaran, lalu membandingkan hasil dengan batas *Overdosage (OD)*, toleransi *Max*, dan *Min*.
- Jika ada hasil yang di luar toleransi (seperti defisit parameter), UI harus dapat memberikan indikator peringatan kepada formulator.

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
    out_path = os.path.join(script_dir, "FSD_LaboratoryFormula_v1.1.md")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(MARKDOWN_CONTENT)
        
    print("FSD Laboratory Formula v1.1 berhasil dibuat!")
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(script)

if __name__ == "__main__":
    generate_fsd()
