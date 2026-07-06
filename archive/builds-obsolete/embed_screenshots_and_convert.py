"""
Embed Screenshots into FSD HTML and Convert to DOCX
Automatically adds screenshot sections to FSD HTML files and converts to DOCX

Requirements:
    pip install beautifulsoup4 pypandoc
    pandoc must be installed

Usage:
    python embed_screenshots_and_convert.py
"""

import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def add_screenshot_style(soup):
    """Add screenshot container style to HTML"""
    style_tag = soup.find('style')
    if style_tag:
        screenshot_css = """
        
        .screenshot-container {
            margin: 20px 0;
            padding: 15px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            page-break-inside: avoid;
        }
        
        .screenshot-container img {
            max-width: 100%;
            border: 1px solid #ccc;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: block;
            margin: 10px auto;
        }
        
        .screenshot-caption {
            text-align: center;
            font-size: 10pt;
            color: #666;
            margin-top: 5px;
            font-style: italic;
        }
"""
        style_tag.string += screenshot_css
    return soup


def create_screenshot_html(screenshot_path, caption):
    """Create HTML for screenshot container"""
    return f"""
    <div class="screenshot-container">
        <p><strong>Screenshot:</strong></p>
        <img src="{screenshot_path}" alt="{caption}">
        <p class="screenshot-caption">Figure: {caption}</p>
    </div>
"""


def embed_screenshots_master_btp(html_path, screenshots_dir):
    """Embed screenshots into Master BTP FSD HTML"""
    print(f"Processing: {html_path.name}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Add screenshot styles
    soup = add_screenshot_style(soup)
    
    # Define screenshot insertions
    screenshots = [
        {
            'after_text': '2.1.1 Layout Index BTP',
            'screenshot': 'screenshots/BTP_Index_Page.png',
            'caption': 'Master BTP Index Page - Daftar BTP dengan DataTable'
        },
        {
            'after_text': '2.1.2 Layout Detail BTP',
            'screenshot': 'screenshots/BTP_Detail_Form.png',
            'caption': 'Master BTP Detail Form - Form Input BTP'
        },
        {
            'after_text': '2.2.1 Layout Index BTP Function',
            'screenshot': 'screenshots/BTP_Function_Index.png',
            'caption': 'BTP Function Index Page - Daftar Fungsi BTP'
        },
        {
            'after_text': '2.2.2 Layout Detail BTP Function',
            'screenshot': 'screenshots/BTP_Function_Detail.png',
            'caption': 'BTP Function Detail Form - Form Input Fungsi'
        },
        {
            'after_text': '2.3.1 Layout BTP Function Mapping',
            'screenshot': 'screenshots/BTP_Function_Mapping.png',
            'caption': 'BTP Function Mapping Page - Mapping BTP dengan Fungsi'
        },
    ]
    
    # Insert screenshots
    for item in screenshots:
        # Find the h4 tag containing the text
        h4_tags = soup.find_all('h4')
        for h4 in h4_tags:
            if item['after_text'] in h4.get_text():
                # Create screenshot HTML
                screenshot_html = create_screenshot_html(item['screenshot'], item['caption'])
                screenshot_soup = BeautifulSoup(screenshot_html, 'html.parser')
                
                # Insert after h4
                h4.insert_after(screenshot_soup)
                print(f"  [OK] Added screenshot: {item['caption']}")
                break
    
    # Save modified HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"  [SUCCESS] Updated {html_path.name}\n")
    return True


def convert_html_to_docx(html_path, output_dir=None):
    """Convert HTML to DOCX using pandoc"""
    try:
        import pypandoc
    except ImportError:
        print("ERROR: pypandoc not installed. Run: pip install pypandoc")
        return False
    
    if output_dir is None:
        output_dir = html_path.parent
    
    docx_path = output_dir / (html_path.stem + '.docx')
    
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
    except RuntimeError as e:
        if "pandoc" in str(e).lower():
            print("\nERROR: pandoc is not installed or not in PATH.")
            print("Please install pandoc and restart terminal.")
            print("Download from: https://pandoc.org/installing.html\n")
        else:
            print(f"ERROR: {e}\n")
        return False
    except Exception as e:
        print(f"ERROR: {e}\n")
        return False


def main():
    """Main function"""
    script_dir = Path(__file__).parent
    
    print("=" * 70)
    print("FSD Screenshot Embedder and DOCX Converter")
    print("=" * 70)
    print(f"Working directory: {script_dir}\n")
    
    # Check if screenshots directory exists
    screenshots_dir = script_dir / "screenshots"
    if not screenshots_dir.exists():
        print("ERROR: screenshots/ directory not found!")
        print("Please run capture_screenshots.py first.\n")
        return
    
    # Process Master BTP FSD
    btp_html = script_dir / "FSD_Master_BTP.html"
    if btp_html.exists():
        print("Step 1: Embedding screenshots into FSD HTML")
        print("-" * 70)
        if embed_screenshots_master_btp(btp_html, screenshots_dir):
            print("Step 2: Converting HTML to DOCX")
            print("-" * 70)
            convert_html_to_docx(btp_html)
    else:
        print(f"ERROR: {btp_html.name} not found!\n")
    
    print("=" * 70)
    print("PROCESS COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Open the DOCX file in Microsoft Word")
    print("2. Review screenshots and formatting")
    print("3. Adjust image sizes if needed (recommended: 80-90% page width)")
    print("4. Save and distribute")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nPlease check the error message and try again.")
