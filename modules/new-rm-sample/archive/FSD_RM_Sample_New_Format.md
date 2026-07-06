# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
# NEW RM SAMPLE MANAGEMENT SYSTEM
## VERSI 1.8 - SIMPLIFIED WORKFLOW DIAGRAM

### INFORMASI DOKUMEN
| Item | Keterangan |
|---|---|
| Nama Modul | New RM Sample Management |
| Versi Dokumen | 1.8 (Simplified Workflow Diagram) |
| Tanggal | 16 Maret 2026 |
| Status | Draft - Enhanced |
| Penyusun | Development Team |

### DAFTAR ISI
1. Pendahuluan
2. Ringkasan Business Flow
3. Spesifikasi Fungsional
4. Struktur Database
5. Business Rules
6. UI Specifications
7. Integration Points
8. Reporting
9. Lampiran

## 1. PENDAHULUAN
### 1.1 Tujuan Dokumen
Dokumen ini menjelaskan spesifikasi fungsional dari sistem New RM Sample Management yang merupakan revamp dari tiga modul terpisah (Document Sample, Sample Purpose, dan RM Evaluation) menjadi satu sistem terintegrasi dengan 4 tahapan proses.

### 1.2 Ruang Lingkup
Sistem ini mencakup:
- Penerimaan dan dokumentasi sample RM dari supplier
- Pendefinisian tujuan penggunaan sample
- Evaluasi teknis dan pengujian laboratorium
- Keputusan disposisi akhir (Approve/Reject/On Hold)

### 1.3 Stakeholder
- R&D Department: Pengguna utama untuk evaluasi sample
- QA/QC Department: Reviewer hasil pengujian
- Purchasing Department: Monitoring status sample untuk procurement
- Management: Approval keputusan akhir

## 2. RINGKASAN BUSINESS FLOW
### 2.1 Proses As-Is (Legacy System)
Sistem lama menggunakan 3 form terpisah: 
1. Document Sample: Input data penerimaan sample 
2. Sample Purpose: Definisi tujuan penggunaan 
3. RM Evaluation: Evaluasi teknis dan hasil lab 

Masalah:
- Data terpisah-pisah
- Duplikasi input
- Tracking progress sulit
- Tidak ada workflow approval terintegrasi

### 2.2 Proses To-Be (New System)
#### 2.2.1 Workflow Flowchart
![Workflow Flowchart](screenshots/new_rm_sample_flow_clear.png){width=100%}

Keuntungan:
- Single entry point
- Progress tracking real-time
- Workflow approval terintegrasi
- Data consistency terjaga

## 3. SPESIFIKASI FUNGSIONAL
Format: Setiap form/halaman didokumentasikan dengan 4 komponen wajib: 
1. Deskripsi — Nama form, tujuan, dan navigation path 
2. Screenshot — Tampilan visual halaman 
3. Functional Description — Detail setiap element UI beserta data source 
4. Business Rules & Validation — RBAC, status permission, field validation, dan business logic

![Status Transition](screenshots/new_rm_sample_erd.png){width=60%}

### 3.1 INDEX PAGE — Daftar New RM Sample
#### 3.1.1 Deskripsi
Navigation: Sidebar > RM Selection > New RM Sample 
Halaman ini menampilkan daftar seluruh data New RM Sample dalam bentuk DataTable, dilengkapi dashboard summary cards untuk monitoring status secara real-time. User dapat melakukan pencarian, filter, dan aksi (View/Edit/Delete) pada setiap record.

#### 3.1.2 Screenshot
![Index Page Dashboard](screenshots/NewRMSample_Index_Page.png)

#### 3.1.3 Functional Description

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Summary Cards | Display | Menampilkan jumlah: Total, Pending, Approved, Rejected, On Hold | Query COUNT GROUP BY status dari trRMSample_Header |
| 2 | Btn New | Button | Buka halaman detail baru, status = Draft | - |
| 3 | Search - Date Range | DatePicker | Filter data berdasarkan range tanggal sample | Field dtSampleDate |
| 4 | Search - Status | Dropdown | Filter data berdasarkan status | Field intStatusId |
| 5 | Search - Supplier | Text Input | Filter berdasarkan nama supplier | Field txtSupplierName |
| 6 | Search - Material | Text Input | Filter berdasarkan nama material | Field txtMaterialName |
| 7 | DataTable | Grid | Menampilkan list data dengan paging, sorting | API: /api/NewRMSample/List |
| 8 | Btn View | Button | Buka detail dalam mode read-only | Navigate ke Detail page by intId |
| 9 | Btn Edit | Button | Buka detail dalam mode edit | Navigate ke Detail page by intId |
| 10 | Btn Delete | Button | Confirm dialog → soft delete (bitActive = 0) | API: /api/NewRMSample/Delete/{id} |

