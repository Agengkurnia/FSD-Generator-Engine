# {NAMA_MODUL} — Template FSD

> **INSTRUKSI AI:** Ganti seluruh `{PLACEHOLDER}` dengan data nyata dari kode/spec.
> **Jangan hapus** struktur heading. **Jangan invent** field yang tidak ada di UI.
> Hapus blok instruksi ini setelah selesai.

# FUNCTIONAL SPECIFICATION DOCUMENT (FSD)
## Modul: {NAMA_MODUL}
### Sistem: {NAMA_SISTEM}
### Versi Dokumen: 1.0

---

| Atribut | Keterangan |
|---------|------------|
| **Nama Dokumen** | FSD Modul {NAMA_MODUL} |
| **Versi** | 1.0 |
| **Tanggal** | {TANGGAL} |
| **Divisi** | {DIVISI} |
| **Status** | Draft |
| **Dibuat oleh** | {TIM_PEMBUAT} |

---

## Riwayat Revisi

| Versi | Tanggal | Diubah Oleh | Keterangan |
|-------|---------|-------------|------------|
| **1.0** | **{TANGGAL}** | **{TIM_PEMBUAT}** | Initial draft |

---

> **Catatan build:** Daftar Gambar, Daftar Tabel, dan caption bernomor dihasilkan otomatis oleh pipeline — jangan tulis manual di MD sumber.

## 1. Pendahuluan

### 1.1 Latar Belakang

{Paragraf kontekstual — jelaskan modul, sistem, dan alasan dokumen ini dibuat.}

### 1.2 Tujuan Dokumen

1. Mendeskripsikan fungsionalitas per komponen UI modul {NAMA_MODUL}.
2. Menjadi acuan pengembangan dan UAT.
3. Mendokumentasikan business rules, RBAC, dan alur approval (jika ada).

### 1.3 Ruang Lingkup

| Dalam lingkup | Di luar lingkup |
|---------------|-----------------|
| {Halaman/fitur A} | {Fitur X — iterasi berikutnya} |

### 1.4 Stakeholder

| Peran | Tim/Divisi | Keterlibatan |
|-------|------------|--------------|
| {Peran 1} | {Divisi} | {Keterlibatan} |

---

## 2. Ringkasan Business Flow

{Paragraf narasi alur bisnis end-to-end. Jelaskan hand-off antar role.}

### 2.1 Lane Swimlane

**Lane (urutan kiri → kanan):**

| # | Lane ID | Label | Tipe | Sumber |
|---|---------|-------|------|--------|
| 1 | L1 | {Role A} | User | `{path spec/kode}` |
| 2 | L2 | {Sistem} | System | `{path}` |
| 3 | L3 | {Role B} | User/External | `{path}` |

### 2.2 Swimlane — Alur {NAMA_PROSES}

```mermaid
flowchart LR
    subgraph L1["{Role A}"]
        direction TB
        A0([Mulai]) --> A1["{Langkah A1}"]
        A1 --> A9([Selesai])
    end
    subgraph L2["{Sistem}"]
        direction TB
        S1["{Proses sistem}"]
    end
    subgraph L3["{Role B}"]
        direction TB
        B1["{Langkah B1}"] --> B2{"{Keputusan?}"}
    end
    A1 --> B1
    B2 -->|"Ya"| S1
    S1 --> A9
    style A0 fill:#C8E6C9,stroke:#388E3C,color:#333
    style A9 fill:#B2DFDB,stroke:#00796B,color:#333
    style B2 fill:#FFE0B2,stroke:#F57C00,color:#333
    style L1 fill:#FFF9C4,stroke:#FBC02D,color:#333
    style L2 fill:#E3F2FD,stroke:#1976D2,color:#333
    style L3 fill:#FCE4EC,stroke:#C62828,color:#333
```

> Template lengkap: `docs/examples/swimlane/swimlane-4-role-template.mmd`

---

## 3. Halaman Index — {NAMA_MODUL}

### 3.1 Tampilan Umum

