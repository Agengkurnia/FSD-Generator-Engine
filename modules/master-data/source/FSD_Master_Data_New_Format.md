# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
# MASTER DATA MANAGEMENT SYSTEM
## VERSI 1.2

### INFORMASI DOKUMEN
| Item | Keterangan |
|---|---|
| Nama Modul | Master Data Management |
| Versi Dokumen | 1.2 |
| Tanggal | 16 Maret 2026 |
| Status | Draft |
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
Dokumen ini menjelaskan spesifikasi fungsional dari Modul Master Data pada sistem RM Selection (Raw Material Selection) dengan struktur database aktual. Master data ini dibutuhkan untuk modul transaksional seperti New RM Sample dan evaluasi laboratorium.

### 1.2 Ruang Lingkup
Sistem ini mencakup 6 form/modul master utama:
- BTP (Bahan Tambahan Pangan)
- BTP Function
- RM Category
- RM Sub Group
- Master UOM (Unit of Measure)
- Test Parameter Conversion

### 1.3 Stakeholder
- R&D Department: Pengguna utama untuk setup kategori dan parameter uji.
- QA/QC Department: Review dan referensi standar parameter pengujian.
- Purchasing Department: Referensi RM yang terdaftar.
- Admin/IT: Maintenance system.

## 2. RINGKASAN BUSINESS FLOW
### 2.1 Proses As-Is (Legacy System)
Pengelolaan spesifikasi RM, BTP, dan Unit menggunakan tabel-tabel terpisah yang belum terpusat sepenuhnya, sehingga maintenance data (Create, Update, Delete) membutuhkan effort administrasi database secara manual, tanpa antarmuka yang tersentralisasi.

### 2.2 Proses To-Be (New System)
Semua master data dikelola melalui antarmuka web yang terpusat dengan single entry point. Menggunakan relasi antartabel dengan Junction tables (contoh: M_BTP_DETAIL) untuk menjaga integritas relasi Many-to-Many tanpa redudansi. Modul ini menyediakan data lookup (LOV) bagi seluruh aplikasi RM Selection.

## 3. SPESIFIKASI FUNGSIONAL
### 3.1 BTP (Bahan Tambahan Pangan)
#### 3.1.1 Deskripsi
Navigation: Sidebar > Master Data > BTP
Halaman ini menampilkan daftar BTP (Bahan Tambahan Pangan) dalam bentuk tabel. Memungkinkan admin untuk menambahkan (Create), mengubah (Edit), dan menghapus secara soft-delete (bitActive=0) data BTP.

#### 3.1.2 Screenshot
![BTP Index](screenshots/BTP_Index_Page.png)
![BTP Detail](screenshots/BTP_Detail_Form.png)

#### 3.1.3 Functional Description
Halaman Detail / Create:

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | BTP Code | Text Input | Kode unik BTP, alfanumerik max 50 char | M_BTP.txtBtpCode |
| 2 | BTP Name | Text Input | Nama BTP, min 3 max 200 char | M_BTP.txtBtpName |
| 3 | Active | Checkbox | Status aktif BTP (default checked/true) | M_BTP.bitActive |
| 4 | Save | Button | Simpan perubahan ke DB dengan validasi unik | - |
| 5 | Cancel | Button | Batal kembali ke Index | - |

#### 3.1.4 Business Rules & Validation
- **RBAC & Status Permission**: Hanya user dengan role Administrator yang dapat Edit/Delete BTP master data.
- **Validasi Field**: `BTP Code` (Required, Unique, tanpa spasi), `BTP Name` (Required).
- **Business Logic**: BTP yang sudah digunakan di `M_BTP_DETAIL` tidak dapat di-soft delete atau diubah kodenya.

### 3.2 BTP Function
#### 3.2.1 Deskripsi
Navigation: Sidebar > Master Data > BTP Function
Halaman untuk mendaftarkan fungsi dari masing-masing BTP, mengacu ke standard BPOM (PERKA BPOM).

#### 3.2.2 Screenshot
![BTP Function Index](screenshots/BTP_Function_Index.png)
![BTP Function Detail](screenshots/BTP_Function_Detail.png)

#### 3.2.3 Functional Description
Halaman Detail:

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Function Code | Text Input | Kode fungsi unik mengacu PERKA BPOM | M_BTP_FUNCTION.txtFunctionCode |
| 2 | Function Name | Text Input | Nama lengkap fungsi | M_BTP_FUNCTION.txtFunctionName |
| 3 | Active | Checkbox | Status fungsi (aktif/nonaktif) | M_BTP_FUNCTION.bitActive |

