# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
## Modul: Sample Result GVN-SHP Integration
### Sistem: Analytical Central (KNAC) — PT. Sanghiang Perkasa
### Versi Dokumen: 1.0

---

| Atribut | Keterangan |
|---------|------------|
| **Nama Dokumen** | FSD Modul Sample Result GVN-SHP Integration |
| **Versi** | 1.0 |
| **Tanggal** | 22 Juli 2026 |
| **Divisi** | IT Digital Solution |
| **Status** | Draft |
| **Dibuat oleh** | Tim IT Digital Solution |
| **Proyek** | Sample Result GVN-SHP Integration / Analytical Central |
| **Referensi BRD** | `2026.GVNSHP-BRD.001` (26 Mar 2026) |
| **PID Ref.** | `2026.GVNSHP-PID.001` |

---

## Riwayat Revisi

| Versi | Tanggal | Diubah Oleh | Keterangan |
|-------|---------|-------------|------------|
| **1.0** | **22 Juli 2026** | **Tim IT Digital Solution** | Initial Document — proses otoritatif mockup + flowapps |

---

> **Catatan build:** Caption bernomor (`Gambar 3.1`, `Tabel 6.2.1`) dihasilkan otomatis — jangan tulis manual di MD sumber.
>
> **Otoritas proses:** Alur fungsional mengikuti **mockup Analytical Central** + `flowapps.txt` (Submit → Generate; Result Draft → Syncronized). Perbedaan dengan BRD dicatat sebagai **[TBD]** / gap di Bab 9.

## 1. Pendahuluan

### 1.1 Latar Belakang

**Analytical Central (KNAC)** adalah portal laboratorium Kalbe Nutritionals / PT Sanghiang Perkasa untuk request analisa, review, COA, dan sinkronisasi ke Oracle SHP. Inisiatif **Sample Result GVN-SHP Integration** memperluas kemampuan KNAC agar pertukaran data lab tersambung ke **Oracle SHP** dan **Oracle GVN**: mulai create sample request, get specification, generate sample paralel, penarikan hasil dari OSIR, hingga sync result ke GVN.

Pada kondisi as-is, codebase `analyticalcentralwebsite` sudah memiliki workflow request dan sync staging SHP saat approval. Integrasi Get Spec / Generate Sample GVN / Input Result belum diimplementasi. Mockup CMS di `Mockup_AnalyticalCentral` dan narasi `flowapps.txt` menjadi acuan UI dan alur to-be untuk FSD ini.

### 1.2 Tujuan Dokumen

1. Mendeskripsikan fungsionalitas UI modul Transaction Sample GVN dan Result Sample GVN berdasarkan mockup.
2. Menjadi acuan pengembangan dan UAT untuk integrasi SHP/GVN.
3. Mendokumentasikan business rules, status workflow, RBAC (inferred), disposisi Sync, serta model data konseptual.
4. Mencatat gap BRD vs mockup/flowapps agar keputusan stakeholder tersurat.

### 1.3 Ruang Lingkup

| Dalam lingkup | Di luar lingkup |
|---------------|-----------------|
| Create / Edit / Submit Sample Request (Retest, Spec GVN, Manual) | Eksekusi analisa lab di aplikasi **OSIR** |
| Generate Sample ke Oracle SHP (± GVN) setelah Submit | Full rebuild master data Oracle SHP/GVN |
| List, Create, Edit, Sync Result Sample GVN | Fitur Master User & Total Capability (CMS existing / pelengkap mockup) |
| Status board, Status History, Parameter & Sample tab | BRD proyek lain (`brd_text.txt` Formulation Revamp) |
| Aturan numbering sample `GVN-MN…`, mutual exclusion Retest↔Spec | Hangfire / background job retry (keputusan terpisah) |

### 1.4 Stakeholder

| Peran | Tim/Divisi | Keterlibatan |
|-------|------------|--------------|
| Document Approver | IT Digital Solution | Review & approval FSD (Hendi Hendrasta, Debby Tantika Ardi) |
| Document Approver | Project Management | Review & approval FSD (Cut Shafira Salsabila, Andreas Kurnijanto) |
| Requestor / Sampler | Lab / Business | Create request, submit, view result |
| Lab Admin | Analytical Central Admin | Monitor request, pull/map result, Sync |
| System Integrator | IT | Integrasi Oracle SHP, Oracle GVN, KN Global |
| Client | Eksternal / internal | > **[TBD]** — alur Client Approved ada di BRD, tidak di mockup |

### 1.5 Sumber Kebenaran & Konvensi

| Prioritas | Sumber |
|-----------|--------|
| 1 | Mockup HTML/JS: `Mockup_AnalyticalCentral/*.html` |
| 2 | `Documentation/flowapps.txt` |
| 3 | `Documentation/BRD - GVN-SHP Integration.md` (numbering, mutual exclusion, gap notes) |
| 4 | Codebase as-is `analyticalcentralwebsite` (pola modul, role existing) |
| 5 | Studi Analisis `Documentation/Studi Analisis - GVN-SHP Integration.md` |

Field tanpa `id`/`name` di HTML ditulis sebagai `> **[TBD]**`. Handler tombol mengikuti nama fungsi JS mockup.

### 1.6 Istilah Singkat

Lihat **Bab 9 — Glosarium** untuk daftar lengkap (KNAC, SHP, GVN, OSIR, Syncronized, FGDUM001).

---

## 2. Ringkasan Business Flow

Alur to-be (otoritatif mockup + flowapps) berlangsung dalam lima fase. User membuat **Sample Request** di KNAC dengan salah satu basis: **Retest**, **Get Spec (Spec GVN)**, atau **Manual**. Setelah data lengkap, user **Submit Request**. Sistem kemudian **Generate Sample**: jika Retest = No → Oracle SHP **dan** Oracle GVN; jika Retest = Yes → **hanya** Oracle SHP. Analisa lab berjalan di **OSIR** (di luar KNAC). Setelah hasil tersedia, user membuka menu **Result Sample GVN**, memetakan Sample SHP ↔ Sample GVN, lalu **Sync** (SYNC = YES) untuk Input Result ke Oracle GVN dengan Sample No. SHP sebagai source; atau berhenti di KNAC jika tidak di-Sync.

