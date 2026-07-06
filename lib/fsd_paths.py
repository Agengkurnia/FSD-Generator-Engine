"""Path standar aset cover FSD Generator Engine."""
import os

ENGINE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(ENGINE_ROOT, 'templates')
TMP_DIR = os.path.join(ENGINE_ROOT, '_tmp')
COVER_TEMPLATE = os.path.join(TEMPLATES_DIR, 'FSD_Cover_Template.docx')
LOGO_PATH = os.path.join(TEMPLATES_DIR, 'logo.png')
REFERENCE_DOCX = os.path.join(TEMPLATES_DIR, 'reference.docx')


def engine_root_from_script(script_path: str) -> str:
    """ENGINE_ROOT dari build.py di modules/{slug}/ atau di root engine."""
    script_dir = os.path.dirname(os.path.abspath(script_path))
    if os.path.basename(os.path.dirname(script_dir)) == 'modules':
        return os.path.dirname(os.path.dirname(script_dir))
    return os.path.dirname(script_dir)


def ensure_lib_on_path():
    """Tambahkan lib/ ke sys.path jika belum (untuk import dari subfolder build script)."""
    import sys
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    if lib_dir not in sys.path:
        sys.path.insert(0, lib_dir)
