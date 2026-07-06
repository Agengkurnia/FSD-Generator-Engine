"""
Render ERD to PNG - simplified version with correct pako encoding
"""
import urllib.request
import base64
import json
import os
import zlib

OUTPUT_DIR = r"d:\Work\Source\RMSelection Hijrah\NewRMSelection\Document\FSD\Screenshots"

# Simplified ERD with relationships only (columns in separate table spec)
ERD_SIMPLE = """erDiagram
    trRMSample_Header ||--|| trDocumentSample_Header : "step1"
    trRMSample_Header ||--|| trSamplePurpose_Header : "step2"
    trRMSample_Header ||--|| trRMEvaluation_Header : "step3"
    trRMSample_Header ||--|| trRMDisposition_Header : "step4"
    trDocumentSample_Header ||--o{ trDocumentSample_Allergen : "contains"
    trDocumentSample_Header ||--o{ trDocumentSample_BTP : "contains"
    trDocumentSample_Header ||--o{ trDocumentSample_Document : "contains"
    trSamplePurpose_Header ||--o{ trSamplePurpose_Product : "applies_to"
    trRMEvaluation_Header ||--o{ trRMEvaluation_Detail : "evaluates"
    trRMEvaluation_Header ||--o{ trRMEvaluation_FoodCategory : "categorizes"
    trRMSample_Header {
        INT intId PK
        VARCHAR txtSampleNo UK
        INT intStatusId
        INT intCurrentStep
    }
    trDocumentSample_Header {
        INT intId PK
        INT intSampleHeaderId FK
        VARCHAR txtMaterialName
        VARCHAR txtSupplierName
    }
    trDocumentSample_Allergen {
        INT intId PK
        INT intDocSampleHeaderId FK
        VARCHAR txtAllergenName
    }
    trDocumentSample_BTP {
        INT intId PK
        INT intDocSampleHeaderId FK
        VARCHAR txtBTPName
    }
    trDocumentSample_Document {
        INT intId PK
        INT intDocSampleHeaderId FK
        VARCHAR txtDocumentType
        VARCHAR txtFileName
    }
    trSamplePurpose_Header {
        INT intId PK
        INT intSampleHeaderId FK
        VARCHAR txtSamplePurposeType
        VARCHAR txtObjective
    }
    trSamplePurpose_Product {
        INT intId PK
        INT intSampleHeaderId FK
        INT intGroupProductTypeId FK
    }
    trRMEvaluation_Header {
        INT intId PK
        INT intSampleHeaderId FK
        DECIMAL decOverallScore
    }
    trRMEvaluation_Detail {
        INT intId PK
        INT intSampleHeaderId FK
        VARCHAR txtTestCode
        VARCHAR txtTestClass
    }
    trRMEvaluation_FoodCategory {
        INT intId PK
        INT intSampleHeaderId FK
        VARCHAR txtCategoryName
    }
    trRMDisposition_Header {
        INT intId PK
        INT intSampleHeaderId FK
        VARCHAR txtDecision
        BIT bitApprovalRequired
    }
"""


def mermaid_ink_pako(mermaid_code, output_path):
    """Use correct pako/deflate encoding for mermaid.ink"""
    
    # The mermaid.ink pako format expects raw deflate (wbits=-15)
    compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)[2:-4]  # strip zlib header/footer
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    url = f"https://mermaid.ink/img/pako:{encoded}?type=png&bgColor=white"
    
    print(f"  URL length: {len(url)} chars")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            png_data = response.read()
        with open(output_path, 'wb') as f:
            f.write(png_data)
        file_size = os.path.getsize(output_path) / 1024
        print(f"  [OK] Saved: {output_path} ({file_size:.0f} KB)")
        return True
    except Exception as e:
        print(f"  [ERROR] pako: {e}")
        return False


def mermaid_ink_b64(mermaid_code, output_path):
    """Use base64 encoding for mermaid.ink"""
    encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('ascii')
    url = f"https://mermaid.ink/img/{encoded}?type=png&bgColor=white"
    
    print(f"  URL length: {len(url)} chars")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            png_data = response.read()
        with open(output_path, 'wb') as f:
            f.write(png_data)
        file_size = os.path.getsize(output_path) / 1024
        print(f"  [OK] Saved: {output_path} ({file_size:.0f} KB)")
        return True
    except Exception as e:
        print(f"  [ERROR] b64: {e}")
        return False


def main():
    print("Rendering ERD (simplified)...")
    
    erd_path = os.path.join(OUTPUT_DIR, "FSD_ERD_Database.png")
    
    # Try pako first
    if not mermaid_ink_pako(ERD_SIMPLE, erd_path):
        print("  Trying base64 fallback...")
        if not mermaid_ink_b64(ERD_SIMPLE, erd_path):
            print("  Both methods failed!")
            return
    
    print("\n[OK] Done!")


if __name__ == "__main__":
    main()