#### 3.2.4 Business Rules & Validation
- **Validasi Field**: Code mengikuti format BPOM (contoh: PERKA BPOM 07-2013).
- **Business Logic**: Fungsi BTP yang sudah di-mapping oleh BTP tertentu tidak dapat dihapus.

### 3.3 RM Category
#### 3.3.1 Deskripsi
Navigation: Sidebar > Master Data > RM Category
Halaman untuk manajemen kategori utama bahan baku.

#### 3.3.2 Screenshot
![RM Category Index](screenshots/RM_Category_Index.png)
![RM Category Detail](screenshots/RM_Category_Detail.png)

#### 3.3.3 Functional Description

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Category Code | Text Input | Kode kategori unik | M_RM_CATEGORY.txtRMCategoryCode |
| 2 | Category Name | Text Input | Nama kategori bahan | M_RM_CATEGORY.txtRMCategoryName |
| 3 | Critical Flag | Checkbox | Menandakan kategori raw material critical | M_RM_CATEGORY.bitCritical |
| 4 | Apply Product | Checkbox | Flag apakah diaplikasikan ke product | M_RM_CATEGORY.bitApplyProduct |
| 5 | Active | Checkbox | Status kategori | M_RM_CATEGORY.bitActive |

#### 3.3.4 Business Rules & Validation
- Kategori berhubungan dengan sub group melalui `M_RM_CATEGORY_DETAIL`.

### 3.4 RM Sub Group
#### 3.4.1 Deskripsi
Navigation: Sidebar > Master Data > RM Sub Group
Halaman mengatur pengelompokan sub-tipe bahan untuk RM Category. Sub group tidak menempel langsung ke RM_CATEGORY tetapi via Junction tabel agar satu sub-group bisa dipakai multi-category.

#### 3.4.2 Screenshot
![RM Sub Group Index](screenshots/RM_SubGroup_Index.png)
![RM Sub Group Detail](screenshots/RM_SubGroup_Detail.png)

#### 3.4.3 Functional Description

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Sub Group Code | Text Input | Kode unik | M_RM_SUB_GROUP.txtRMSubGroupCode |
| 2 | Sub Group Name | Text Input | Nama dari sub group bahan | M_RM_SUB_GROUP.txtRMSubGroupName |
| 3 | Active | Checkbox | Status | M_RM_SUB_GROUP.bitActive |

#### 3.4.4 Business Rules & Validation
- **Mapping Constraint**: Dikelola secara terpisah dari RM Category.

### 3.5 Master UOM (Unit of Measure)
#### 3.5.1 Deskripsi
Navigation: Sidebar > Master Data > UOM
Halaman manajemen satuan ukuran (Kg, Litre, Gram, dll).

#### 3.5.2 Screenshot
![UOM Index](screenshots/UOM_Index_Page.png)
![UOM Detail](screenshots/UOM_Detail_Form.png)

#### 3.5.3 Functional Description

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | UOM Code | Text Input | Kode unit satuan | M_UNIT.txtUnitCode |
| 2 | UOM Name | Text Input | Deskripsi satuan | M_UNIT.txtUnitName |
| 3 | Active | Checkbox | Status satuan | M_UNIT.bitActive |

### 3.6 Test Parameter Conversion
#### 3.6.1 Deskripsi
Navigation: Sidebar > Master Data > Test Parameter Conversion
Halaman untuk setup rumus konversi evaluasi tes RM dari nilai raw lab menjadi final standar (mis. Protein %).

#### 3.6.2 Screenshot
![Parameter Index](screenshots/Parameter_Index.png)
![Parameter Detail](screenshots/Parameter_Detail.png)

#### 3.6.3 Functional Description

| No | Element | Type | Action / Behavior | Data Source |
|---|---|---|---|---|
| 1 | Factor Number | Decimal | Sebagai angka penyebut rumus konversi | M_TEST_PARAMETER_CONVERSION.decFactorNumber |
| 2 | txtFactor | Text Input | Pengali dari nilai test | M_TEST_PARAMETER_CONVERSION.txtFactor |
| 3 | Target | Data Grid | Target per grup RM | M_TARGET_PER_RM_CATEGORY |

#### 3.6.4 Business Rules & Validation
- **Formula Hitung**: Hasil Konversi = (Nilai Test × txtFactor) / decFactorNumber.

## 4. STRUKTUR DATABASE
### 4.1 Konvensi Penamaan
- Tabel Master menggunakan awalan `M_`. Relasi many-to-many dilayani oleh tabel junction dengan imbuhan `_DETAIL` atau nama penghubung.
- Penamaan field mengikuti standar prefix Hungary (`int` untuk nomor/ID autonumber, `txt` untuk teks varchar).

