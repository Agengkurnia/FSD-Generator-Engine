"""Build FSD Item Code Trial v3.0."""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_module_runner import build_fsd_module, ModuleBuildConfig, MermaidHandler

SCREENSHOTS = os.path.join(SCRIPT_DIR, 'screenshots')

if __name__ == '__main__':
    build_fsd_module(ModuleBuildConfig(
        slug='item-code-trial',
        md_filename='FSD_ItemCodeTrial_v3.0.md',
        output_filename='FSD_ItemCodeTrial_v3.0.docx',
        mermaid_handlers=[
            MermaidHandler(
                lambda c: 'XXSHP_INV_MASTER_ITEM_STG' in c and 'erDiagram' in c,
                os.path.join(SCREENSHOTS, 'itemcodetrial_erd.png'),
                'ERD', 'ERD – Item Code Trial',
            ),
            MermaidHandler(
                lambda c: 'K2 BPM' in c or 'ApproverAct' in c,
                os.path.join(SCREENSHOTS, 'itemcodetrial_flow_approval.png'),
                'Flow-Approval', 'Approval Flow – Item Code Trial',
            ),
        ],
    ), __file__)
