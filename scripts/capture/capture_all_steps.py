"""
Capture Screenshots for All 4 Steps - New RM Sample
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    script_dir = Path(__file__).parent
    screenshot_dir = script_dir / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    
    # Define mockup files and their screenshot names
    pages = [
        ('mockup_step1.html', 'Step1_Document_Sample.png'),
        ('mockup_step2.html', 'Step2_Sample_Purpose.png'),
        ('mockup_step3.html', 'Step3_RM_Evaluation.png'),
        ('mockup_step4.html', 'Step4_Disposition.png'),
    ]
    
    print("=" * 70)
    print("Capturing New RM Sample Screenshots - All 4 Steps")
    print("=" * 70)
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        for html_file, screenshot_file in pages:
            html_path = script_dir / html_file
            screenshot_path = screenshot_dir / screenshot_file
            
            if not html_path.exists():
                print(f"  [SKIP] {html_file} not found")
                continue
            
            print(f"  Capturing: {html_file}")
            page.goto(f'file:///{html_path}')
            page.wait_for_timeout(2000)  # Wait for page to fully render
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"  [OK] Saved: {screenshot_file}")
        
        browser.close()
    
    print()
    print("=" * 70)
    print("[SUCCESS] All screenshots captured!")
    print("=" * 70)
    print()
    print("Screenshots saved in:", screenshot_dir)


if __name__ == "__main__":
    main()
