"""Apply FSD revision notes + capture LOV/popup screenshots."""
from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(r"D:\Work\Source\FSD Generator Engine\modules\sample-result-gvn-shp")
MD = ROOT / "source" / "FSD_Sample_Result_GVN_SHP_v1.0.md"
SHOT = ROOT / "screenshots"
BASE = "http://127.0.0.1:8765"


# ---------------------------------------------------------------------------
# Screenshot LOV / popup
# ---------------------------------------------------------------------------
def capture_lovs() -> None:
    SHOT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(viewport={"width": 1920, "height": 1080}).new_page()

        # 1) Modal + New Parameter (request create)
        page.goto(f"{BASE}/request_create_cms.html", wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.locator("#pills-parameter-tab").click()
        page.wait_for_timeout(400)
        page.locator('button[data-bs-target="#addParameterModal"]').click()
        page.wait_for_selector("#addParameterModal.show", timeout=10000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOT / "ss_07_lov_modal_add_parameter.png"), full_page=True)
        print("OK ss_07_lov_modal_add_parameter.png")
        page.locator('#addParameterModal button[data-bs-dismiss="modal"]').click()
        page.wait_for_timeout(500)

        # 2) Spec GVN Select2 open
        page.locator("#specGvnYes").click()
        page.wait_for_timeout(600)
        page.locator("#specGvnSelect").wait_for(state="attached")
        # open select2
        page.locator("#specGvnSelect + .select2-container .select2-selection").click()
        page.wait_for_selector(".select2-container--open", timeout=10000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOT / "ss_08_lov_spec_gvn.png"), full_page=True)
        print("OK ss_08_lov_spec_gvn.png")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        # 3) Retest Sample No SHP Select2
        page.locator("#retestYes").click()
        page.wait_for_timeout(800)
        page.locator("#retestSampleNoShp + .select2-container .select2-selection").click()
        page.wait_for_selector(".select2-container--open", timeout=10000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOT / "ss_09_lov_retest_sample_shp.png"), full_page=True)
        print("OK ss_09_lov_retest_sample_shp.png")
        page.keyboard.press("Escape")

        # 4) Result create — Sample SHP LOV
        page.goto(f"{BASE}/result_sample_gvn_create_cms.html", wait_until="networkidle")
        page.wait_for_timeout(3500)
        page.locator("#sampleNoShpSelectResult + .select2-container .select2-selection").click()
        page.wait_for_selector(".select2-container--open", timeout=10000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOT / "ss_10_lov_result_sample_shp.png"), full_page=True)
        print("OK ss_10_lov_result_sample_shp.png")
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

        # 5) Result create — Sample GVN LOV
        page.locator("#sampleNoGvnSelectResult + .select2-container .select2-selection").click()
        page.wait_for_selector(".select2-container--open", timeout=10000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOT / "ss_11_lov_result_sample_gvn.png"), full_page=True)
        print("OK ss_11_lov_result_sample_gvn.png")

        browser.close()


# ---------------------------------------------------------------------------
# MD transforms
# ---------------------------------------------------------------------------
def drop_id_elemen_column(table_block: str) -> str:
    """Remove 'ID Elemen' column from a markdown pipe table block."""
    lines = table_block.strip("\n").split("\n")
    if len(lines) < 2 or "ID Elemen" not in lines[0]:
        return table_block
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    try:
        idx = headers.index("ID Elemen")
    except ValueError:
        return table_block
    new_lines = []
    for line in lines:
        if not line.strip().startswith("|"):
            new_lines.append(line)
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers) and "---" not in line:
            # separator or mismatched — try drop by position if same length headers
            pass
        if len(cells) > idx:
            cells = cells[:idx] + cells[idx + 1 :]
        new_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(new_lines)


