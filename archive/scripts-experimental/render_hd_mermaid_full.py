import os
from pathlib import Path
from playwright.sync_api import sync_playwright

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
              fontFamily: 'Segoe UI, Arial, sans-serif',
              fontSize: '14px',
          },
          flowchart: {
              curve: 'basis',
              padding: 15
          }
      });
    </script>
    <style>
        body { background: white; margin: 40px; font-family: 'Segoe UI', Tahoma, Verdana, sans-serif; }
        #container { padding: 40px; background: white; display: inline-block; }
        
        .cluster rect { fill: #fcfcfcf0 !important; stroke: #cfcfcf !important; stroke-width: 2px !important; }
        .cluster-label text { font-size: 16px !important; font-weight: bold; fill: #444 !important; }
        
        .node rect { fill: #ffffff !important; stroke: #1e88e5 !important; stroke-width: 2px !important; rx: 6px !important; ry: 6px !important; }
        .node text { font-size: 13px; color: #222 !important; }
        .node.decision polygon { fill: #fff3e0 !important; stroke: #fb8c00 !important; stroke-width: 2px !important; }
        .edgeLabel { background-color: white !important; font-weight: 600; font-size: 11px; color: #555; padding: 2px 6px; border-radius: 4px; }
        
        .node .label { color: #333; }
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
flowchart TD
    subgraph RA ["RA (Regulatory Affairs)"]
        direction LR
        Start((Start)) --> S1["STEP 1: DOCUMENT<br/>Sample Reception<br/>• Receive sample<br/>• Document details<br/>• Upload COA, MSDS<br/>• Gen Sample No"]
        S1 --> S2["STEP 2: PURPOSE<br/>Sample Analysis<br/>• Define purpose<br/>• Map target products<br/>• Expected benefits<br/>• Analysis deadline"]
    end
    
    subgraph EVAL ["Evaluator (R&D / QA)"]
        direction LR
        S3["STEP 3: EVALUATION<br/>Technical Testing<br/>• Lab testing<br/>• Trial production<br/>• Quality scoring<br/>• Compliance check"]
        S4["STEP 4: DISPOSITION<br/>Final Decision<br/>• Review all steps"]
        Dec1{"Decision?"}
        OnHold["Wait for<br/>Additional Info"]
    end
    
    subgraph MGR ["Approver (Manager)"]
        direction LR
        Chk{"Approval<br/>Required?"}
        PendApp["Pending<br/>Approval"]
        AppRev["Approver<br/>Review"]
        Dec2{"Approval<br/>Decision?"}
    end
    
    subgraph SYS ["System / Database"]
        direction LR
        EndRej(["END<br/>REJECTED"])
        EndCan(["END<br/>CANCELLED"])
        EndApp(["END<br/>APPROVED"])
    end
    
    S2 --> S3
    S3 --> S4
    
    S4 --> Dec1
    Dec1 -- "ON HOLD" --> OnHold
    OnHold -- "Back to" --> S3
    
    Dec1 -- "APPROVED" --> Chk
    Dec1 -- "REJECTED" --> EndRej
    Dec1 -- "CANCEL" --> EndCan
    
    Chk -- "YES" --> PendApp
    Chk -- "NO" --> EndApp
    
    PendApp --> AppRev
    AppRev --> Dec2
    
    Dec2 -- "APPROVE" --> EndApp
    Dec2 -- "REJECT" --> BackS4["Back to<br/>Step 4"]
    BackS4 --> S4
    
    
    classDef startend fill:#f5f5f5,stroke:#333,stroke-width:2px,color:#000
    classDef process fill:#fff,stroke:#1e88e5,stroke-width:2px,color:#000
    classDef decision fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#000
    
    class Start startend
    class S1,S2,S3,S4,AppRev process
    class Dec1,Chk,Dec2 decision
    class OnHold fill:#E7F3FF,stroke:#0D6EFD,stroke-width:2px
    class PendApp fill:#FFF9C4,stroke:#F57F17,stroke-width:2px
    class EndRej,EndCan fill:#FFCDD2,stroke:#D32F2F,stroke-width:2px
    class EndApp fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    class BackS4 fill:#FFE0B2,stroke:#FF6F00,stroke-width:2px
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
    
    print("Launching Playwright for HD Screenshot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 3x device scale factor for HD crispness
        context = browser.new_context(device_scale_factor=3, viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        page.goto(f"file:///{html_file.as_posix()}")
        
        # Wait for SVG rendering
        page.wait_for_selector("svg")
        page.wait_for_timeout(2500)
        
        element = page.locator("#container")
        element.screenshot(path=str(screenshot_path))
        
        browser.close()
        
    print(f"Successfully saved {screenshot_path}")
    
    if html_file.exists():
        html_file.unlink()

if __name__ == "__main__":
    main()
