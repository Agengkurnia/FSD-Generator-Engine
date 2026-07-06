"""
SIMPLE SCREENSHOT SCRIPT - NEW RM SAMPLE MANAGEMENT
Menggunakan Playwright untuk capture screenshots
Lebih simple dan reliable daripada Selenium
"""

import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INDEX_PAGE = PROJECT_ROOT / "NewRMSampleIndex.html"
DETAIL_PAGE = PROJECT_ROOT / "NewRMSampleDetail.html"
OUTPUT_DIR = SCRIPT_DIR / "Screenshots"
WAIT_TIME = 2000  # milliseconds

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("NEW RM SAMPLE MANAGEMENT - AUTOMATED SCREENSHOT TOOL")
print("=" * 80)
print(f"\nConfiguration:")
print(f"  Index Page   : {INDEX_PAGE}")
print(f"  Detail Page  : {DETAIL_PAGE}")
print(f"  Output Folder: {OUTPUT_DIR}")
print(f"  Wait Time    : {WAIT_TIME} ms\n")

async def expand_all_accordions(page):
    """Expand all Bootstrap accordions and collapsible elements"""
    try:
        await page.evaluate("""
            () => {
                // Expand all Bootstrap collapse elements
                document.querySelectorAll('.collapse').forEach(el => {
                    el.classList.add('show');
                });
                
                // Expand all accordion buttons
                document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(btn => {
                    btn.setAttribute('aria-expanded', 'true');
                    btn.classList.remove('collapsed');
                });
                
                // Expand all details/summary elements
                document.querySelectorAll('details').forEach(el => {
                    el.open = true;
                });
            }
        """)
        await page.wait_for_timeout(500)
    except Exception as e:
        print(f"  Warning: Could not expand accordions - {e}")

async def take_screenshot(page, filename, description):
    """Take a screenshot and save it"""
    try:
        await page.wait_for_timeout(WAIT_TIME)
        filepath = OUTPUT_DIR / f"{filename}.png"
        await page.screenshot(path=str(filepath), full_page=True)
        print(f"  [OK] {description}")
        return True
    except Exception as e:
        print(f"  [FAIL] Failed: {description} - {e}")
        return False

async def click_element(page, selector):
    """Click an element safely"""
    try:
        await page.click(selector, timeout=5000)
        await page.wait_for_timeout(500)
        return True
    except Exception as e:
        print(f"  Warning: Could not click element: {selector}")
        return False

