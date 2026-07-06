"""
Capture New RM Sample Screenshots
Quick script to capture screenshots for New RM Sample pages
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    script_dir = Path(__file__).parent
    prototype_dir = script_dir.parent.parent
    screenshot_dir = script_dir / "screenshots"
    
    pages = [
        ('NewRMSampleIndex.html', 'NewRMSample_Index_Page.png'),
        ('NewRMSampleDetail.html', 'NewRMSample_Detail_Wizard.png'),
    ]
    
    print("Capturing New RM Sample screenshots...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        for html_file, screenshot_file in pages:
            html_path = prototype_dir / html_file
            screenshot_path = screenshot_dir / screenshot_file
            
            print(f"  Capturing: {html_file}")
            page.goto(f'file:///{html_path}')
            page.wait_for_timeout(2000)
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"  [OK] Saved: {screenshot_file}")
        
        browser.close()
    
    print("\n[SUCCESS] Screenshots captured!")


if __name__ == "__main__":
    main()
