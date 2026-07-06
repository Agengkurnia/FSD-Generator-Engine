# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
## Modul: Item Registration – Item Trial & Item Production
### Sistem: IDC System (New RM Selection)

---

| Atribut          | Keterangan                                                    |
|------------------|---------------------------------------------------------------|
| **Nama Dokumen** | FSD Modul Item Registration – Item Trial & Item Production    |
| **Versi**        | 1.0                                                           |
| **Tanggal**      | 06 April 2026                                                 |
| **Divisi**       | Packaging Development / ICT                                   |
| **Status**       | Draft                                                         |
| **Revamp dari**  | KN2015_RMPM (UploadItemTrial – IndexTrial, IndexProd, IndexProdNonTrial) |

---

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
   - 1.1 [Tujuan Dokumen](#11-tujuan-dokumen)
   - 1.2 [Ruang Lingkup](#12-ruang-lingkup)
   - 1.3 [Stakeholder](#13-stakeholder)
2. [Ringkasan Business Flow](#2-ringkasan-business-flow)
   - 2.1 [Proses As-Is (Sistem Lama)](#21-proses-as-is-sistem-lama)
   - 2.2 [Proses To-Be (Sistem Baru)](#22-proses-to-be-sistem-baru)
3. [Spesifikasi Fungsional](#3-spesifikasi-fungsional)
   - 3.1 [Halaman Item Trial Index](#31-halaman-item-trial-index)
   - 3.2 [Halaman Item Trial Detail](#32-halaman-item-trial-detail)
   - 3.3 [Halaman Item Production Index](#33-halaman-item-production-index)
   - 3.4 [Halaman Item Production Detail](#34-halaman-item-production-detail)
4. [Struktur Database](#4-struktur-database)
5. [Aturan Bisnis](#5-aturan-bisnis)
6. [List of Values (LOV) & Referensi Data](#6-list-of-values-lov--referensi-data)
7. [Hak Akses & Peran Pengguna](#7-hak-akses--peran-pengguna)
8. [Notifikasi](#8-notifikasi)

---

## 1. Pendahuluan

Modul **Item Registration** merupakan modul inti dalam sistem IDC New RM Selection yang mengelola proses pendaftaran item baru ke Oracle ERP. Modul ini merupakan hasil *revamp* dari sistem lama **KN2015_RMPM**, yang sebelumnya terbagi dalam tiga sub-modul terpisah:

- **IndexTrial**: Daftar dan formulir pendaftaran item percobaan (trial)
- **IndexProd**: Daftar dan formulir pendaftaran item produksi (berdasarkan item trial)
- **IndexProdNonTrial**: Daftar dan formulir pendaftaran item produksi langsung (tanpa trial)

Pada sistem baru (IDC), ketiga sub-modul tersebut telah dikonsolidasikan menjadi **dua modul terintegrasi** dengan antarmuka yang lebih modern, efisien, dan konsisten.

### 1.1 Tujuan Dokumen

Dokumen ini bertujuan untuk:

1. Menjelaskan fungsionalitas lengkap modul Item Registration di sistem IDC.
2. Menjadi acuan pengembangan (*development reference*) bagi tim ICT.
3. Mendeskripsikan alur proses, desain layar, struktur data, serta aturan bisnis yang berlaku.
4. Mencatat perubahan dan penyesuaian dari sistem lama (KN2015_RMPM) ke sistem baru (IDC).

### 1.2 Ruang Lingkup

Dokumen ini mencakup empat halaman utama:

1. `ItemTrialIndex.html` – Halaman daftar item trial
2. `ItemTrialDetail.html` – Halaman input/edit data item trial
3. `ItemProductionIndex.html` – Halaman daftar item production
4. `ItemProductionDetail.html` – Halaman input/edit data item production (Trial & Non-Trial)

### 1.3 Stakeholder

| Peran                | Nama / Tim                    | Keterlibatan                                      |
|----------------------|-------------------------------|---------------------------------------------------|
| Business Owner       | Packaging Development / R&D   | Pemilik proses bisnis, validasi kebutuhan         |
| ICT Developer        | KN IT                         | Pengembangan dan implementasi sistem              |
| Initiator / Uploader | IDC / Procurement / R&D       | Pengguna modul, membuat dan mengisi formulir      |
| Approver             | Atasan / PIC terkait          | Menelaah dan menyetujui dokumen yang disubmit     |
| Administrator        | KN IT / IDC Admin             | Manajemen konfigurasi dan pengguna                |

---

## 2. Ringkasan Business Flow

### 2.1 Proses As-Is (Sistem Lama)

Pada sistem lama (KN2015_RMPM), proses pendaftaran item dibagi menjadi tiga modul terpisah:

| Aspek              | Sistem Lama (KN2015_RMPM)                       | Sistem Baru (IDC)                                 |
|--------------------|-------------------------------------------------|---------------------------------------------------|
| Modul Trial        | View `IndexTrial` + Form `ItemTrial`            | `ItemTrialIndex.html` + `ItemTrialDetail.html`    |
| Modul Production   | View `IndexProd` + Form `ItemProduction`         | `ItemProductionIndex.html` + `ItemProductionDetail.html` (Trial Mode) |
| Modul Non-Trial    | View `IndexProdNonTrial` + Form `ItemProdNonTrial` | Sama dengan Production, di-toggle via **Non-Trial Mode** |
| UI Framework       | Bootstrap 3 / AdminLTE                          | Bootstrap 5 / Vuexy                               |
| LOV Selector       | Modal jQuery terpisah                           | SweetAlert2 responsive (lebar 850px, searchable)  |
| Template Logic     | Terpisah per modul                              | Satu form dengan toggle mode & template selector  |

### 2.2 Proses To-Be (Sistem Baru)

#### 2.2.1 Alur Item Trial

*(Gambar 1: Flowchart Alur Item Trial)*

#### 2.2.2 Alur Item Production

*(Gambar 2: Flowchart Alur Item Production)*

#### 2.2.3 Status Dokumen

| Kode              | Label                | Deskripsi                                                              |
|-------------------|----------------------|------------------------------------------------------------------------|
| `DRAFT`           | Draft                | Baru dibuat atau disimpan sementara; dapat diedit dan disubmit kembali |
| `WAIT_APPROVAL`   | Waiting For Approval | Sudah disubmit, menunggu review dan persetujuan Approver               |
| `APPROVED`        | Approved             | Telah disetujui oleh Approver; siap dikirim ke Oracle ERP              |
| `SUBMITTED`       | Submitted to Oracle  | Data telah dikirim ke Oracle ERP melalui tabel staging                 |
| `REJECTED`        | Rejected             | Ditolak oleh Approver; Initiator perlu memperbaiki dan submit ulang    |

---

## 3. Spesifikasi Fungsional

### 3.1 Halaman Item Trial Index

**Path**: `ItemTrialIndex.html`

**Tujuan**: Menampilkan semua dokumen Item Trial dalam bentuk daftar tabel, dilengkapi dashboard ringkasan status.

#### 3.1.1 Dashboard Summary Cards

| Kartu            | Filter          | Warna  | Isi                                            |
|------------------|-----------------|--------|------------------------------------------------|
| Total            | ALL             | Navy   | Jumlah seluruh dokumen Item Trial              |
| Draft            | DRAFT           | Kuning | Jumlah dokumen berstatus Draft                 |
| Waiting Approval | WAIT_APPROVAL   | Cyan   | Jumlah dokumen menunggu persetujuan            |
| Approved         | APPROVED        | Hijau  | Jumlah dokumen yang telah disetujui            |
| Submitted to Oracle | SUBMITTED    | Biru   | Jumlah dokumen yang telah terkirim ke Oracle   |

Klik pada kartu akan memfilter data tabel secara otomatis. Kartu aktif ditandai dengan bayangan berwarna sesuai status.

#### 3.1.2 Screenshot

*(Gambar 3: Halaman Item Trial Index)*

#### 3.1.3 Functional Description

**Action Bar:**

| Tombol              | Fungsi                                                          |
|---------------------|-----------------------------------------------------------------|
| Export Excel        | Mengekspor data tabel ke format Excel                           |
| Create New Item Trial | Mengarahkan ke halaman `ItemTrialDetail.html`                |

**Tabel Daftar Item Trial:**

| Kolom           | Sumber Data       | Keterangan                                              |
|-----------------|-------------------|---------------------------------------------------------|
| Document Status | `status`          | Badge berwarna sesuai status dokumen                    |
| Item Template   | `template`        | RM TRIAL atau PM TRIAL                                  |
| Item Code       | `itemCode`        | Link ke halaman Detail                                  |
| Description     | `itemDesc`        | Deskripsi item dari Oracle                              |
| Primary UOM     | `uom`             | Satuan ukur                                             |
| Created By      | `createdBy`       | Nama pengguna yang membuat                              |
| Created Date    | `createdDate`     | Tanggal dokumen dibuat                                  |
| Next Approver   | `nextApprover`    | Nama approver berikutnya dalam workflow                 |
| Action          | –                 | Tombol View menuju `ItemTrialDetail.html?id={id}`       |

#### 3.1.4 Business Rules & Validation

1. Kartu filter menjalankan pencarian pada kolom **Document Status** di DataTable secara real-time.
2. Tombol **Create New Item Trial** selalu aktif dan dapat diklik kapan saja.
3. DataTable mendukung pencarian global, pengurutan per kolom, dan paginasi.

---

### 3.2 Halaman Item Trial Detail

**Path**: `ItemTrialDetail.html`

**Tujuan**: Halaman input dan editing data item trial. Formulir dibagi menjadi empat bagian (card) utama.

#### 3.2.1 Deskripsi Toolbar

| Elemen         | Kondisi Tampil | Fungsi                                                        |
|----------------|----------------|---------------------------------------------------------------|
| Tombol Back    | Selalu         | Kembali ke `ItemTrialIndex.html`                              |
| Tombol Save Draft | Selalu      | Menyimpan data dengan status `Draft`                          |
| Tombol Submit  | Selalu         | Memvalidasi kelengkapan data, mengubah status ke `WAIT_APPROVAL` |

#### 3.2.2 Screenshot

*(Gambar 4: Halaman Item Trial Detail)*

#### 3.2.3 Functional Description

**Bagian A: Basic Information**

| Field             | ID Elemen       | Tipe       | Wajib | Keterangan                                                  |
|-------------------|-----------------|------------|-------|-------------------------------------------------------------|
| Item Template     | `itemTemplate`  | Input+LOV  | Ya    | Pilih RM TRIAL atau PM TRIAL dari Oracle MTL_ITEM_TEMPLATES. Mengaktifkan LOV Item Code. |
| Item Code Trial   | `itemCodeTrial` | Input+LOV  | Ya    | LOV aktif setelah template dipilih. Auto-fill Description & UOM. Source: `XXSHP_INV_MASTER_ITEM_STG` |
| Item Description  | `itemDesc`      | Textarea   | Tidak | Read-only. Terisi otomatis setelah Item Code dipilih        |
| Primary UOM       | `primaryUOM`    | Input+LOV  | Ya    | Satuan ukur dari Oracle `MTL_UNITS_OF_MEASURE_TL`           |

**Bagian B: SHP Inventory**

| Field            | ID Elemen        | Tipe  | Nilai Default | Keterangan                                          |
|------------------|------------------|-------|---------------|-----------------------------------------------------|
| Item Type        | `itemType`       | Input | –             | Read-only. Auto-fill: `RM` jika template RM TRIAL, `PM` jika PM TRIAL |
| Item Sub Type    | `itemSubType`    | Input | ALL           | Read-only                                           |
| Item LOB         | `itemLob`        | LOV   | –             | Pilih dari Oracle `FND_LOOKUP_VALUES` (LOB lookup)  |
| Corporate LOB    | `corporateLob`   | Input | SHP_NA        | Read-only                                           |
| Product Category | `productCategory`| Input | NA            | Read-only                                           |
| Production Site  | `productionSite` | Input | NA            | Read-only                                           |

**Bagian C: SHP Purchasing Type**

| Field          | ID Elemen        | Tipe  | Nilai Default | Keterangan                                       |
|----------------|------------------|-------|---------------|--------------------------------------------------|
| Purchasing Types | `purchasingTypes` | Input | INDIRECT2  | Read-only                                        |
| Item Types     | `itemTypes`      | Input | –             | Read-only. Auto-fill sesuai template             |
| Item Sub Types | `itemSubTypes`   | Input | ALL           | Read-only                                        |
| SHP Future     | `shpFuture`      | Input | ALL           | Read-only                                        |

**Bagian D: Pallet & Packing Size**

| Field        | ID Elemen    | Tipe   | Wajib | Keterangan                          |
|--------------|--------------|--------|-------|-------------------------------------|
| Packing Size | `packingSize`| Number | Tidak | Input manual. Contoh: 25            |
| Pallet Size  | `palletSize` | Number | Tidak | Input manual. Contoh: 500           |

#### 3.2.4 Business Rules & Validation

1. LOV **Item Code Trial** hanya aktif setelah **Item Template** dipilih.
2. Memilih **Item Template** akan me-reset field Item Code, Description, dan UOM jika sudah terisi (dengan dialog konfirmasi).
3. Memilih **Item Code** otomatis mengisi **Item Description** dan **Primary UOM**.
4. Template **RM TRIAL** → Item Type auto-fill = `RM`; Template **PM TRIAL** → Item Type = `PM`.
5. Tombol **Submit** memvalidasi bahwa Item Template, Item Code, dan Primary UOM telah terisi.

---

### 3.3 Halaman Item Production Index

**Path**: `ItemProductionIndex.html`

**Tujuan**: Menampilkan semua dokumen Item Production (Trial & Non-Trial) dalam satu daftar terpadu.

#### 3.3.1 Dashboard Summary Cards

Identik dengan Item Trial Index (5 kartu: Total, Draft, Waiting Approval, Approved, Submitted to Oracle).

#### 3.3.2 Screenshot

*(Gambar 5: Halaman Item Production Index)*

#### 3.3.3 Functional Description

**Action Bar:**

| Tombol                    | Fungsi                                                         |
|---------------------------|----------------------------------------------------------------|
| Export Excel              | Mengekspor data tabel ke format Excel                          |
| Create New Item Production | Mengarahkan ke `ItemProductionDetail.html`                   |

**Tabel Daftar Item Production:**

| Kolom           | Keterangan                                                      |
|-----------------|-----------------------------------------------------------------|
| Document Status | Badge berwarna sesuai status                                    |
| Mode            | `Trial` atau `Non-Trial`                                        |
| Item Template   | RM atau PM                                                      |
| Item Code       | Link ke halaman Detail                                          |
| Description     | Deskripsi item                                                  |
| Primary UOM     | Satuan ukur                                                     |
| Created By      | Nama pembuat                                                    |
| Created Date    | Tanggal dibuat                                                  |
| Next Approver   | Approver berikutnya dalam workflow                              |
| Action          | Tombol View / Edit                                              |

---

### 3.4 Halaman Item Production Detail

**Path**: `ItemProductionDetail.html`

**Tujuan**: Halaman input dan editing data item production. Mendukung dua jalur dalam satu formulir: **Trial Mode** (berdasarkan item trial yang disetujui) dan **Non-Trial Mode** (pendaftaran langsung).

#### 3.4.1 Mode Toggle: Trial vs Non-Trial

| Mode       | Value     | Keterangan                                                        |
|------------|-----------|-------------------------------------------------------------------|
| Trial      | `TRIAL`   | LOV Item Code Trial aktif, LOV General Item nonaktif. Default.    |
| Non-Trial  | `NONTRIAL`| LOV General Item aktif, LOV Item Code Trial nonaktif              |

> **Catatan**: Mengubah mode setelah data terisi akan memunculkan dialog konfirmasi sebelum form di-reset.

#### 3.4.2 Screenshot

*(Gambar 6: Halaman Item Production Detail – Trial Mode)*

#### 3.4.3 Functional Description

**Bagian A: Item Information**

| Field                | ID Elemen         | Tipe          | Wajib | Keterangan                                                              |
|----------------------|-------------------|---------------|-------|-------------------------------------------------------------------------|
| Item Template        | `itemTemplate`    | Select        | Ya    | RM atau PM. Menentukan field Compliance yang aktif.                     |
| Item Code Trial      | `itemCodeTrial`   | Input+LOV     | Ya*   | *Wajib di Trial Mode. Source: `XXSHP_INV_MASTER_ITEM_STG`              |
| Item Code            | `generalItem`     | Input         | Tidak | Auto-fill dari Item Code Trial (Trial Mode) atau dipilih manual (Non-Trial) |
| General Item         | `segment1`        | Radio+LOV     | Ya*   | *Wajib di Non-Trial Mode. New/Existing. Source: Oracle `MTL_SYSTEM_ITEMS_B` |
| Shelf Life (Month)   | `shelfLife`       | Number        | Tidak | Default: 0                                                              |
| Shelf Life Open Pack | `shelfLifeOpenPack` | Number      | Tidak | Dalam hari. Default: 0                                                  |
| Item Description     | `itemDescription` | Textarea      | Ya    | Dapat diedit                                                            |
| Closed Code          | `closedCode`      | Textarea      | Ya    | Kode internal                                                           |
| Primary UOM          | `primaryUOM`      | Input+LOV     | Ya    | Source: Oracle `MTL_UNITS_OF_MEASURE_TL`                               |
| Supplier Item        | `supplierItem`    | Text          | Tidak | Input bebas                                                             |
| Supplier Name        | `supplierName`    | Input+LOV     | Ya    | Source: Oracle `AP_SUPPLIERS`. Mengaktifkan LOV Principal.              |
| Principal Name       | `principalName`   | Input+LOV     | Ya    | Source: Oracle `AP_SUPPLIER_SITES_ALL`. Aktif setelah Supplier dipilih. |
| Bar Code             | `barCode`         | Input+LOV     | Tidak | Source: `XXSHP_INV_BAR_CODE`                                           |

**Bagian B: Compliance & Certification**

*Field Halal (aktif untuk template RM):*

| Field         | ID Elemen   | Tipe      | N/A | Keterangan                                             |
|---------------|-------------|-----------|-----|--------------------------------------------------------|
| Halal Country | `country`   | Input+LOV | Ya  | Source: Oracle `FND_LOOKUP_VALUES` (COUNTRY lookup)   |
| CHalal No     | `halalNo`   | Text      | Ya  | Nomor sertifikasi halal                                |
| CHalal ED     | `halalValid`| Date      | Ya  | Tanggal kadaluarsa sertifikasi halal                   |
| Halal Logo    | `halalLogo` | Input+LOV | Ya  | Source: Oracle `FND_LOOKUP_VALUES` (HALAL_LOGO lookup) |
| Halal Body    | `halalBody` | Input+LOV | Ya  | Source: Oracle `FND_LOOKUP_VALUES` (HALAL_BODY lookup) |

*Field bersama (RM & PM):*

| Field          | ID Elemen | Tipe      | N/A | Keterangan                                                              |
|----------------|-----------|-----------|-----|-------------------------------------------------------------------------|
| Akasia Number  | `akasiaNum`| Input+LOV| Ya  | Source: `XXSHP_AKASIA_MD_MASTER`. Auto-fill MD Number & MD Expire Date. |
| MD Number      | `cmdNo`   | Text      | –   | Read-only. Auto-fill dari Akasia Number.                                |
| MD Expire Date | `cmdValid` | Text     | –   | Read-only. Auto-fill dari Akasia Number.                                |

*Field Forestry (aktif untuk template PM):*

| Field                 | ID Elemen       | Tipe  | N/A | Keterangan                        |
|-----------------------|-----------------|-------|-----|-----------------------------------|
| Need Forestry Cert    | `forestryCert`  | Text  | Ya  | Indikator kebutuhan sertifikasi   |
| Forestry Cert Body    | `forestryBody`  | Text  | Ya  | Badan sertifikasi kehutanan       |
| Forestry Cert Valid To| `forestryValid` | Date  | Ya  | Tanggal berlaku sertifikasi       |
| Forestry Cert Num     | `forestryNum`   | Text  | Ya  | Nomor sertifikasi kehutanan       |

*Pecah KN (switch toggle, selalu disabled – diisi oleh sistem):*

| Field    | ID Elemen | Tipe   | Keterangan                                   |
|----------|-----------|--------|----------------------------------------------|
| Pecah KN | `pecahKn` | Switch | Read-only. Diisi otomatis oleh sistem Oracle. |

**Bagian C: Sub-Tables Accordion**

Tiga tabel penunjang yang dapat diperluas/diciutkan (accordion). Setiap tabel mendukung penambahan (**Add**) dan penghapusan (**Delete**) baris secara dinamis.

**Tabel Barcode List:**

| Kolom        | Keterangan                    |
|--------------|-------------------------------|
| No           | Nomor urut baris              |
| Barcode      | Nomor barcode produk          |
| Product Name | Nama produk yang bersangkutan |
| Action       | Tombol Delete per baris       |

LOV Barcode: menampilkan kolom Action, Barcode, Item Code, Country, Description dari `XXSHP_INV_BAR_CODE`.

**Tabel MD Number List:**

| Kolom              | Keterangan                            |
|--------------------|---------------------------------------|
| No                 | Nomor urut baris                      |
| MD Number          | Nomor MD (dari AKASIA)                |
| MD Product's Name  | Nama dagang produk                    |
| MD Production Site | Lokasi produksi                       |
| MD Expiry Date     | Tanggal kadaluarsa MD                 |
| Action             | Tombol Delete per baris               |

LOV MD Number: menampilkan kolom Action, AKASIA No, MD No, Nama Dagang, Nama Produk dari `XXSHP_AKASIA_MD_MASTER`.

**Tabel Halal Number List:**

| Kolom                | Keterangan                         |
|----------------------|------------------------------------|
| No                   | Nomor urut baris                   |
| Halal Number         | Nomor sertifikasi halal            |
| Halal Product's Name | Nama produk dalam sertifikat halal |
| Halal Expiry Date    | Tanggal kadaluarsa sertifikat      |
| Action               | Tombol Delete per baris            |

LOV Halal Number: menampilkan kolom Action, Halal Number, Halal Product, Expiry Date.

#### 3.4.4 Business Rules & Validation

1. **Mode Toggle**: Perubahan mode (Trial ↔ Non-Trial) memunculkan dialog konfirmasi. Jika dikonfirmasi, seluruh data form di-reset.
2. **Template Toggle**: Perubahan template (RM ↔ PM) memunculkan dialog konfirmasi. Jika dikonfirmasi, form di-reset dan field Compliance disesuaikan.
3. **Template RM** → field Halal aktif, field Forestry tersembunyi.
4. **Template PM** → field Forestry aktif, field Halal tertentu tersembunyi.
5. **N/A Checkbox**: Saat dicentang, field terkait dikosongkan dan dinonaktifkan; saat tidak dicentang, field diaktifkan kembali.
6. **LOV Supplier → Principal**: LOV Principal hanya aktif setelah Supplier dipilih. Memilih ulang Supplier akan me-reset Principal.
7. **LOV Akasia Number**: Memilih Akasia Number otomatis mengisi MD Number dan MD Expire Date (read-only).
8. **Sub-Tables**: Setiap tabel (Barcode, MD, Halal) mendukung multi-entri dalam satu transaksi.
9. **Submit**: Memvalidasi field wajib sebelum mengubah status ke `WAIT_APPROVAL`.

---

## 4. Struktur Database

### 4.1 Entity Relationship Diagram (ERD)

*(Gambar 7: ERD – Relasi Tabel Modul Item Registration)*

### 4.2 Tabel Staging Utama

#### 4.2.1 `XXSHP_INV_MASTER_ITEM_STG` — Tabel Staging Item

> Tabel utama yang menampung data hasil input dari formulir Item Trial dan Item Production sebelum dikirim ke Oracle ERP.

| Kolom                  | Tipe Data     | Keterangan                                                   |
|------------------------|---------------|--------------------------------------------------------------|
| `INTERFACE_ID`         | NUMBER (PK)   | Primary key, auto-generated                                  |
| `PROCESS_FLAG`         | VARCHAR2(1)   | Status proses: `1`=Pending, `7`=Success, `3`=Error           |
| `ITEM_TEMPLATE`        | VARCHAR2(50)  | Template item (RM TRIAL / PM TRIAL / RM / PM)               |
| `SEGMENT1`             | VARCHAR2(40)  | Item code (kode segment Oracle)                              |
| `DESCRIPTION`          | VARCHAR2(240) | Deskripsi item                                               |
| `PRIMARY_UOM_CODE`     | VARCHAR2(3)   | Satuan ukur utama                                            |
| `ITEM_TYPE`            | VARCHAR2(30)  | Tipe item (RM / PM)                                          |
| `LOB`                  | VARCHAR2(50)  | Line of Business                                             |
| `PURCHASING_TYPES`     | VARCHAR2(50)  | Tipe pembelian (default: INDIRECT2)                          |
| `PACKING_SIZE`         | NUMBER        | Ukuran kemasan                                               |
| `PALLET_SIZE`          | NUMBER        | Ukuran pallet                                                |
| `VENDOR_ID`            | NUMBER        | ID supplier dari Oracle `AP_SUPPLIERS`                       |
| `VENDOR_SITE_ID`       | NUMBER        | ID lokasi supplier dari Oracle `AP_SUPPLIER_SITES_ALL`       |
| `SUPPLIER_NAME`        | VARCHAR2(240) | Nama supplier                                                |
| `PRINCIPAL_NAME`       | VARCHAR2(240) | Nama prinsipal (supplier site)                               |
| `HALAL_COUNTRY`        | VARCHAR2(100) | Negara asal sertifikasi halal                                |
| `CHALAL_NO`            | VARCHAR2(100) | Nomor sertifikasi halal                                      |
| `CHALAL_EXPIRED_DATE`  | DATE          | Tanggal kadaluarsa sertifikasi halal                         |
| `HALAL_LOGO`           | VARCHAR2(100) | Jenis logo halal                                             |
| `HALAL_BODY`           | VARCHAR2(100) | Lembaga sertifikasi halal                                    |
| `AKASIA_NUM`           | VARCHAR2(50)  | Nomor AKASIA (MD Number reference)                           |
| `CMD_NO`               | VARCHAR2(50)  | Nomor MD (Izin Edar)                                         |
| `CMD_VALID`            | DATE          | Tanggal kadaluarsa MD                                        |
| `FORESTRY_CERT`        | VARCHAR2(10)  | Perlu sertifikasi kehutanan (Y/N)                            |
| `FORESTRY_BODY`        | VARCHAR2(200) | Badan sertifikasi kehutanan                                  |
| `FORESTRY_VALID_TO`    | DATE          | Tanggal berlaku sertifikasi kehutanan                        |
| `FORESTRY_NUM`         | VARCHAR2(100) | Nomor sertifikasi kehutanan                                  |
| `PROCESS_MODE`         | VARCHAR2(10)  | Mode proses: `TRIAL` atau `NONTRIAL`                         |
| `DOC_STATUS`           | VARCHAR2(30)  | Status dokumen (DRAFT / WAIT_APPROVAL / APPROVED / SUBMITTED)|
| `CREATED_BY`           | VARCHAR2(100) | Username pembuat dokumen                                     |
| `CREATION_DATE`        | DATE          | Tanggal pembuatan                                            |
| `LAST_UPDATED_BY`      | VARCHAR2(100) | Username yang terakhir mengubah                              |
| `LAST_UPDATE_DATE`     | DATE          | Tanggal perubahan terakhir                                   |

#### 4.2.2 `XXSHP_INV_MASTER_ITEM_STG_BARCODE` — Sub-Tabel Barcode

| Kolom          | Tipe Data     | Keterangan                                        |
|----------------|---------------|---------------------------------------------------|
| `ID`           | NUMBER (PK)   | Primary key                                       |
| `INTERFACE_ID` | NUMBER (FK)   | Referensi ke `XXSHP_INV_MASTER_ITEM_STG`          |
| `BARCODE`      | VARCHAR2(100) | Nomor barcode                                     |
| `PRODUCT_NAME` | VARCHAR2(240) | Nama produk                                       |
| `CREATED_BY`   | VARCHAR2(100) | Username pembuat                                  |
| `CREATION_DATE`| DATE          | Tanggal dibuat                                    |

#### 4.2.3 `XXSHP_INV_MASTER_ITEM_STG_MD` — Sub-Tabel MD Number

| Kolom               | Tipe Data     | Keterangan                                   |
|---------------------|---------------|----------------------------------------------|
| `ID`                | NUMBER (PK)   | Primary key                                  |
| `INTERFACE_ID`      | NUMBER (FK)   | Referensi ke `XXSHP_INV_MASTER_ITEM_STG`     |
| `MD_NUMBER`         | VARCHAR2(100) | Nomor MD (Izin Edar)                         |
| `MD_PRODUCT_NAME`   | VARCHAR2(240) | Nama dagang produk                           |
| `MD_PRODUCTION_SITE`| VARCHAR2(240) | Lokasi produksi                              |
| `MD_EXPIRY_DATE`    | DATE          | Tanggal kadaluarsa MD                        |
| `CREATED_BY`        | VARCHAR2(100) | Username pembuat                             |
| `CREATION_DATE`     | DATE          | Tanggal dibuat                               |

#### 4.2.4 `XXSHP_INV_MASTER_ITEM_STG_HALAL` — Sub-Tabel Halal Number

| Kolom               | Tipe Data     | Keterangan                                   |
|---------------------|---------------|----------------------------------------------|
| `ID`                | NUMBER (PK)   | Primary key                                  |
| `INTERFACE_ID`      | NUMBER (FK)   | Referensi ke `XXSHP_INV_MASTER_ITEM_STG`     |
| `HALAL_NUMBER`      | VARCHAR2(100) | Nomor sertifikasi halal                      |
| `HALAL_PRODUCT_NAME`| VARCHAR2(240) | Nama produk dalam sertifikat                 |
| `HALAL_EXPIRY_DATE` | DATE          | Tanggal kadaluarsa sertifikat                |
| `CREATED_BY`        | VARCHAR2(100) | Username pembuat                             |
| `CREATION_DATE`     | DATE          | Tanggal dibuat                               |

### 4.3 Tabel Oracle yang Digunakan (Existing)

> Tabel-tabel berikut **sudah ada** di Oracle EBS. Modul ini hanya membaca data dari tabel-tabel tersebut — tidak perlu dibuat ulang.

| Tabel Oracle                 | Kegunaan                                               |
|------------------------------|--------------------------------------------------------|
| `MTL_ITEM_TEMPLATES`         | Sumber data template item (RM TRIAL, PM TRIAL, RM, PM) |
| `MTL_SYSTEM_ITEMS_B`         | Master item Oracle (kode item, deskripsi, UOM)         |
| `MTL_UNITS_OF_MEASURE_TL`    | Master satuan ukur (UOM)                               |
| `FND_LOOKUP_VALUES`          | Master lookup (LOB, Halal Logo, Halal Body, Country)   |
| `AP_SUPPLIERS`               | Master supplier (Vendor ID, Supplier Name)             |
| `AP_SUPPLIER_SITES_ALL`      | Master lokasi supplier/principal (Vendor Site ID)      |
| `XXSHP_INV_BAR_CODE`         | Master data barcode internal                           |
| `XXSHP_AKASIA_MD_MASTER`     | Master AKASIA/MD Number                                |

---

## 5. Aturan Bisnis

### 5.1 Aturan Template

1. Template **RM TRIAL** → Item Type otomatis terisi `RM`; Item Types terisi nilai RM sesuai konfigurasi Oracle.
2. Template **PM TRIAL** → Item Type otomatis terisi `PM`; Item Types terisi nilai PM.
3. Template **RM** (Production) → mengaktifkan section Halal; menyembunyikan section Forestry.
4. Template **PM** (Production) → mengaktifkan section Forestry; menyembunyikan field Halal Logo dan Halal Body.
5. Mengubah template setelah data terisi memerlukan konfirmasi. Jika dikonfirmasi, seluruh form di-reset.

### 5.2 Aturan LOV

1. LOV **Item Code Trial** hanya aktif setelah **Item Template** dipilih.
2. Pilih Item Code Trial → auto-fill **Item Description** dan **Primary UOM** (read-only).
3. LOV **Principal** hanya aktif setelah **Supplier** dipilih.
4. Pilih **Supplier** → LOV Principal aktif; ganti Supplier → Principal di-reset.
5. Pilih **Akasia Number** → auto-fill **MD Number** dan **MD Expire Date** (read-only).

### 5.3 Aturan N/A Checkbox

1. Tersedia pada field: Halal Country, CHalal No, CHalal ED, Halal Logo, Halal Body, Akasia Number, Forestry Cert, Forestry Body, Forestry Valid To, Forestry Num.
2. Saat **N/A dicentang** → field terkait dikosongkan dan dinonaktifkan (*disabled*).
3. Saat **N/A tidak dicentang** → field terkait diaktifkan kembali dan dapat diisi.

### 5.4 Aturan Mode Trial vs Non-Trial

1. **Trial Mode** (default) → LOV Item Code Trial aktif; LOV General Item dan radio New/Existing nonaktif.
2. **Non-Trial Mode** → LOV General Item dan radio New/Existing aktif; LOV Item Code Trial nonaktif.
3. Mengubah mode setelah data terisi memerlukan dialog konfirmasi sebelum form di-reset.

### 5.5 Aturan Submit & Approval

1. Tombol **Submit** memvalidasi semua field bertanda wajib (*) sebelum diproses.
2. Setelah submit berhasil, status berubah dari `DRAFT` ke `WAIT_APPROVAL`.
3. Semua field menjadi read-only setelah disubmit.
4. **Approver** dapat menyetujui (→ `APPROVED`) atau menolak (→ `REJECTED`) dokumen.
5. Dokumen yang ditolak (*Rejected*) dapat diperbaiki dan disubmit ulang oleh Initiator.
6. Dokumen yang disetujui (*Approved*) secara otomatis dikirim ke Oracle ERP melalui tabel staging → status berubah ke `SUBMITTED`.

### 5.6 Aturan Sub-Tables

1. Tabel **Barcode**, **MD Number**, dan **Halal Number** mendukung multi-entri dalam satu transaksi.
2. Pengguna dapat menambah baris baru (tombol **Add**) atau menghapus baris (tombol **Delete** per baris).
3. Setiap baris yang ditambahkan melalui LOV akan otomatis mengisi field sesuai kolom yang tersedia.

---

## 6. List of Values (LOV) & Referensi Data

| LOV Name           | Sumber         | Tabel / Query                                           | Field Tujuan                                |
|--------------------|----------------|---------------------------------------------------------|---------------------------------------------|
| Item Template      | Oracle EBS     | `MTL_ITEM_TEMPLATES` (filter: RM TRIAL / PM TRIAL / RM / PM) | `itemTemplate`                        |
| Item Code Trial    | IDC + Oracle   | `XXSHP_INV_MASTER_ITEM_STG` JOIN `MTL_SYSTEM_ITEMS_B`  | `itemCodeTrial`, `itemDesc`, `primaryUOM`   |
| General Item (PM/RM) | Oracle EBS   | `MTL_SYSTEM_ITEMS_B` (filter by template)               | `segment1`                                  |
| Primary UOM        | Oracle EBS     | `MTL_UNITS_OF_MEASURE_TL`                               | `primaryUOM`                                |
| Item LOB           | Oracle EBS     | `FND_LOOKUP_VALUES` (where LOOKUP_TYPE = 'LOB')         | `itemLob`                                   |
| Supplier Name      | Oracle EBS     | `AP_SUPPLIERS`                                          | `supplierName`, `vendorId` (hidden)         |
| Principal Name     | Oracle EBS     | `AP_SUPPLIER_SITES_ALL` (filter by VENDOR_ID)           | `principalName`, `vendorSiteId` (hidden)    |
| Halal Country      | Oracle EBS     | `FND_LOOKUP_VALUES` (LOOKUP_TYPE = 'COUNTRY')           | `country`                                   |
| Halal Logo         | Oracle EBS     | `FND_LOOKUP_VALUES` (LOOKUP_TYPE = 'HALAL_LOGO')        | `halalLogo`                                 |
| Halal Body         | Oracle EBS     | `FND_LOOKUP_VALUES` (LOOKUP_TYPE = 'HALAL_BODY')        | `halalBody`                                 |
| Akasia Number      | IDC Internal   | `XXSHP_AKASIA_MD_MASTER` (Active records)               | `akasiaNum`, `cmdNo`, `cmdValid`            |
| Barcode            | IDC Internal   | `XXSHP_INV_BAR_CODE`                                    | Row di Barcode List table                   |
| MD Number (List)   | IDC Internal   | `XXSHP_AKASIA_MD_MASTER`                                | Row di MD Number List table                 |
| Halal Number (List)| IDC/Oracle     | Tabel Halal internal                                    | Row di Halal Number List table              |

---

## 7. Hak Akses & Peran Pengguna

| Peran               | Buat Item Trial | Edit Item Trial    | Submit Item Trial | Approve | Buat Item Prod | Edit Item Prod     | Lihat Semua |
|---------------------|-----------------|--------------------|-------------------|---------|----------------|--------------------|-------------|
| Initiator (IDC/Proc)| ✓               | ✓ (milik sendiri)  | ✓                 | ✗       | ✓              | ✓ (milik sendiri)  | ✗           |
| Approver            | ✗               | ✗                  | ✗                 | ✓       | ✗              | ✗                  | ✓           |
| Administrator       | ✓               | ✓                  | ✓                 | ✓       | ✓              | ✓                  | ✓           |

**Catatan**: Initiator hanya dapat melihat dan mengedit dokumen yang dibuat oleh dirinya sendiri. Approver dapat melihat semua dokumen yang masuk ke antrian persetujuannya.

---

## 8. Notifikasi

| Event                              | Penerima                          | Jenis          |
|------------------------------------|-----------------------------------|----------------|
| Dokumen baru disubmit              | Approver terkait                  | Email + In-App |
| Dokumen disetujui (Approved)       | Initiator                         | Email + In-App |
| Dokumen ditolak (Rejected)         | Initiator                         | Email + In-App |
| Data berhasil dikirim ke Oracle    | Initiator + Administrator         | In-App         |
| Pengiriman ke Oracle gagal         | Administrator                     | Email + In-App |
| Reminder: dokumen belum diproses   | Approver (belum action 2×24 jam)  | Email (Jadwal) |

---

*Dokumen ini dibuat berdasarkan analisis kode sumber modul UploadItemTrial sistem lama (KN2015\_RMPM) dan implementasi baru pada sistem IDC New RM Selection.*

*Revisi dokumen dilakukan jika ada perubahan spesifikasi dari Business Owner.*

**End of Document**
