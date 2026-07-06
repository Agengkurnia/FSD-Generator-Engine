"""
Build FSD — TEMPLATE MODUL BARU

Cara pakai:
  1. Salin folder _template ke modules/{slug-baru}/
  2. Ganti slug, md_filename, output_filename di bawah
  3. Rename source/FSD_TEMPLATE.md sesuai md_filename
  4. py build.py

Acuan: modules/item-registration/build.py
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_module_runner import build_fsd_module, ModuleBuildConfig, MermaidHandler

SCREENSHOTS = os.path.join(SCRIPT_DIR, 'screenshots')

# --- KONFIGURASI: UBAH INI ---
SLUG = 'my-module-slug'
MD_FILE = 'FSD_TEMPLATE.md'           # harus ada di source/
OUTPUT_DOCX = 'FSD_MyModule_v1.0.docx'

# Opsional: override metadata cover (BRD/PID/project)
COVER_DEFAULTS = {
  # 'project': 'NAMA SISTEM',
  # 'brd_no': '2026.SHP-FSD.0000',
  # 'pid_no': '2026.SHP-PID.0000',
}

# Opsional: mapping Mermaid → PNG (tambah handler per diagram)
MERMAID_HANDLERS = [
    # Contoh ERD:
    # MermaidHandler(
    #     lambda c: 'erDiagram' in c and 'TABEL_HDR' in c,
    #     os.path.join(SCREENSHOTS, 'diagram_erd.png'),
    #     'ERD', 'ERD – {NAMA_MODUL}',
    # ),
    # Contoh flow:
    # MermaidHandler(
    #     lambda c: 'flowchart' in c and 'Draft' in c,
    #     os.path.join(SCREENSHOTS, 'diagram_flow.png'),
    #     'Flow', 'Business Flow – {NAMA_MODUL}',
    # ),
]

if __name__ == '__main__':
    build_fsd_module(ModuleBuildConfig(
        slug=SLUG,
        md_filename=MD_FILE,
        output_filename=OUTPUT_DOCX,
        mermaid_handlers=MERMAID_HANDLERS,
        cover_defaults=COVER_DEFAULTS or None,
    ), __file__)
