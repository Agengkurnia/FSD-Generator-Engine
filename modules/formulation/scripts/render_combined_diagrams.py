"""
render_combined_diagrams.py
============================
Render diagram Mermaid untuk FSD Combined via mermaid.ink
dengan cara memecah menjadi request yang lebih kecil.
"""
import base64, urllib.request, os, time

SCREENSHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
os.makedirs(SCREENSHOTS, exist_ok=True)

DIAGRAMS = {
    "flow_main": """
flowchart LR
    subgraph L1["LAYER 1"]
        PX["Premix"]
        DB["DryBlend"]
    end
    subgraph L2["LAYER 2"]
        LQ["Liquid"]
        BK["Baking"]
        DR["Drying"]
    end
    subgraph L3["LAYER 3"]
        PK["Packaging"]
    end
    Start([Start]) --> L1
    PX -->|"item code"| L2
    DB -->|"item code"| L2
    DR -.->|"cross-ref"| L1
    L2 -->|"Formula No"| L3
    L3 --> End([Done])
    style L1 fill:#FFF9C4,stroke:#F9A825
    style L2 fill:#E3F2FD,stroke:#1565C0
    style L3 fill:#E8F5E9,stroke:#2E7D32
""",
    "flow_layer1": """
flowchart TD
    A["Pilih Project No"] --> B["Isi Header Formula"]
    B --> C["Input Bahan Baku di Grid"]
    C --> D["BatchSize = sum DosageConv"]
    D --> E{Validasi?}
    E -->|Gagal| F["Tampilkan Error"]
    E -->|OK| G{Pilih Aksi}
    G -->|SAVE| H["Status DRAFT 10"]
    G -->|SUBMIT| I["Cek Item Code Oracle"]
    I -->|Belum Approved| J["Blokir Submit"]
    I -->|Semua OK| K["Kalkulasi + K2 Approval"]
    K --> L(["Item Code siap di Layer 2"])
""",
    "flow_layer2": """
flowchart TD
    A["Pilih Project No"] --> B["Input Header Formula"]
    B --> C["Input Grid Bahan Baku dari Layer 1"]
    C --> D{Tipe Formula?}
    D -->|Liquid| E["ServingSize g = mL x Density\nWater = Batch - Total"]
    D -->|Baking| F["Min 1 Main Ingredient\nInput Water Manual"]
    D -->|Drying| G["Dosage in FG pct\nBase Item Code\nTotal Solid pct"]
    E --> H{Validasi?}
    F --> H
    G --> H
    H -->|OK| I["SAVE atau SUBMIT K2"]
    I --> J(["Formula No Layer 2 siap"])
""",
    "flow_layer3": """
flowchart TD
    A["Pilih Project No"] --> B["Pilih Formula No dari Layer 2"]
    B --> C["Isi Header: Desc, BatchSize, Netto"]
    C --> D["Isi Grid Detail Kemasan"]
    D --> E["Isi Grid Parameter"]
    E --> F["calculateQty otomatis"]
    F --> G{Cek Duplikat?}
    G -->|Duplikat| H["Blokir Save"]
    G -->|OK| I{Pilih Aksi}
    I -->|DRAFT| J["Status 10"]
    I -->|SUBMIT| K["Status 20 + insertMApprove"]
    K --> L(["Packaging Selesai"])
""",
    "erd_cross_layer": """
erDiagram
    trProjectRegistration {
        int intProjectRegistrationID PK
        varchar txtProjectNo
    }
    trPremixHeader {
        int intPremixHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        varchar txtPremixItemCode
        decimal decProductBatchSize
    }
    trDryBlendHeader {
        int intDryBlendHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decProductBatchSize
    }
    trLiquidHeader {
        int intLiquidHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decDensity
        decimal decServingSize
    }
    trBakingHeader {
        int intBakingHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decWater
        decimal decTargetMaxMoisture
    }
    trDryingHeader {
        int intDryingHeaderId PK
        int intProjectRegistrationID FK
        varchar txtFormulaNo
        decimal decDosageinFG
        decimal decTotalSolid
    }
    trPackagingHeader {
        int intPHeaderId PK
        varchar txtFormulaNo
        varchar txtRMFormulaNo
        decimal decBatchSize
        decimal decNetto
    }
    trProjectRegistration ||--o{ trPremixHeader : "has Premix"
    trProjectRegistration ||--o{ trDryBlendHeader : "has DryBlend"
    trProjectRegistration ||--o{ trLiquidHeader : "has Liquid"
    trProjectRegistration ||--o{ trBakingHeader : "has Baking"
    trProjectRegistration ||--o{ trDryingHeader : "has Drying"
    trLiquidHeader ||--o| trPackagingHeader : "ref via RMFormulaNo"
    trBakingHeader ||--o| trPackagingHeader : "ref via RMFormulaNo"
    trDryingHeader ||--o| trPackagingHeader : "ref via RMFormulaNo"
"""
}

def render(code, name):
    encoded = base64.urlsafe_b64encode(code.strip().encode('utf-8')).decode('ascii')
    url = f'https://mermaid.ink/img/{encoded}?type=png&scale=2'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    out = os.path.join(SCREENSHOTS, f'{name}.png')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(out, 'wb') as f:
            f.write(data)
        print(f'  [OK] {name}.png ({len(data):,} bytes)')
        return out
    except Exception as e:
        print(f'  [FAIL] {name}: {e}')
        return None

print("Rendering diagrams...")
for name, code in DIAGRAMS.items():
    render(code, name)
    time.sleep(1)  # avoid rate limit
print("Done.")