### 4.2 Entity Relationship Diagram (ERD)
![ERD Database](erd_master_data.png)
Setiap sub-modul master memiliki dependency key ke tabel junction yang mengatur parameter-parameter khusus.

### 4.3 Tabel Detail Master & Junction

| Nama Tabel | Tipe | Primary Key | Keterangan |
|---|---|---|---|
| M_BTP | Master | intBtp | Bahan Tambahan Pangan |
| M_BTP_FUNCTION | Master | intBtpFunction | Master Fungsi BTP |
| M_BTP_DETAIL | Junction | intBtpDetail | (intBtp, intBtpFunction) relation |
| M_RM_CATEGORY | Master | intRMCategoryId | Master kategori RM |
| M_RM_SUB_GROUP | Master | intRMSubGroupId | Master sub grup RM |
| M_RM_CATEGORY_DETAIL | Junction | intRMCategoryDetailId | Menghubungkan Kategori dengan Subgroup |
| M_UNIT | Master | intUnitId | Master satuan (UOM) |
| M_PARENT_EXAM_PARAMETER | Master | intParentExamParameterId | Master tipe uji (FK: intUnitId) |
| M_TEST_PARAMETER_CONVERSION | Trans | intTestId | Set nilai convert untuk parameter pengujian |
| M_TARGET_PER_RM_CATEGORY| Junction | intTargetPerRMCategory | Target untuk tiap SubGroup pengujian |

## 5. BUSINESS RULES
### 5.1 General Rules
- Seluruh form master harus mempertahankan sistem CRUD tersendiri.
- Audit trail fields: `txtInsertedBy`, `dtInserted`, `txtUpdatedBy`, `dtUpdated` diisi otomatis oleh system backend.
- Proses penghapusan data bersifat **Soft Delete** via flag `bitActive` (diset 0).
- Record aktif adalah data dengan flag `bitActive` = 1.

### 5.2 Modul-Specific Rules
- Mengubah/Menonaktifkan BTP tidak boleh merusak riwayat form New RM Sample yang telah disubmit sebelumnya.
- Formula hitung dalam Conversion Test adalah mutlak tersimpan dalam standar perhitungan backend untuk konsistensi di layar RM Evaluation.

### 5.3 Workflow Rules
- Data yang sudah tersimpan menjadi referensi List of Value (LOV) bagi form utama (seperti New RM Sample, Document Sample, Allocation Sample).
- Update data akan secara real-time terefleksi ke LOV untuk inputan baru.

## 6. UI SPECIFICATIONS
### 6.1 Index Page Dashboard
Halaman Master menggunakan **DataTables jQuery Plugin** untuk list datagrid dengan fungsionalitas:
- Pencarian global (Search TextBox).
- Fitur Sort per header kolom Asc/Desc.
- Data Paging default 25 entry per list.
- Kolom "Action" berupa sepasang tombol Edit dan icon tong sampah (Delete/Non-active).

### 6.2 Detail Page (Form Input)
Halaman formulir menerapkan:
- Bootstrap FormGroup styling.
- Validasi Required on-leave dengan border merah dan pesan *in-line error text*.
- Tombol `Save` dilengkapi event listener *SweetAlert Confirmation*.

## 7. INTEGRATION POINTS
### 7.1 Master Data Dependencies
Sistem RM akan memanggil API dari master ini guna me-populate form dropdown LOV secara asinkron tanpa *post-back*.
Contoh LOV Dependencies:
- LOV BTP dan Allergen akan menarik `M_BTP`.
- LOV Test Conversion menarik `M_UNIT` dan `M_PARENT_EXAM_PARAMETER`.

## 8. REPORTING
### 8.1 Master Data Export
Untuk keperluan pelaporan setup data, disediakan fitur standard Export Excel dari DataTables untuk Master BTP dan RM Category.

## 9. LAMPIRAN
### 9.1 Screenshots
Mencakup screen capture dari mockup desain UI yang diimplementasikan pada file `.html`:
- BTPIndex.html & BTPDetail.html
- BTPFunctionIndex.html & BTPFunctionDetail.html
- RMCategoryIndex.html
- RMSubGroupIndex.html
- TestParameterConversionIndex.html

### 9.2 Change Log

| Versi | Tanggal | Catatan Revision |
|---|---|---|
| 1.0 | 25 Januari 2026 | Initial Dokumen base FSD_Master_Data (As-Is DB) |
| 1.2 | 16 Maret 2026 | Transformasi format struktur FSD mengikuti stardardisasi New RM Sample Format V1.8 |