> **Gap BRD:** BRD memicu generate setelah **Client Approved**, disposisi **OK / NOT OK** + auto-retest, serta **Notify Sampler** dan **Failed Integration**. Fitur tersebut **belum** ada di mockup/flowapps — dicatat di Bab 5 & 9 sebagai **[TBD]**.

### 2.1 Lane Swimlane — Business Flow End-to-End

**Lane (urutan kiri → kanan):**

| # | Lane ID | Label | Tipe | Sumber |
|---|---------|-------|------|--------|
| 1 | L1 | Requestor / Sampler | User | `flowapps.txt` Fase 1–2; mockup create |
| 2 | L2 | Analytical Central (KNAC) | System | `flowapps.txt` Fase 2–3, 5 |
| 3 | L3 | Oracle SHP / GVN | ERP / Integrasi | `flowapps.txt` Fase 3, 5; BRD §2 |
| 4 | L4 | OSIR Lab | External | `flowapps.txt` Fase 4 |

### 2.2 Swimlane — Alur Sample Request hingga Result Sync

```plantuml
@startuml
skinparam SwimlaneBorderColor #000000
skinparam SwimlaneBorderThickness 3
skinparam SwimlaneTitleBackgroundColor #D9EAD3
skinparam SwimlaneTitleFontStyle bold
skinparam ActivityBackgroundColor #FFFFFF
skinparam ActivityBorderColor #000000
skinparam ActivityStartColor #C8E6C9
skinparam ActivityEndColor #B2DFDB

|Requestor / Sampler|
start
:Buat Sample Request\n(Retest / Spec GVN / Manual);
:Lengkapi Header,\nParameter, Quantity Sample;
:Save Draft (opsional);
:Submit Request ke Oracle;

|Analytical Central (KNAC)|
:Validasi request &\nubah status Submitted to Oracle;
if (Retest = Yes?) then (Ya)
  |Oracle SHP / GVN|
  :Generate Sample\nhanya di Oracle SHP;
else (Tidak)
  |Oracle SHP / GVN|
  :Generate Sample paralel\nOracle SHP + Oracle GVN;
endif

|OSIR Lab|
:Analisa sample\n(as-is hingga result diinput);

|Requestor / Sampler|
:Buka menu Result Sample GVN;
:Petakan Sample SHP ↔ Sample GVN\n+ isi/review parameter result;

|Analytical Central (KNAC)|
if (Sync = YES?) then (Ya)
  |Oracle SHP / GVN|
  :Input Result ke Oracle GVN\n(+ Sample No. SHP sebagai source);
  |Analytical Central (KNAC)|
  :Status Syncronized;
else (Tidak)
  :Data tetap di KNAC\n(status Draft);
endif
stop
@enduml
```

**Hand-off antar lane:**

1. Requestor → KNAC: Submit Request menyimpan data dan memicu generate.
2. KNAC → Oracle: Generate Sample SHP (± GVN) sesuai flag Retest.
3. Oracle/OSIR → Requestor: Hasil lab tersedia untuk ditarik di menu Result (tanpa UI OSIR di KNAC).
4. Requestor → KNAC → Oracle GVN: Sync Result mengirim hasil terpetakan.

### 2.3 Ringkasan Status Request (Mockup)

| Kode Status | Label | Transisi |
|-------------|-------|----------|
| `New` | New | Saat buka form create |
| `Draft` | Draft | Setelah `saveData()` |
| `Submitted to Oracle` | Submitted to Oracle | Setelah `submitRequest()` sukses |

### 2.4 Ringkasan Status Result (Mockup)

| Kode Status | Label | Transisi |
|-------------|-------|----------|
| `Draft` | Draft | Create / Save result |
| `Syncronized` | Syncronized | Setelah `syncResult()` sukses |

---

## 3. Transaction Sample GVN

Modul Transaction Sample GVN mencakup daftar request, form create, dan halaman detail. Sumber UI: `transaction_cms.html`, `request_create_cms.html`, `request_detail_cms.html`. Navigasi sidebar: Transaction → Transaction Sample GVN (`assets/js/sidebar.js`).

### 3.1 Dashboard List — Transaction Sample GVN

Halaman list menampilkan kartu ringkasan (Total / Draft / Submitted to Oracle) dan tabel request. Klik kartu memanggil `filterTable` dengan teks status.

**Tampilan Halaman List Transaction:**

![Halaman List Transaction Sample GVN](screenshots/ss_01_transaction_list.png)

#### 3.1.1 Dashboard Cards

| Elemen | ID Elemen | Handler | Keterangan |
|--------|-----------|---------|------------|
| Total Requests | `countAll` | `filterTable('')` | Menampilkan semua baris |
| Draft | `countDraft` | `filterTable('Draft')` | Filter status Draft |
| Submitted to Oracle | `countSubmit` | `filterTable('Submitted to Oracle')` | Filter status Submitted |

#### 3.1.2 Kolom DataTable List

| Kolom | Field Key / Entity Field | Render | Sortable | Keterangan |
|-------|--------------------------|--------|----------|------------|
| Request No | Request Number | Text / Link | Ya | Contoh format mock: `{seq}/{NOR\|TOP}/{MM}/{YYYY}` |
| Requester | Requester | Text | Ya | Nama user pembuat |
| Created Date | Created Date | DateTime | Ya | Tanggal dibuat |
| Updated Date | Updated Date | DateTime | Ya | Tanggal diubah |
| Status | Status | Badge | Ya | `Draft` atau `Submitted to Oracle` |
| Action | — | Icon Edit | Tidak | Navigasi ke `request_detail_cms.html` |

#### 3.1.3 Tombol Aksi — List Transaction

| Tampilan | Tombol | ID / Handler | Warna/Style | Fungsi |
|----------|--------|--------------|-------------|--------|
| ![Tombol + New Transaction](screenshots/ss_btn_trx_new.png) | + New | `btnNewTransaction` → `request_create_cms.html` | btn warning (`#ffc107`) | Membuka form Create Sample Request |
| ![Tombol Edit Transaction](screenshots/ss_btn_trx_edit.png) | Edit | Link ke detail | Icon / outline | Membuka `request_detail_cms.html` |

#### 3.1.4 CRUD — List Transaction