def transform_all_tables_drop_id(text: str) -> str:
    def repl(m: re.Match) -> str:
        block = m.group(0)
        if "ID Elemen" in block.split("\n")[0]:
            return drop_id_elemen_column(block)
        return block

    # Match markdown tables (header + separator + rows)
    return re.sub(
        r"(?:^\|.+\|\s*\n)(?:^\|[-:| ]+\|\s*\n)(?:^\|.+\|\s*\n?)+",
        repl,
        text,
        flags=re.M,
    )


def apply_md_updates() -> None:
    text = MD.read_text(encoding="utf-8")

    # Version bump in header meta
    text = text.replace("### Versi Dokumen: 1.0", "### Versi Dokumen: 1.1")
    text = text.replace("| **Versi** | 1.0 |", "| **Versi** | 1.1 |")
    # Revision history — add 1.1 row, keep 1.0
    if "| **1.1** |" not in text:
        text = text.replace(
            "| **1.0** | **22 Juli 2026** | **Tim IT Digital Solution** | Initial Document — proses otoritatif mockup + flowapps |",
            "| **1.1** | **22 Juli 2026** | **Tim IT Digital Solution** | Revisi: bullet flow, swimlane OSIR→SHP, status NEW, hapus ID Elemen, query Oracle, ERD DAL, screenshot LOV |\n"
            "| 1.0 | 22 Juli 2026 | Tim IT Digital Solution | Initial Document — proses otoritatif mockup + flowapps |",
        )

    # 3) Remove BRD proyek lain from scope (right cell)
    text = text.replace(
        "| Status board, Status History, Parameter & Sample tab | BRD proyek lain (`brd_text.txt` Formulation Revamp) |",
        "| Status board, Status History, Parameter & Sample tab | — |",
    )

    # 2) Remove Lab Admin stakeholder row
    text = text.replace(
        "| Lab Admin | Analytical Central Admin | Monitor request, pull/map result, Sync |\n",
        "",
    )

    # 1) Business flow as bullets
    old_flow = (
        "Alur to-be (otoritatif mockup + flowapps) berlangsung dalam lima fase. "
        "User membuat **Sample Request** di KNAC dengan salah satu basis: **Retest**, **Get Spec (Spec GVN)**, atau **Manual**. "
        "Setelah data lengkap, user **Submit Request**. Sistem kemudian **Generate Sample**: jika Retest = No → Oracle SHP **dan** Oracle GVN; "
        "jika Retest = Yes → **hanya** Oracle SHP. Analisa lab berjalan di **OSIR** (di luar KNAC). Setelah hasil tersedia, user membuka menu "
        "**Result Sample GVN**, memetakan Sample SHP ↔ Sample GVN, lalu **Sync** (SYNC = YES) untuk Input Result ke Oracle GVN dengan Sample No. SHP "
        "sebagai source; atau berhenti di KNAC jika tidak di-Sync."
    )
    new_flow = """Alur to-be (otoritatif mockup + flowapps) ringkas sebagai berikut:

1. Requestor membuat **Sample Request** di KNAC dengan salah satu basis: **Retest**, **Get Spec (Spec GVN)**, atau **Manual**.
2. Requestor melengkapi header, parameter, dan quantity sample, lalu **Save Draft** (opsional) atau langsung **Submit Request**.
3. Sistem mengubah status menjadi **Submitted to Oracle** dan **Generate Sample**:
   - Retest = **No** → generate di **Oracle SHP** dan **Oracle GVN**
   - Retest = **Yes** → generate **hanya di Oracle SHP**
4. Analisa lab dilakukan di **OSIR** (di luar KNAC) hingga result diinput.
5. Setelah result diinput di OSIR, data **tersinkron ke Oracle SHP**.
6. Requestor membuka menu **Result Sample GVN**, memetakan Sample SHP ↔ Sample GVN, lalu mereview parameter result.
7. Requestor memilih **Sync** (SYNC = YES) untuk Input Result ke Oracle GVN (Sample No. SHP sebagai source) → status **Syncronized**; atau hanya Save → tetap **Draft** di KNAC."""
    if old_flow in text:
        text = text.replace(old_flow, new_flow)
    else:
        print("WARN: old flow paragraph not found exact")

    # 4) Lane tables — remove Sumber column (2.1 and 7.2)
    text = text.replace(
        """| # | Lane ID | Label | Tipe | Sumber |
|---|---------|-------|------|--------|
| 1 | L1 | Requestor / Sampler | User | `flowapps.txt` Fase 1–2; mockup create |
| 2 | L2 | Analytical Central (KNAC) | System | `flowapps.txt` Fase 2–3, 5 |
| 3 | L3 | Oracle SHP / GVN | ERP / Integrasi | `flowapps.txt` Fase 3, 5; BRD §2 |
| 4 | L4 | OSIR Lab | External | `flowapps.txt` Fase 4 |""",
        """| # | Lane ID | Label | Tipe |
|---|---------|-------|------|
| 1 | L1 | Requestor / Sampler | User |
| 2 | L2 | Analytical Central (KNAC) | System |
| 3 | L3 | Oracle SHP / GVN | ERP / Integrasi |
| 4 | L4 | OSIR Lab | External |""",
    )
    text = text.replace(
        """| # | Lane ID | Label | Tipe | Sumber |
|---|---------|-------|------|--------|
| 1 | L1 | Requestor / Lab Admin | User | mockup result create/edit |
| 2 | L2 | Analytical Central (KNAC) | System | `syncResult()`, `saveData()` |
| 3 | L3 | Oracle GVN | ERP | `flowapps.txt` Fase 5 |""",
        """| # | Lane ID | Label | Tipe |
|---|---------|-------|------|
| 1 | L1 | Requestor | User |
| 2 | L2 | Analytical Central (KNAC) | System |
| 3 | L3 | Oracle GVN | ERP |""",
    )

    # 5) Swimlane 2.2 — OSIR input → sync SHP → then requestor opens result
    old_uml = """|OSIR Lab|
:Analisa sample\\n(as-is hingga result diinput);

|Requestor / Sampler|
:Buka menu Result Sample GVN;
:Petakan Sample SHP ↔ Sample GVN\\n+ isi/review parameter result;"""
    new_uml = """|OSIR Lab|
:Analisa sample\\n(as-is hingga result diinput);
:Sinkronkan result\\nke Oracle SHP;

|Oracle SHP / GVN|
:Result tersedia\\ndi Oracle SHP;

|Requestor / Sampler|
:Buka menu Result Sample GVN;
:Petakan Sample SHP ↔ Sample GVN\\n+ isi/review parameter result;"""
    if old_uml in text:
        text = text.replace(old_uml, new_uml)
    else:
        print("WARN: swimlane OSIR block not found")

    # Hand-off bullets update
    text = text.replace(
        """**Hand-off antar lane:**

1. Requestor → KNAC: Submit Request menyimpan data dan memicu generate.
2. KNAC → Oracle: Generate Sample SHP (± GVN) sesuai flag Retest.
3. Oracle/OSIR → Requestor: Hasil lab tersedia untuk ditarik di menu Result (tanpa UI OSIR di KNAC).
4. Requestor → KNAC → Oracle GVN: Sync Result mengirim hasil terpetakan.""",
        """**Hand-off antar lane:**

1. Requestor → KNAC: Submit Request menyimpan data dan memicu generate.
2. KNAC → Oracle: Generate Sample SHP (± GVN) sesuai flag Retest.
3. OSIR → Oracle SHP: Setelah result diinput di OSIR, data tersinkron ke Oracle SHP.
4. Requestor → KNAC: Buka Result Sample GVN setelah data tersedia di Oracle SHP.
5. Requestor → KNAC → Oracle GVN: Sync Result mengirim hasil terpetakan.""",
    )

    # Swimlane 7 rename Lab Admin
    text = text.replace("|Requestor / Lab Admin|", "|Requestor|")

    # 6) Status Result add NEW
    text = text.replace(
        """### 2.4 Ringkasan Status Result (Mockup)

| Kode Status | Label | Transisi |
|-------------|-------|----------|
| `Draft` | Draft | Create / Save result |
| `Syncronized` | Syncronized | Setelah `syncResult()` sukses |""",
        """### 2.4 Ringkasan Status Result (Mockup)

| Kode Status | Label | Transisi |
|-------------|-------|----------|
| `New` | New | Saat buka form create result |
| `Draft` | Draft | Setelah `saveData()` pada result |
| `Syncronized` | Syncronized | Setelah `syncResult()` sukses |""",
    )
    text = text.replace(
        """### 9.2 LOV Status Result (Mockup)

| Kode Status | Label | Warna Badge | Keterangan |
|-------------|-------|-------------|------------|
| Draft | Draft | Warning | Belum Sync |
| Syncronized | Syncronized | Success | Setelah Sync sukses |""",
        """### 9.2 LOV Status Result (Mockup)

| Kode Status | Label | Warna Badge | Keterangan |
|-------------|-------|-------------|------------|
| New | New | > **[TBD]** | Form create result baru |
| Draft | Draft | Warning | Belum Sync |
| Syncronized | Syncronized | Success | Setelah Sync sukses |""",
    )

    # Soften Lab Admin in CRUD to Requestor / Admin (stakeholder removed)
    text = text.replace("Requestor / Lab Admin (inferred)", "Requestor / Admin (inferred)")
    text = text.replace("Requestor / Lab Admin", "Requestor / Admin")
    text = text.replace("| Lab Admin (inferred) |", "| Admin (inferred) |")
    text = text.replace("| Lab Admin |", "| Admin |")

    # 8) Insert Oracle query sections after screenshots
    sql_create = """
#### 3.2.0 Query Oracle — Sumber LOV Create Request

Halaman Create Request memakai extract Oracle (mock file di `Mockup_AnalyticalCentral/Data/`). Query referensi:

**Spec GVN** (`Spec_GVN.json`) — Spec = Yes:

```sql
SELECT gs.spec_id, gs.spec_name, gs.spec_vers, gs.spec_desc, gs.inventory_item_id,
       msi.segment1 AS Item_Code, msi.description, msi.item_type,
       svr.ORGANIZATION_CODE,
       gst.test_id, gqt.test_code, gqt.test_desc AS Parameter, gqt.test_class,
       gtm.test_method_id, gtm.test_method_desc AS Test_Method,
       gqt.test_type, gqt.test_unit AS UOM,
       NVL(TO_CHAR(gst.min_value_num), gst.min_value_char) AS combined_min,
       NVL(TO_CHAR(gst.max_value_num), gst.max_value_char) AS combined_max,
       NVL(TO_CHAR(gst.target_value_num), gst.target_value_char) AS combined_target
FROM gmd_specifications gs
INNER JOIN GMD_ALL_SPEC_VRS_VL svr ON gs.spec_id = svr.spec_id
LEFT JOIN MTL_SYSTEM_ITEMS msi
  ON msi.inventory_item_id = gs.inventory_item_id
 AND gs.owner_organization_id = msi.organization_id
LEFT JOIN gmd_spec_tests gst ON gs.spec_id = gst.spec_id
LEFT JOIN GMD_QC_TESTS gqt ON gqt.test_id = gst.test_id
LEFT JOIN GMD_TEST_METHODS gtm ON gqt.test_method_id = gtm.test_method_id
WHERE svr.SPEC_VR_STATUS = 700
```

**Sample SHP Retest** (`Sample_SHP.json`) — Retest = Yes:

```sql
SELECT gs.sample_id, gs.sample_no, gs.sample_desc, gs.batch_id,
       gs.inventory_item_id, msi.segment1, gs.lot_number, gs.creation_date,
       gr.seq, gqt.test_code, gr.result_value_num, gqt.test_unit, gr.result_value_char
FROM GMD_SAMPLES gs, mtl_system_items msi, gmd_results gr,
     GMD_QC_TESTS gqt, Gmd_spec_results gsr
WHERE gs.inventory_item_id = msi.inventory_item_id
  AND gs.organization_id = msi.organization_id
  AND gs.sample_id = gr.sample_id
  AND gr.test_id = gqt.test_id
  AND gr.result_id = gsr.result_id
  AND gsr.evaluation_ind <> '5O'
  AND gs.creation_date >= TO_DATE('2026-02-01', 'YYYY-MM-DD')
  AND (msi.segment1 LIKE 'IBMIX%' OR msi.segment1 LIKE 'FGDUM%')
ORDER BY gs.sample_no, gr.seq
```

**Item Lot GVN** (`Item Lot GVN.json`):

```sql
SELECT msi.segment1 AS item_code, msi.description AS item_description,
       mln.lot_number,
       mln.origination_date AS lot_creation_date,
       mln.expiration_date AS lot_expired_date,
       mln.status_id, msi.organization_id
FROM mtl_lot_numbers mln
JOIN mtl_system_items_b msi
  ON mln.inventory_item_id = msi.inventory_item_id
 AND mln.organization_id = msi.organization_id
WHERE msi.organization_id = 84
ORDER BY mln.origination_date DESC
```

**Test Code SHP** (`Test Code SHP.json`) — enrich Method/UOM/Test Class:

```sql
SELECT gqt.test_id, gqt.test_code AS PARAMETER, gqt.test_desc, gqt.test_class,
       gtm.test_method_id, gtm.test_method_desc AS TEST_METHOD,
       gqt.test_type, gqt.test_unit, gqt.delete_mark,
       gqt.min_value_num, gqt.max_value_num
FROM GMD_QC_TESTS gqt
LEFT JOIN GMD_TEST_METHODS gtm ON gqt.test_method_id = gtm.test_method_id
LEFT JOIN GMD_QC_TEST_VALUES gqtv ON gqt.test_id = gqtv.test_id
```

**Tampilan LOV / Popup Create Request:**

![Modal + New Parameter](screenshots/ss_07_lov_modal_add_parameter.png)

![LOV Spec GVN (Select2)](screenshots/ss_08_lov_spec_gvn.png)

![LOV Retest Sample No. SHP](screenshots/ss_09_lov_retest_sample_shp.png)
"""

    sql_result = """
#### 4.2.0 Query Oracle — Sumber LOV Create Result

**Sample SHP Ver2** (`Sample_SHP_Ver2.json`) — Sample No. SHP + disposition/dates:

```sql
SELECT gs.sample_id, gs.sample_no, gs.sample_desc, gs.batch_id,
       gs.inventory_item_id, msi.segment1, gs.lot_number, gs.creation_date,
       gs.last_update_date AS LAST_UPDATE_DATE,
       gs.sample_disposition AS SAMPLE_DISPOSITION,
       gr.seq, gqt.test_code, gr.result_value_num, gqt.test_unit, gr.result_value_char
FROM GMD_SAMPLES gs, mtl_system_items msi, gmd_results gr,
     GMD_QC_TESTS gqt, Gmd_spec_results gsr
WHERE gs.inventory_item_id = msi.inventory_item_id
  AND gs.organization_id = msi.organization_id
  AND gs.sample_id = gr.sample_id
  AND gr.test_id = gqt.test_id
  AND gr.result_id = gsr.result_id
  AND gsr.evaluation_ind <> '5O'
  AND gs.creation_date >= TO_DATE('2026-02-01', 'YYYY-MM-DD')
  AND (msi.segment1 LIKE 'IBMIX%' OR msi.segment1 LIKE 'FGDUM%')
ORDER BY gs.sample_no, gr.seq
```

**Sample GVN** (`Sample_GVN.json`) — Sample No. GVN + list Result:

```sql
SELECT gs.sample_id, gs.sample_no, gs.sample_desc, gs.batch_id,
       gs.inventory_item_id, msi.segment1, gs.lot_number, gs.creation_date,
       gr.seq, gqt.test_code, gr.result_value_num, gqt.test_unit, gr.result_value_char
FROM GMD_SAMPLES gs, mtl_system_items msi, gmd_results gr,
     GMD_QC_TESTS gqt, Gmd_spec_results gsr
WHERE gs.inventory_item_id = msi.inventory_item_id
  AND gs.organization_id = msi.organization_id
  AND gs.sample_id = gr.sample_id
  AND gr.test_id = gqt.test_id
  AND gr.result_id = gsr.result_id
  AND gsr.evaluation_ind <> '5O'
  AND gs.creation_date >= TO_DATE('2026-02-01', 'YYYY-MM-DD')
  AND (msi.segment1 LIKE 'IBMIX%' OR msi.segment1 LIKE 'FGDUM%')
ORDER BY gs.sample_no, gr.seq
```

**Tampilan LOV Create Result:**

![LOV Sample No. SHP (Result)](screenshots/ss_10_lov_result_sample_shp.png)

![LOV Sample No. GVN (Result)](screenshots/ss_11_lov_result_sample_gvn.png)
"""

    if "#### 3.2.0 Query Oracle" not in text:
        text = text.replace(
            "![Halaman Create Sample Request](screenshots/ss_02_request_create.png)\n",
            "![Halaman Create Sample Request](screenshots/ss_02_request_create.png)\n" + sql_create + "\n",
        )
    if "#### 4.2.0 Query Oracle" not in text:
        text = text.replace(
            "![Halaman Create Result Sample GVN](screenshots/ss_05_result_create.png)\n",
            "![Halaman Create Result Sample GVN](screenshots/ss_05_result_create.png)\n" + sql_result + "\n",
        )

    # 9) Replace ERD section with DAL-aligned design
    erd_new = r'''## 8. Database & ERD

### 8.1 Standarisasi Kolom (AnalyticalCentral.DAL)

Pola entity transaction existing (`TrrequestAnalysis`, `TrrequestDParameter`, `TrrequestDSample`, `TrstatusHistory`) di `AnalyticalCentral.Common\Entity\Transaction`:

| Kolom wajib | Tipe | Keterangan |
|-------------|------|------------|
| `Id` | string (GUID) | Primary key |
| `IdHeader` | string | FK ke header (untuk tabel detail) |
| `BitActive` | bool / bool? | Soft active flag |
| `CreatedBy` | string? | User pembuat |
| `CreatedDate` | DateTime? | Waktu buat |
| `UpdatedBy` | string? | User pengubah |
| `UpdatedDate` | DateTime? | Waktu ubah |

Naming: prefix **`Tr*`** untuk transaction, **`M*`** untuk master. DbSet di `AnalyticalCenterContext`: `TrrequestAnalyses`, `TrrequestDParameters`, `TrrequestDSamples`, `TrstatusHistories`.

### 8.2 Strategi Desain Tabel Modul GVN-SHP

1. **Ekstensi** entity request existing (`TrrequestAnalysis` + detail) untuk field Retest / Spec GVN / Item / Lot / Sample No. SHP–GVN.
2. **Tabel baru** untuk Result Sample GVN: header + detail parameter, mengikuti pola audit di atas.
3. **Reuse** `TrstatusHistory` dengan `Type` = `REQUEST` / `RESULT` dan `ContraintId` = Id header.
4. LOV Spec/Sample Oracle **tidak** disimpan sebagai master PG penuh — di-query ke Oracle (lihat §3.2.0 / §4.2.0); snapshot boleh disimpan di baris transaksi jika diperlukan.

### 8.3 Entitas Usulan

| Entitas | Peran | Catatan |
|---------|-------|---------|
| `TrrequestAnalysis` *(extend)* | Header request | Tambah `BitRetest`, `RetestSampleNoShp`, `BitSpecGvn`, `SpecIdGvn`, `SpecNameGvn`, `SpecVers`, `ItemGvn`, `LotGvn` |
| `TrrequestDParameter` *(extend)* | Parameter grid | Tambah `ParameterGvn`, `ParameterShp`, `MethodShp`, `UomShp`, `TestClassShp`, `MinSpec`, `MaxSpec`, `TargetSpec` |
| `TrrequestDSample` *(extend)* | Sample/pooling | Map `NoSample`/`NoPolling` ke Sample No. SHP / Pooling; tambah `SampleNoGvn` |
| `TrstatusHistory` *(reuse)* | Histori status | `ContraintId`, `Type`, `StatusCode` + audit |
| `TrresultSampleGvn` *(baru)* | Header result | Mapping SHP↔GVN + `SyncStatus` |
| `TrresultDParameter` *(baru)* | Baris result | Result value, conclusion, remarks, override |
| `TrintegrationLog` *(baru, opsional)* | Log generate/sync | Mendukung Failed Integration **[TBD]** |

### 8.4 Kolom Usulan — `TrresultSampleGvn` & Detail

**Header `TrresultSampleGvn`:** `Id`, `IdRequest` (opsional), `SampleNoShp`, `SampleIdShp`, `ItemShp`, `LotShp`, `RequestDate`, `AnalysisCompletionDate`, `SampleNoGvn`, `SampleIdGvn`, `ItemGvn`, `LotGvn`, `SyncStatus`, `StatusCode`, `BitActive`, `CreatedBy`, `CreatedDate`, `UpdatedBy`, `UpdatedDate`.

**Detail `TrresultDParameter`:** `Id`, `IdHeader`, `Seq`, `ParameterShp`, `ParameterGvn`, `UomShp`, `UomGvn`, `MinSpecGvn`, `MaxSpecGvn`, `ResultValue`, `Conclusion`, `Remarks`, `OverrideBy`, `BitActive`, `CreatedBy`, `CreatedDate`, `UpdatedBy`, `UpdatedDate`.

### 8.5 ERD

```mermaid
erDiagram
    TrrequestAnalysis ||--o{ TrrequestDParameter : IdHeader
    TrrequestAnalysis ||--o{ TrrequestDSample : IdHeader
    TrrequestAnalysis ||--o{ TrstatusHistory : ContraintId
    TrrequestAnalysis ||--o| TrresultSampleGvn : IdRequest
    TrresultSampleGvn ||--o{ TrresultDParameter : IdHeader
    TrresultSampleGvn ||--o{ TrstatusHistory : ContraintId
    TrresultSampleGvn ||--o{ TrintegrationLog : optional
    TrrequestAnalysis ||--o{ TrintegrationLog : optional

    TrrequestAnalysis {
        string Id PK
        string RequestNo
        string StatusCode
        bool BitRetest
        string RetestSampleNoShp
        bool BitSpecGvn
        string SpecNameGvn
        string SpecVers
        string ItemGvn
        string LotGvn
        bool BitActive
        string CreatedBy
        datetime CreatedDate
        string UpdatedBy
        datetime UpdatedDate
    }
    TrrequestDParameter {
        string Id PK
        string IdHeader FK
        string ParameterGvn
        string ParameterShp
        string MethodShp
        string UomShp
        string MinSpec
        string MaxSpec
        string TargetSpec
        bool BitActive
    }
    TrrequestDSample {
        string Id PK
        string IdHeader FK
        string NoSample
        string NoPolling
        string SampleNoGvn
        string SampleDesc
        decimal TotalMinQty
        bool BitActive
    }
    TrresultSampleGvn {
        string Id PK
        string IdRequest FK
        string SampleNoShp
        string SampleNoGvn
        string SyncStatus
        string StatusCode
        bool BitActive
        string CreatedBy
        datetime CreatedDate
        string UpdatedBy
        datetime UpdatedDate
    }
    TrresultDParameter {
        string Id PK
        string IdHeader FK
        int Seq
        string ParameterShp
        string ParameterGvn
        string ResultValue
        string Conclusion
        string Remarks
        string OverrideBy
        bool BitActive
    }
    TrstatusHistory {
        string Id PK
        string ContraintId
        string Type
        string StatusCode
        bool BitActive
        string CreatedBy
        datetime CreatedDate
    }
    TrintegrationLog {
        string Id PK
        string IntegrationType
        string Direction
        string Status
        string CorrelationId
        string ErrorMessage
        bool BitActive
    }
```

### 8.6 Mapping UI → Entity

| Field UI | Entity / Kolom | Keterangan |
|----------|----------------|------------|
| Request Number | `TrrequestAnalysis.RequestNo` | Autogenerate |
| Retest | `BitRetest` | Mutual exclusion |
| Spec GVN | `BitSpecGvn` | — |
| Sample No. SHP (retest) | `RetestSampleNoShp` | LOV Sample_SHP |
| Select Spec GVN | `SpecNameGvn` + `SpecVers` | LOV Spec_GVN |
| Sample No. SHP (result) | `TrresultSampleGvn.SampleNoShp` | — |
| Sample No. GVN (result) | `TrresultSampleGvn.SampleNoGvn` | — |
| Sync Status | `TrresultSampleGvn.SyncStatus` | New / Draft / Syncronized |

### 8.7 Integrasi Oracle

| Integrasi | Arah | Trigger | Catatan teknis |
|-----------|------|---------|----------------|
| Get Specification | GVN → KNAC | Spec GVN = Yes | Query Spec_GVN (§3.2.0) |
| Generate Sample SHP | KNAC → SHP | Setelah Submit | Dummy `FGDUM001`; fondasi as-is staging + `run_create_sample` |
| Generate Sample GVN | KNAC → GVN | Retest = No | > **[TBD]** package/API |
| Sync result OSIR → SHP | OSIR → SHP | Setelah input di OSIR | Di luar UI KNAC; prasyarat menu Result |
| Pull Result | Oracle SHP → KNAC | Menu Result | Query Sample_SHP_Ver2 / Sample_GVN (§4.2.0) |
| Input Result / Sync | KNAC → GVN | `syncResult()` | Sertakan Sample SHP sebagai source |
| Failed Integration | Internal | Error generate | > **[TBD]** BRD only |

---
'''

    # Replace from ## 8. Database through --- before ## 9.
    text2, n = re.subn(
        r"## 8\. Database & ERD\n.*?(?=\n## 9\. LOV)",
        lambda _m: erd_new.rstrip() + "\n\n",
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        print("WARN: ERD section replace count=", n)
    else:
        text = text2

    # 7) Drop ID Elemen columns
    text = transform_all_tables_drop_id(text)

    # Clean leftover TBD-only keterangan that were only IDs - optional light cleanup
    text = text.replace(
        "| Request Number | Text (readonly) | Ya (Auto) | `AUTOGENERATE` | — | Nomor request otomatis |",
        "| Request Number | Text (readonly) | Ya (Auto) | `AUTOGENERATE` | — | Nomor request otomatis |",
    )

    MD.write_text(text, encoding="utf-8")
    print("MD updated:", MD)
    print("remaining ID Elemen headers:", text.count("| ID Elemen |"))
    print("remaining Lab Admin stakeholder check:", "Lab Admin | Analytical" in text)


if __name__ == "__main__":
    import sys

    do_capture = "--skip-capture" not in sys.argv
    if do_capture:
        print("=== Capture LOVs ===")
        capture_lovs()
    else:
        print("=== Skip capture ===")
    print("=== Update MD ===")
    apply_md_updates()
    print("DONE")
