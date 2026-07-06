"""Build FSD Oracle Registration v1.1."""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_module_runner import build_fsd_module, ModuleBuildConfig, MermaidHandler

SCREENSHOTS = os.path.join(SCRIPT_DIR, 'screenshots')

if __name__ == '__main__':
    build_fsd_module(ModuleBuildConfig(
        slug='oracle-registration',
        md_filename='FSD_Oracle_Registration_v1.1.md',
        output_filename='FSD_Oracle_Registration_v1.1.docx',
        mermaid_handlers=[
            MermaidHandler(
                lambda c: 'RMApproved' in c and 'CreateTrial' in c,
                os.path.join(SCREENSHOTS, 'oracle_reg_flow_main.png'),
                'Flow-Main', 'Business Flow – Oracle Registration',
            ),
            MermaidHandler(
                lambda c: 'Item Trial' in c and 'Approver' in c,
                os.path.join(SCREENSHOTS, 'oracle_reg_approval_trial.png'),
                'Flow-Approval-Trial', 'Approval Flow – Item Trial',
            ),
            MermaidHandler(
                lambda c: 'Item Production' in c and 'Approver' in c,
                os.path.join(SCREENSHOTS, 'oracle_reg_approval_prod.png'),
                'Flow-Approval-Prod', 'Approval Flow – Item Production',
            ),
            MermaidHandler(
                lambda c: 'erDiagram' in c,
                os.path.join(SCREENSHOTS, 'oracle_reg_erd.png'),
                'ERD', 'ERD – Oracle Registration',
            ),
        ],
    ), __file__)
