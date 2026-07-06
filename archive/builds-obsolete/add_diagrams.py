"""
Add Flowchart, ERD, and Business Flow Summary to FSD New RM Sample
"""

import sys
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def create_business_flow_section():
    """Create business flow summary section"""
    return """
    <h2>1.4 Business Flow Summary</h2>
    <p>New RM Sample Management adalah sistem untuk mengelola proses evaluasi sample Raw Material baru dari supplier. 
    Workflow dirancang untuk memastikan setiap sample melalui tahapan evaluasi yang terstruktur sebelum keputusan final dibuat.</p>
    
    <h4>Alur Bisnis Utama:</h4>
    <ol>
        <li><strong>Sample Reception (Step 1: Document)</strong>
            <ul>
                <li>Supplier mengirimkan sample RM ke perusahaan</li>
                <li>PIC menerima sample dan mendokumentasikan detail (material name, supplier, quantity, price)</li>
                <li>Upload dokumen pendukung (COA, MSDS, Spec Sheet)</li>
                <li>Sample diberi nomor unik untuk tracking</li>
            </ul>
        </li>
        <li><strong>Purpose Analysis (Step 2: Sample Purpose)</strong>
            <ul>
                <li>Tim R&D menganalisis tujuan penggunaan sample</li>
                <li>Mapping sample dengan target product yang akan menggunakan</li>
                <li>Identifikasi expected benefit (cost reduction, quality improvement, dll)</li>
                <li>Set deadline untuk analisis dan testing</li>
            </ul>
        </li>
        <li><strong>Technical Evaluation (Step 3: RM Evaluation)</strong>
            <ul>
                <li>Lab melakukan testing sesuai spesifikasi yang dibutuhkan</li>
                <li>Trial production untuk validasi performa material</li>
                <li>Evaluator memberikan quality score dan compliance assessment</li>
                <li>Upload hasil test report dan dokumentasi</li>
            </ul>
        </li>
        <li><strong>Final Decision (Step 4: Disposition)</strong>
            <ul>
                <li>Review summary lengkap dari semua step sebelumnya</li>
                <li>Decision maker memberikan keputusan: Approved / Rejected / On Hold</li>
                <li>Jika approved dan memerlukan approval atasan, masuk ke approval workflow</li>
                <li>Setelah final approval, sample status menjadi Completed</li>
            </ul>
        </li>
    </ol>

    <h4>Key Benefits:</h4>
    <ul>
        <li><strong>Standardized Process:</strong> Setiap sample melalui evaluasi yang sama, mengurangi subjektivitas</li>
        <li><strong>Traceability:</strong> Full audit trail dari reception hingga final decision</li>
        <li><strong>Collaboration:</strong> Melibatkan multiple stakeholders (Procurement, R&D, Lab, Management)</li>
        <li><strong>Data-Driven Decision:</strong> Keputusan berdasarkan data testing dan evaluasi objektif</li>
        <li><strong>Time Management:</strong> Deadline tracking untuk memastikan sample tidak tertunda</li>
    </ul>

    <h4>Stakeholders:</h4>
    <table>
        <thead>
            <tr>
                <th width="25%">Role</th>
                <th>Responsibility</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Sample Requestor (PIC)</strong></td>
                <td>Menerima sample, dokumentasi awal, koordinasi dengan supplier</td>
            </tr>
            <tr>
                <td><strong>R&D Team</strong></td>
                <td>Analisis purpose, mapping dengan product, set requirement</td>
            </tr>
            <tr>
                <td><strong>Lab/QC Team</strong></td>
                <td>Testing sample, validasi compliance, quality scoring</td>
            </tr>
            <tr>
                <td><strong>Decision Maker</strong></td>
                <td>Review hasil evaluasi, keputusan final (approve/reject)</td>
            </tr>
            <tr>
                <td><strong>Approver (Management)</strong></td>
                <td>Final approval untuk sample yang di-approve (jika diperlukan)</td>
            </tr>
        </tbody>
    </table>
"""


