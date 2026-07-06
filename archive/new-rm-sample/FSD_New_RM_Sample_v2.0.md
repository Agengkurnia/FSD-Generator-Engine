# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
## Modul: New RM Sample Management
### Sistem: IDC System (New RM Selection)

---

| Atribut          | Keterangan                                           |
|------------------|------------------------------------------------------|
| **Nama Dokumen** | FSD Modul New RM Sample Management                   |
| **Versi**        | 2.0                                                  |
| **Tanggal**      | 8 April 2026                                         |
| **Divisi**       | R&D / Procurement / ICT                              |
| **Status**       | Draft                                                |
| **Dibuat oleh**  | Tim ICT – IDC System                                 |

---

## Riwayat Revisi

| Versi | Tanggal       | Diubah Oleh     | Keterangan                                                                                  |
|-------|---------------|-----------------|---------------------------------------------------------------------------------------------|
| 1.0   | —             | Tim ICT         | Initial draft                                                                               |
| 1.8   | Feb 2026      | Tim ICT         | Penambahan ERD, DDL scripts, modul RM Database                                              |
| 1.9   | Feb 2026      | Tim ICT         | Update field EG-DEG di Step 3, data LOV dari MAppParam                                     |
| **2.0** | **Apr 2026** | **Tim ICT**   | Penghapusan field Shipping Method dari accordion Storage & Shelf Life; penambahan dropdown **Status Organik** dan **Potensi Bahan Mengandung EG DEG** (multi-select, Select2) ke accordion **Halal, GMO & PHO** di Step 1; EG-DEG dipindahkan dari Step 3 ke Step 1 |