| Operasi | Cara | Role | Keterangan |
|---------|------|------|------------|
| **Create** | Klik + New | Requestor / Lab Admin (inferred) | Form create |
| **Read** | Buka list / filter card | Semua role terautentikasi (inferred) | Filter via `filterTable` |
| **Update** | Klik Edit pada baris | Requestor / Lab Admin (inferred) | Detail page |

### 3.2 Create Sample Request

Halaman create (`request_create_cms.html`) berisi Status Board (Alert `New`, Progress 0%), accordion Status History, form header dua kolom, serta tab Parameter dan Sample. Tiga jalur penentuan parameter: **Retest**, **Spec GVN**, atau **Manual** (+ New parameter).

**Tampilan Halaman Create Request:**

![Halaman Create Sample Request](screenshots/ss_02_request_create.png)

#### 3.2.1 Status Board & Status History

| Elemen | ID Elemen | Keterangan |
|--------|-----------|------------|
| Status History Accordion | `statusHistoryAccordion` | Riwayat status dokumen |
| Heading Status | `headingStatus` | Judul accordion |
| Collapse Status | `collapseStatus` | Konten tabel history |

Kolom history (mock): No, Status, Created By (role), Timestamp.

#### 3.2.2 Fields – Header (Create)

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Request Number | > **[TBD]** — tanpa `id` di HTML | Text (readonly) | Ya (Auto) | `AUTOGENERATE` | — | Nomor request otomatis |
| Requester | > **[TBD]** | Text (readonly) | Ya (Auto) | `AUTOGENERATE` | — | Dari sesi login |
| Request Date | > **[TBD]** | Text (readonly) | Ya (Auto) | `AUTOGENERATE` | — | Tanggal pengajuan |
| Objective | > **[TBD]** | Text | Opsional | (kosong) | — | Tujuan request |
| Company Name | > **[TBD]** | Text | Ya | `PT. Global Vita Nutritech` | — | Nama perusahaan |
| Priority | > **[TBD]** | Dropdown/LOV | Ya | Select Priority | Normal / Urgent / Top Urgent | Prioritas request |
| Factory (Same with Company) | > **[TBD]** | Checkbox | Tidak | Checked | — | Salin nama/alamat perusahaan |
| Factory Name | > **[TBD]** | Text | Ya | Sama Company Name | — | Nama pabrik |
| Factory Address | > **[TBD]** | Textarea | Ya | Alamat demo mock | — | Alamat pabrik |
| Retest | `retestYes` / `retestNo` (`name=retest`) | Radio | Ya | No | Mutual exclusive dengan Spec GVN | Handler `updateLogic()` |
| Sample No. SHP | `retestSampleNoShp` (row `sampleNoShpRow`) | Dropdown/LOV | Ya jika Retest=Yes | (kosong) | Wajib pilih sample prior | Sumber `Sample_SHP.json` |
| Spec GVN | `specGvnYes` / `specGvnNo` (`name=specGvn`) | Radio | Ya | No | Mutual exclusive dengan Retest | = Use Spec BRD |
| Select Spec GVN | `specGvnSelect` (row `specGvnSelectRow`) | Dropdown/LOV | Ya jika Spec=Yes | (kosong) | `SPEC_NAME \| SPEC_VERS` | Sumber `Spec_GVN.json` |
| Item GVN | `itemGvnInput` (row `itemGvnRow`) | Dropdown/LOV (Select2, tags) | Ya | (kosong) | — | Autofill dari Spec jika Spec=Yes |
| Lot GVN | `lotGvnInput` (row `lotGvnRow`) | Dropdown/LOV | Opsional | (kosong) | Filter by Item | Sumber `Item Lot GVN.json` |
| Sample Name | `headerSampleName` | Text | Ya | Auto Item atau Item-Lot | — | Diisi `updateSampleName()` |
| Matrix Product | > **[TBD]** | Dropdown/LOV | Opsional | --Select Data-- | — | Placeholder mock |
| Packaging | > **[TBD]** | Dropdown/LOV | Opsional | --Select Packaging-- | — | Placeholder mock |
| Storage Condition | > **[TBD]** | Dropdown/LOV | Opsional | --Select Storage-- | — | Placeholder mock |
| Reference Sample | > **[TBD]** | Text | Opsional | (kosong) | — | Referensi sample |
| Remark | > **[TBD]** | Textarea | Opsional | (kosong) | — | Catatan |

#### 3.2.3 Tab Parameter — Kolom Grid

Tab `pills-parameter` / `pills-parameter-tab`. Body: `parameterTableBody`.

| Kolom | Field Key | Render | Sortable | Keterangan |
|-------|-----------|--------|----------|------------|
| Parameter GVN | TEST_CODE / param | Text | Tidak | Dari Spec atau capability |
| Parameter SHP | TEST_CODE map | Text | Tidak | Enrich `Test Code SHP.json`; hilang → baris kuning |
| Method SHP | Method | Text | Tidak | Dari Test Code SHP |
| UOM SHP | Unit | Text | Tidak | Dari Test Code SHP |
| Test Class SHP | Class | Text | Tidak | Dari Test Code SHP |
| Min Spec | COMBINED_MIN | Text | Tidak | Dari Spec GVN |
| Max Spec | COMBINED_MAX | Text | Tidak | Dari Spec GVN |
| Target Spec | COMBINED_TARGET | Text | Tidak | Dari Spec GVN |
| Action | — | Hapus baris | Tidak | Hapus baris parameter |

**Sumber auto-populate:**

1. Spec GVN dipilih → match `Spec_GVN.json`; unique by `TEST_CODE`; enrich Method/UOM/Test Class.
2. Retest Sample dipilih → baris dari `Sample_SHP.json` untuk `SAMPLE_NO`; Min/Max/Target kosong; enrich sama.
3. Manual → modal `addParameterModal`.

#### 3.2.4 Modal + New Parameter

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Parameter | `swal-param` | Dropdown/LOV (Select2) | Ya | (kosong) | Required (`alert` jika kosong) | Capability parameter |
| Jumlah Baris | `qtyParam` | Number | Ya | 1 | ≥ 1 | Append N baris kosong |
| + Tambah | `btnAddParameter` | Button | — | — | — | Menambah baris ke grid |

#### 3.2.5 Tab Sample — Generate