**Tampilan Halaman Index:**

![Halaman Index {NAMA_MODUL}](screenshots/ss_01_index.png)

{Paragraf deskripsi halaman index.}

#### 3.1.1 Fields / Kolom Grid

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| {Field} | `{idElemen}` | Text | Ya | (kosong) | — | {Keterangan} |

#### 3.1.2 Tombol / Action Bar

| Tombol | ID | Warna/Style | Kondisi Aktif | Fungsi |
|--------|-----|-------------|---------------|--------|
| Baru | `btnNew` | Primary | Selalu | Buka form baru |

#### 3.1.3 Business Rules

| Rule ID | Aturan |
|---------|--------|
| BR-01 | {Aturan bisnis eksplisit} |

#### 3.1.4 CRUD

| Operasi | Cara | Role | Keterangan |
|---------|------|------|------------|
| **Create** | Klik Baru | {Role} | — |
| **Read** | Buka halaman index | Semua | — |
| **Update** | — | — | — |
| **Delete** | — | — | — |

---

## 4. Halaman Detail — {NAMA_MODUL}

**Tampilan Halaman Detail:**

![Halaman Detail {NAMA_MODUL}](screenshots/ss_02_detail.png)

### 4.1 Section Header

#### 4.1.1 Fields – Header

| Field Name | ID Elemen | Tipe | Mandatory | Default | Validasi | Keterangan |
|------------|-----------|------|-----------|---------|----------|------------|
| {Field} | `{id}` | Dropdown/LOV | Ya | (kosong) | — | — |

---

## 5. Aturan Bisnis (Business Rules)

| Rule ID | Aturan |
|---------|--------|
| BR-01 | {Ringkasan semua rules modul} |

---

## 6. Hak Akses & Peran Pengguna (RBAC)

| Bagian/Tab | {Role A} | {Role B} | Keterangan |
|------------|----------|----------|------------|
| Index | Read | Read | — |
| Detail – Simpan | — | Write | — |

---

## 7. Alur Persetujuan (jika ada)

### 7.1 Lane Swimlane

| # | Lane ID | Label | Tipe | Sumber |
|---|---------|-------|------|--------|
| 1 | L1 | {Initiator} | User | `{path}` |
| 2 | L2 | {Approver} | User | `{path}` |

### 7.2 Swimlane — Workflow Approval

```mermaid
flowchart LR
    subgraph INIT["{Initiator}"]
        direction TB
        I0([Mulai]) --> I1["Draft"] --> I2["Submit"]
    end
    subgraph APR["{Approver}"]
        direction TB
        A1{"Review?"} --> A2(["Approved"])
        A1 --> A3(["Rejected"])
    end
    I2 --> A1
    A3 --> I1
    A2 --> I9([Selesai])
    style I0 fill:#C8E6C9,stroke:#388E3C,color:#333
    style I9 fill:#B2DFDB,stroke:#00796B,color:#333
    style A1 fill:#FFE0B2,stroke:#F57C00,color:#333
    style INIT fill:#FFF9C4,stroke:#FBC02D,color:#333
    style APR fill:#E8F5E9,stroke:#388E3C,color:#333
```

> Template: `docs/examples/swimlane/swimlane-approval-template.mmd`

---

## 8. Struktur Database & ERD

```mermaid
erDiagram
    TABEL_HDR ||--o{ TABEL_DTL : contains
    TABEL_HDR {
        number ID PK
        varchar STATUS
    }
```

---

## 9. List of Values (LOV)

| LOV | Sumber Data | Dipakai di |
|-----|-------------|------------|
| {Nama LOV} | {Tabel/API} | {Field UI} |

---

## 10. Appendix

### 10.1 Status Dokumen

| Kode Status | Label | Warna Badge | Keterangan |
|-------------|-------|---------------|------------|
| DRAFT | Draft | Abu-abu | — |

### 10.2 Glosarium

| Istilah | Definisi |
|---------|----------|
| LOV | List of Values |