---

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
   - 1.1 [Tujuan Dokumen](#11-tujuan-dokumen)
   - 1.2 [Ruang Lingkup](#12-ruang-lingkup)
   - 1.3 [Stakeholder](#13-stakeholder)
2. [Ringkasan Business Flow](#2-ringkasan-business-flow)
   - 2.1 [Proses As-Is (Manual)](#21-proses-as-is-manual)
   - 2.2 [Proses To-Be (Sistem IDC)](#22-proses-to-be-sistem-idc)
3. [Spesifikasi Fungsional](#3-spesifikasi-fungsional)
   - 3.1 [Halaman Index – New RM Sample](#31-halaman-index--new-rm-sample)
   - 3.2 [Halaman Detail – Wizard Form (4 Step)](#32-halaman-detail--wizard-form-4-step)
4. [Struktur Database](#4-struktur-database)
5. [Aturan Bisnis](#5-aturan-bisnis)
6. [List of Values (LOV) & Referensi Data](#6-list-of-values-lov--referensi-data)
7. [Hak Akses & Peran Pengguna](#7-hak-akses--peran-pengguna)
8. [Notifikasi](#8-notifikasi)
9. [Appendix A – SQL Server DDL Scripts](#appendix-a-sql-server-ddl-scripts)

---

## 1. Pendahuluan

Modul **New RM Sample Management** merupakan modul dalam sistem IDC (Integrated Data Center) untuk mengelola proses pengajuan, evaluasi, dan disposisi sample Raw Material baru dari supplier. Modul ini dirancang untuk menggantikan proses manual yang sebelumnya dilakukan melalui email dan spreadsheet, menjadi alur terstandardisasi dengan workflow yang terstruktur dan terdokumentasi secara digital.

### 1.1 Tujuan Dokumen

Dokumen ini bertujuan untuk:

1. Menjelaskan fungsionalitas lengkap modul New RM Sample Management di sistem IDC.
2. Menjadi acuan pengembangan (*development reference*) bagi tim ICT.
3. Mendeskripsikan alur proses, desain layar, struktur database, serta aturan bisnis yang berlaku.
4. Mendokumentasikan field, validasi, dan business rules untuk setiap step workflow.
5. Mencatat perubahan desain terkini (v2.0) — penambahan Status Organik & EG-DEG, penghapusan Shipping Method.

### 1.2 Ruang Lingkup

Dokumen ini mencakup dua halaman utama:

1. `NewRMSampleIndex.html` – Halaman daftar & monitoring semua RM Sample
2. `NewRMSampleDetail.html` – Halaman wizard form 4-step untuk input, evaluasi, dan disposisi sample

**Empat Step Workflow:**

| Step | Nama            | Deskripsi                                                 |
|------|-----------------|-----------------------------------------------------------|
| 1    | Document Registration | Pendaftaran dan dokumentasi sample RM dari supplier       |
| 2    | Document Sample  | Analisis tujuan dan kebutuhan sample, mapping ke produk   |
| 3    | RM Evaluation   | Testing dan evaluasi teknis sample di laboratorium        |
| 4    | Disposition     | Review final dan keputusan approve / reject / on hold     |

### 1.3 Stakeholder

| Peran                | Tim / Nama              | Keterlibatan                                               |
|----------------------|-------------------------|-------------------------------------------------------------|
| Business Owner       | Procurement / R&D       | Pemilik proses bisnis, validasi kebutuhan                  |
| ICT Developer        | KN IT                   | Pengembangan dan implementasi                              |
| Sample Requestor (PIC) | Procurement Team      | Menerima sample, dokumentasi awal, koordinasi supplier     |
| R&D Team            | R&D Department          | Analisis purpose, mapping produk, set requirement          |
| Lab / QC Team       | Laboratorium / QC       | Testing sample, validasi compliance, quality scoring       |
| Decision Maker      | Manager / Supervisor    | Review hasil evaluasi, keputusan final (approve/reject)    |
| Approver            | Management              | Final approval untuk sample yang di-approve (jika perlu)  |

---

## 2. Ringkasan Business Flow

### 2.1 Proses As-Is (Manual)

Sebelum sistem IDC, proses evaluasi RM Sample dilakukan secara manual:

- **Penerimaan Sample**: Supplier mengirim sample fisik, PIC mencatat via email atau spreadsheet Excel.
- **Analisis Purpose**: R&D menganalisis tujuan melalui meeting dan komunikasi informal, tidak ada tracking terstruktur.
- **Evaluasi Lab**: Hasil testing dikirim via email, tidak ada centralized tracking per sample.
- **Keputusan**: Decision maker memberikan keputusan verbal atau via email, tidak ada audit trail.

| Aspek              | Proses Lama (Manual)                        | Proses Baru (IDC)                              |
|--------------------|---------------------------------------------|------------------------------------------------|
| Pencatatan         | Spreadsheet Excel / Email                   | Database terpusat, web-based                   |
| Tracking           | Manual, tidak real-time                     | Dashboard otomatis, real-time                  |
| Dokumen Pendukung  | File attachment via email                   | Upload langsung ke sistem, per tahap           |
| Audit Trail        | Tidak ada / tidak terstruktur               | Full history log setiap perubahan              |
| Notifikasi         | Manual (email pribadi)                      | Otomatis oleh sistem                           |
| Keputusan          | Verbal / email tidak terstruktur            | Formal disposition dengan timestamp & reason   |

### 2.2 Proses To-Be (Sistem IDC)

#### 2.2.1 Flow Diagram

*(Gambar 1: New RM Sample Business Flow Diagram)*

```mermaid
flowchart TD
    subgraph Row1 [Tahap 1: Evaluasi]
        direction LR
        Start(["Mulai"]) --> Step1["STEP 1: DOCUMENT REGISTRATION"] --> Step2["STEP 2: DOCUMENT SAMPLE"] --> Step3["STEP 3: RM EVALUATION"]
    end
    
    Step3 --> Step4["STEP 4: DISPOSITION"]
    
    subgraph Row2 [Tahap 2: Keputusan]
        direction RL
        Step4 --> Decision{"Keputusan?"}
        Decision --> |"APPROVED"| ApprovalCheck{"Perlu Approval?"}
        Decision --> |"REJECTED"| EndReject(["REJECTED"])
        Decision --> |"ON HOLD"| OnHold["ON HOLD"]
        Decision --> |"CANCELLED"| EndCancel(["CANCELLED"])
    end
    
    OnHold -.-> |"Kembali"| Step3
    ApprovalCheck --> PendingApproval["Pending Approval"]
    ApprovalCheck --> |"Tidak"| Completed1(["COMPLETED"])
    
    subgraph Row3 [Tahap 3: Approval Atasan]
        direction LR
        PendingApproval --> ApproverReview["Approver Review"] --> ApprovalDecision{"Hasil Approval?"}
        ApprovalDecision --> |"APPROVE"| Completed(["COMPLETED"])
    end
    
    ApprovalDecision -.-> |"REJECT"| Step4

    style Start fill:#8CC63F,color:#fff,stroke:#009B4D,stroke-width:2px
    style Completed fill:#388E3C,color:#fff,stroke:#1B5E20,stroke-width:2px
    style Completed1 fill:#388E3C,color:#fff,stroke:#1B5E20,stroke-width:2px
    style EndReject fill:#D32F2F,color:#fff,stroke:#B71C1C,stroke-width:2px
    style EndCancel fill:#9E9E9E,color:#fff,stroke:#616161,stroke-width:2px
    style Step1 fill:#FFF3CD,stroke:#FFC107,stroke-width:2px
    style Step2 fill:#D1ECF1,stroke:#17A2B8,stroke-width:2px
    style Step3 fill:#E2E3E5,stroke:#6C757D,stroke-width:2px
    style Step4 fill:#F8D7DA,stroke:#DC3545,stroke-width:2px
    style Decision fill:#FFF3E0,stroke:#F7941E,stroke-width:3px
    style ApprovalCheck fill:#FFF3E0,stroke:#F7941E,stroke-width:2px
    style ApprovalDecision fill:#FFF3E0,stroke:#F7941E,stroke-width:2px
    style OnHold fill:#E7F3FF,stroke:#0D6EFD,stroke-width:2px
    style PendingApproval fill:#FFF9C4,stroke:#F57F17,stroke-width:2px
    style ApproverReview fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
```

#### 2.2.2 Status Sample

| Kode              | Label              | Deskripsi                                                              |
|-------------------|--------------------|------------------------------------------------------------------------|
| `DRAFT`           | Draft              | Baru dibuat, wizard belum selesai                                      |
| `PENDING`         | Pending            | Dalam proses evaluasi (salah satu step sedang berjalan)                |
| `PENDING_APPROVAL`| Pending Approval   | Disposisi Approved, menunggu approval atasan                           |
| `COMPLETED`       | Completed          | Semua step selesai, keputusan final sudah diberikan                    |
| `REJECTED`        | Rejected           | Keputusan disposisi adalah Rejected                                    |
| `ON_HOLD`         | On Hold            | Ditunda, menunggu informasi tambahan                                   |
| `CANCELLED`       | Cancelled          | Dibatalkan oleh PIC (hanya saat masih Draft)                          |

---

## 3. Spesifikasi Fungsional

### 3.1 Halaman Index – New RM Sample

**Path**: `NewRMSampleIndex.html`

**Tujuan**: Menampilkan semua RM Sample dalam bentuk daftar tabel, dilengkapi dashboard ringkasan berdasarkan workflow stage.

#### 3.1.1 Deskripsi

*(Gambar 2: Halaman Index – Dashboard dan Data Table)*

| Card               | Warna               | Isi                                                   |
|--------------------|---------------------|-------------------------------------------------------|
| Total Samples      | Biru (Primary)      | Total semua sample yang terdaftar                     |
| Step 1: Document   | Kuning (Warning)    | Sample yang sedang di tahap dokumentasi               |
| Step 2: Analysis   | Cyan (Info)         | Sample yang sedang di tahap analisis purpose          |
| Step 3: Evaluation | Abu-abu (Secondary) | Sample yang sedang di tahap evaluasi teknis           |
| Completed          | Hijau (Success)     | Sample yang sudah selesai (approved/rejected)         |

#### 3.1.2 Functional Description

**Action Bar:**

| Tombol              | Fungsi                                                              |
|---------------------|---------------------------------------------------------------------|
| Create New Sample   | Arahkan ke halaman Detail dengan wizard fresh (mode Create)         |
| Export Excel        | Export data tabel ke format Excel (.xlsx)                           |

**Tabel Daftar Sample:**

| Kolom          | Sumber Data          | Keterangan                                          |
|----------------|----------------------|-----------------------------------------------------|
| Sample No      | `txtSampleNo`        | Nomor unik sample (format: XXX-R-RM-MM-YY)          |
| Material Name  | `txtMaterialName`    | Nama material/RM yang di-sample                     |
| Supplier Name  | `txtSupplierName`    | Nama supplier yang mengajukan sample                |
| Date           | `dtSubmissionDate`   | Tanggal submission sample                           |
| Workflow Stage | `txtWorkflowStage`   | Tahap workflow saat ini (Badge berwarna)             |
| Status         | `txtStatus`          | Status sample (Badge warna sesuai status)           |
| Action         | —                    | Dropdown: Edit / View / Delete                      |

#### 3.1.3 Business Rules & Validation

| Status Sample    | Tombol Action | Keterangan                                            |
|------------------|---------------|-------------------------------------------------------|
| Draft            | Edit / Delete | Bisa diedit dan dihapus (soft delete)                 |
| Pending          | Edit          | Bisa diedit (lanjutkan wizard)                        |
| Completed        | View          | Read-only, tidak bisa diedit atau dihapus             |
| Rejected         | View          | Read-only                                             |
| On Hold          | Edit          | Bisa diedit untuk kembali ke Step 3                   |

---

### 3.2 Halaman Detail – Wizard Form (4 Step)

**Path**: `NewRMSampleDetail.html`

**Tujuan**: Form wizard 4 step untuk mengelola lifecycle lengkap RM Sample dari dokumentasi hingga disposition.

*(Gambar 3: Halaman Detail – 4-Step Wizard Form)*

---

#### 3.2.1 Step 1: Document Registration

*(Gambar 4: Step 1 – Document Registration)*

**Fungsi Utama:**
- Mendokumentasikan informasi dasar sample RM dari supplier
- Input data supplier, material, pricing, quantity, informasi Halal-GMO-Organik
- Upload dokumen pendukung (COA, MSDS, Spec Sheet, dll)

**Sub-Accordion di Step 1:**

| Accordion             | Konten Utama                                                            |
|-----------------------|-------------------------------------------------------------------------|
| Supplier & Material   | Material Name, Supplier, Principal, Country, Plant Site                 |
| Pricing & Packaging   | Currency, Price, UOM, Net Weight, Packaging                             |
| Storage & Shelf Life  | Storage Condition (LOV), Shelf Life (Months)                            |
| **Halal, GMO & PHO**  | Halal Category, Halal Body, GMO Status, Contains PHO, **Status Organik**, **Potensi Bahan Mengandung EG DEG** |
| Allergen Information  | Checklist allergen (Gluten, Egg, Fish, Peanuts, dll.)                   |
| BTP Content           | Tabel: BTP Name, Function, PPM                                          |
| Project Members (PIC) | Tabel assignee per departemen (auto-fill dari Item Code PM)             |

> **Perubahan v2.0**: Accordion "Storage & Shelf Life" **tidak lagi** memuat field Shipping Method. Field Status Organik dan Potensi EG DEG kini berada di accordion **Halal, GMO & PHO**.

**Keterangan Field — Accordion Supplier & Material:**

| Field Name        | ID Elemen                     | Mandatory | Validasi              | Keterangan                                                  |
|-------------------|-------------------------------|-----------|-----------------------|-------------------------------------------------------------|
| Type Document     | `txtTypeDocument`             | Yes       | LOV Selection         | Jenis dokumen (New Material / Replacement / Alternative)    |
| Sample No         | `txtSampleNo`                 | Auto      | Auto-generated        | Nomor unik sample (format: XXX-R-RM-MM-YY)                  |
| I2MS Project No   | `txtI2MSProjectNo`            | No        | LOV Selection         | Nomor proyek I2MS terkait (opsional)                        |
| Sample Date       | `sampleDate`                  | Yes       | Date                  | Tanggal sample diterima                                     |
| Date of Receipt   | `receiptDate`                 | Yes       | Date                  | Tanggal penerimaan fisik sample                             |
| Material Name     | `materialName`                | Yes       | Min 3, Max 200 char   | Nama material yang di-sample                                |
| Supplier          | `DocumentSample_txtSupplierName`| Yes     | LOV Selection         | Supplier yang mengajukan sample                             |
| Principal         | `principalName`               | No        | Max 200 char          | Nama manufacturer / principal                               |
| Country           | `DocumentSample_txtCountryName`| No       | LOV Selection         | Negara manufaktur                                           |
| Plant Site        | `plantSite`                   | No        | Max 200 char          | Lokasi pabrik                                               |

**Keterangan Field — Accordion Pricing & Packaging:**

| Field Name  | ID Elemen                          | Mandatory   | Validasi                | Keterangan                       |
|-------------|------------------------------------|-------------|-------------------------|----------------------------------|
| Currency    | `DocumentSample_txtCurrencyName`   | Conditional | LOV Selection           | Wajib jika Price diisi           |
| Price       | `price`                            | No          | Numeric, >= 0           | Harga per UOM                    |
| UOM         | `DocumentSample_txtUOMName`        | Yes         | LOV Selection           | Unit of Measure (kg, liter, pcs) |
| Net Weight  | `netWeight`                        | Yes         | Numeric, > 0            | Berat bersih sample              |
| Packaging   | `packaging`                        | No          | Max 200 char            | Informasi kemasan                |

**Keterangan Field — Accordion Storage & Shelf Life:**

| Field Name        | ID Elemen                              | Mandatory | Validasi         | Keterangan                                  |
|-------------------|----------------------------------------|-----------|------------------|---------------------------------------------|
| Storage Condition | `DocumentSample_txtStorageCondition`   | Yes       | LOV Selection    | Kondisi penyimpanan (source: MAppParam)     |
| Shelf Life (Months)| `shelfLife`                           | No        | Numeric, > 0     | Masa simpan dalam bulan                     |

> **Catatan v2.0**: Field **Shipping Method** (`shipping`) telah **dihapus** dari accordion ini mulai versi 2.0.

**Keterangan Field — Accordion Halal, GMO & PHO:**

| Field Name                        | ID Elemen              | Mandatory | Validasi               | Keterangan                                                            |
|-----------------------------------|------------------------|-----------|------------------------|-----------------------------------------------------------------------|
| Halal Category                    | `Halal_txtHalalDesc`   | No        | LOV Selection          | Kategori halal material (source: master Halal Category)               |
| Halal Body                        | `Halal_txtHalalBodyInst`| No       | LOV Selection          | Lembaga sertifikasi halal (MUI, JAKIM, dll.)                          |
| GMO Status                        | `Halal_txtGMOStatusDesc`| Yes      | LOV Selection          | Status GMO: Non GMO / GMO Free / PCR Negative                         |
| Contains PHO                      | `pho`                  | Yes       | Select (Yes/No)        | Apakah mengandung Partially Hydrogenated Oil                          |
| **Status Organik** *(Baru v2.0)*  | `evalStatusOrganik`    | No        | Select                 | NON ORGANIK / ORGANIK (source: MAppParam)                             |
| **Potensi EG DEG** *(Baru v2.0)*  | `evalEgDeg`            | No        | Multi-select (Select2) | Pilihan: N/A, Gliserol, Polietilen Glikol, Propilen Glikol, Sorbitol Cair (source: MAppParam) |

**Document Attachment Table:**

- Upload multiple dokumen per sample (COA, MSDS, Spec Sheet, dll)
- Kolom: Document Type, Remarks, File Name, Upload Date, Action (Delete)
- Format yang didukung: PDF, DOC, DOCX, XLS, XLSX, JPG, PNG
- Ukuran maksimum: **10 MB** per file

---

#### 3.2.2 Step 2: Document Sample

*(Gambar 5: Step 2 – Document Sample)*

**Fungsi Utama:**
- Mendefinisikan tujuan dan alasan pengajuan sample
- Mapping sample dengan product/formula yang akan menggunakan material
- Input target usage percentage dan expected benefit

**Keterangan Field:**

| Field Name        | ID Elemen             | Mandatory | Validasi               | Keterangan                                            |
|-------------------|-----------------------|-----------|------------------------|-------------------------------------------------------|
| RM Category       | `rmCategory`          | Yes       | LOV Selection          | Kategori RM (Dairy, Flavoring, dll.)                  |
| Purpose Type      | `txtSamplePurposeType`| Yes       | LOV Selection          | New Ingredients / Alternative / dll.                  |
| Item Code Trial   | `txtItemCodeTrial`    | Yes       | LOV Selection          | Kode item trial dari IDC                              |
| Item Code Existing| `txtItemCodeExisting` | No        | LOV Selection          | Material yang akan digantikan (jika ada)              |
| Objective         | `objective`           | No        | Max 2000 char          | Tujuan penggunaan sample                              |
| Analysis Deadline | `dtAnalysisDeadline`  | Yes       | Date, >= Current Date  | Target deadline analisis sample                       |

**Variant Table (Apply to Product):**

- Tabel mapping product group, parent type, child type, dan Kategori Pangan
- Kategori Pangan dipilih via LOV dengan search
- Multiple row diperbolehkan

---

#### 3.2.3 Step 3: RM Evaluation

*(Gambar 6: Step 3 – RM Evaluation)*

**Fungsi Utama:**
- Input hasil testing dan evaluasi teknis sample di laboratorium
- Comparison dengan spec requirement dan existing material
- Upload hasil lab test dan trial production

**Keterangan Field:**

| Field Name              | ID Elemen               | Mandatory | Validasi              | Keterangan                                         |
|-------------------------|-------------------------|-----------|------------------------|----------------------------------------------------|
| Penyusun Bahan Baku     | `txtMaterialComposition`| No        | Text                  | Deskripsi komposisi bahan baku                     |
| Test Result Category    | Tab panel               | —         | —                     | Organoleptic, Nutrition, Microbiology, Heavy Metal, Antibiotics, Mycotoxin, Pesticides, Foreign |
| Status Conformance      | Per test row            | No        | Selection             | Conform / Non Conform per parameter                |

> **Catatan v2.0**: Field **Status Organik** dan **Potensi EG DEG** telah **dipindahkan** dari Step 3 ke accordion Halal, GMO & PHO di Step 1 (sejak versi 2.0). Tab parameter uji masih lengkap di Step 3.

**Tabel Parameter Uji (per kategori):**

| Kolom           | Keterangan                                                  |
|-----------------|-------------------------------------------------------------|
| Test Code       | Kode parameter uji (LOV Search)                             |
| Test Class      | Kategori: Physical / Chemical / Microbiology                |
| Regulation No   | Nomor regulasi acuan                                        |
| Regulation Min  | Batas minimum regulasi                                      |
| Regulation Max  | Batas maximum regulasi                                      |
| Spec Supplier Min / Max / Target | Nilai spec dari supplier                 |
| COA Result      | Hasil dari dokumen COA                                      |
| Analysis Result | Hasil analisa laboratorium internal                         |
| Spec SHP Min / Max | Nilai spec internal SHP                               |
| Target          | Nilai target                                                |

---

#### 3.2.4 Step 4: Disposition

*(Gambar 7: Step 4 – Disposition)*

**Fungsi Utama:**
- Review summary lengkap dari semua step sebelumnya (read-only)
- Input keputusan final (Approved / Rejected / On Hold)
- Setup approval workflow jika keputusan memerlukan persetujuan atasan

**Keterangan Field:**

| Field Name          | ID Elemen              | Mandatory    | Validasi               | Keterangan                                        |
|---------------------|------------------------|--------------|------------------------|---------------------------------------------------|
| Disposition Decision| `txtDisposition`       | Yes          | Selection              | Keputusan: Approved / Rejected / On Hold          |
| Decision Date       | `dtDecisionDate`       | Auto         | Auto: Current Date     | Tanggal keputusan dibuat                          |
| Decision By         | `txtDecisionBy`        | Auto         | Auto from Login User   | User yang membuat keputusan                       |
| Reason              | `txtReason`            | Yes          | Min 10, Max 1000 char  | Alasan keputusan (wajib untuk semua keputusan)    |
| Next Action         | `txtNextAction`        | No           | Max 500 char           | Action plan selanjutnya (jika On Hold / Approved) |
| Approval Required   | `bitApprovalRequired`  | No           | Boolean (Yes/No)       | Apakah memerlukan approval atasan                 |
| Approver            | `txtApproverId`        | Conditional  | LOV Selection          | Wajib jika Approval Required = Yes                |

**Summary Review Section (Read-Only):**
- Menampilkan ringkasan data dari Step 1, 2, dan 3
- Link ke dokumen attachment yang sudah diupload

---

#### 3.2.5 Wizard Navigation & Actions

**Tombol Navigasi:**

| Button            | Visibility       | Fungsi                                                         |
|-------------------|------------------|----------------------------------------------------------------|
| Previous          | Step 2, 3, 4     | Kembali ke step sebelumnya (data tersimpan)                    |
| Next Step         | Step 1, 2, 3     | Lanjut ke step berikutnya (validasi field mandatory terlebih dahulu) |
| Save Draft        | Semua Step       | Simpan sebagai draft, bisa dilanjutkan nanti                   |
| Submit Complete   | Step 4 only      | Submit final — ubah status menjadi Completed / Pending Approval|
| Back to Index     | Semua Step       | Kembali ke halaman Index tanpa mengubah data                   |

---

## 4. Struktur Database

> **Database**: SQL Server – `IDC_Formulation`
> **Engine**: Microsoft SQL Server
> **Referensi DDL**: `idc-system/Database/Scripts/03 – 06_Step*.sql`

### 4.1 Konvensi Penamaan (Actual)

| Prefix | Tipe Data | Contoh |
|--------|-----------|--------|
| `int` | INT (auto-inc) | `intId`, `intSampleHeaderId` |
| `txt` | VARCHAR | `txtSampleNo`, `txtMaterialName` |
| `dt` / `dtm` | DATE / DATETIME | `dtSampleDate`, `dtmCreatedDate` |
| `dec` | DECIMAL | `decPricePerUOM`, `decOverallScore` |
| `bit` | BIT | `bitActive`, `bitApprovalRequired` |
| `tr` | Tabel transaksi | `trRMSample_Header`, `trDocumentSample_Header` |
| `m` | Tabel master | `mDepartment`, `mSampleType` |

**Primary Key Convention (Dual PK):**
- `intId` — INT IDENTITY auto-increment (FK reference)
- `txtId` — VARCHAR(50) GUID (unique business key)

**Audit Fields (setiap tabel transaksi):**
`txtCreatedBy`, `dtmCreatedDate`, `txtUpdatedBy`, `dtmUpdatedDate`, `bitActive`

### 4.2 Entity Relationship Diagram (ERD)

*(Gambar 8: ERD – Relasi Tabel Modul New RM Sample)*

```mermaid
erDiagram
    trRMSample_Header {
        int intId PK
        varchar txtId UK
        varchar txtSampleNo UK
        int intStatusId
        int intCurrentStep
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trDocumentSample_Header {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        date dtSampleDate
        int intTypeDocumentId FK
        varchar txtMaterialName
        varchar txtSupplierName
        int intStorageId FK
        varchar txtHalalCategoryCode
        int intHalalBodyId FK
        varchar txtGMOStatus
        bit bitContainPHO
        varchar txtStatusOrganik
        varchar txtEgDegContent
        int intShelfLifeMonth
    }
    trDocumentSample_Allergen {
        int intId PK
        int intSampleHeaderId FK
        varchar txtAllergenCode
        bit bitIsChecked
    }
    trDocumentSample_BTP {
        int intId PK
        int intSampleHeaderId FK
        varchar txtBTPName
        varchar txtFunctionName
        decimal decPercentagePPM
    }
    trDocumentSample_Document {
        int intId PK
        int intSampleHeaderId FK
        varchar txtDocumentType
        varchar txtFileName
        varchar txtFilePath
    }
    trSamplePurpose_Header {
        int intId PK
        int intSampleHeaderId FK
        varchar txtRMCategoryCode
        varchar txtSamplePurposeType
        varchar txtItemCodeTrial
        varchar txtItemCodeExisting
        varchar txtObjective
    }
    trRMEvaluation_Header {
        int intId PK
        int intSampleHeaderId FK
        decimal decOverallScore
        varchar txtEvaluationStatus
        varchar txtMaterialComposition
    }
    trRMDisposition_Header {
        int intId PK
        int intSampleHeaderId FK
        varchar txtDecision
        datetime dtDecisionDate
        bit bitApprovalRequired
        varchar txtApprovalStatus
    }

    trRMSample_Header ||--o| trDocumentSample_Header : "has Step1"
    trRMSample_Header ||--o{ trDocumentSample_Allergen : "has Allergens"
    trRMSample_Header ||--o{ trDocumentSample_BTP : "has BTP"
    trRMSample_Header ||--o{ trDocumentSample_Document : "has Documents"
    trRMSample_Header ||--o| trSamplePurpose_Header : "has Step2"
    trRMSample_Header ||--o| trRMEvaluation_Header : "has Step3"
    trRMSample_Header ||--o| trRMDisposition_Header : "has Step4"
```

### 4.3 Tabel Transaksi

Total tabel transaksi: **11 tabel**, terbagi per step workflow.

#### STEP 1 – Document Registration (5 Tabel)

**4.3.1 `trDocumentSample_Header`** — Step 1: Data Dokumentasi Sample

> **Perubahan v2.0**: Kolom `txtShippingMethod` dihapus. Ditambahkan kolom `txtStatusOrganik` dan `txtEgDegContent` untuk menyimpan data dari accordion Halal, GMO & PHO.

| Kolom | Tipe Data | Nullable | Keterangan |
|-------|-----------|----------|------------|
| `intId` | INT IDENTITY (PK) | No | Primary key |
| `txtId` | VARCHAR(50) (UK) | No | GUID |
| `intSampleHeaderId` | INT (FK) | No | FK → `trRMSample_Header.intId` |
| `dtSampleDate` | DATE | No | Tanggal pembuatan dokumen |
| `intTypeDocumentId` | INT (FK) | No | FK → master type document |
| `txtMaterialName` | VARCHAR(200) | No | Nama material |
| `txtPrincipalName` | VARCHAR(200) | No | Nama principal/manufacturer |
| `intSupplierId` | INT (FK) | Yes | FK → master supplier |
| `txtSupplierName` | VARCHAR(200) | No | Nama supplier (denormalized) |
| `intShelfLifeMonth` | INT | No | Masa simpan (bulan) |
| `txtPackaging` | VARCHAR(200) | No | Kemasan |
| ~~`txtShippingMethod`~~ | ~~VARCHAR(200)~~ | ~~Yes~~ | **DIHAPUS** di v2.0 |
| `intStorageId` | INT (FK) | No | FK → `mAppParam` (STORAGE_CONDITION) |
| `txtHalalCategoryCode` | VARCHAR(10) | No | Kode kategori halal |
| `intHalalBodyId` | INT (FK) | No | FK → master halal body |
| `dtDateReceipt` | DATE | No | Tanggal terima sample |
| `txtCurrencyCode` | VARCHAR(10) | No | Kode mata uang |
| `txtUOMCode` | VARCHAR(10) | No | Kode UOM |
| `decPricePerUOM` | DECIMAL(18,2) | Yes | Harga per UOM |
| `decNetWeight` | DECIMAL(18,4) | Yes | Berat bersih |
| `intPegawaiId` | INT (FK) | No | FK → user/pegawai (PIC) |
| `txtGMOStatus` | VARCHAR(50) | No | Non GMO / GMO Free / PCR Negative |
| `bitContainPHO` | BIT | No | Mengandung PHO (0=No, 1=Yes) |
| **`txtStatusOrganik`** | **VARCHAR(50)** | **Yes** | **Baru v2.0** — NON ORGANIK / ORGANIK (source: MAppParam) |
| **`txtEgDegContent`** | **VARCHAR(MAX)** | **Yes** | **Baru v2.0** — JSON/CSV pilihan EG DEG (source: MAppParam) |

---

**4.3.2 `trDocumentSample_Allergen`** — Allergen Checklist

Multiple rows per sample, satu row per allergen type yang dicek.

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| `intId` | INT IDENTITY (PK) | Primary key |
| `txtId` | VARCHAR(50) (UK) | GUID |
| `intSampleHeaderId` | INT (FK) | FK → `trRMSample_Header.intId` |
| `intDocSampleHeaderId` | INT (FK) | FK → `trDocumentSample_Header.intId` |
| `txtAllergenCode` | VARCHAR(50) | e.g. CEREAL_GLUTEN, EGG, FISH |
| `txtAllergenName` | VARCHAR(200) | Nama allergen lengkap |
| `bitIsChecked` | BIT | 0=Tidak mengandung, 1=Mengandung |

---

**4.3.3 `trDocumentSample_BTP`** — Carry Over BTP

Multiple rows, satu row per BTP item.

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| `intId` | INT IDENTITY (PK) | Primary key |
| `txtId` | VARCHAR(50) (UK) | GUID |
| `intSampleHeaderId` | INT (FK) | FK → `trRMSample_Header.intId` |
| `intDocSampleHeaderId` | INT (FK) | FK → `trDocumentSample_Header.intId` |
| `intLineNo` | INT | Nomor urut baris |
| `txtBTPName` | VARCHAR(200) | Nama BTP |
| `txtFunctionName` | VARCHAR(200) | Fungsi BTP |
| `decPercentagePPM` | DECIMAL(18,4) | Persentase dalam ppm |

---

**4.3.4 `trDocumentSample_Document`** — Upload Dokumen Pendukung

Multiple rows, satu row per file yang diupload.

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| `intId` | INT IDENTITY (PK) | Primary key |
| `txtId` | VARCHAR(50) (UK) | GUID |
| `intSampleHeaderId` | INT (FK) | FK → `trRMSample_Header.intId` |
| `txtDocumentType` | VARCHAR(50) | Specification / COA / Halal Certificate / dll. |
| `txtFileName` | VARCHAR(255) | Nama file asli |
| `txtFilePath` | VARCHAR(500) | Path server |
| `txtFileExtension` | VARCHAR(10) | pdf, jpg, docx, dll |
| `intFileSize` | INT | Ukuran file (bytes) |
| `dtExpiredDate` | DATE | Tanggal expired (opsional) |
| `txtRemarks` | VARCHAR(MAX) | Keterangan |

---

#### STEP 2 – Document Sample (2 Tabel)

**4.3.5 `trSamplePurpose_Header`** dan **4.3.6 `trSamplePurpose_Product`** — Data Purpose & Produk Tujuan

*(Struktur sama dengan versi 1.9, tidak ada perubahan di v2.0)*

---

#### STEP 3 – RM Evaluation (3 Tabel)

**4.3.7 `trRMEvaluation_Header`**

> **Perubahan v2.0**: Kolom `txtStatusOrganik` dan `txtEgDegContent` dipindahkan ke `trDocumentSample_Header`. Kolom di tabel ini dikembalikan ke strukturnya yang lebih fokus pada hasil evaluasi lab.

| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| `intId` | INT IDENTITY (PK) | Primary key |
| `txtId` | VARCHAR(50) (UK) | GUID |
| `intSampleHeaderId` | INT (FK) | FK → `trRMSample_Header.intId` |
| `decOverallScore` | DECIMAL(5,2) | Skor keseluruhan (0–100) |
| `txtEvaluationStatus` | VARCHAR(50) | Draft / Completed / Reviewed |
| `txtEvaluationNotes` | VARCHAR(MAX) | Catatan Evaluasi |
| `txtMaterialComposition` | VARCHAR(MAX) | Deskripsi penyusun bahan baku |

---

#### STEP 4 – Disposition (1 Tabel)

**4.3.8 `trRMDisposition_Header`** — Keputusan Final & Approval

*(Struktur tidak berubah dari versi 1.9)*

---

### 4.4 Tabel Master yang Digunakan (Existing)

| Nama Tabel | DB Asal | Digunakan di | Keterangan |
|------------|---------|--------------|------------|
| `mDepartment` | KN2017_Formulation | LOV Departemen | Departemen user |
| `mAppParam` | IDC_Formulation | Step 1 | Storage condition, Status Organik, EG-DEG options |
| Master supplier, currency, UOM, pegawai | Existing | Step 1, 4 | Reuse dari modul lain |

> **Catatan v2.0**: `mAppParam` kini juga menjadi source untuk **Status Organik** dan opsi **EG DEG**. Filter: `WHERE txtAppParamVariable IN ('IDC_STATUS_ORGANIK', 'IDC_EG_DEG_OPTION')`.

---

## 5. Aturan Bisnis

### 5.1 Pembuatan Sample

1. **Sample No** bersifat read-only dan di-generate otomatis saat save pertama kali, format: `{DEPT}-R-RM-{MM}-{YY}`.
2. **Submission Date** default adalah tanggal hari ini dan tidak dapat diubah manual.
3. **Status** awal adalah `DRAFT` dan tidak dapat diubah manual.

### 5.2 Navigasi Wizard

1. User harus menyelesaikan step secara **berurutan** — tidak bisa lompat ke step yang belum dilalui.
2. Data tersimpan otomatis ketika user berpindah step (klik Next Step).
3. Tombol **Previous** tersedia di Step 2, 3, dan 4 untuk kembali ke step sebelumnya tanpa kehilangan data.
4. Draft bisa diedit kapan saja sebelum Submit Complete.

### 5.3 Validasi Field

1. Semua field mandatory harus terisi sebelum user bisa lanjut ke step berikutnya.
2. **Price Currency** wajib diisi jika field Price diisi.
3. **Approver** wajib diisi jika `bitApprovalRequired = 1`.
4. **Catatan Keputusan** (Reason) wajib minimal 10 karakter untuk semua jenis keputusan disposisi.
5. **Analysis Deadline** tidak boleh kurang dari tanggal hari ini.
6. **Status Organik** dan **EG DEG** bersifat opsional (tidak mandatory) di Step 1.

### 5.4 Upload Dokumen

1. Format file yang diizinkan: **PDF, DOC, DOCX, XLS, XLSX, JPG, PNG**. Ukuran maksimum: **10 MB** per file.
2. Multiple file diperbolehkan per sample.
3. File yang sudah diupload bisa dihapus hanya saat status masih **Draft** atau **Pending**.

### 5.5 Submit & Perubahan Status

1. Tombol **Submit Complete** hanya muncul di Step 4 (Disposition).
2. Setelah Submit Complete:
   - Jika `bitApprovalRequired = 0`: status berubah menjadi `COMPLETED`.
   - Jika `bitApprovalRequired = 1`: status berubah menjadi `PENDING_APPROVAL`, notifikasi dikirim ke Approver.
3. Sample dengan status **Completed** atau **Rejected** tidak bisa diedit dan tidak bisa dihapus.

### 5.6 EG DEG Multi-Select

1. Field **Potensi Bahan Mengandung EG DEG** menggunakan komponen **Select2 multi-select** sehingga user dapat memilih lebih dari satu opsi.
2. Pilihan tersedia: **N/A**, Gliserol, Polietilen Glikol, Propilen Glikol, Sorbitol Cair.
3. Nilai tersimpan dalam format JSON/CSV di kolom `txtEgDegContent` pada `trDocumentSample_Header`.
4. Default value saat form dibuat: **N/A**.

---

## 6. List of Values (LOV) & Referensi Data

| LOV Name              | Sumber Data         | Query / Endpoint                                                                    | Field Tujuan                      |
|-----------------------|---------------------|-------------------------------------------------------------------------------------|-----------------------------------|
| Type Document         | `M_TYPE_DOCUMENT`   | `SELECT * FROM M_TYPE_DOCUMENT WHERE bitActive = 1`                                 | `txtTypeDocument`                 |
| Supplier              | `M_SUPPLIER`        | `SELECT * FROM M_SUPPLIER WHERE bitActive = 1`                                      | `txtSupplierName`, `intSupplierId`|
| Currency              | `M_CURRENCY`        | `SELECT * FROM M_CURRENCY WHERE bitActive = 1`                                      | `txtCurrencyId`                   |
| UOM                   | `M_UOM`             | `SELECT * FROM M_UOM WHERE bitActive = 1`                                           | `txtUOMCode`                      |
| Storage Condition     | `mAppParam`         | `WHERE txtAppParamVariable = 'IDC_STORAGE_CONDITION'`                               | `DocumentSample_txtStorageCondition`|
| Halal Category        | Master Halal Cat    | `SELECT * FROM mHalalCategory WHERE bitActive = 1`                                  | `Halal_txtHalalDesc`              |
| Halal Body            | Master Halal Body   | `SELECT * FROM mHalalBody WHERE bitActive = 1`                                      | `Halal_txtHalalBodyInst`          |
| GMO Status            | `mAppParam`         | `WHERE txtAppParamVariable = 'IDC_GMO_STATUS'`                                      | `Halal_txtGMOStatusDesc`          |
| **Status Organik**    | **`mAppParam`**     | **`WHERE txtAppParamVariable = 'IDC_STATUS_ORGANIK'`**                              | **`evalStatusOrganik`**           |
| **Potensi EG DEG**    | **`mAppParam`**     | **`WHERE txtAppParamVariable = 'IDC_EG_DEG_OPTION'`**                              | **`evalEgDeg` (multi-select)**    |
| I2MS Project No       | IDC Project Master  | LOV modal dengan search                                                              | `txtI2MSProjectNo`                |
| PIC / Pegawai         | `M_PEGAWAI`         | `SELECT * FROM M_PEGAWAI WHERE bitActive = 1`                                       | `DocumentSample_txtPegawaiName`   |
| Approver              | `M_PEGAWAI`         | `SELECT * FROM M_PEGAWAI WHERE bitActive = 1 AND txtRole IN ('MANAGER','ADMIN')`    | `txtApproverId`                   |

> **Catatan**: Field `evalEgDeg` menggunakan komponen **Select2 multi-select** agar user bisa memilih lebih dari satu bahan sekaligus. Opsi data di-load dari `mAppParam` dengan variable `IDC_EG_DEG_OPTION`.

---

## 7. Hak Akses & Peran Pengguna

| Peran            | Buat Sample | Edit Sample         | Upload Dokumen | Submit Complete | Approve  | Lihat Semua |
|------------------|-------------|---------------------|----------------|-----------------|----------|-------------|
| PIC / Requestor  | ✓           | ✓ (milik sendiri)   | ✓              | ✓               | ✗        | ✗           |
| R&D Team         | ✓           | ✓ (milik sendiri)   | ✓              | ✓               | ✗        | ✗           |
| Lab / QC Team    | ✗           | ✓ (Step 3 only)     | ✓              | ✗               | ✗        | ✗           |
| Manager          | ✗           | ✗                   | ✗              | ✗               | ✓        | ✓           |
| Administrator    | ✓           | ✓                   | ✓              | ✓               | ✓        | ✓           |

---

## 8. Notifikasi

| Event                              | Penerima                          | Jenis            |
|------------------------------------|-----------------------------------|------------------|
| Sample baru berhasil dibuat        | PIC (konfirmasi)                  | In-App           |
| Sample masuk ke Step 3 (Evaluation)| Lab / QC Team terkait             | Email + In-App   |
| Sample Submit Complete             | Approver (jika required)          | Email + In-App   |
| Approver telah approve             | PIC / Requestor                   | Email + In-App   |
| Approver telah reject              | PIC / Requestor                   | Email + In-App   |
| Sample Completed                   | PIC / Requestor                   | Email + In-App   |
| Sample Rejected (Disposisi)        | PIC / R&D Team                    | Email + In-App   |
| Reminder deadline sample           | PIC / Evaluator yang belum action | Email (Terjadwal)|

---

*Dokumen ini dibuat berdasarkan analisis kebutuhan sistem dan kode sumber yang ada oleh tim ICT.*
*Revisi dokumen dilakukan jika ada perubahan spesifikasi dari Business Owner.*

**End of Document**

---

## Appendix A: SQL Server DDL Scripts

> **Database:** `IDC_Formulation` (SQL Server)
> **Konvensi:** Nama tabel `tr` prefix + PascalCase. Dual PK: `intId` (IDENTITY) + `txtId` (VARCHAR GUID).

### A.1 `trRMSample_Header` — Unified Workflow Header

```sql
IF OBJECT_ID('dbo.trRMSample_Header', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[trRMSample_Header](
        [intId]           INT           IDENTITY(1,1) NOT NULL,
        [txtId]           VARCHAR(50)   NOT NULL,
        [txtSampleNo]     VARCHAR(50)   NOT NULL,
        [intStatusId]     INT           NOT NULL DEFAULT 0,
        [intCurrentStep]  INT           NOT NULL DEFAULT 1,
        [txtCreatedBy]    VARCHAR(100)  NOT NULL,
        [dtmCreatedDate]  DATETIME      NOT NULL DEFAULT GETDATE(),
        [txtUpdatedBy]    VARCHAR(100)  NULL,
        [dtmUpdatedDate]  DATETIME      NULL,
        [bitActive]       BIT           NOT NULL DEFAULT 1,
        CONSTRAINT [PK_trRMSample_Header] PRIMARY KEY ([intId]),
        CONSTRAINT [UQ_trRMSample_Header_txtId] UNIQUE ([txtId]),
        CONSTRAINT [UQ_trRMSample_Header_SampleNo] UNIQUE ([txtSampleNo])
    )
END
GO
```

### A.2 `trDocumentSample_Header` — Step 1: Document Registration (v2.0)

> **v2.0**: Kolom `txtShippingMethod` dihapus. Ditambah `txtStatusOrganik` dan `txtEgDegContent`.

```sql
IF OBJECT_ID('dbo.trDocumentSample_Header', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[trDocumentSample_Header](
        [intId]                INT           IDENTITY(1,1) NOT NULL,
        [txtId]                VARCHAR(50)   NOT NULL,
        [intSampleHeaderId]    INT           NOT NULL,
        [dtSampleDate]         DATE          NOT NULL,
        [intTypeDocumentId]    INT           NOT NULL,
        [txtMaterialName]      VARCHAR(200)  NOT NULL,
        [txtPrincipalName]     VARCHAR(200)  NOT NULL,
        [intSupplierId]        INT           NULL,
        [txtSupplierName]      VARCHAR(200)  NOT NULL,
        [intShelfLifeMonth]    INT           NOT NULL,
        [txtPackaging]         VARCHAR(200)  NOT NULL,
        -- [txtShippingMethod] VARCHAR(200) NULL  -- REMOVED in v2.0
        [intStorageId]         INT           NOT NULL,
        [txtHalalCategoryCode] VARCHAR(10)   NOT NULL,
        [intHalalBodyId]       INT           NOT NULL,
        [dtDateReceipt]        DATE          NOT NULL,
        [txtCurrencyCode]      VARCHAR(10)   NOT NULL,
        [txtUOMCode]           VARCHAR(10)   NOT NULL,
        [decPricePerUOM]       DECIMAL(18,2) NULL,
        [decNetWeight]         DECIMAL(18,4) NULL,
        [intPegawaiId]         INT           NOT NULL,
        [txtGMOStatus]         VARCHAR(50)   NOT NULL,
        [bitContainPHO]        BIT           NOT NULL DEFAULT 0,
        [txtStatusOrganik]     VARCHAR(50)   NULL,   -- NEW in v2.0: NON ORGANIK / ORGANIK
        [txtEgDegContent]      VARCHAR(MAX)  NULL,   -- NEW in v2.0: JSON multi-select EG DEG
        [txtCreatedBy]         VARCHAR(100)  NOT NULL,
        [dtmCreatedDate]       DATETIME      NOT NULL DEFAULT GETDATE(),
        [txtUpdatedBy]         VARCHAR(100)  NULL,
        [dtmUpdatedDate]       DATETIME      NULL,
        [bitActive]            BIT           NOT NULL DEFAULT 1,
        CONSTRAINT [PK_trDocumentSample_Header] PRIMARY KEY ([intId]),
        CONSTRAINT [UQ_trDocumentSample_Header_txtId] UNIQUE ([txtId]),
        CONSTRAINT [FK_trDocumentSample_Header_Sample] FOREIGN KEY ([intSampleHeaderId])
            REFERENCES [dbo].[trRMSample_Header]([intId])
    )
END
GO
```

### A.3 Script Alter untuk Database Existing (Migrasi v1.9 → v2.0)

```sql
-- Hapus kolom Shipping Method (jika sudah ada di database)
IF COL_LENGTH('dbo.trDocumentSample_Header', 'txtShippingMethod') IS NOT NULL
BEGIN
    ALTER TABLE [dbo].[trDocumentSample_Header]
    DROP COLUMN [txtShippingMethod];
    PRINT 'txtShippingMethod column dropped.';
END
GO

-- Tambah kolom Status Organik (jika belum ada)
IF COL_LENGTH('dbo.trDocumentSample_Header', 'txtStatusOrganik') IS NULL
BEGIN
    ALTER TABLE [dbo].[trDocumentSample_Header]
    ADD [txtStatusOrganik] VARCHAR(50) NULL;
    PRINT 'txtStatusOrganik column added.';
END
GO

-- Tambah kolom EG DEG Content (jika belum ada)
IF COL_LENGTH('dbo.trDocumentSample_Header', 'txtEgDegContent') IS NULL
BEGIN
    ALTER TABLE [dbo].[trDocumentSample_Header]
    ADD [txtEgDegContent] VARCHAR(MAX) NULL;
    PRINT 'txtEgDegContent column added.';
END
GO
```

### A.4 Seed Data MAppParam untuk Opsi EG-DEG dan Status Organik

```sql
-- Seeding mAppParam untuk Status Organik
INSERT INTO [dbo].[mAppParam] (txtAppParamVariable, txtAppParamCode, txtAppParamName, bitActive)
SELECT 'IDC_STATUS_ORGANIK', 'NON_ORGANIK', 'NON ORGANIK', 1
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[mAppParam] WHERE txtAppParamVariable = 'IDC_STATUS_ORGANIK' AND txtAppParamCode = 'NON_ORGANIK');

INSERT INTO [dbo].[mAppParam] (txtAppParamVariable, txtAppParamCode, txtAppParamName, bitActive)
SELECT 'IDC_STATUS_ORGANIK', 'ORGANIK', 'ORGANIK', 1
WHERE NOT EXISTS (SELECT 1 FROM [dbo].[mAppParam] WHERE txtAppParamVariable = 'IDC_STATUS_ORGANIK' AND txtAppParamCode = 'ORGANIK');
GO

-- Seeding mAppParam untuk Opsi EG DEG
INSERT INTO [dbo].[mAppParam] (txtAppParamVariable, txtAppParamCode, txtAppParamName, bitActive)
VALUES
    ('IDC_EG_DEG_OPTION', 'NA',              'N/A',              1),
    ('IDC_EG_DEG_OPTION', 'GLISEROL',        'Gliserol',         1),
    ('IDC_EG_DEG_OPTION', 'POLIETILEN_GLIKOL','Polietilen Glikol',1),
    ('IDC_EG_DEG_OPTION', 'PROPILEN_GLIKOL', 'Propilen Glikol',  1),
    ('IDC_EG_DEG_OPTION', 'SORBITOL_CAIR',   'Sorbitol Cair',    1);
GO
```

---

*End of Appendix A*