Tab `pills-sample` / `pills-sample-tab`. Body: `sampleTableBody`.

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Quantity Sample | `qtySample` | Number | Ya saat Submit (tooltip) | 0 | Tooltip: minimal 1 — **belum enforce di JS** | Jumlah sample yang digenerate |
| Generate | `btnGenerateSample` | Button | — | — | — | Bangun N baris sample |

| Kolom Grid Sample | Keterangan |
|-------------------|------------|
| No | Urutan |
| Sample No. SHP | Format baru `GVN-MN[MM][YY]-[XXXXX]`; retest `[NOMOR]-[XX]` (tooltip) |
| Pooling No. SHP | Format tooltip `GVN-[YY]-[MM]-[XXX]` |
| Sample No. GVN | Baru: sama konsep Sample SHP; retest: tanpa counter retest; data Oracle nyata: numerik |
| Sample Description for (COA) | Default = Sample Name header |
| Total Min Sample (g) | Mock hardcoded `125` |

#### 3.2.6 Tombol Aksi — Create Request

| Tampilan | Tombol | ID / Handler | Warna/Style | Fungsi |
|----------|--------|--------------|-------------|--------|
| ![Tombol Save Request](screenshots/ss_btn_req_save.png) | Save | `saveData()` | btn-primary | Simpan sebagai **Draft** (konfirmasi Swal) |
| ![Tombol Submit Request](screenshots/ss_btn_req_submit.png) | Submit | `submitRequest()` | btn-success | Konfirmasi submit ke Oracle → sukses → redirect list |
| ![Tombol Back Request](screenshots/ss_btn_req_back.png) | Back | Link list | Outline | Kembali ke list |

**Tooltip Submit (bisnis mockup):** Jika Retest = No → Create Sample di Oracle SHP **dan** Oracle GVN. Validasi Qty Sample minimal 1.

> **Gap:** Tooltip tidak menyatakan Retest = Yes = SHP only (disurat di `flowapps.txt`). Enforce qty≥1 belum ada di `submitRequest()`.

#### 3.2.7 CRUD — Create Request

| Operasi | Cara | Role | Keterangan |
|---------|------|------|------------|
| **Create** | Isi form → Save / Submit | Requestor | Draft atau Submitted |
| **Read** | Buka form New | Requestor | Status New |
| **Update** | Ubah field sebelum Submit | Requestor | Setelah Submit lihat detail |

---

### 3.3 Detail Sample Request (Setelah Submit)

Halaman `request_detail_cms.html` menampilkan request yang sudah **Submitted to Oracle**. Alert meminta update Admin Review & Conclusion; Progress 100%. Header mayoritas readonly; radio Retest/Spec masih interaktif. Tab Sample: Qty readonly, `btnGenerateSample` disembunyikan (`d-none`), sample prefilled.

**Tampilan Halaman Detail Request:**

![Halaman Detail Request Sample](screenshots/ss_03_request_detail.png)

#### 3.3.1 Fields – Detail (perbedaan vs Create)

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Sample Name | `headerSampleName` | Text (readonly) | Ya | Nilai tersimpan | — | Background readonly |
| Quantity Sample | `qtySample` | Number (readonly) | Ya | Nilai tersimpan | — | Generate hidden |
| Parameter Min/Max/Target | sel di `parameterTableBody` | Text | Opsional | Demo rows | — | Masih editable di mock |
| Admin Review / Conclusion | > **[TBD]** — kolom **tidak ada** di HTML | — | — | — | — | Bertentangan dengan teks alert |

#### 3.3.2 Tombol Aksi — Detail Request

| Tampilan | Tombol | ID / Handler | Warna/Style | Fungsi |
|----------|--------|--------------|-------------|--------|
| ![Tombol Save Detail](screenshots/ss_btn_det_save.png) | Save | > **[TBD]** — onclick Save di detail | btn-primary | Simpan perubahan detail |
| ![Tombol Back Detail](screenshots/ss_btn_det_back.png) | Back | Link list | Outline | Kembali ke list |

Tidak ada tombol **Submit** pada halaman detail mockup.

#### 3.3.3 CRUD — Detail Request

| Operasi | Cara | Role | Keterangan |
|---------|------|------|------------|
| **Read** | Buka dari list Edit | Requestor / Lab Admin | Status Submitted |
| **Update** | Ubah field → Save | Lab Admin (inferred) | Parameter masih editable di mock |

---

## 4. Result Sample GVN

Modul Result mencakup list, create (mapping SHP↔GVN), dan edit/sync. Sumber: `result_sample_gvn_list_cms.html`, `result_sample_gvn_create_cms.html`, `result_sample_gvn_cms.html`.

### 4.1 Dashboard List — Result Sample GVN

Data list dimuat dari `fetch('./Data/Sample_GVN.json')`, distinct by `SAMPLE_NO`. Status Sync mock: `(countAll % 3 === 0) ? 'Syncronized' : 'Draft'`.

**Tampilan Halaman List Result:**

![Halaman List Result Sample GVN](screenshots/ss_04_result_list.png)

#### 4.1.1 Dashboard Cards

| Elemen | ID Elemen | Handler | Keterangan |
|--------|-----------|---------|------------|
| Total | `countAll` | `filterStatus('')` | Semua result |
| Draft | `countDraft` | `filterStatus('Draft')` | Belum Sync |
| Syncronized | `countSync` | `filterStatus('Syncronized')` | Sudah Sync |

#### 4.1.2 Kolom DataTable List Result

| Kolom | Field Key | Render | Sortable | Keterangan |
|-------|-----------|--------|----------|------------|
| Sample No. GVN | `SAMPLE_NO` | Text | Ya | Nomor sample GVN |
| Sample No. SHP | (mock map) | Text | Ya | Relasi SHP |
| Item | `SEGMENT1` / Item | Text | Ya | Kode item |
| Lot | Lot | Text | Ya | Lot number |
| Requested Date | Request Date | Date | Ya | Tanggal request |
| Completion Date | Completion Date | Date | Ya | Tanggal selesai analisa |
| Sync Status | Sync Status | Badge | Ya | `Draft` / `Syncronized` |
| Action | — | Input Result | Tidak | Ke halaman edit/detail |

Tabel: `tableResultSample`, body `tableResultSampleBody`.

#### 4.1.3 Tombol Aksi — List Result

