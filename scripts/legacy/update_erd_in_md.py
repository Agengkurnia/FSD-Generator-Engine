"""
update_erd_in_md.py – Ganti section ERD di FSD_New_RM_Sample_v3.0.md dengan ERD lengkap.
Run: py update_erd_in_md.py
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SCRIPT_DIR, 'FSD_New_RM_Sample_v3.0.md')

NEW_ERD_SECTION = """### 5.2 Entity Relationship Diagram (ERD)

#### 5.2.1 ERD – Transaksi Workflow (11 Tabel)

Diagram berikut menampilkan seluruh relasi tabel transaksi yang digunakan dalam 4 tahap workflow New RM Sample:

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
        varchar txtUpdatedBy
        datetime dtmUpdatedDate
        bit bitActive
    }
    trDocumentSample_Header {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        date dtSampleDate
        date dtDateReceipt
        int intTypeDocumentId FK
        varchar txtMaterialName
        varchar txtPrincipalName
        int intSupplierId FK
        varchar txtSupplierName
        int intStorageId FK
        varchar txtHalalCategoryCode FK
        int intHalalBodyId FK
        varchar txtGMOStatus
        bit bitContainPHO
        varchar txtStatusOrganik
        varchar txtEgDegContent
        int intShelfLifeMonth
        varchar txtPackaging
        varchar txtCurrencyCode
        varchar txtUOMCode
        decimal decPricePerUOM
        decimal decNetWeight
        int intPegawaiId FK
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trDocumentSample_Allergen {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        int intDocSampleHeaderId FK
        varchar txtAllergenCode
        varchar txtAllergenName
        bit bitIsChecked
        varchar txtCreatedBy
        datetime dtmCreatedDate
    }
    trDocumentSample_BTP {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        int intDocSampleHeaderId FK
        int intLineNo
        varchar txtBTPName
        varchar txtFunctionName
        decimal decPercentagePPM
        varchar txtCreatedBy
        datetime dtmCreatedDate
    }
    trDocumentSample_Document {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        varchar txtDocumentType
        varchar txtFileName
        varchar txtFilePath
        varchar txtFileExtension
        int intFileSize
        date dtExpiredDate
        varchar txtRemarks
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trSamplePurpose_Header {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        int intRMCategoryId FK
        varchar txtRMCategoryCode
        varchar txtRMCategoryName
        int intSamplePurposeTypeId FK
        varchar txtSamplePurposeType
        varchar txtItemCodeTrial
        varchar txtItemDescTrial
        varchar txtItemCodeExisting
        varchar txtObjective
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trSamplePurpose_Product {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        int intSamplePurposeHeaderId FK
        int intLineNo
        int intGroupProductTypeId FK
        varchar txtGroupProductTypeName
        int intGroupProductTypeDetailId FK
        int intChildProductTypeId FK
        varchar txtChildProductTypeName
        int intChildProductTypeDetailId FK
        int intVariantId FK
        varchar txtVariantName
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trRMEvaluation_Header {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        decimal decOverallScore
        varchar txtEvaluationStatus
        varchar txtEvaluationNotes
        varchar txtMaterialComposition
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trRMEvaluation_Detail {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        int intEvaluationHeaderId FK
        int intLineNo
        varchar txtTestCode
        varchar txtTestClass
        varchar txtTestName
        varchar txtTestUnit
        varchar txtRegulationNo
        decimal decRegulationMin
        decimal decRegulationMax
        decimal decSpecSupplierMin
        decimal decSpecSupplierMax
        decimal decSpecSupplierTarget
        varchar txtCOAResult
        varchar txtAnalysisResult
        decimal decSpecSHPMin
        decimal decSpecSHPMax
        decimal decTarget
        varchar txtCreatedBy
        datetime dtmCreatedDate
        bit bitActive
    }
    trRMEvaluation_FoodCategory {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        int intEvaluationHeaderId FK
        int intCategoryId FK
        varchar txtCategoryCode
        varchar txtCategoryName
        varchar txtRegulationRef
    }
    trRMDisposition_Header {
        int intId PK
        varchar txtId UK
        int intSampleHeaderId FK
        varchar txtRecommendation
        varchar txtDecision
        varchar txtDecisionReason
        datetime dtDecisionDate
        bit bitApprovalRequired
        int intApproverId FK
        varchar txtApproverName
        varchar txtApprovalStatus
        datetime dtApprovalDate
        varchar txtApprovalNotes
        varchar txtCreatedBy
        datetime dtmCreatedDate
        varchar txtUpdatedBy
        datetime dtmUpdatedDate
        bit bitActive
    }

    trRMSample_Header ||--o| trDocumentSample_Header : "memiliki Step1"
    trRMSample_Header ||--o{ trDocumentSample_Allergen : "memiliki Allergen"
    trRMSample_Header ||--o{ trDocumentSample_BTP : "memiliki BTP"
    trRMSample_Header ||--o{ trDocumentSample_Document : "memiliki Dokumen"
    trRMSample_Header ||--o| trSamplePurpose_Header : "memiliki Step2"
    trSamplePurpose_Header ||--o{ trSamplePurpose_Product : "memiliki Produk"
    trRMSample_Header ||--o| trRMEvaluation_Header : "memiliki Step3"
    trRMEvaluation_Header ||--o{ trRMEvaluation_Detail : "memiliki Parameter"
    trRMEvaluation_Header ||--o{ trRMEvaluation_FoodCategory : "memiliki FoodCategory"
    trRMSample_Header ||--o| trRMDisposition_Header : "memiliki Step4"
    trDocumentSample_Header ||--o{ trDocumentSample_Allergen : "parent of"
    trDocumentSample_Header ||--o{ trDocumentSample_BTP : "parent of"
```

#### 5.2.2 ERD – Relasi ke Tabel Master

Diagram berikut menunjukkan ketergantungan tabel transaksi terhadap tabel-tabel master yang digunakan untuk LOV / referensi data:

```mermaid
erDiagram
    mSupplier {
        int intId PK
        varchar txtSupplierId UK
        varchar txtSupplierName
        varchar txtCountryCode
        bit bitActive
    }
    mHalalCategory {
        int intId PK
        varchar txtHalalCategoryCode UK
        varchar txtHalalCategoryName
        bit bitActive
    }
    mHalalBody {
        int intId PK
        varchar txtHalalBodyInstitution
        varchar txtCountry
        bit bitActive
    }
    mAppParam {
        int intId PK
        varchar txtAppParamVariable
        varchar txtAppParamCode
        varchar txtAppParamValue
        varchar txtAppParamDesc
        bit bitActive
    }
    mPegawai {
        int intId PK
        varchar txtPegawaiCode UK
        varchar txtPegawaiName
        int intDepartmentId
        varchar txtRole
        bit bitActive
    }
    mGroupProductType {
        int intId PK
        varchar txtGroupProductTypeName
        bit bitActive
    }
    mGroupProductTypeDetail {
        int intId PK
        int intGroupProductTypeId FK
        varchar txtProductBrand
        varchar txtProductCategory
        bit bitActive
    }
    mChildProductType {
        int intId PK
        int intGroupProductTypeId FK
        varchar txtChildProductTypeName
        bit bitActive
    }
    mChildProductTypeDetail {
        int intId PK
        int intChildProductTypeId FK
        varchar txtProductName
        bit bitActive
    }
    mVarian {
        int intId PK
        int intChildProductTypeId FK
        varchar txtVarianName
        bit bitActive
    }
    trDocumentSample_Header {
        int intSupplierId FK
        int intHalalBodyId FK
        varchar txtHalalCategoryCode FK
        int intStorageId FK
        int intPegawaiId FK
    }
    trSamplePurpose_Product {
        int intGroupProductTypeId FK
        int intGroupProductTypeDetailId FK
        int intChildProductTypeId FK
        int intChildProductTypeDetailId FK
        int intVariantId FK
    }
    trRMDisposition_Header {
        int intApproverId FK
    }

    trDocumentSample_Header }o--|| mSupplier : "FK Supplier"
    trDocumentSample_Header }o--|| mHalalCategory : "FK HalalCat"
    trDocumentSample_Header }o--|| mHalalBody : "FK HalalBody"
    trDocumentSample_Header }o--|| mPegawai : "FK PIC"
    trDocumentSample_Header }o--|| mAppParam : "FK Storage Condition"
    trRMDisposition_Header }o--|| mPegawai : "FK Approver"
    trSamplePurpose_Product }o--|| mGroupProductType : "FK Group"
    trSamplePurpose_Product }o--|| mGroupProductTypeDetail : "FK GroupDetail"
    trSamplePurpose_Product }o--|| mChildProductType : "FK Child"
    trSamplePurpose_Product }o--|| mChildProductTypeDetail : "FK ChildDetail"
    trSamplePurpose_Product }o--|| mVarian : "FK Varian"
    mGroupProductType ||--o{ mGroupProductTypeDetail : "has Detail"
    mGroupProductType ||--o{ mChildProductType : "has Child"
    mChildProductType ||--o{ mChildProductTypeDetail : "has Detail"
    mChildProductType ||--o{ mVarian : "has Varian"
```

"""

START_MARKER = '### 5.2 Entity Relationship Diagram (ERD)'
END_MARKER   = '### 5.3 Tabel Transaksi'

with open(SRC, encoding='utf-8') as f:
    content = f.read()

si = content.find(START_MARKER)
ei = content.find(END_MARKER)

if si < 0 or ei < 0:
    print('ERROR: marker tidak ditemukan')
else:
    updated = content[:si] + NEW_ERD_SECTION + '\n' + content[ei:]
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(updated)
    print(f'OK: ERD section diperbarui ({ei - si} chars diganti {len(NEW_ERD_SECTION)} chars)')
    print(f'File disimpan: {SRC}')
