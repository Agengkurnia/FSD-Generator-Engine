import os
from pathlib import Path
from playwright.sync_api import sync_playwright

# ---------------------------------------------------
# FLOWCHART LOGIC based on NewRMSampleDetail.html and
# NewRMSampleIndex.html analysis:
#
# WIZARD STEPS (filled by Requestor/User):
#   Step 1: Document Sample (supplier, material, halal, storage, docs)
#   Step 2: Sample Purpose (category, purpose type, apply to products)
#   Step 3: RM Evaluation (lab test params: organo, nutrition, micro, heavy metals, etc.)
#   Step 4: Disposition (recommendation, decision, approval routing)
#
# APPROVAL FLOW (from PDF Business Rules):
#   Decision = "Approved" + Approval Required = No => Status: APPROVED
#   Decision = "Approved" + Approval Required = Yes => Status: WAITING APPROVAL => PCD reviews
#   Decision = "Rejected" => Status: REJECTED => Requestor can re-submit
#   Decision = "On Hold" => Back to Step 3
#
#   PCD (when Waiting Approval):
#     Approve => Status: APPROVED
#     Reject => Status: REJECTED => Requestor can re-submit
#
# ACTORS:
#   Requestor (user) = handles all 4 wizard steps + decision in Step 4
#   PCD (approver)   = handles Waiting Approval reviews
#
# SWIMLANES: Top-down, Left-to-Right within each lane
# ---------------------------------------------------

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({ 
          startOnLoad: true, 
          theme: 'base',
          themeVariables: {
              fontFamily: 'Calibri, Arial, sans-serif',
              fontSize: '22px',
          },
          flowchart: {
              curve: 'linear',
              padding: 25,
              nodeSpacing: 40,
              rankSpacing: 50
          }
      });
      window.addEventListener('load', () => {
          setTimeout(() => document.getElementById('container').style.display = 'inline-block', 100);
      });
    </script>
    <style>
        body { background: white; margin: 30px; font-family: Calibri, 'Segoe UI', Arial; }
        #container { padding: 40px; background: white; display: none; }
        .cluster rect { fill: #f0f4ff !important; stroke: #7799cc !important; stroke-width: 1.5px !important; }
        .cluster span, .cluster-label text { font-size: 20px !important; font-weight: bold; fill: #1a3c8c !important; }
        .node rect { fill: #fff !important; stroke: #3366cc !important; stroke-width: 1.5px  !important; }
        .node text { font-size: 18px !important; fill: #111 !important; line-height: 1.3 !important; }
        .node.decision polygon { fill: #fffbe6 !important; stroke: #cc8800 !important; stroke-width: 1.5px !important; }
        .edgeLabel { background-color: rgba(255,255,255,0.9) !important; font-size: 16px !important; font-weight: 700 !important; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
flowchart LR
    %% Tentukan arah dari Kiri ke Kanan
    A(["Mulai"]) --> S1
    
    S1["Step 1: Document Sample<br/>───────────────<br/>• Input Data Sample<br/>• Material & UOM<br/>• Storage & Halal<br/>• Upload COA/MSDS"]

    S1 -->|Next| S2

    S2["Step 2: Sample Purpose<br/>───────────────<br/>• Category RM<br/>• Purpose Type<br/>• Objective<br/>• Product Mapping"]

    S2 -->|Next| S3

    S3["Step 3: Evaluation<br/>───────────────<br/>• Uji Lab & Teknis<br/>• Organoleptik, Mikro,<br/>  Logam Berat, dll<br/>• Input Hasil Analisis"]

    S3 -->|Next| S4

    S4["Step 4: Disposition<br/>───────────────<br/>• Review Score<br/>• Input Rekomendasi<br/>• Pilih Decision<br/>• Set Approver (Opsional)"]

    S4 --> DEC

    DEC{"Decision?"}
    
    %% Alur On Hold dan Rejected
    DEC -->|"On Hold"| ONHOLD["Kembali ke Step 3<br/>untuk evaluasi ulang"]
    ONHOLD --> S3
    DEC -->|"Rejected"| REJECTED(["X  STATUS: REJECTED<br/>(Requestor dpt Re-submit)"])
    REJECTED -->|"Re-submit"| S1

    %% Alur Approval
    DEC -->|"Approved +<br/>Approval Req."| WAIT["Waiting Approval<br/>───────────────<br/>PCD melakukan<br/>review data"]
    DEC -->|"Approved,<br/>tanpa Approval"| APPROVED(["✓  STATUS: APPROVED<br/>(Selesai)"])

    WAIT --> APPR_DEC{"Keputusan<br/>Approver?"}
    APPR_DEC -->|"Approve"| APPROVED
    APPR_DEC -->|"Reject"| REJECTED
    

    %% Styling 
    classDef req fill:#e8f4fd,stroke:#2196F3,stroke-width:1.5px,color:#111
    classDef pcd fill:#fff3e0,stroke:#FF9800,stroke-width:1.5px,color:#111
    classDef dec fill:#fffbe6,stroke:#F9A825,stroke-width:1.5px,color:#111
    classDef end_ok fill:#e8f5e9,stroke:#43A047,stroke-width:2px,color:#000,font-weight:bold
    classDef end_no fill:#ffebee,stroke:#e53935,stroke-width:2px,color:#000,font-weight:bold

    class S1,S2,S3,S4 req
    class WAIT pcd
    class DEC,APPR_DEC dec
    class APPROVED end_ok
    class REJECTED end_no
    class ONHOLD pcd
    
    %% Buat legenda/keterangan warna
    subgraph Legend ["Keterangan Aktor"]
        L1[Requestor / User]:::req
        L2[PCD / Approver]:::pcd
    end
    
    style Legend fill:#fafafa,stroke:#ccc,stroke-width:1px
        </div>
    </div>
</body>
</html>
"""

def main():
    base_dir = Path(__file__).parent
    html_file = base_dir / "temp_mermaid_hd.html"
    screenshot_dir = base_dir / "screenshots"
    screenshot_path = screenshot_dir / "new_rm_sample_flow_clear.png"
    
    html_file.write_text(HTML_CONTENT, encoding="utf-8")
    
    print("Launching Playwright for HD Screenshot (3x scale)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(device_scale_factor=3, viewport={'width': 2600, 'height': 1200})
        page = context.new_page()
        
        page.goto(f"file:///{html_file.as_posix()}")
        # Wait for the container to become visible (JS delay)
        page.wait_for_selector("#container", state='visible', timeout=15000)
        page.wait_for_timeout(3000)
        
        element = page.locator("#container")
        element.screenshot(path=str(screenshot_path))
        
        browser.close()
        
    print(f"Successfully saved {screenshot_path}")
    
    if html_file.exists():
        html_file.unlink()

if __name__ == "__main__":
    main()
