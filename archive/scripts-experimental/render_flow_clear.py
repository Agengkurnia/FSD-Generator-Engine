import urllib.request
import base64
import os

OUTPUT_DIR = r"d:\Work\Source\RMSelection Hijrah\NewRMSelection\Document\FSD\screenshots"

FLOWCHART = """flowchart LR
    S1[Step 1: Doc Reception] --> S2[Step 2: Purpose Analysis]
    S2 --> S3[Step 3: Eval Testing]
    S3 --> S4[Step 4: Disposition]
    
    S4 --> Dec{Decision?}
    Dec -->|Approve| PendApp[Pending Approval]
    Dec -->|Reject| EndRej([END: Rejected])
    Dec -->|On Hold| S3
    
    PendApp -->|Manager Approves| EndApp([END: Approved])
    PendApp -->|Manager Rejects| BackS4[Back to Step 4]
    BackS4 --> S4
    
    style S1 fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    style S2 fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    style S3 fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    style S4 fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    style Dec fill:#fff3e0,stroke:#fb8c00,stroke-width:2px
    style EndApp fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,font-weight:bold
    style EndRej fill:#ffebee,stroke:#e53935,stroke-width:2px,font-weight:bold
    style PendApp fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style BackS4 fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
"""

def mermaid_ink_b64(mermaid_code, output_path):
    encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('ascii')
    url = f"https://mermaid.ink/img/{encoded}?type=png&bgColor=white"
    print(f"URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f"Saved: {output_path}")

try:
    path = os.path.join(OUTPUT_DIR, "new_rm_sample_flow_clear.png")
    mermaid_ink_b64(FLOWCHART, path)
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
