# Table of Contents {#table-of-contents .TOC-Heading}

# Functional Specification Document (FSD)

Modul Master Data - RM Selection System

**Versi 1.1** \| 25 Januari 2026 \| IT & Squad IDC

- [Pendahuluan](#pendahuluan)
- [Arsitektur Database](#arsitektur)
- [BTP](#btp)
- [BTP Function](#btp-function)
- [RM Category](#rm-category)
- [RM Sub Group](#rm-subgroup)
- [Master UOM](#uom)
- [Test Parameter Conversion](#test-conversion)

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumentasi spesifikasi fungsional untuk Modul Master Data pada sistem
RM Selection (Raw Material Selection) dengan struktur database aktual.

### 1.2 Ruang Lingkup

Dokumentasi ini mencakup 6 modul master utama berdasarkan database
existing:

- BTP (Bahan Tambahan Pangan)
- BTP Function
- RM Category
- RM Sub Group
- Master UOM (Unit of Measure)
- Test Parameter Conversion

## 2. Arsitektur Database

### 2.1 Entity Relationship Diagram (ERD)

#### Diagram Relasi Tabel Master Data

##### BTP Module

**M_BTP**

intBtp (PK)

↕️

**M_BTP_DETAIL**

intBtp (FK)

intBtpFunction (FK)

↕️

**M_BTP_FUNCTION**

intBtpFunction (PK)

##### RM Category Module

**M_RM_CATEGORY**

intRMCategoryId (PK)

↕️

**M_RM_CATEGORY_DETAIL**

intRMCategoryId (FK)

intRMSubGroupId (FK)

↕️

**M_RM_SUB_GROUP**

intRMSubGroupId (PK)

##### Parameter Module

**M_UNIT**

intUnitId (PK)

↕️

**M_PARENT_EXAM_PARAMETER**

intUnitId (FK)

↕️

**M_TEST_PARAMETER_CONVERSION**

intParentExamParameterId (FK)

↕️

**M_TARGET_PER_RM_CATEGORY**

intTestId (FK)

intRMSubGroupId (FK)

**Keterangan Warna:**

- Biru - Tabel Master Utama
- Kuning - Tabel Relasi/Junction

### 2.2 Struktur Tabel Database

  ------------------------------------------------------------------------------------------------------------------
  Nama Tabel                        Tipe          Primary Key                Foreign Keys               Keterangan
  --------------------------------- ------------- -------------------------- -------------------------- ------------
  **M_BTP**                         Master        intBtp                     \-                         Bahan
                                                                                                        Tambahan
                                                                                                        Pangan

  **M_BTP_FUNCTION**                Master        intBtpFunction             \-                         Fungsi BTP
                                                                                                        (PERKA BPOM)

  **M_BTP_DETAIL**                  Junction      intBtpDetail               intBtp, intBtpFunction     Relasi BTP ↔
                                                                                                        Function

  **M_RM_CATEGORY**                 Master        intRMCategoryId            \-                         Kategori Raw
                                                                                                        Material

  **M_RM_SUB_GROUP**                Master        intRMSubGroupId            \-                         Sub Group
                                                                                                        Raw Material

  **M_RM_CATEGORY_DETAIL**          Junction      intRMCategoryDetailId      intRMCategoryId,           Relasi
                                                                             intRMSubGroupId            Category ↔
                                                                                                        Sub Group

  **M_UNIT**                        Master        intUnitId                  \-                         Unit of
                                                                                                        Measure
                                                                                                        (UOM)

  **M_PARENT_EXAM_PARAMETER**       Master        intParentExamParameterId   intUnitId                  Parameter
                                                                                                        Pengujian

  **M_TEST_PARAMETER_CONVERSION**   Transaction   intTestId                  intParentExamParameterId   Konversi
                                                                                                        Parameter
                                                                                                        Test

  **M_TARGET_PER_RM_CATEGORY**      Junction      intTargetPerRMCategoryId   intTestId, intRMSubGroupId Target per
                                                                                                        Sub Group
  ------------------------------------------------------------------------------------------------------------------

### 2.3 Relasi Antar Tabel

  -------------------------------------------------------------------------------------------
  Tabel Parent                  Tabel Child                   Relasi          Keterangan
  ----------------------------- ----------------------------- --------------- ---------------
  M_BTP                         M_BTP_DETAIL                  1:N             Satu BTP dapat
                                                                              memiliki banyak
                                                                              fungsi melalui
                                                                              detail

  M_BTP_FUNCTION                M_BTP_DETAIL                  1:N             Satu fungsi
                                                                              dapat digunakan
                                                                              oleh banyak BTP

  M_RM_CATEGORY                 M_RM_CATEGORY_DETAIL          1:N             Kategori
                                                                              memiliki detail
                                                                              sub group

  M_RM_SUB_GROUP                M_RM_CATEGORY_DETAIL          1:N             Sub group
                                                                              terkait dengan
                                                                              kategori
                                                                              melalui detail

  M_UNIT                        M_PARENT_EXAM_PARAMETER       1:N             Unit/UOM untuk
                                                                              parameter

  M_PARENT_EXAM_PARAMETER       M_TEST_PARAMETER_CONVERSION   1:N             Parameter
                                                                              dikonversi
                                                                              dalam test

  M_TEST_PARAMETER_CONVERSION   M_TARGET_PER_RM_CATEGORY      1:N             Test memiliki
                                                                              target per sub
                                                                              group

  M_RM_SUB_GROUP                M_TARGET_PER_RM_CATEGORY      1:N             Target untuk
                                                                              sub group
                                                                              tertentu
  -------------------------------------------------------------------------------------------

### 2.4 Tabel Relasi (Junction Tables)

#### M_BTP_DETAIL

Menghubungkan BTP dengan BTP Function (Many-to-Many)

- Satu BTP dapat memiliki banyak fungsi
- Satu fungsi dapat digunakan oleh banyak BTP
- Menyimpan persentase (decPercentage) untuk setiap kombinasi

#### M_RM_CATEGORY_DETAIL

Menghubungkan RM Category dengan RM Sub Group (Many-to-Many)

- Satu kategori dapat memiliki banyak sub group
- Satu sub group dapat terkait dengan banyak kategori
- Relasi tidak langsung antara M_RM_CATEGORY dan M_RM_SUB_GROUP

#### M_TARGET_PER_RM_CATEGORY

Target value per kombinasi Test dan RM Sub Group

- Setiap test conversion dapat memiliki target berbeda untuk setiap sub
  group
- Menyimpan target value dan deskripsi target

## 3. Modul BTP (Bahan Tambahan Pangan)

### 3.1 Halaman Index BTP

**URL:** `BTPIndex.html`

![BTP Index](media/rId26.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Index BTP

#### Fungsi Utama:

- Menampilkan daftar semua BTP dalam tabel dengan DataTables
- Search global untuk mencari BTP berdasarkan code atau name
- Filter by status (Active/Inactive)
- Pagination (25 rows/page, dapat diubah)
- Sorting per kolom (ascending/descending)

#### Aksi & Navigasi:

  ----------------------------------------------------------------------
  Button/Action        Navigasi                     Keterangan
  -------------------- ---------------------------- --------------------
  **Add New**          → BTPDetail.html (mode:      Membuka form kosong
                       create)                      untuk create BTP
                                                    baru

  **Edit (per row)**   → BTPDetail.html?id={intBtp} Membuka form terisi
                       (mode: edit)                 data untuk edit BTP

  **Delete (per row)** Confirmation dialog → API    Soft delete (set
                       Delete                       bitActive = 0)
  ----------------------------------------------------------------------

**Business Rules - Index:**

- BTP yang sudah digunakan di M_BTP_DETAIL tidak dapat dihapus
- Hanya menampilkan data dengan bitActive = 1 secara default
- User dapat toggle untuk melihat inactive records

### 3.2 Halaman Detail BTP

**URL:** `BTPDetail.html`

![BTP Detail](media/rId32.png){width="5.833333333333333in"
height="2.4430719597550308in"}

Halaman Detail/Create BTP

#### Mode Halaman:

- **Create Mode:** Semua field kosong, intBtp auto-generated
- **Edit Mode:** Field terisi data existing, intBtp read-only

#### Form Fields & Validasi:

  ---------------------------------------------------------------------------
  Field        Type         Required     Validasi              Error Message
  ------------ ------------ ------------ --------------------- --------------
  BTP Code     Text         Ya           • Alphanumeric only\  \"BTP Code
                                         • Max 50 karakter\    sudah
                                         • Unique              digunakan\"\
                                         (case-insensitive)\   \"BTP Code
                                         • Tidak boleh spasi   hanya boleh
                                                               huruf dan
                                                               angka\"

  BTP Name     Text         Ya           • Min 3 karakter\     \"BTP Name
                                         • Max 200 karakter\   minimal 3
                                         • Tidak boleh hanya   karakter\"\
                                         spasi                 \"BTP Name
                                                               maksimal 200
                                                               karakter\"

  Active       Checkbox     Tidak        Default: checked      \-
                                         (true)                
  ---------------------------------------------------------------------------

#### Buttons & Actions:

  --------------------------------------------------------------
  Button               Action               Validasi
  -------------------- -------------------- --------------------
  **Save**             • Validate semua     Semua required field
                       field\               harus terisi\
                       • Check unique BTP   Validasi format
                       Code\                harus pass
                       • Insert/Update ke   
                       database\            
                       • Set audit fields   
                       (txtInsertedBy,      
                       dtInserted, dll)\    
                       • Redirect ke Index  
                       dengan success       
                       message              

  **Back/Cancel**      • Confirmation jika  \-
                       ada perubahan belum  
                       disimpan\            
                       • Redirect ke        
                       BTPIndex.html        
  --------------------------------------------------------------

**Business Rules - Detail:**

- **Create:** BTP Code harus unique di seluruh database
- **Edit:** BTP Code tidak dapat diubah jika sudah ada di M_BTP_DETAIL
- **Deactivate:** BTP dapat di-nonaktifkan (bitActive = 0) kapan saja
- **Audit Trail:** Setiap perubahan tercatat (user & timestamp)
- **Concurrent Edit:** Last save wins, tidak ada locking

### 3.3 Database Schema - M_BTP

  ----------------------------------------------------------------
  Kolom            Tipe            Null            Keterangan
  ---------------- --------------- --------------- ---------------
  **intBtp**       INT             No              PK Identity

  **txtBtpCode**   VARCHAR         No              UK Kode BTP

  txtBtpName       VARCHAR         No              Nama BTP

  bitActive        BIT             Yes             Status aktif
                                                   (default 1)

  dtNonActive      DATETIME        Yes             Tanggal
                                                   non-aktif

  txtInsertedBy    VARCHAR         Yes             User pembuat

  dtInserted       DATETIME        Yes             Tanggal dibuat

  txtUpdatedBy     VARCHAR         Yes             User pengubah

  dtUpdated        DATETIME        Yes             Tanggal diubah
  ----------------------------------------------------------------

## 4. Modul BTP Function

### 4.1 Halaman Index BTP Function

**URL:** `BTPFunctionIndex.html`

![BTP Function Index](media/rId42.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Index BTP Function

### 4.2 Halaman Detail BTP Function

**URL:** `BTPFunctionDetail.html`

![BTP Function Detail](media/rId46.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Detail/Create BTP Function

**Business Rules:**

- Function Code mengikuti format PERKA BPOM (contoh: PERKA BPOM 07-2013)
- Satu fungsi dapat digunakan oleh multiple BTP
- Fungsi yang sudah ter-mapping tidak dapat dihapus

### 4.3 Database Schema - M_BTP_FUNCTION

  ---------------------------------------------------------------------
  Kolom                 Tipe            Null            Keterangan
  --------------------- --------------- --------------- ---------------
  **intBtpFunction**    INT             No              PK Identity

  **txtFunctionCode**   VARCHAR         No              UK Kode fungsi

  txtFunctionName       VARCHAR         No              Nama fungsi

  bitActive             BIT             No              Status aktif
  ---------------------------------------------------------------------

## 5. Modul RM Category

### 5.1 Halaman Index RM Category

![RM Category Index](media/rId53.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Index RM Category

### 5.2 Halaman Detail RM Category

![RM Category Detail](media/rId57.png){width="5.833333333333333in"
height="3.0193547681539807in"}

Halaman Detail/Create RM Category

### 5.3 Database Schema - M_RM_CATEGORY

  -----------------------------------------------------------------
  Kolom                   Tipe                 Keterangan
  ----------------------- -------------------- --------------------
  **intRMCategoryId**     INT                  PK Identity

  **txtRMCategoryCode**   VARCHAR              UK Kode kategori

  txtRMCategoryName       VARCHAR              Nama kategori

  bitCritical             BIT                  Flag kategori
                                               critical

  bitApplyProduct         BIT                  Flag apply product

  bitActive               BIT                  Status aktif
  -----------------------------------------------------------------

## 6. Modul RM Sub Group

### 6.1 Halaman Index RM Sub Group

![RM Sub Group Index](media/rId64.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Index RM Sub Group

### 6.2 Halaman Detail RM Sub Group

![RM Sub Group Detail](media/rId68.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Detail/Create RM Sub Group

**Catatan Penting:**

Tabel M_RM_SUB_GROUP TIDAK memiliki foreign key langsung ke
M_RM_CATEGORY. Relasi dikelola melalui tabel M_RM_CATEGORY_DETAIL.

## 7. Modul Master UOM

### 7.1 Halaman Index Master UOM

![Master UOM Index](media/rId74.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Index Master UOM

### 7.2 Halaman Detail Master UOM

![Master UOM Detail](media/rId78.png){width="5.833333333333333in"
height="3.0193547681539807in"}

Halaman Detail/Create Master UOM

**Catatan:** Nama tabel adalah `M_UNIT`, bukan M_UOM.

## 8. Modul Test Parameter Conversion

### 8.1 Halaman Index Test Parameter Conversion

![Test Parameter Conversion
Index](media/rId84.png){width="5.833333333333333in"
height="2.7708333333333335in"}

Halaman Index Test Parameter Conversion

### 8.2 Halaman Detail Test Parameter Conversion

![Test Parameter Conversion
Detail](media/rId88.png){width="5.833333333333333in"
height="3.629711286089239in"}

Halaman Detail/Create Test Parameter Conversion

### 8.3 Formula Konversi

Hasil Konversi = (Nilai Test × txtFactor) / decFactorNumber

#### Contoh Perhitungan:

**TEST-001:** Konversi Protein

- Nilai Test: 4.0
- txtFactor: 6.38
- decFactorNumber: 1
- **Hasil:** Protein % = (4.0 × 6.38) / 1 = 25.52%

**Catatan Penting:**

- `txtFactor` dan `txtTarget` disimpan sebagai VARCHAR/TEXT, bukan
  DECIMAL
- `decFactorNumber` adalah DECIMAL
- Tidak ada kolom `bitActive` pada tabel ini
- Foreign key ke `M_PARENT_EXAM_PARAMETER`, bukan ke tabel PARAMETER

© 2026 IT & Squad IDC \| RM Selection System

Functional Specification Document - Master Data Module
