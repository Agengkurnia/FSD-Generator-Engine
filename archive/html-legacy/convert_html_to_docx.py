"""
HTML to DOCX Converter for FSD Documents
Converts FSD HTML files to Microsoft Word DOCX format using pandoc

Requirements:
    pip install pypandoc
    
Note: pandoc must be installed on your system
    Windows: choco install pandoc
    Or download from: https://pandoc.org/installing.html
"""

import os
import sys
from pathlib import Path

try:
    import pypandoc
except ImportError:
    print("ERROR: pypandoc is not installed.")
    print("Please install it using: pip install pypandoc")
    sys.exit(1)


def convert_html_to_docx(html_file_path, output_dir=None):
    """
    Convert HTML file to DOCX format
    
    Args:
        html_file_path (str): Path to HTML file
        output_dir (str): Output directory for DOCX file (default: same as HTML)
    
    Returns:
        str: Path to generated DOCX file
    """
    html_path = Path(html_file_path)
    
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file_path}")
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = html_path.parent
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate DOCX filename
    docx_filename = html_path.stem + ".docx"
    docx_path = output_path / docx_filename
    
    print(f"Converting: {html_path.name}")
    print(f"Output: {docx_path}")
    
    try:
        # Convert HTML to DOCX using pandoc
        pypandoc.convert_file(
            str(html_path),
            'docx',
            outputfile=str(docx_path),
            extra_args=[
                '--reference-doc=reference.docx',  # Optional: use custom template
                '--toc',  # Table of contents
                '--toc-depth=3',  # TOC depth
            ]
        )
        print(f"✓ Successfully converted to: {docx_path}\n")
        return str(docx_path)
    
    except RuntimeError as e:
        if "pandoc" in str(e).lower():
            print("\nERROR: pandoc is not installed on your system.")
            print("\nPlease install pandoc:")
            print("  Windows: choco install pandoc")
            print("  Or download from: https://pandoc.org/installing.html")
            print("\nAfter installation, restart your terminal and try again.")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to convert {html_path.name}")
        print(f"Reason: {e}")
        return None


def convert_all_fsd_html_files(directory):
    """
    Convert all FSD HTML files in directory to DOCX
    
    Args:
        directory (str): Directory containing FSD HTML files
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"ERROR: Directory not found: {directory}")
        sys.exit(1)
    
    # Find all FSD HTML files
    html_files = list(dir_path.glob("FSD*.html"))
    
    if not html_files:
        print(f"No FSD HTML files found in: {directory}")
        return
    
    print(f"Found {len(html_files)} FSD HTML file(s) to convert:\n")
    
    converted = []
    failed = []
    
    for html_file in html_files:
        try:
            docx_path = convert_html_to_docx(str(html_file))
            if docx_path:
                converted.append(docx_path)
            else:
                failed.append(str(html_file))
        except Exception as e:
            print(f"ERROR: {e}\n")
            failed.append(str(html_file))
    
    # Summary
    print("=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(html_files)}")
    print(f"Successfully converted: {len(converted)}")
    print(f"Failed: {len(failed)}")
    
    if converted:
        print("\n✓ Converted files:")
        for path in converted:
            print(f"  - {Path(path).name}")
    
    if failed:
        print("\n✗ Failed files:")
        for path in failed:
            print(f"  - {Path(path).name}")


def main():
    """Main function"""
    # Get current script directory
    script_dir = Path(__file__).parent
    
    print("=" * 60)
    print("FSD HTML to DOCX Converter")
    print("=" * 60)
    print(f"Working directory: {script_dir}\n")
    
    # Convert all FSD HTML files in current directory
    convert_all_fsd_html_files(script_dir)


if __name__ == "__main__":
    main()
