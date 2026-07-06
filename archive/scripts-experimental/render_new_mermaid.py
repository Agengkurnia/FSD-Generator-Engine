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
        body { background: transparent; margin: 20px; display: inline-block; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #container { padding: 20px; background: white; display: inline-block; border-radius: 8px; }
    </style>
</head>
<body>
    <div id="container">
        <div class="mermaid">
flowchart TD
    subgraph Row1 [Tahap 1: Evaluasi]
        direction LR
        Start(["Mulai"]) --> Step1["STEP 1: DOCUMENT SAMPLE"] --> Step2["STEP 2: SAMPLE PURPOSE"] --> Step3["STEP 3: RM EVALUATION"]
    end
    
    Step3 --> Step4
    
    subgraph Row2 [Tahap 2: Keputusan]
        direction RL
        Step4["STEP 4: DISPOSITION"] --> Decision{"Keputusan?"}
        Decision --> |"APPROVED"| ApprovalCheck{"Perlu Approval?"}
        Decision --> |"REJECTED"| EndReject(["REJECTED"])
        Decision --> |"ON HOLD"| OnHold["ON HOLD"]
        Decision --> |"CANCELLED"| EndCancel(["CANCELLED"])
    end
    
    OnHold -.-> |"Kembali"| Step3
    ApprovalCheck --> PendingApproval["Pending Approval"]
    ApprovalCheck --> |"Tidak"| Completed1(["COMPLETED"])
    
    subgraph Row3 [Tahap 3: Approval Atasan]
        direction LR
        PendingApproval --> ApproverReview["Approver Review"] --> ApprovalDecision{"Hasil Approval?"}
        ApprovalDecision --> |"APPROVE"| Completed(["COMPLETED"])
    end
    
    ApprovalDecision -.-> |"REJECT"| Step4

    style Start fill:#8CC63F,color:#fff,stroke:#009B4D,stroke-width:2px
    style Completed fill:#388E3C,color:#fff,stroke:#1B5E20,stroke-width:2px
    style Completed1 fill:#388E3C,color:#fff,stroke:#1B5E20,stroke-width:2px
    style EndReject fill:#D32F2F,color:#fff,stroke:#B71C1C,stroke-width:2px
    style EndCancel fill:#9E9E9E,color:#fff,stroke:#616161,stroke-width:2px
    style Step1 fill:#FFF3CD,stroke:#FFC107,stroke-width:2px
    style Step2 fill:#D1ECF1,stroke:#17A2B8,stroke-width:2px
    style Step3 fill:#E2E3E5,stroke:#6C757D,stroke-width:2px
    style Step4 fill:#F8D7DA,stroke:#DC3545,stroke-width:2px
    style Decision fill:#FFF3E0,stroke:#F7941E,stroke-width:3px
    style ApprovalCheck fill:#FFF3E0,stroke:#F7941E,stroke-width:2px
    style ApprovalDecision fill:#FFF3E0,stroke:#F7941E,stroke-width:2px
    style OnHold fill:#E7F3FF,stroke:#0D6EFD,stroke-width:2px
    style PendingApproval fill:#FFF9C4,stroke:#F57F17,stroke-width:2px
    style ApproverReview fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
        </div>
    </div>
</body>
</html>
"""

def main():
    base_dir = Path(__file__).parent
    html_file = base_dir / "temp_mermaid_custom.html"
    screenshot_dir = base_dir / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = screenshot_dir / "new_rm_sample_flow.png"
    
    html_file.write_text(HTML_CONTENT, encoding="utf-8")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(device_scale_factor=4)
        page = context.new_page()
        page.goto(f"file:///{html_file.as_posix()}")
        
        page.wait_for_selector("svg")
        page.wait_for_timeout(2000)
        
        element = page.locator("#container")
        element.screenshot(path=str(screenshot_path))
        
        context.close()
        browser.close()
        
    print(f"Successfully saved {screenshot_path}")
    if html_file.exists():
        html_file.unlink()

if __name__ == "__main__":
    main()