**Kolom DataTable:**

| No | Column | Description | Sortable | Searchable |
|---|---|---|---|---|
| 1 | Sample No | Nomor sample (SMPL-YYYY-XXXX) | Ya | Ya |
| 2 | Material Name | Nama material dari supplier | Ya | Ya |
| 3 | Supplier Name | Nama supplier | Ya | Ya |
| 4 | Sample Date | Tanggal penerimaan sample | Ya | Ya |
| 5 | Status | Badge status (Draft/Pending/Approved/Rejected) | Ya | Ya |
| 6 | Progress | Step terakhir yang diselesaikan (1-4) | Ya | Tidak |
| 7 | Actions | Buttons: View, Edit, Delete | Tidak | Tidak |

#### 3.1.4 Business Rules & Validation
**A. RBAC & Status Permission**

| Role | Aksi | Kondisi |
|---|---|---|
| RA (Regulatory Affairs) | New, View, Edit, Delete | Status = Draft |
| RA | View | Status selain Draft |
| PCD | View | Semua status |
| PCD | Approve, Reject | Status = Waiting Approval |
| Admin | Full Access | Semua status |

### 3.2 DETAIL PAGE — Step 1: Document Sample
#### 3.2.1 Deskripsi
Halaman detail step 1 untuk mendokumentasikan penerimaan sample dari supplier. Berisi header information, material details, allergen checklist, carry over BTP table, dan document upload section.

#### 3.2.2 Screenshot
![Step 1 Details](screenshots/Step1_Document_Sample.png)

#### 3.2.3 Functional Description
**A. Header Information**

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Sample No | Display | Auto-generate saat pertama kali save | Sequence dari trRMSample_Header |
| 2 | Sample Date | DatePicker | Pilih tanggal sample | - |
| 3 | LOV Type Document | LOV Modal | Klik icon cari, pilih tipe dokumen | mAppParam.docTypes |
| 4 | Date of Receipt | DatePicker | Pilih tanggal penerimaan sample | - |

**(Sesuai dengan lampiran FSD v1.8 untuk detail inputan Supplier, Material, Pricing, Packaging, Halal, GMO, dsb)**

### 3.3 DETAIL PAGE — Step 2: Sample Purpose
#### 3.3.1 Deskripsi
Halaman step 2 untuk mendefinisikan tujuan penggunaan sample, mapping ke kategori RM, item code, dan produk target. User harus menentukan purpose type, objective, dan mapping product yang akan menggunakan material ini.

#### 3.3.2 Screenshot
![Step 2 Details](screenshots/Step2_Sample_Purpose.png)

#### 3.3.3 Functional Description
Input meliputi mapping Category Code, Material Name, Sample Purpose Type (New Ingredients / Alternative / Reformulation / Cost Saving), dan Apply To Product table.

### 3.4 DETAIL PAGE — Step 3: RM Evaluation
#### 3.4.1 Deskripsi
Halaman step 3 untuk evaluasi teknis dan hasil pengujian laboratorium. Terdiri dari 6 sub-tab: Organoleptic, Nutrition & Physical, Microbiological, Heavy Metals, Other Contaminant, dan Food Category. Setiap tab memiliki tabel parameter yang sama strukturnya.

#### 3.4.2 Screenshot
![Step 3 Details](screenshots/Step3_RM_Evaluation.png)

#### 3.4.3 Functional Description
**A. Tab Navigation**
- Organoleptic
- Nutrition & Physical
- Microbiological
- Heavy Metals
- Other Contaminant
- Food Category

Pengguna membandingkan nilai parameter dari dokumen COA dengan hasil *Analysis Result* internal, kemudian menyimpulkan apakah *Conform*, *Not Conform*, atau *N/A*.

