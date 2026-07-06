"""Render swimlane PoC — bandingkan Mermaid vs PlantUML via Kroki."""
import os
import sys

ENGINE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ENGINE_ROOT, 'lib'))

from fsd_build import render_kroki, render_kroki_plantuml

EXAMPLES = os.path.join(ENGINE_ROOT, 'docs', 'examples', 'swimlane')
OUTPUT = os.path.join(EXAMPLES, 'output')


def main():
    os.makedirs(OUTPUT, exist_ok=True)

    mmd_path = os.path.join(EXAMPLES, 'restaurant-poc-mermaid.mmd')
    puml_path = os.path.join(EXAMPLES, 'restaurant-poc-plantuml.puml')

    with open(mmd_path, 'r', encoding='utf-8') as f:
        mermaid = f.read()
    with open(puml_path, 'r', encoding='utf-8') as f:
        plantuml = f.read()

    print('=== Swimlane PoC Render ===\n')
    ok_m = render_kroki(mermaid, os.path.join(OUTPUT, 'poc_mermaid.png'), 'PoC-Mermaid')
    ok_p = render_kroki_plantuml(plantuml, os.path.join(OUTPUT, 'poc_plantuml.png'), 'PoC-PlantUML')

    print()
    if ok_m:
        print(f'Mermaid:  {OUTPUT}\\poc_mermaid.png')
    if ok_p:
        print(f'PlantUML: {OUTPUT}\\poc_plantuml.png')
    if not (ok_m and ok_p):
        sys.exit(1)


if __name__ == '__main__':
    main()