async def main():
    screenshot_count = 0
    success_count = 0
    
    async with async_playwright() as p:
        # Launch browser
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)  # headless=False to see what's happening
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})
        print("  [OK] Browser launched\n")
        
        print("=" * 80)
        print("CAPTURING SCREENSHOTS")
        print("=" * 80 + "\n")
        
        # ====================================================================
        # INDEX PAGE
        # ====================================================================
        print("[1/2] NewRMSampleIndex.html")
        
        try:
            await page.goto(f"file:///{str(INDEX_PAGE).replace(chr(92), '/')}")
            await page.wait_for_timeout(WAIT_TIME)
            await expand_all_accordions(page)
            
            # Screenshot 1: Dashboard
            screenshot_count += 1
            if await take_screenshot(page, "01_Index_Dashboard", f"Screenshot {screenshot_count}/22: Index Dashboard"):
                success_count += 1
            
            # Scroll to table
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await page.wait_for_timeout(500)
            
            # Screenshot 2: DataTable
            screenshot_count += 1
            if await take_screenshot(page, "02_Index_DataTable", f"Screenshot {screenshot_count}/22: Index DataTable"):
                success_count += 1
        except Exception as e:
            print(f"  [ERROR] Error loading Index page: {e}")
        
        # ====================================================================
        # DETAIL PAGE
        # ====================================================================
        print(f"\n[2/2] NewRMSampleDetail.html")
        
        try:
            await page.goto(f"file:///{str(DETAIL_PAGE).replace(chr(92), '/')}")
            await page.wait_for_timeout(WAIT_TIME)
            await expand_all_accordions(page)
            
            # STEP 1: DOCUMENT
            print(f"\n  Step 1: Document")
            await page.evaluate("window.scrollTo(0, 0)")
            
            screenshot_count += 1
            if await take_screenshot(page, "03_Detail_Step1_Header", f"Screenshot {screenshot_count}/22: Step 1 - Header"):
                success_count += 1
            
            await page.evaluate("window.scrollBy(0, 400)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "04_Detail_Step1_Materials", f"Screenshot {screenshot_count}/22: Step 1 - Materials"):
                success_count += 1
            
            await page.evaluate("window.scrollBy(0, 400)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "05_Detail_Step1_Allergen", f"Screenshot {screenshot_count}/22: Step 1 - Allergen"):
                success_count += 1
            
            await page.evaluate("window.scrollBy(0, 400)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "06_Detail_Step1_BTP", f"Screenshot {screenshot_count}/22: Step 1 - BTP"):
                success_count += 1
            
            await page.evaluate("window.scrollBy(0, 400)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "07_Detail_Step1_Documents", f"Screenshot {screenshot_count}/22: Step 1 - Documents"):
                success_count += 1
            
            # STEP 2: PURPOSE
            print(f"\n  Step 2: Purpose")
            await click_element(page, "#btnNext")
            await page.wait_for_timeout(WAIT_TIME)
            await expand_all_accordions(page)
            await page.evaluate("window.scrollTo(0, 0)")
            
            screenshot_count += 1
            if await take_screenshot(page, "08_Detail_Step2_Category", f"Screenshot {screenshot_count}/22: Step 2 - Category"):
                success_count += 1
            
            await page.evaluate("window.scrollBy(0, 400)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "09_Detail_Step2_Items", f"Screenshot {screenshot_count}/22: Step 2 - Items"):
                success_count += 1
            
            await page.evaluate("window.scrollBy(0, 400)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "10_Detail_Step2_Products", f"Screenshot {screenshot_count}/22: Step 2 - Products"):
                success_count += 1
            
            # STEP 3: EVALUATION
            print(f"\n  Step 3: Evaluation")
            await click_element(page, "#btnNext")
            await page.wait_for_timeout(WAIT_TIME)
            await expand_all_accordions(page)
            await page.evaluate("window.scrollTo(0, 0)")
            
            screenshot_count += 1
            if await take_screenshot(page, "11_Detail_Step3_Organoleptic", f"Screenshot {screenshot_count}/22: Step 3 - Organoleptic"):
                success_count += 1
            
            # Try different tab selectors
            for tab_selector in ["a[href='#nutrition-tab']", ".nav-link:has-text('Nutrition')", "text=Nutrition"]:
                if await click_element(page, tab_selector):
                    break
            await page.wait_for_timeout(500)
            
            screenshot_count += 1
            if await take_screenshot(page, "12_Detail_Step3_Nutrition", f"Screenshot {screenshot_count}/22: Step 3 - Nutrition"):
                success_count += 1
            
            for tab_selector in ["a[href='#microbiological-tab']", ".nav-link:has-text('Microbiological')", "text=Microbiological"]:
                if await click_element(page, tab_selector):
                    break
            await page.wait_for_timeout(500)
            
            screenshot_count += 1
            if await take_screenshot(page, "13_Detail_Step3_Microbiological", f"Screenshot {screenshot_count}/22: Step 3 - Microbiological"):
                success_count += 1
            
            for tab_selector in ["a[href='#heavymetals-tab']", ".nav-link:has-text('Heavy')", "text=Heavy Metals"]:
                if await click_element(page, tab_selector):
                    break
            await page.wait_for_timeout(500)
            
            screenshot_count += 1
            if await take_screenshot(page, "14_Detail_Step3_HeavyMetals", f"Screenshot {screenshot_count}/22: Step 3 - Heavy Metals"):
                success_count += 1
            
            for tab_selector in ["a[href='#othercontaminant-tab']", ".nav-link:has-text('Other')", "text=Other Contaminant"]:
                if await click_element(page, tab_selector):
                    break
            await page.wait_for_timeout(500)
            
            screenshot_count += 1
            if await take_screenshot(page, "15_Detail_Step3_OtherContaminant", f"Screenshot {screenshot_count}/22: Step 3 - Other Contaminant"):
                success_count += 1
            
            for tab_selector in ["a[href='#foodcategory-tab']", ".nav-link:has-text('Food')", "text=Food Category"]:
                if await click_element(page, tab_selector):
                    break
            await page.wait_for_timeout(500)
            
            screenshot_count += 1
            if await take_screenshot(page, "16_Detail_Step3_FoodCategory", f"Screenshot {screenshot_count}/22: Step 3 - Food Category"):
                success_count += 1
            
            # STEP 4: DISPOSITION
            print(f"\n  Step 4: Disposition")
            await click_element(page, "#btnNext")
            await page.wait_for_timeout(WAIT_TIME)
            await expand_all_accordions(page)
            await page.evaluate("window.scrollTo(0, 0)")
            
            screenshot_count += 1
            if await take_screenshot(page, "17_Detail_Step4_Disposition", f"Screenshot {screenshot_count}/22: Step 4 - Disposition"):
                success_count += 1
            
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(300)
            
            screenshot_count += 1
            if await take_screenshot(page, "18_Detail_Step4_Actions", f"Screenshot {screenshot_count}/22: Step 4 - Actions"):
                success_count += 1
            
            # MODALS
            print(f"\n  Modals")
            await page.goto(f"file:///{str(DETAIL_PAGE).replace(chr(92), '/')}")
            await page.wait_for_timeout(WAIT_TIME)
            
            # Modal 1: Add Document
            if await click_element(page, "button[data-bs-target='#addAttachmentModal']"):
                await page.wait_for_timeout(500)
                screenshot_count += 1
                if await take_screenshot(page, "19_Modal_AddDocument", f"Screenshot {screenshot_count}/22: Modal - Add Document"):
                    success_count += 1
                await page.evaluate("document.querySelector('#addAttachmentModal .btn-close').click()")
                await page.wait_for_timeout(500)
            
            # Modal 2: LOV Type Document
            if await click_element(page, "button[data-bs-target='#lovTypeModal']"):
                await page.wait_for_timeout(500)
                screenshot_count += 1
                if await take_screenshot(page, "20_Modal_LOV_TypeDocument", f"Screenshot {screenshot_count}/22: Modal - LOV Type"):
                    success_count += 1
                await page.evaluate("document.querySelector('#lovTypeModal .btn-close').click()")
                await page.wait_for_timeout(500)
            
            # Modal 3: LOV Currency
            if await click_element(page, "button[data-bs-target='#lovCurrencyModal']"):
                await page.wait_for_timeout(500)
                screenshot_count += 1
                if await take_screenshot(page, "21_Modal_LOV_Currency", f"Screenshot {screenshot_count}/22: Modal - LOV Currency"):
                    success_count += 1
                await page.evaluate("document.querySelector('#lovCurrencyModal .btn-close').click()")
                await page.wait_for_timeout(500)
            
            # Modal 4: LOV UOM
            if await click_element(page, "button[data-bs-target='#lovUOMModal']"):
                await page.wait_for_timeout(500)
                screenshot_count += 1
                if await take_screenshot(page, "22_Modal_LOV_UOM", f"Screenshot {screenshot_count}/22: Modal - LOV UOM"):
                    success_count += 1
        
        except Exception as e:
            print(f"  [ERROR] Error during screenshot capture: {e}")
        
        # Close browser
        await browser.close()
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80 + "\n")
        print(f"Total Screenshots Attempted: {screenshot_count}/22")
        print(f"Successfully Captured      : {success_count}/22")
        print(f"Failed                     : {screenshot_count - success_count}/22")
        print(f"\nOutput Folder: {OUTPUT_DIR}\n")
        
        if success_count == 22:
            print("[SUCCESS] ALL SCREENSHOTS CAPTURED SUCCESSFULLY!")
        elif success_count > 0:
            print("[WARNING] PARTIAL SUCCESS - Some screenshots may need manual capture")
        else:
            print("[FAILED] Please check error messages above")
        
        print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    print("\nInstalling Playwright if needed...")
    os.system("python -m playwright install chromium")
    print("\nStarting screenshot capture...\n")
    asyncio.run(main())
