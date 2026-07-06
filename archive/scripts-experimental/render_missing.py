import base64, urllib.request, time, os

SCREENSHOTS_DIR = r"C:\Users\Lenovo\.gemini\antigravity\brain\2e88ab95-8a65-4966-82f2-b215afb1f06f\screenshots"

def render(code, name):
    encoded = base64.urlsafe_b64encode(code.encode('utf-8')).decode('utf-8')
    url = f"https://mermaid.ink/img/{encoded}?bgColor=white&width=900"
    print(f"Rendering {name} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        path = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
        with open(path, 'wb') as f:
            f.write(data)
        print(f"  OK: {path} ({len(data)//1024} KB)")
    except Exception as e:
        print(f"  FAIL: {e}")

# Diagram 3: flowchart with subgraphs (was 503 - retry)
diag3 = """flowchart TD
    Start(["Mulai"]) --> S1

    subgraph S1 ["STEP 1 - Document"]
        direction TB
        A1["Input Data Sample & LOV Fields"] --> A2["Upload Dokumen COA / Spec / Halal Cert"] --> A3["Allergen & BTP Checklist"]
    end

    subgraph S2 ["STEP 2 - Purpose"]
        direction TB
        B1["Pilih RM Category"] --> B2["Tentukan Tujuan Sample"] --> B3["Map Item Code & Apply To Product"]
    end

    subgraph S3 ["STEP 3 - Evaluation"]
        direction TB
        C1["Input Parameter Uji Organo / Nutrisi / Mikro / dll"] --> C2["Input Hasil COA & Analysis Result"]
    end

    subgraph S4 ["STEP 4 - Disposition"]
        direction TB
        D1["Review Data & Overall Score"] --> D2{{"Keputusan"}}
        D2 -->|"Approve"| D3["Submit ke Approver"]
        D2 -->|"Reject"| D4["Input Alasan Penolakan"]
        D2 -->|"On Hold"| D5["Kembali ke Step 3"]
    end

    S1 -->|"Next"| S2
    S2 -->|"Next"| S3
    S3 -->|"Next"| S4
    D3 --> Approve(["Status: Approved"])
    D4 --> Reject(["Status: Rejected"])
    D5 --> S3

    style S1 fill:#fff9e6,stroke:#f0ad4e
    style S2 fill:#e8f4ff,stroke:#3d8bcd
    style S3 fill:#fff0f0,stroke:#dc3545
    style S4 fill:#e8f9f9,stroke:#0dcaf0
    style Approve fill:#d4edda,stroke:#28a745
    style Reject fill:#f8d7da,stroke:#dc3545"""

# Diagram 4: stateDiagram - simplified without aliases
diag4 = """stateDiagram-v2
    [*] --> Draft : User creates new sample

    Draft --> WaitingApproval : Submit for Approval
    Draft --> Draft : Save Draft

    WaitingApproval --> Approved : Approver menyetujui
    WaitingApproval --> Rejected : Approver menolak
    WaitingApproval --> OnHold : Approver tunda

    Rejected --> Draft : User revise and re-submit
    OnHold --> Step3Eval : Return for re-evaluation
    Step3Eval --> WaitingApproval : Re-submit after evaluation

    Approved --> [*] : Process Complete
    Rejected --> [*] : Process Ended"""

render(diag3, "FSD_Diagram_03")
time.sleep(2)
render(diag4, "FSD_Diagram_04")
