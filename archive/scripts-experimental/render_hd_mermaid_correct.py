import os
from pathlib import Path
from playwright.sync_api import sync_playwright

# Correct Mermaid diagram based on real RM Sample workflow:
# Actors: RA (Requestor), PCD (Approver), System
# Steps: 1(Doc Sample) -> 2(Purpose) -> 3(Evaluation) -> 4(Disposition) -> Submit -> PCD Review -> End
# On Hold: PCD sends back to RA to revise Step 3
# Rejected: Sample rejected by PCD or RA elects to Reject in Step 4

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
              fontFamily: 'Calibri, Segoe UI, Arial, sans-serif',
              fontSize: '14px',
              primaryColor: '#dce5ff',
              primaryBorderColor: '#4466cc',
              lineColor: '#555'
          },
          flowchart: {
              curve: 'linear',
              padding: 20,
              nodeSpacing: 50,
              rankSpacing: 70
          }
      });
    </script>
    <style>
        body { background: white; margin: 30px; font-family: Calibri, 'Segoe UI', Arial; }
        #container { padding: 20px; background: white; display: inline-block; }

        /* Swimlane bands */
        .cluster rect { fill: #f7f9ff !important; stroke: #8899cc !important; stroke-width: 1.5px !important; rx: 5 !important; }
        .cluster span, .cluster-label text { font-size: 15px !important; font-weight: bold; fill: #223399 !important; }

        /* Process boxes */
        .node rect { fill: #ffffff !important; stroke: #3366cc !important; stroke-width: 1.5px !important; }
        .node text { font-size: 13px !important; fill: #222 !important; }

        /* Decision diamond */
        .node.decision polygon { fill: #fff8e6 !important; stroke: #cc8800 !important; stroke-width: 1.5px !important; }
        
        /* Edge labels */
        .edgeLabel { background-color: rgba(255,255,255,0.85) !important; font-size: 11px !important; font-weight: 600 !important; padding: 2px 5px; border-radius: 4px; }
        
        /* Start/End terminal */
        .node .label { color: #333; }
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
flowchart LR
    subgraph RA_LANE["RA (Regulatory Affairs)"]
        direction LR
        START(["Start"])
        S1["Step 1<br/>Document Sample<br/>-----<br/>• Input data supplier<br/>• Input material details<br/>• Upload dokumen COA<br/>• Generate Sample No"]
        S2["Step 2<br/>Sample Purpose<br/>-----<br/>• Pilih kategori RM<br/>• Pilih purpose type<br/>• Input objective<br/>• Mapping produk"]
        S3["Step 3<br/>RM Evaluation<br/>-----<br/>• Input parameter uji<br/>• Input COA Result<br/>• Input Analysis Result<br/>• Conform / Not Conform"]
        S4["Step 4<br/>Disposition<br/>-----<br/>• Review overall score<br/>• Input rekomendasi<br/>• Pilih Decision<br/>• Submit"]
        SUBMIT(["Submit"])
    end

    subgraph PCD_LANE["PCD (Approver)"]
        direction LR
        REVIEW["Review<br/>Submission"]
        DEC_PCD{"Keputusan<br/>PCD?"}
        APPROVED(["STATUS:<br/>APPROVED"])
        REJECTED(["STATUS:<br/>REJECTED"])
        ONHOLD["On Hold:<br/>Kembalikan ke<br/>Step 3"]
    end

    START --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> SUBMIT

    SUBMIT --> REVIEW
    REVIEW --> DEC_PCD

    DEC_PCD -->|"Approve"| APPROVED
    DEC_PCD -->|"Reject"| REJECTED
    DEC_PCD -->|"On Hold"| ONHOLD

    ONHOLD -->|"RA revisi<br/>evaluasi"| S3

    style START fill:#6aa84f,color:#fff,stroke:#4a7c30,stroke-width:2px
    style SUBMIT fill:#e6f0ff,stroke:#3366cc,stroke-width:2px,color:#000
    style APPROVED fill:#b6d7a8,stroke:#38761d,stroke-width:2px,color:#000,font-weight:bold
    style REJECTED fill:#f4cccc,stroke:#cc0000,stroke-width:2px,color:#000,font-weight:bold
    style ONHOLD fill:#fff2cc,stroke:#f6b26b,stroke-width:2px,color:#000
    style DEC_PCD fill:#fff2cc,stroke:#f6b26b,stroke-width:2px
    style REVIEW fill:#e8eaf6,stroke:#5c6bc0,stroke-width:2px,color:#000
    style S1 fill:#e8f4fd,stroke:#3366cc,stroke-width:1.5px
    style S2 fill:#e8f4fd,stroke:#3366cc,stroke-width:1.5px
    style S3 fill:#e8f4fd,stroke:#3366cc,stroke-width:1.5px
    style S4 fill:#e8f4fd,stroke:#3366cc,stroke-width:1.5px
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
        context = browser.new_context(device_scale_factor=3, viewport={'width': 2400, 'height': 1200})
        page = context.new_page()
        
        page.goto(f"file:///{html_file.as_posix()}")
        page.wait_for_selector("svg")
        page.wait_for_timeout(3000)
        
        element = page.locator("#container")
        element.screenshot(path=str(screenshot_path))
        
        browser.close()
        
    print(f"Successfully saved {screenshot_path}")
    
    if html_file.exists():
        html_file.unlink()

if __name__ == "__main__":
    main()
