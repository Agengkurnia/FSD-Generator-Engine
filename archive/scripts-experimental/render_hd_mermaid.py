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
              fontSize: '16px',
              primaryColor: '#e3f2fd',
              primaryBorderColor: '#1e88e5',
              tertiaryColor: '#f8f9fa'
          },
          flowchart: {
              curve: 'basis',
              padding: 20
          }
      });
    </script>
    <style>
        body { background: white; margin: 40px; font-family: 'Segoe UI', Tahoma, Verdana, sans-serif; }
        #container { padding: 40px; background: white; display: inline-block; }
        
        /* Swimlane adjustments */
        .cluster rect { fill: #fcfcfcf0 !important; stroke: #cfcfcf !important; stroke-width: 2px !important; }
        .cluster-label text { font-size: 18px !important; font-weight: bold; fill: #444 !important; }
        
        .node rect { fill: #ffffff !important; stroke: #1e88e5 !important; stroke-width: 2px !important; rx: 6px !important; ry: 6px !important; }
        .node text { font-size: 14px; color: #222 !important; }
        .node.decision polygon { fill: #fff3e0 !important; stroke: #fb8c00 !important; stroke-width: 2px !important; }
        .edgeLabel { background-color: white !important; font-weight: 600; font-size: 12px; color: #555; padding: 2px 6px; border-radius: 4px; }
        
        .node .label { color: #333; }
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
flowchart TD
    subgraph RA ["RA (Regulatory Affairs)"]
        direction LR
        Start((Start)) --> S1["Step 1: Document Sample<br/>(Input Supplier & Material)"]
        S1 --> S2["Step 2: Sample Purpose<br/>(Define Objective & Mapping)"]
        Revise(("Revise<br/>Data"))
    end
    
    subgraph EVAL ["Evaluator (R&D / QA)"]
        direction LR
        S3["Step 3: RM Evaluation<br/>(Lab Testing & COA)"]
        S4["Step 4: Disposition<br/>(Recommendation)"]
        Dec1{"Analyst<br/>Decision?"}
    end
    
    subgraph MGR ["Approver (Manager)"]
        direction LR
        Chk{"Approval<br/>Required?"}
        AppForm["Wait for Approval<br/>(Review Data)"]
        Dec2{"Manager<br/>Decision?"}
    end
    
    subgraph SYS ["System / Database"]
        direction LR
        EndApp(["Status: Approved"])
        EndRej(["Status: Rejected"])
    end
    
    S2 --> S3
    S3 --> S4
    S4 --> Dec1
    
    Dec1 -- "On Hold" --> Revise
    Revise --> S3
    
    Dec1 -- "Approve" --> Chk
    Dec1 -- "Reject" --> EndRej
    
    Chk -- "No" --> EndApp
    Chk -- "Yes" --> AppForm
    
    AppForm --> Dec2
    Dec2 -- "Approve" --> EndApp
    Dec2 -- "Reject" --> EndRej
    
    classDef startend fill:#f5f5f5,stroke:#333,stroke-width:2px,color:#000
    classDef process fill:#fff,stroke:#1e88e5,stroke-width:2px,color:#000
    classDef decision fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#000
    
    class Start,EndApp,EndRej startend
    class S1,S2,S3,S4,AppForm process
    class Dec1,Chk,Dec2 decision
    class Revise fill:#ffebee,stroke:#e53935,stroke-width:2px
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
