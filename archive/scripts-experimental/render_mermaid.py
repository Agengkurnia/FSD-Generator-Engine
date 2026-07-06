"""
render_mermaid.py
Render the SEAL flow diagram (Mermaid) → PNG via mermaid.ink API.
Output: screenshots/seal_flow_diagram.png
"""

import base64
import os
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH   = os.path.join(SCRIPT_DIR, "screenshots", "seal_flow_diagram.png")

MERMAID_CODE = """
flowchart TD
    A(["🚀 Buat SEAL Baru"]) --> B["Input Data SEAL Identity (Product Group, Supplier, Item Code, PIC)"]
    B --> C["Document Upload: PIC upload file per jenis dokumen sesuai PM Category"]
    C --> D{{Submit?}}
    D -->|Ya| E["Status: WAIT_APPROVAL"]
    E --> F{{"Semua Reviewer Approve? (AND Logic)"}}
    F -->|"Semua Approve"| G["Status: APPROVED"]
    G --> K(["🏁 Status: COMPLETED"])
    F -->|"Salah satu Revise"| I["Status: REVISE"]
    I -->|"Notifikasi ke Uploader - Upload Ulang"| C

    style A fill:#4CAF50,color:#fff
    style K fill:#1565C0,color:#fff
    style G fill:#4CAF50,color:#fff
    style I fill:#F44336,color:#fff
    style E fill:#FF9800,color:#fff
    style F fill:#FF9800,color:#fff
"""

def render():
    encoded = base64.urlsafe_b64encode(MERMAID_CODE.encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/img/{encoded}?type=png"
    print(f"Fetching: {url[:80]}...")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()

    with open(OUT_PATH, "wb") as f:
        f.write(data)

    print(f"Saved PNG ({len(data):,} bytes) → {OUT_PATH}")

if __name__ == "__main__":
    render()
