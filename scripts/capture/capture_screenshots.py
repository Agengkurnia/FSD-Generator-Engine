"""
Automated Screenshot Capture for FSD Documentation
Captures full-page screenshots of all prototype HTML pages

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python capture_screenshots.py
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def capture_screenshot(page, url, output_path, wait_time=2000):
    """
    Capture full-page screenshot of a URL
    
    Args:
        page: Playwright page object
        url: URL to capture
        output_path: Path to save screenshot
        wait_time: Time to wait for page load (ms)
    """
    try:
        print(f"  Navigating to: {Path(url).name}")
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Additional wait for JavaScript to execute
        page.wait_for_timeout(wait_time)
        
        # Capture screenshot
        page.screenshot(path=output_path, full_page=True)
        print(f"  [OK] Saved: {Path(output_path).name}\n")
        return True
    
    except Exception as e:
        print(f"  [FAIL] Failed: {e}\n")
        return False


def main():
    """Main function to capture all screenshots"""
    
    # Base paths
    base_dir = Path(__file__).parent.parent.parent
    prototype_dir = base_dir  # HTML files are in the root project directory
    screenshot_dir = Path(__file__).parent / "screenshots"
    
    # Create screenshots directory
    screenshot_dir.mkdir(exist_ok=True)
    
    # Define pages to capture
    pages_to_capture = [
        # Master BTP
        {
            'html': 'BTPIndex.html',
            'screenshot': 'BTP_Index_Page.png',
            'description': 'Master BTP Index Page'
        },
        {
            'html': 'BTPDetail.html',
            'screenshot': 'BTP_Detail_Form.png',
            'description': 'Master BTP Detail Form'
        },
        {
            'html': 'BTPFunctionIndex.html',
            'screenshot': 'BTP_Function_Index.png',
            'description': 'BTP Function Index Page'
        },
        {
            'html': 'BTPFunctionDetail.html',
            'screenshot': 'BTP_Function_Detail.png',
            'description': 'BTP Function Detail Form'
        },
        {
            'html': 'BTPFunctionMapping.html',
            'screenshot': 'BTP_Function_Mapping.png',
            'description': 'BTP Function Mapping Page'
        },
        
        # Master UOM
        {
            'html': 'MasterUOMIndex.html',
            'screenshot': 'UOM_Index_Page.png',
            'description': 'Master UOM Index Page'
        },
        {
            'html': 'MasterUOMDetail.html',
            'screenshot': 'UOM_Detail_Form.png',
            'description': 'Master UOM Detail Form'
        },
        
        # Master RM Category
        {
            'html': 'RMCategoryIndex.html',
            'screenshot': 'RM_Category_Index.png',
            'description': 'RM Category Index Page'
        },
        {
            'html': 'RMCategoryDetail.html',
            'screenshot': 'RM_Category_Detail.png',
            'description': 'RM Category Detail Form'
        },
        {
            'html': 'RMCategorySubGroupMapping.html',
            'screenshot': 'RM_Category_Mapping.png',
            'description': 'RM Category SubGroup Mapping'
        },
        
        # Master RM SubGroup
        {
            'html': 'RMSubGroupIndex.html',
            'screenshot': 'RM_SubGroup_Index.png',
            'description': 'RM SubGroup Index Page'
        },
        {
            'html': 'RMSubGroupDetail.html',
            'screenshot': 'RM_SubGroup_Detail.png',
            'description': 'RM SubGroup Detail Form'
        },
        
        # Master Parameter
        {
            'html': 'ParameterIndex.html',
            'screenshot': 'Parameter_Index.png',
            'description': 'Master Parameter Index Page'
        },
        {
            'html': 'ParameterDetail.html',
            'screenshot': 'Parameter_Detail.png',
            'description': 'Master Parameter Detail Form'
        },
    ]
    
    print("=" * 70)
    print("FSD Screenshot Capture Tool")
    print("=" * 70)
    print(f"Prototype directory: {prototype_dir}")
    print(f"Screenshot directory: {screenshot_dir}")
    print(f"Total pages to capture: {len(pages_to_capture)}\n")
    
    # Launch browser
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        
        # Create context with larger viewport
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1
        )
        
        page = context.new_page()
        
        # Capture screenshots
        success_count = 0
        failed_count = 0
        
        for i, page_info in enumerate(pages_to_capture, 1):
            html_file = prototype_dir / page_info['html']
            screenshot_path = screenshot_dir / page_info['screenshot']
            
            print(f"[{i}/{len(pages_to_capture)}] {page_info['description']}")
            
            if not html_file.exists():
                print(f"  [FAIL] HTML file not found: {html_file}\n")
                failed_count += 1
                continue
            
            # Convert to file:// URL
            file_url = f"file:///{html_file.as_posix()}"
            
            if capture_screenshot(page, file_url, str(screenshot_path)):
                success_count += 1
            else:
                failed_count += 1
        
        # Close browser
        browser.close()
    
    # Summary
    print("=" * 70)
    print("CAPTURE SUMMARY")
    print("=" * 70)
    print(f"Total pages: {len(pages_to_capture)}")
    print(f"Successfully captured: {success_count}")
    print(f"Failed: {failed_count}")
    
    if success_count > 0:
        print(f"\n[SUCCESS] Screenshots saved to: {screenshot_dir}")
        print("\nNext steps:")
        print("1. Review screenshots in the screenshots/ folder")
        print("2. Add screenshots to FSD HTML files")
        print("3. Convert HTML to DOCX")
        print("4. Adjust screenshot size and alignment in Word")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("\nERROR: Required packages not installed.")
        print("\nPlease install:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("\nThen run this script again.")
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nPlease check the error message and try again.")