### 3.5 DETAIL PAGE — Step 4: Disposition
#### 3.5.1 Deskripsi
Halaman step 4 (terakhir) untuk keputusan akhir terhadap sample. Menampilkan Overall Score dari evaluasi, field rekomendasi, keputusan (Approved/Rejected/On Hold), dan workflow approval.

#### 3.5.2 Screenshot
![Step 4 Details](screenshots/Step4_Disposition.png)

#### 3.5.3 Functional Description

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Overall Score | Display | Read-only, calculated dari semua parameter Step 3 | Calculated field |
| 2 | Recommendation | TextArea | Input rekomendasi evaluator | - |
| 3 | Decision | Radio Button | Pilih: Approved / Rejected / On Hold | - |
| 4 | Reason | TextArea | Input alasan keputusan | - |
| 5 | Approval Required | Checkbox | Centang jika memerlukan approval atasan | - |
| 6 | Btn Submit | Button | Submit final dengan full validation | API: /api/NewRMSample/Submit |

## 4. STRUKTUR DATABASE
### 4.1 Konvensi Penamaan
- Tabel Header menggunakan awalan `trRMSample_Header`.
- Sub-tabel untuk setiap step menggunakan penomoran step (contoh: `trRMSample_Step1`).
- Penamaan field mengikuti standar prefix Hungary (`int` untuk nomor, `txt` untuk teks varchar, `dt` untuk datetime).

### 4.2 Entity Relationship Diagram (ERD)
![ERD Database](screenshots/new_rm_sample_erd.png){width=60%}

## 5. BUSINESS RULES
### 5.1 General Rules
- Seluruh form transaksi terpisah dalam 4 tab wizard yang diakses linear (Step 1 -> 2 -> 3 -> 4) kecuali bagi revisi *On Hold*.
- Audit trail fields diisi otomatis oleh system backend.
- Proses penghapusan data bersifat **Soft Delete**.

### 5.2 Step-Specific Rules
- Step 1 tidak dapat di by-pass. Material Name dan Type Document wajib ada sebelum bisa berlanjut ke Step 2.
- Tab Evaluation di Step 3 wajib diisi jika material sudah diterima oleh R&D atau Laboratorium QA.
- Keputusan *Rejected* atau *On Hold* wajib menyertakan Alasan (Reason) pada Step 4.

## 6. UI SPECIFICATIONS
### 6.1 Index Page (NewRMSampleIndex.html)
Halaman Index menggunakan framework DataTables dengan fungsionalitas:
- Pencarian global (Search TextBox).
- Fitur Sort per header kolom Asc/Desc.
- Data Paging default 10-25 entry per list.
- Tombol action: View/Edit/Delete per baris data.

### 6.2 Detail Page (NewRMSampleDetail.html)
Halaman wizard menggunakan integrasi form `bs-stepper` untuk UI yang dinamis:
- Form akan terkunci (disabled) apabila user memilik *read-only* access (PCD di level draft).
- Required field validation memicu border merah dan pesan *tooltip*.

## 7. INTEGRATION POINTS
### 7.1 Master Data Dependencies
- API /lov/TypeDocument
- API /lov/Currency
- API /lov/UOM
- API /lov/Storage
- API /lov/Halal
- API /lov/GMO
Semua Data LOV dipanggil dinamis melalui fungsi JS injection: `app.openLOV(modalId, renderFn)`.

## 8. REPORTING
- Tersedia fitur Export Excel via DataTables di Dashboard Index.
- Format cetak SP/FP dari RM Evaluation tersedia dalam tombol Print di Step 4 (akan meng-generate PDF dokumen formal).

## 9. LAMPIRAN
### 9.1 Screenshots Tambahan
![Detail Wizard Header](screenshots/NewRMSample_Detail_Wizard.png)
![Approval Process](screenshots/ss_approval.png)

### 9.2 Change Log
| Versi | Tanggal | Catatan Revision |
|---|---|---|
| 1.0 | 25 Januari 2026 | Initial Dokumen base FSD RM Sample |
| 1.8 | 19 Februari 2026 | Simplifikasi Flowchart Diagram |
| 2.0 | 16 Maret 2026 | Transformasi format struktur FSD mengikuti stardardisasi Docx v2 |
