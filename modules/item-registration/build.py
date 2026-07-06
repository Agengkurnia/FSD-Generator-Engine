"""Build FSD Item Registration v1.0."""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_module_runner import build_fsd_module, ModuleBuildConfig, MermaidHandler

SCREENSHOTS = os.path.join(SCRIPT_DIR, 'screenshots')

if __name__ == '__main__':
    build_fsd_module(ModuleBuildConfig(
        slug='item-registration',
        md_filename='FSD_Item_Registration_v1.0.md',
        output_filename='FSD - Item Registration v1.0.docx',
        mermaid_handlers=[
            MermaidHandler(
                lambda c: 'Item Trial' in c and 'INITIATOR' in c,
                os.path.join(SCREENSHOTS, 'item_reg_flow_trial.png'),
                'Flow-Trial', 'Business Flow – Item Trial',
            ),
            MermaidHandler(
                lambda c: 'Item Production' in c and 'INITIATOR' in c,
                os.path.join(SCREENSHOTS, 'item_reg_flow_prod.png'),
                'Flow-Prod', 'Business Flow – Item Production',
            ),
            MermaidHandler(
                lambda c: 'erDiagram' in c and 'XXSHP_INV_MASTER_ITEM_STG' in c,
                os.path.join(SCREENSHOTS, 'item_reg_erd.png'),
                'ERD', 'ERD – Item Registration',
            ),
        ],
    ), __file__)