| Tampilan | Tombol | ID / Handler | Warna/Style | Fungsi |
|----------|--------|--------------|-------------|--------|
| ![Tombol + New Result](screenshots/ss_btn_res_new.png) | + New | `btnNewTransaction` → create | btn warning | Buka create result |
| ![Tombol Input Result](screenshots/ss_btn_res_input.png) | Input Result | Link edit | Outline | Buka `result_sample_gvn_cms.html` |

#### 4.1.4 CRUD — List Result

| Operasi | Cara | Role | Keterangan |
|---------|------|------|------------|
| **Create** | + New | Lab Admin (inferred) | Mapping baru |
| **Read** | List + filter | Requestor / Lab Admin | `filterStatus` |
| **Update** | Input Result | Lab Admin | Edit + Sync |

---

### 4.2 Create Result — Mapping SHP ↔ GVN

Halaman `result_sample_gvn_create_cms.html`. Status **Draft**, Progress 50%. Section **SHP Information** dari `Sample_SHP_Ver2.json`; **GVN Information** dari `Sample_GVN.json`.

**Tampilan Halaman Create Result:**

![Halaman Create Result Sample GVN](screenshots/ss_05_result_create.png)

#### 4.2.1 Fields – SHP Information

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Sample No. SHP | `sampleNoShpSelectResult` | Dropdown/LOV | Ya | (kosong) | Tooltip: nomor sudah dipakai tidak bisa reuse — **belum enforce** | Pilih sample SHP sumber result |
| Item | `itemShpInputResult` | Text (readonly) | Ya (Auto) | (kosong) | — | Autofill dari sample SHP |
| Lot | `lotShpInputResult` | Text (readonly) | Opsional | (kosong) | — | Autofill |
| Request Date | `reqDateInputResult` | Text (readonly) | Ya (Auto) | (kosong) | — | Tanggal request |
| Analysis Completion Date | `compDateInputResult` | Text (readonly) | Opsional | (kosong) | — | Tanggal selesai |

#### 4.2.2 Fields – GVN Information

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Sample No. GVN | `sampleNoGvnSelectResult` | Dropdown/LOV | Ya | (kosong) | Tooltip: exclude disposition Accept (`4A`) / Accept with Variance (`5AV`) — **belum difilter di JS** | Target sample GVN |
| Item | `itemGvnInputResult` | Text (readonly) | Ya (Auto) | (kosong) | — | Autofill |
| Lot | `lotGvnInputResult` | Text (readonly) | Opsional | (kosong) | — | Autofill |

#### 4.2.3 Kolom Grid Parameter Result (Create)

Body: `parameterTableBody`. Saat Sample GVN berubah, grid diisi dari `TEST_CODE` / `RESULT_VALUE_*`.

| Kolom | Field Key | Render | Keterangan |
|-------|-----------|--------|------------|
| Parameter SHP | TEST_CODE | Text | Belum ada map nyata SHP↔GVN di mock |
| Parameter GVN | TEST_CODE | Text | Duplikat kode di create |
| UOM | TEST_UNIT | Text | Unit uji |
| Min | — | Text | Mock `-` |
| Max | — | Text | Mock `-` |
| Result | RESULT_VALUE_* | Text | Nilai hasil lab |
| Conclusion | — | Dropdown | **Conform** / **Not Conform** |
| Remarks | — | Text | Catatan |
| Override By | — | Text | User override |

#### 4.2.4 Tombol Aksi — Create Result

| Tampilan | Tombol | ID / Handler | Warna/Style | Fungsi |
|----------|--------|--------------|-------------|--------|
| ![Tombol Save Result Create](screenshots/ss_btn_resc_save.png) | Save | `saveData()` | btn-primary | Simpan Draft |
| ![Tombol Sync Result Create](screenshots/ss_btn_resc_sync.png) | Sync | `syncResult()` | btn-success | Konfirmasi sync ke GVN → status Syncronized → list |

Tidak ada auto-retest loop pada Sync.

---

### 4.3 Edit Result / Sync Disposition

Halaman `result_sample_gvn_cms.html`. Status **Syncronized**, Progress 100%. Mapping demo hardcoded (contoh `00040`→`37934`). Conclusion baris: **Accept** | **Retest (Out of Spec)** — perubahan dari original mengaktifkan Remarks + Override By (user demo hardcoded).

**Tampilan Halaman Edit Result:**

![Halaman Edit Result Sample GVN](screenshots/ss_06_result_edit.png)

#### 4.3.1 Fields – Edit Result

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| Sample No. SHP | `sampleNoShpSelectResult` | Dropdown/LOV | Ya | Nilai tersimpan | — | Mapping SHP |
| Sample No. GVN | `sampleNoGvnInputResult` | Text | Ya | Nilai tersimpan | — | Input/teks di edit (bukan select create) |
| Conclusion (baris) | > **[TBD]** per-row select | Dropdown/LOV | Ya | Accept / Retest | Override → Remarks wajib (mock) | **Bukan** loop Create Sample BRD |
| Parameter grid | `parameterTableBody` | Grid | — | Demo mismatch nama | — | Dokumentasi kebutuhan mapping asimetrik |

Modal tambah parameter sama: `addParameterModal`, `swal-param`, `qtyParam`, `btnAddParameter`.

#### 4.3.2 Tombol Aksi — Edit Result

| Tampilan | Tombol | ID / Handler | Warna/Style | Fungsi |
|----------|--------|--------------|-------------|--------|
| ![Tombol Save Result Edit](screenshots/ss_btn_rese_save.png) | Save | `saveData()` | btn-primary | Simpan perubahan |
| ![Tombol Sync Result Edit](screenshots/ss_btn_rese_sync.png) | Sync | `syncResult()` | btn-success | Sync ulang / konfirmasi ke GVN |

#### 4.3.3 CRUD — Result

| Operasi | Cara | Role | Keterangan |
|---------|------|------|------------|
| **Create** | Form create → Save / Sync | Lab Admin | Draft atau Syncronized |
| **Read** | List / Edit | Requestor / Lab Admin | — |
| **Update** | Edit conclusion / remarks → Save / Sync | Lab Admin | Override logic mock |

---

## 5. Aturan Bisnis

