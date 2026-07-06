"""Build FSD Laboratory Formula v1.1."""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_module_runner import build_fsd_module, ModuleBuildConfig

if __name__ == '__main__':
    build_fsd_module(ModuleBuildConfig(
        slug='formulation-lab',
        md_filename='FSD_LaboratoryFormula_v1.1.md',
        output_filename='FSD_LaboratoryFormula_v1.1.docx',
    ), __file__)
