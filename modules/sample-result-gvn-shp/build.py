"""
Build FSD — Sample Result GVN-SHP Integration v1.0

Proses otoritatif: mockup + flowapps (Submit → Generate; Result Sync Draft→Syncronized).
Salinan deliverable:
  - Main: Sample Result …/Documentation/FSD/FSD_Sample_Result_GVN_SHP_v1.0.docx
  - Log:  …/Documentation/FSD/Log File/{YYYYMMDDHHmmss}__FSD_….docx
"""
import os
import sys
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'lib'))

from fsd_module_runner import build_fsd_module, ModuleBuildConfig, MermaidHandler, PlantumlHandler
from fsd_deliver import DeliverableConfig

SCREENSHOTS = os.path.join(SCRIPT_DIR, 'screenshots')

SLUG = 'sample-result-gvn-shp'
MD_FILE = 'FSD_Sample_Result_GVN_SHP_v1.0.md'
OUTPUT_DOCX = 'FSD_Sample_Result_GVN_SHP_v1.0.docx'

PROJECT_FSD_DIR = os.path.join(
    r'D:\Work\Source\Sample Result GVN-SHP Integration',
    'Documentation', 'FSD',
)
PROJECT_LOG_DIR = os.path.join(PROJECT_FSD_DIR, 'Log File')

COVER_DEFAULTS = {
    'project': 'Sample Result GVN-SHP Integration / Analytical Central',
    'brd_no': '2026.GVNSHP-BRD.001',
    'pid_no': '2026.GVNSHP-PID.001',
    'prepared_by': 'Tim IT Digital Solution',
    'document_approval': [
        {'name': 'Hendi Hendrasta', 'title': 'IT Digital Solution'},
        {'name': 'Debby Tantika Ardi', 'title': 'IT Digital Solution'},
        {'name': 'Cut Shafira Salsabila', 'title': 'Project Management'},
        {'name': 'Andreas Kurnijanto', 'title': 'Project Management Lead'},
    ],
}

PLANTUML_HANDLERS = [
    PlantumlHandler(
        lambda c: '|Requestor / Sampler|' in c and '|OSIR Lab|' in c,
        os.path.join(SCREENSHOTS, 'diagram_swimlane_business_flow.png'),
        'Swimlane',
        'Swimlane – Business Flow Sample Result GVN-SHP',
    ),
    PlantumlHandler(
        lambda c: '|Requestor|' in c and 'Lakukan Sync?' in c,
        os.path.join(SCREENSHOTS, 'diagram_swimlane_result_sync.png'),
        'Swimlane-Sync',
        'Swimlane – Result Sync Disposition',
    ),
]

MERMAID_HANDLERS = [
    MermaidHandler(
        lambda c: 'erDiagram' in c and 'TrresultSampleGvn' in c,
        os.path.join(SCREENSHOTS, 'diagram_erd.png'),
        'ERD',
        'ERD – Sample Result GVN-SHP (standar DAL)',
    ),
]

ENGINE_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

DELIVERABLE = DeliverableConfig(
    project_log_name='Sample Result GVN-SHP Integration',
    deliverable_code='GVNSHP_SAMPLE_RESULT',
    include_md=False,
    repo_copy_path=os.path.join(PROJECT_FSD_DIR, OUTPUT_DOCX),
)


def copy_timestamped_log(docx_path: str) -> str:
    """Arsip timestamp langsung di Documentation/FSD/Log File/."""
    os.makedirs(PROJECT_LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    dest = os.path.join(PROJECT_LOG_DIR, f'{ts}__{OUTPUT_DOCX}')
    shutil.copy2(docx_path, dest)
    print(f'   [FSD Log File] {dest}')
    return dest


if __name__ == '__main__':
    result = build_fsd_module(ModuleBuildConfig(
        slug=SLUG,
        md_filename=MD_FILE,
        output_filename=OUTPUT_DOCX,
        mermaid_handlers=MERMAID_HANDLERS,
        plantuml_handlers=PLANTUML_HANDLERS,
        cover_defaults=COVER_DEFAULTS,
        deliverable=DELIVERABLE,
    ), __file__)

    out_docx = os.path.join(SCRIPT_DIR, 'output', OUTPUT_DOCX)
    if os.path.isfile(out_docx):
        copy_timestamped_log(out_docx)
    else:
        print(f'ERROR: output tidak ditemukan: {out_docx}')
        sys.exit(1)