| Rule ID | Aturan |
|---------|--------|
| BR-01 | Running Counter sample (`XXXXX`) dan Counter Retest (`RR`/`XX`) wajib increment berurutan, tersentralisasi, tanpa duplikasi. `MM`/`YY` mengikuti waktu pengajuan (BRD §4.1). |
| BR-02 | Format Sample No. baru: `GVN-MN[MM][YY]-[XXXXX]`. Retest: akhiran `-[RR]` / `-[XX]` sesuai tooltip mockup. |
| BR-03 | Format Pooling No. SHP (tooltip mockup): `GVN-[YY]-[MM]-[XXX]`. |
| BR-04 | Mutual exclusion: jika **Retest = Yes**, maka **Spec GVN** dipaksa No dan sebaliknya (`updateLogic()`; BRD §4.2). |
| BR-05 | Jika Spec GVN = Yes, parameter di-populate dari Spec / Validity Rule Oracle GVN (`Spec_GVN.json` di mock). |
| BR-06 | Jika Retest = Yes, parameter di-populate dari sample SHP prior; Spec disabled; generate sample **hanya di Oracle SHP** (`flowapps.txt`). |
| BR-07 | Jika Retest = No pada Submit, sistem Generate Sample di **Oracle SHP dan Oracle GVN** (`flowapps.txt` + tooltip Submit). |
| BR-08 | Submit mengubah status request menjadi **Submitted to Oracle** dan memicu generate (otoritas mockup/flowapps). |
| BR-09 | Quantity Sample minimal 1 saat Submit (tooltip). > **[TBD]** — enforce server-side wajib; mock belum enforce di JS. |
| BR-10 | Baris parameter tanpa mapping Test Code SHP ditandai visual (baris kuning) di mock. |
| BR-11 | Analisa lab berlangsung di **OSIR** hingga result diinput; KNAC tidak menggantikan OSIR. |
| BR-12 | Pada Result, Sample No. SHP yang sudah dipakai tidak boleh dipilih ulang (tooltip). > **[TBD]** enforce. |
| BR-13 | Sample GVN dengan disposition Accept (`4A`) / Accept with Variance (`5AV`) dikecualikan dari pilihan (tooltip). > **[TBD]** enforce. |
| BR-14 | **Sync = YES** (`syncResult`): Input Result ke Oracle GVN + lampirkan Sample No. SHP sebagai source; status → **Syncronized**. |
| BR-15 | **Sync = NO** (hanya Save / tidak Sync): data tetap di KNAC berstatus **Draft**; proses berhenti tanpa kirim ke GVN. |
| BR-16 | Conclusion baris **Retest (Out of Spec)** pada edit result adalah disposisi line-level, **bukan** auto-loop Create Sample BRD. |
| BR-17 | Item dummy SHP untuk generate administratif: `FGDUM001` (BRD); filter mock data mencakup `FGDUM%` / `IBMIX%`. |
| BR-18 | > **[TBD] — Gap BRD:** Trigger generate setelah **Client Approved** (bukan Submit). Belum di mockup. |
| BR-19 | > **[TBD] — Gap BRD:** Disposisi hasil **OK / NOT OK** dengan auto-retest `-[RR]`. Digantikan model Sync di FSD ini sampai keputusan stakeholder. |
| BR-20 | > **[TBD] — Gap BRD:** **Notify Sampler** email saat Result Approved / Ready. Tidak ada di mockup/flowapps. |
| BR-21 | > **[TBD] — Gap BRD:** **Failed Integration** + retry wajib, no bypass sebelum lab queue. Tidak ada di mockup. |
| BR-22 | > **[TBD] — Gap BRD:** Status request `DRAFT` → `SUBMIT TO LAB` → `CLIENT FEEDBACK` → `APPROVED` vs mockup `New`/`Draft`/`Submitted to Oracle`. |
| BR-23 | > **[TBD]:** Kolom Admin Review / Conclusion pada detail request (disebut alert & BRD) belum ada di HTML mockup. |
| BR-24 | Prefix sample di detail demo (`LAB-MN…`) inkonsisten vs tooltip create (`GVN-MN…`). Canonical untuk implementasi: **`GVN-MN`** sampai diputuskan lain. |

---

## 6. RBAC

BRD tidak mendefinisikan matriks RBAC formal. Matriks berikut **inferred** dari label UI mockup + role existing KNAC (`REQ`, `ADMIN_LAB`, `ADMIN`, `eksternal`). Semua sel bertanda **?** atau catatan TBD wajib dikonfirmasi stakeholder.

### 6.1 Matriks Akses Modul

| Bagian / Operasi | Requestor (`REQ`) | Lab Admin (`ADMIN_LAB`) | Admin (`ADMIN`) | Client (`eksternal`) | System |
|------------------|-------------------|-------------------------|-----------------|----------------------|--------|
| List Transaction | R | R | R | > **[TBD]** | — |
| Create / Save Draft Request | C/U | C/U | C/U | > **[TBD]** | — |
| Submit Request | U | U | U | N | Trigger generate |
| Detail Request (post-submit) | R | R/U | R/U | > **[TBD]** Client approve BRD | — |
| List Result | R | R | R | N | — |
| Create / Edit Result | > **[TBD]** | C/U | C/U | N | — |
| Sync Result ke GVN | > **[TBD]** | U | U | N | Input Result API |
| Master Capability / User | N | > **[TBD]** | Y (inferred) | N | — |

Keterangan: **C**=Create, **R**=Read, **U**=Update, **N**=No, **Y**=Yes.

### 6.2 Catatan As-Is KNAC

Role constants existing dipakai sebagai titik awal implementasi menu/auth via KN Global. Mockup **tidak** memiliki role gating.

---

## 7. Approval / Sync Disposition

### 7.1 Model Disposisi Otoritatif (Mockup / flowapps)

Disposisi hasil lab di KNAC diwakili oleh aksi **Sync**:

| Keputusan | Aksi UI | Status Result | Efek Integrasi |
|-----------|---------|---------------|----------------|
| SYNC = YES | Tombol **Sync** / `syncResult()` | `Syncronized` | Input Result ke Oracle GVN + Sample No. SHP sebagai source |
| SYNC = NO | Hanya **Save** / tidak Sync | `Draft` | Data tetap di KNAC; tidak masuk GVN |

### 7.2 Lane Swimlane — Result Sync

**Lane (urutan kiri → kanan):**