def create_flowchart_section():
    """Create flowchart using Mermaid"""
    return """
    <h2>1.5 Business Process Flowchart</h2>
    <div style="background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; margin: 20px 0;">
        <pre style="font-size: 9pt; line-height: 1.4;">
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NEW RM SAMPLE WORKFLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

    [START]
       │
       ▼
┌──────────────────────┐
│  STEP 1: DOCUMENT    │
│  Sample Reception    │
└──────────────────────┘
       │
       │ • Receive sample from supplier
       │ • Document material details
       │ • Upload COA, MSDS
       │ • Generate Sample No
       │
       ▼
┌──────────────────────┐
│ STEP 2: PURPOSE      │
│ Sample Analysis      │
└──────────────────────┘
       │
       │ • Define purpose category
       │ • Map to target products
       │ • Set expected benefits
       │ • Set analysis deadline
       │
       ▼
┌──────────────────────┐
│ STEP 3: EVALUATION   │
│ Technical Testing    │
└──────────────────────┘
       │
       │ • Lab testing
       │ • Trial production
       │ • Quality scoring
       │ • Compliance check
       │
       ▼
┌──────────────────────┐
│ STEP 4: DISPOSITION  │
│ Final Decision       │
└──────────────────────┘
       │
       │ • Review all steps
       │ • Decision: Approve/Reject/On Hold
       │
       ▼
    Decision?
       │
       ├─────────────┬─────────────┬─────────────┐
       │             │             │             │
    APPROVED      REJECTED     ON HOLD      CANCEL
       │             │             │             │
       ▼             ▼             ▼             ▼
  Approval      [END]      Wait for     [END]
  Required?              Additional
       │                    Info
       │                       │
   ┌───┴───┐                  │
   │       │                  │
  YES     NO                  │
   │       │                  │
   ▼       ▼                  ▼
Pending  Completed      Back to
Approval    │           Step 3
   │        │               │
   ▼        │               │
Approver    │               │
Review      │               │
   │        │               │
┌──┴──┐     │               │
│     │     │               │
APPROVE REJECT │            │
│     │     │               │
▼     ▼     ▼               ▼
Completed  Back to      Continue
[END]     Step 4       Evaluation
          [END]            │
                           │
                        [LOOP]

        </pre>
        <p style="text-align: center; font-size: 10pt; color: #666; margin-top: 10px;">
            <em>Figure 1: New RM Sample Complete Workflow</em>
        </p>
    </div>
"""


