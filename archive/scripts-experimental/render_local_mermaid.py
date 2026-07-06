import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({ startOnLoad: true, theme: 'default' });
    </script>
    <style>
        body { background: white; margin: 20px; display: inline-block; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #container { padding: 20px; background: white; display: inline-block; }
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
flowchart LR
    S1["Step 1:<br/>Doc Reception"] --> S2["Step 2:<br/>Purpose Analysis"]
    S2 --> S3["Step 3:<br/>Eval Testing"]
    S3 --> S4["Step 4:<br/>Disposition"]
    
    S4 --> Dec{"Decision?"}
    Dec -->|"Approve"| PendApp["Pending<br/>Approval"]
    Dec -->|"Reject"| EndRej(["END:<br/>Rejected"])
    Dec -->|"On Hold"| S3
    
    PendApp -->|"Manager<br/>Approves"| EndApp(["END:<br/>Approved"])
    PendApp -->|"Manager<br/>Rejects"| BackS4["Back to<br/>Step 4"]
    BackS4 --> S4
    
    classDef step fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    classDef dec fill:#fff3e0,stroke:#fb8c00,stroke-width:2px
    classDef endApp fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef endRej fill:#ffebee,stroke:#e53935,stroke-width:2px
    classDef pend fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    
    class S1,S2,S3,S4 step
    class Dec dec
    class EndApp endApp
    class EndRej endRej
    class PendApp,BackS4 pend
        </div>
    </div>
</body>
</html>
"""

def main():
    base_dir = Path(__file__).parent
    html_file = base_dir / "temp_mermaid.html"
    screenshot_dir = base_dir / "screenshots"
    screenshot_path = screenshot_dir / "new_rm_sample_flow_clear.png"
    
    html_file.write_text(HTML_CONTENT, encoding="utf-8")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.as_posix()}")
        
        # Wait for SVG to be rendered
        page.wait_for_selector("svg")
        page.wait_for_timeout(1000) # give it a moment to finish rendering
        
        # Get exact bounding box
        element = page.locator("#container")
        element.screenshot(path=str(screenshot_path))
        
        browser.close()
        
    print(f"Successfully saved {screenshot_path}")
    
    # Cleanup temp html
    if html_file.exists():
        html_file.unlink()

if __name__ == "__main__":
    main()