| # | Lane ID | Label | Tipe | Sumber |
|---|---------|-------|------|--------|
| 1 | L1 | Requestor / Lab Admin | User | mockup result create/edit |
| 2 | L2 | Analytical Central (KNAC) | System | `syncResult()`, `saveData()` |
| 3 | L3 | Oracle GVN | ERP | `flowapps.txt` Fase 5 |

```plantuml
@startuml
skinparam SwimlaneBorderColor #000000
skinparam SwimlaneBorderThickness 3
skinparam SwimlaneTitleBackgroundColor #D9EAD3
skinparam SwimlaneTitleFontStyle bold
skinparam ActivityBackgroundColor #FFFFFF
skinparam ActivityBorderColor #000000
skinparam ActivityStartColor #C8E6C9
skinparam ActivityEndColor #B2DFDB

|Requestor / Lab Admin|
start
:Narik / pilih Sample SHP &\nSample GVN;
:Review parameter result &\nconclusion baris;
if (Lakukan Sync?) then (Ya)
  |Analytical Central (KNAC)|
  :Validasi mapping &\npanggil Sync Result;
  |Oracle GVN|
  :Input Result +\nsimpan source Sample SHP;
  |Analytical Central (KNAC)|
  :Update status Syncronized;
else (Tidak)
  |Analytical Central (KNAC)|
  :Simpan Draft saja;
endif
stop
@enduml
```

### 7.3 Gap vs BRD (Approval Client & OK/NOT OK)

| Topik BRD | Perilaku BRD | Perilaku FSD (mockup) | Status |
|-----------|--------------|----------------------|--------|
| Client Approved | Syarat generate paralel | Tidak ada di mockup | > **[TBD]** |
| OK | Input Result GVN | Diganti **Sync** | Gap tercatat |
| NOT OK | Auto Create Sample retest | Tidak; conclusion Retest line-level saja | Gap tercatat |
| Notify Sampler | Email dari SHP | Tidak ada | > **[TBD]** |
| Submit Review lock | Kunci parameter | Belum spek di mock | > **[TBD]** |

---

## 8. Database & ERD

### 8.1 Catatan Sumber Data

Integrasi GVN **belum** memiliki tabel PostgreSQL khusus di `analyticalcentralwebsite`. Entity as-is terkait request: `TrrequestAnalysis`, `TrrequestDParameter`, `TrrequestDSample`, `TrstatusHistory`. Oracle as-is: `XxshpKnAwcStg`, package `XXSHP_GMD_CRTSMPL_KNAC_PKG.run_create_sample`.

Berikut model **konseptual** untuk modul baru. Nama tabel fisik PostgreSQL ditandai **[TBD]** hingga desain DAL dikunci.

### 8.2 Entitas Konseptual

| Entitas | Deskripsi | Catatan fisik |
|---------|-----------|---------------|
| `TR_SAMPLE_REQUEST` | Header request sample GVN-SHP | > **[TBD]** — bisa ekstensi `TrrequestAnalysis` atau tabel baru |
| `TR_SAMPLE_REQUEST_PARAM` | Baris parameter uji | > **[TBD]** |
| `TR_SAMPLE_REQUEST_SAMPLE` | Baris sample / pooling | > **[TBD]** |
| `TR_STATUS_HISTORY` | Histori status request/result | Pola as-is `TrstatusHistory` |
| `TR_RESULT_HEADER` | Header mapping result SHP↔GVN | > **[TBD]** |
| `TR_RESULT_LINE` | Baris result + conclusion | > **[TBD]** |
| `TR_INTEGRATION_LOG` | Log generate / sync / error | > **[TBD]** — terkait Failed Integration BRD |
| Spec / Sample Oracle | Sumber LOV & result | View/API Oracle GVN/SHP — bukan PG |

### 8.3 ERD Konseptual

```mermaid
erDiagram
    TR_SAMPLE_REQUEST ||--o{ TR_SAMPLE_REQUEST_PARAM : has
    TR_SAMPLE_REQUEST ||--o{ TR_SAMPLE_REQUEST_SAMPLE : has
    TR_SAMPLE_REQUEST ||--o{ TR_STATUS_HISTORY : tracks
    TR_SAMPLE_REQUEST ||--o| TR_RESULT_HEADER : may_produce
    TR_RESULT_HEADER ||--o{ TR_RESULT_LINE : has
    TR_SAMPLE_REQUEST ||--o{ TR_INTEGRATION_LOG : logs
    TR_RESULT_HEADER ||--o{ TR_INTEGRATION_LOG : logs

    TR_SAMPLE_REQUEST {
        string request_no
        string status
        string retest_flag
        string spec_gvn_flag
        string sample_no_shp_retest
        string spec_name
        string spec_vers
        string item_gvn
        string lot_gvn
        string sample_name
        string priority
    }
    TR_SAMPLE_REQUEST_PARAM {
        string param_gvn
        string param_shp
        string method_shp
        string uom_shp
        string test_class
        string min_spec
        string max_spec
        string target_spec
    }
    TR_SAMPLE_REQUEST_SAMPLE {
        string sample_no_shp
        string pooling_no_shp
        string sample_no_gvn
        string description_coa
        decimal total_min_sample
    }
    TR_RESULT_HEADER {
        string sample_no_shp
        string sample_no_gvn
        string sync_status
        date request_date
        date completion_date
    }
    TR_RESULT_LINE {
        string param_shp
        string param_gvn
        string uom
        string result_value
        string conclusion
        string remarks
        string override_by
    }
    TR_INTEGRATION_LOG {
        string integration_type
        string direction
        string status
        string correlation_id
        string error_message
    }
    TR_STATUS_HISTORY {
        string status_code
        string created_by
        datetime created_at
    }
```

### 8.4 Mapping UI → Data (Konseptual)

| Field UI | Entitas / Kolom Konseptual | Tipe Data | Keterangan |
|----------|----------------------------|-----------|------------|
| Request Number | `TR_SAMPLE_REQUEST.request_no` | string | Autogenerate |
| Retest | `retest_flag` | string Yes/No | Mutual exclusion |
| Spec GVN | `spec_gvn_flag` | string Yes/No | — |
| Sample No. SHP (retest) | `sample_no_shp_retest` | string | LOV Sample_SHP |
| Select Spec GVN | `spec_name` + `spec_vers` | string | LOV Spec_GVN |
| Sample No. SHP (result) | `TR_RESULT_HEADER.sample_no_shp` | string | — |
| Sample No. GVN (result) | `TR_RESULT_HEADER.sample_no_gvn` | string | — |
| Sync Status | `sync_status` | string | Draft / Syncronized |

