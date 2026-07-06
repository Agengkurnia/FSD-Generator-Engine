"""
capture_screenshots.py
======================
Mengambil screenshot halaman prototype Item Spec RM menggunakan Playwright.
Halaman yang di-capture:
  1. ItemSpecRMIndex.html  – halaman daftar
  2. ItemSpecRMDetail.html – halaman detail (berbagai tab + modal)

Run:
    py capture_screenshots.py
"""
import sys, io, os, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

# ──────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ITEMSPEC_DIR= os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'RMPM', 'ItemSpec'))
SHOTS_DIR   = os.path.join(SCRIPT_DIR, 'screenshots')
os.makedirs(SHOTS_DIR, exist_ok=True)

INDEX_URL  = 'file:///' + ITEMSPEC_DIR.replace('\\', '/') + '/ItemSpecRMIndex.html'
DETAIL_URL = 'file:///' + ITEMSPEC_DIR.replace('\\', '/') + '/ItemSpecRMDetail.html'

WAIT_MS = 2500   # wait after page load for JS to settle


def shot(page, filename: str, full: bool = True):
    path = os.path.join(SHOTS_DIR, filename)
    page.screenshot(path=path, full_page=full)
    size = os.path.getsize(path)
    print(f'   [OK] {filename}  ({size:,} bytes)')


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})

        # ─────────────────────────────────────────
        # 1. INDEX PAGE
        # ─────────────────────────────────────────
        print('\n[1] Halaman Index – Item Spec RM')
        pg = ctx.new_page()
        pg.goto(INDEX_URL, wait_until='networkidle', timeout=20000)
        pg.wait_for_timeout(WAIT_MS)
        shot(pg, 'ss_01_index_full.png', full=True)

        # Dashboard cards + table header viewport crop
        shot(pg, 'ss_02_index_cards.png', full=False)
        pg.close()

        # ─────────────────────────────────────────
        # 2. DETAIL PAGE – HEADER
        # ─────────────────────────────────────────
        print('\n[2] Halaman Detail – Header Section')
        pg = ctx.new_page()
        pg.goto(DETAIL_URL, wait_until='networkidle', timeout=20000)
        pg.wait_for_timeout(WAIT_MS)

        # Full initial view (header + first tab)
        shot(pg, 'ss_03_detail_header.png', full=False)

        # ─────────────────────────────────────────
        # 3. TAB: Material Description
        # ─────────────────────────────────────────
        print('\n[3] Tab – Material Description')
        pg.click('button[data-tab-id="MaterialDescription"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_04_tab_material_desc.png', full=True)

        # ─────────────────────────────────────────
        # 4. TAB: Organoleptic
        # ─────────────────────────────────────────
        print('\n[4] Tab – Organoleptic')
        pg.click('button[data-tab-id="Organoleptic"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_05_tab_organoleptic.png', full=True)

        # ─────────────────────────────────────────
        # 5. TAB: Nutrition & Physical
        # ─────────────────────────────────────────
        print('\n[5] Tab – Nutrition & Physical')
        pg.click('button[data-tab-id="Nutrition"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_06_tab_nutrition.png', full=True)

        # ─────────────────────────────────────────
        # 6. TAB: Microbiological
        # ─────────────────────────────────────────
        print('\n[6] Tab – Microbiological')
        pg.click('button[data-tab-id="Microbiological"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_07_tab_microbiological.png', full=True)

        # ─────────────────────────────────────────
        # 7. TAB: Heavy Metals
        # ─────────────────────────────────────────
        print('\n[7] Tab – Heavy Metals')
        pg.click('button[data-tab-id="HeavyMetals"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_08_tab_heavy_metals.png', full=True)

        # ─────────────────────────────────────────
        # 8. TAB: Other Contaminant
        # ─────────────────────────────────────────
        print('\n[8] Tab – Other Contaminant')
        pg.click('button[data-tab-id="OtherContaminant"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_09_tab_other_contaminant.png', full=True)

        # ─────────────────────────────────────────
        # 9. TAB: Food Category
        # ─────────────────────────────────────────
        print('\n[9] Tab – Food Category')
        pg.click('button[data-tab-id="FoodCategory"]')
        pg.wait_for_timeout(600)
        shot(pg, 'ss_10_tab_food_category.png', full=True)

        # ─────────────────────────────────────────
        # 10. MODAL: Universal Input (Add Row)
        # ─────────────────────────────────────────
        print('\n[10] Modal – Universal Input (Add/Edit Row)')
        # Make sure we're on a tab that uses common modal (Organoleptic)
        pg.click('button[data-tab-id="Organoleptic"]')
        pg.wait_for_timeout(400)
        pg.click('#btnAddNewRow')
        pg.wait_for_timeout(800)
        try:
            pg.wait_for_selector('#universalInputModal.show', timeout=5000)
            shot(pg, 'ss_11_modal_universal_input.png', full=False)
        except Exception as e:
            print(f'   [WARN] Modal tidak terbuka: {e}')
        # Close modal
        try:
            pg.click('#universalInputModal .btn-close')
            pg.wait_for_timeout(400)
        except Exception:
            pass

        # ─────────────────────────────────────────
        # 11. MODAL: LOV Oracle Reference
        # ─────────────────────────────────────────
        print('\n[11] LOV – Oracle Reference')
        try:
            # Set refType to ORACLE first
            pg.select_option('#refType', value='ORACLE')
            pg.wait_for_timeout(300)
            pg.click('#btnSearchRef')
            pg.wait_for_timeout(800)
            pg.wait_for_selector('#lovOracleModal.show', timeout=5000)
            shot(pg, 'ss_12_lov_oracle_ref.png', full=False)
            pg.click('#lovOracleModal .btn-close')
            pg.wait_for_timeout(400)
        except Exception as e:
            print(f'   [WARN] LOV Oracle tidak terbuka: {e}')

        # ─────────────────────────────────────────
        # 12. MODAL: LOV RM Evaluation Reference
        # ─────────────────────────────────────────
        print('\n[12] LOV – RM Evaluation Reference')
        try:
            pg.select_option('#refType', value='RMEVAL')
            pg.wait_for_timeout(300)
            pg.click('#btnSearchRef')
            pg.wait_for_timeout(800)
            pg.wait_for_selector('#lovRMEvalModal.show', timeout=5000)
            shot(pg, 'ss_13_lov_rmeval_ref.png', full=False)
            pg.click('#lovRMEvalModal .btn-close')
            pg.wait_for_timeout(400)
        except Exception as e:
            print(f'   [WARN] LOV RM Eval tidak terbuka: {e}')

        # ─────────────────────────────────────────
        # 13. ROLE TOGGLE: Simulate QA/QS
        # ─────────────────────────────────────────
        print('\n[13] Detail – Simulate QA/QS Role (toggle aktif)')
        try:
            pg.check('#roleToggle')
            pg.wait_for_timeout(800)
            # Scroll ke header agar keliatan efeknya
            pg.evaluate('window.scrollTo(0, 0)')
            pg.wait_for_timeout(400)
            shot(pg, 'ss_14_detail_qa_role_header.png', full=False)

            # Microbiological tab – tombol edit/delete visible untuk QA
            pg.click('button[data-tab-id="Microbiological"]')
            pg.wait_for_timeout(500)
            shot(pg, 'ss_15_detail_qa_role_micro.png', full=True)
        except Exception as e:
            print(f'   [WARN] Role toggle: {e}')

        pg.close()
        browser.close()

    print('\n[DONE] Semua screenshot tersimpan di:')
    print(f'  {SHOTS_DIR}')
    screenshots = [f for f in os.listdir(SHOTS_DIR) if f.startswith('ss_')]
    screenshots.sort()
    print(f'  Total: {len(screenshots)} file')


if __name__ == '__main__':
    print('=' * 60)
    print('  CAPTURE SCREENSHOTS – Item Spec RM Prototype')
    print('=' * 60)
    run()