def create_erd_section():
    """Create ERD diagram"""
    return """
    <h2>1.6 Entity Relationship Diagram (ERD)</h2>
    <div style="background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; margin: 20px 0;">
        <pre style="font-size: 8pt; line-height: 1.3;">
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           NEW RM SAMPLE - DATABASE SCHEMA                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐         ┌──────────────────────────┐
│  M_TYPE_DOCUMENT         │         │  M_SUPPLIER              │
├──────────────────────────┤         ├──────────────────────────┤
│ PK intTypeDocId          │         │ PK intSupplierId         │
│    txtTypeName           │         │    txtSupplierName       │
│    bitActive             │         │    txtCountry            │
└──────────────────────────┘         │    bitActive             │
         │                            └──────────────────────────┘
         │                                      │
         │                                      │
         │                                      │
         │                                      │
         └──────────────┬───────────────────────┘
                        │
                        │
                        ▼
        ┌───────────────────────────────────────────────┐
        │  T_RM_SAMPLE_HEADER (Main Table)              │
        ├───────────────────────────────────────────────┤
        │ PK intSampleId                                │
        │    txtSampleNo (UNIQUE)                       │
        │ FK intTypeDocumentId ──→ M_TYPE_DOCUMENT      │
        │    txtMaterialName                            │
        │ FK intSupplierId ──→ M_SUPPLIER               │
        │    decPrice                                   │
        │ FK intCurrencyId ──→ M_CURRENCY               │
        │ FK intUOMId ──→ M_UOM                         │
        │    decQuantity                                │
        │ FK intPICId ──→ M_PEGAWAI                     │
        │    dtSubmissionDate                           │
        │    txtRemarks                                 │
        │    txtWorkflowStage (Document/Sample/Eval/Disp)│
        │    txtStatus (Draft/Pending/Completed)        │
        │    bitActive                                  │
        │    txtCreatedBy, dtCreatedDate                │
        │    txtModifiedBy, dtModifiedDate              │
        └───────────────────────────────────────────────┘
                        │
                        │
        ┌───────────────┼───────────────┬───────────────┐
        │               │               │               │
        ▼               ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ T_RM_SAMPLE_    │ │ T_RM_SAMPLE_    │ │ T_RM_SAMPLE_    │ │ T_RM_SAMPLE_    │
│ PURPOSE         │ │ EVALUATION      │ │ DISPOSITION     │ │ ATTACHMENT      │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ PK intPurposeId │ │ PK intEvalId    │ │ PK intDispId    │ │ PK intAttachId  │
│ FK intSampleId  │ │ FK intSampleId  │ │ FK intSampleId  │ │ FK intSampleId  │
│ FK intPurpose   │ │    dtTestDate   │ │    txtDecision  │ │ FK intDocTypeId │
│    CategoryId   │ │ FK intTestTypeId│ │    dtDecisionDt │ │    txtRemarks   │
│    txtExpected  │ │    txtTestResult│ │ FK intDecisionBy│ │    txtFileName  │
│    Benefit      │ │    txtSpecComp  │ │    txtReason    │ │    txtFilePath  │
│    decUsagePct  │ │    intQualScore │ │    txtNextAction│ │    intFileSize  │
│ FK intReplace   │ │    txtEvalNotes │ │    bitApproval  │ │    txtUploadBy  │
│    MaterialId   │ │ FK intEvaluator │ │    Required     │ │    dtUploadDate │
│    dtAnalysis   │ │    Id           │ │ FK intApproverId│ └─────────────────┘
│    Deadline     │ └─────────────────┘ │    txtApproval  │
└─────────────────┘                     │    Status       │
                                        └─────────────────┘

┌──────────────────────────┐         ┌──────────────────────────┐
│  M_CURRENCY              │         │  M_UOM                   │
├──────────────────────────┤         ├──────────────────────────┤
│ PK intCurrencyId         │         │ PK intUOMId              │
│    txtCurrencyCode       │         │    txtUOMCode            │
│    txtCurrencyName       │         │    txtUOMName            │
│    bitActive             │         │    bitActive             │
└──────────────────────────┘         └──────────────────────────┘

┌──────────────────────────┐         ┌──────────────────────────┐
│  M_PEGAWAI (Employee)    │         │  M_PURPOSE_CATEGORY      │
├──────────────────────────┤         ├──────────────────────────┤
│ PK intPegawaiId          │         │ PK intCategoryId         │
│    txtPegawaiName        │         │    txtCategoryName       │
│    txtEmail              │         │    txtDescription        │
│    txtDepartment         │         │    bitActive             │
│    bitActive             │         └──────────────────────────┘
└──────────────────────────┘

┌──────────────────────────┐         ┌──────────────────────────┐
│  M_TEST_TYPE             │         │  M_DOCUMENT_TYPE         │
├──────────────────────────┤         ├──────────────────────────┤
│ PK intTestTypeId         │         │ PK intDocTypeId          │
│    txtTestTypeName       │         │    txtDocTypeName        │
│    txtDescription        │         │    txtDescription        │
│    bitActive             │         │    bitActive             │
└──────────────────────────┘         └──────────────────────────┘

RELATIONSHIP SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• T_RM_SAMPLE_HEADER (1) ──→ (N) T_RM_SAMPLE_PURPOSE
• T_RM_SAMPLE_HEADER (1) ──→ (N) T_RM_SAMPLE_EVALUATION
• T_RM_SAMPLE_HEADER (1) ──→ (1) T_RM_SAMPLE_DISPOSITION
• T_RM_SAMPLE_HEADER (1) ──→ (N) T_RM_SAMPLE_ATTACHMENT
• M_TYPE_DOCUMENT (1) ──→ (N) T_RM_SAMPLE_HEADER
• M_SUPPLIER (1) ──→ (N) T_RM_SAMPLE_HEADER
• M_CURRENCY (1) ──→ (N) T_RM_SAMPLE_HEADER
• M_UOM (1) ──→ (N) T_RM_SAMPLE_HEADER
• M_PEGAWAI (1) ──→ (N) T_RM_SAMPLE_HEADER (as PIC)
• M_PEGAWAI (1) ──→ (N) T_RM_SAMPLE_EVALUATION (as Evaluator)
• M_PEGAWAI (1) ──→ (N) T_RM_SAMPLE_DISPOSITION (as Decision Maker/Approver)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        </pre>
        <p style="text-align: center; font-size: 10pt; color: #666; margin-top: 10px;">
            <em>Figure 2: Entity Relationship Diagram - New RM Sample Module</em>
        </p>
    </div>
"""


def main():
    fsd_path = Path(__file__).parent / "FSD_New_RM_Sample.html"
    
    print("Adding Business Flow, Flowchart, and ERD to FSD...")
    
    with open(fsd_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find insertion point (after 1.3 Definitions)
    insertion_marker = '<h3>1.3 Definitions and Acronyms</h3>'
    
    if insertion_marker in content:
        # Find the end of the definitions table
        table_end = content.find('</table>', content.find(insertion_marker))
        if table_end != -1:
            table_end += len('</table>')
            
            # Create new sections
            new_sections = create_business_flow_section() + create_flowchart_section() + create_erd_section()
            
            # Insert new sections
            content = content[:table_end] + new_sections + content[table_end:]
            
            # Write back
            with open(fsd_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("[SUCCESS] Added:")
            print("  ✓ Business Flow Summary")
            print("  ✓ Business Process Flowchart")
            print("  ✓ Entity Relationship Diagram (ERD)")
        else:
            print("[ERROR] Could not find table end")
    else:
        print("[ERROR] Could not find insertion point")


if __name__ == "__main__":
    main()