### 8.5 Integrasi Oracle (Konseptual)

| Integrasi | Arah | Trigger | Catatan teknis |
|-----------|------|---------|----------------|
| Get Specification | GVN → KNAC | Spec GVN = Yes | Validity Rule / Spec tests |
| Generate Sample SHP | KNAC → SHP | Setelah Submit (FSD) | Dummy `FGDUM001`; fondasi as-is staging + `run_create_sample` |
| Generate Sample GVN | KNAC → GVN | Retest = No | > **[TBD]** package/API |
| Pull Result | Oracle/OSIR → KNAC | Menu Result | Sumber `GMD_RESULTS` mock |
| Input Result / Sync | KNAC → GVN | `syncResult()` | Sertakan Sample SHP sebagai source |
| Failed Integration | Internal | Error generate | > **[TBD]** BRD only |

---

## 9. LOV, Appendix & Gap

### 9.1 LOV Status Request (Mockup)

| Kode Status | Label | Warna Badge | Keterangan |
|-------------|-------|-------------|------------|
| New | New | > **[TBD]** | Form create baru |
| Draft | Draft | Warning / kuning (card) | Setelah Save |
| Submitted to Oracle | Submitted to Oracle | Success / hijau (card) | Setelah Submit |

### 9.2 LOV Status Result (Mockup)

| Kode Status | Label | Warna Badge | Keterangan |
|-------------|-------|-------------|------------|
| Draft | Draft | Warning | Belum Sync |
| Syncronized | Syncronized | Success | Setelah Sync sukses |

### 9.3 LOV Priority

| Nilai | Keterangan |
|-------|------------|
| Normal | Prioritas normal |
| Urgent | Prioritas urgent |
| Top Urgent | Prioritas tertinggi (contoh Request No memuat `TOP`) |

### 9.4 LOV Conclusion Result

| Layar | Nilai | Keterangan |
|-------|-------|------------|
| Create Result | Conform / Not Conform | Enum create |
| Edit Result | Accept / Retest (Out of Spec) | Enum edit — **inkonsisten** antar layar; > **[TBD]** standardisasi |

### 9.5 Disposition Codes (Oracle — Glosarium Operasional)

| Kode | Label sementara | Sumber | Keterangan |
|------|-----------------|--------|------------|
| `1P` | > **[TBD]** | SQL/mock Sample | Muncul di extract |
| `4A` | Accept | Tooltip Result create | Exclude dari pilihan GVN |
| `5AV` | Accept with Variance | Tooltip Result create | Exclude dari pilihan GVN |
| `5O` | > **[TBD]** | Filter SQL `evaluation_ind <> '5O'` | Arti bisnis belum resmi |

### 9.6 Glosarium

| Istilah | Arti |
|---------|------|
| KNAC / Analytical Central | Portal web request & CMS lab Kalbe Nutritionals |
| Oracle SHP | Ekosistem Oracle sisi SHP (sample admin, staging, dummy item) |
| Oracle GVN | Ekosistem Oracle sisi GVN (spec, sample numerik, input result) |
| OSIR | Aplikasi lab eksternal untuk eksekusi analisa |
| Spec / Validity Rule | Spesifikasi & aturan validitas di GVN sebagai template parameter |
| Pooling Number | Nomor pooling terkait sample lab |
| FGDUM001 | Item dummy SHP untuk generate sample (BRD) |
| Retest | Pengajuan ulang berbasis sample sebelumnya |
| Syncronized | Status result setelah Sync ke GVN sukses (ejaan mengikuti mockup) |
| Failed Integration | Status/log BRD saat generate gagal — > **[TBD]** di UI |
| COA | Certificate of Analysis |
| Capability | Master kemampuan uji lab + mapping method |

### 9.7 Gap BRD vs Mockup / flowapps

| # | Topik | BRD | Mockup / flowapps | Keputusan FSD v1.0 |
|---|-------|-----|-------------------|--------------------|
| 1 | Disposisi hasil | OK / NOT OK + auto-retest | Sync YES/NO (Draft→Syncronized) | Ikuti **Sync**; BRD sebagai gap |
| 2 | Trigger generate | Setelah Client Approved | Setelah Submit | Ikuti **Submit** |
| 3 | Retest generate | Paralel kurang tegas | SHP only | Ikuti **SHP only** |
| 4 | Notify Sampler | Ada | Tidak ada | > **[TBD]** |
| 5 | Failed Integration | Wajib | Tidak ada | > **[TBD]** |
| 6 | Status request | DRAFT→…→APPROVED | New/Draft/Submitted to Oracle | Ikuti **mockup** |
| 7 | Cakupan item | Non-internal divert | Semua item | Ikuti **flowapps** (semua item) |

### 9.8 File Mockup Acuan

| File | Peran |
|------|-------|
| `transaction_cms.html` | List Transaction Sample GVN |
| `request_create_cms.html` | Create Sample Request |
| `request_detail_cms.html` | Detail setelah submit |
| `result_sample_gvn_list_cms.html` | List Result |
| `result_sample_gvn_create_cms.html` | Create Result |
| `result_sample_gvn_cms.html` | Edit Result / Sync |
| `assets/js/sidebar.js` | Navigasi menu |
| `Data/*.json` | Kontrak data mock Oracle extracts |

### 9.9 Open Questions (ringkas)

1. Kapan hybrid BRD (Client Approved, Failed Integration, Notify) digabung ke UI?
2. Standardisasi enum Conclusion Create vs Edit?
3. Nama API/package Oracle untuk Get Spec, Generate GVN, Input Result?
4. Scope counter numbering (global / per company / per matrix)?
5. Apakah Sync=NO dapat di-Sync belakangan?

---

*Dokumen ini disusun mengikuti standar FSD Generator Engine. Proses otoritatif: mockup + flowapps. Referensi BRD `2026.GVNSHP-BRD.001` untuk numbering, mutual exclusion, dan pencatatan gap.*
