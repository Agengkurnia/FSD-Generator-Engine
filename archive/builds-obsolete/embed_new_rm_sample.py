"""
Embed Screenshots into New RM Sample FSD and Convert to DOCX
"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def create_screenshot_html(screenshot_path, caption):
    """Create HTML for screenshot container"""
    return f"""
    <div class="screenshot-container">
        <p><strong>Screenshot:</strong></p>
        <img src="{screenshot_path}" alt="{caption}">
        <p class="screenshot-caption">Figure: {caption}</p>
    </div>
"""


def embed_screenshots(html_path):
    """Embed screenshots into New RM Sample FSD HTML"""
    print(f"Processing: {html_path.name}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Define screenshot insertions
    screenshots = [
        {
            'after_text': '2.1.2 Data Table',
            'screenshot': 'screenshots/NewRMSample_Index_Page.png',
            'caption': 'New RM Sample Index Page - Dashboard dan Data Table'
        },
        {
            'after_text': '2.2 RM Sample Detail - Wizard Form',
            'screenshot': 'screenshots/NewRMSample_Detail_Wizard.png',
            'caption': 'New RM Sample Detail - 4-Step Wizard Form'
        },
    ]
    
    # Insert screenshots
    for item in screenshots:
        # Find the h4 or h3 tag containing the text
        headers = soup.find_all(['h3', 'h4'])
        for header in headers:
            if item['after_text'] in header.get_text():
                # Create screenshot HTML
                screenshot_html = create_screenshot_html(item['screenshot'], item['caption'])
                screenshot_soup = BeautifulSoup(screenshot_html, 'html.parser')
                
                # Insert after header
                header.insert_after(screenshot_soup)
                print(f"  [OK] Added screenshot: {item['caption']}")
                break
    
    # Save modified HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"  [SUCCESS] Updated {html_path.name}\n")
    return True


def convert_to_docx(html_path):
    """Convert HTML to DOCX using pandoc"""
    try:
        import pypandoc
    except ImportError:
        print("ERROR: pypandoc not installed")
        return False
    
    docx_path = html_path.parent / (html_path.stem + '.docx')
    
    print(f"Converting {html_path.name} to DOCX...")
    
    try:
        pypandoc.convert_file(
            str(html_path),
            'docx',
            outputfile=str(docx_path),
            extra_args=['--toc', '--toc-depth=3']
        )
        print(f"  [SUCCESS] Created: {docx_path.name}\n")
        return True
    except Exception as e:
        print(f"ERROR: {e}\n")
        return False


def main():
    script_dir = Path(__file__).parent
    fsd_html = script_dir / "FSD_New_RM_Sample.html"
    
    print("=" * 70)
    print("New RM Sample FSD - Screenshot Embedder and DOCX Converter")
    print("=" * 70)
    print()
    
    if not fsd_html.exists():
        print(f"ERROR: {fsd_html.name} not found!")
        return
    
    # Embed screenshots
    print("Step 1: Embedding screenshots")
    print("-" * 70)
    embed_screenshots(fsd_html)
    
    # Convert to DOCX
    print("Step 2: Converting to DOCX")
    print("-" * 70)
    convert_to_docx(fsd_html)
    
    print("=" * 70)
    print("PROCESS COMPLETE")
    print("=" * 70)
    print("\nFSD New RM Sample dengan screenshot sudah siap!")
    print("File: FSD_New_RM_Sample.docx")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
