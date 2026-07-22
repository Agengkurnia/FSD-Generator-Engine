"""Capture full-page + button screenshots from Mockup_AnalyticalCentral."""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

MOCKUP = Path(r"D:\Work\Source\Sample Result GVN-SHP Integration\Mockup_AnalyticalCentral")
OUT = Path(__file__).resolve().parent / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("transaction_cms.html", "ss_01_transaction_list.png"),
    ("request_create_cms.html", "ss_02_request_create.png"),
    ("request_detail_cms.html", "ss_03_request_detail.png"),
    ("result_sample_gvn_list_cms.html", "ss_04_result_list.png"),
    ("result_sample_gvn_create_cms.html", "ss_05_result_create.png"),
    ("result_sample_gvn_cms.html", "ss_06_result_edit.png"),
]

# (html, selector, out_name, wait_ms_extra)
BUTTONS = [
    ("transaction_cms.html", "#btnNewTransaction", "ss_btn_trx_new.png", 500),
    (
        "transaction_cms.html",
        "table tbody tr:first-child a.btn-primary",
        "ss_btn_trx_edit.png",
        500,
    ),
    (
        "request_create_cms.html",
        "button.btn-primary[onclick=\"saveData()\"]",
        "ss_btn_req_save.png",
        800,
    ),
    (
        "request_create_cms.html",
        "button.btn-success[onclick=\"submitRequest()\"]",
        "ss_btn_req_submit.png",
        800,
    ),
    (
        "request_create_cms.html",
        "a.btn-danger[href=\"./transaction_cms.html\"]",
        "ss_btn_req_back.png",
        800,
    ),
    (
        "request_detail_cms.html",
        "button.btn-primary[onclick*=\"save\"], button.btn-primary:has-text(\"Save\")",
        "ss_btn_det_save.png",
        800,
    ),
    (
        "request_detail_cms.html",
        "a.btn-danger[href=\"./transaction_cms.html\"], a.btn:has-text(\"Back\")",
        "ss_btn_det_back.png",
        800,
    ),
    (
        "result_sample_gvn_list_cms.html",
        "#btnNewTransaction, a.btn:has-text(\"New\")",
        "ss_btn_res_new.png",
        1500,
    ),
    (
        "result_sample_gvn_list_cms.html",
        "table tbody tr:first-child a.btn, a:has-text(\"Input Result\")",
        "ss_btn_res_input.png",
        1500,
    ),
    (
        "result_sample_gvn_create_cms.html",
        "button.btn-primary[onclick=\"saveData()\"], button:has-text(\"Save\")",
        "ss_btn_resc_save.png",
        1500,
    ),
    (
        "result_sample_gvn_create_cms.html",
        "button.btn-success[onclick=\"syncResult()\"], button:has-text(\"Sync\")",
        "ss_btn_resc_sync.png",
        1500,
    ),
    (
        "result_sample_gvn_cms.html",
        "button.btn-primary[onclick=\"saveData()\"], button:has-text(\"Save\")",
        "ss_btn_rese_save.png",
        800,
    ),
    (
        "result_sample_gvn_cms.html",
        "button.btn-success[onclick=\"syncResult()\"], button:has-text(\"Sync\")",
        "ss_btn_rese_sync.png",
        800,
    ),
]


def file_url(html: str) -> str:
    return (MOCKUP / html).resolve().as_uri()


def shot_page(page, html: str, fname: str) -> None:
    page.goto(file_url(html), wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    # Allow fetch JSON to settle on result pages
    page.wait_for_timeout(1500)
    out = OUT / fname
    page.screenshot(path=str(out), full_page=True)
    print(f"PAGE  {out.name}  ({out.stat().st_size} bytes)")


def shot_btn(page, html: str, selector: str, fname: str, wait_extra: int) -> None:
    page.goto(file_url(html), wait_until="domcontentloaded")
    page.wait_for_timeout(2000 + wait_extra)
    loc = page.locator(selector).first
    try:
        loc.wait_for(state="visible", timeout=8000)
        out = OUT / fname
        loc.screenshot(path=str(out))
        print(f"BTN   {out.name}  ({out.stat().st_size} bytes)")
    except Exception as exc:
        print(f"SKIP  {fname}  selector={selector!r}  err={exc}")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        for html, fname in PAGES:
            shot_page(page, html, fname)
        for html, sel, fname, wait_extra in BUTTONS:
            shot_btn(page, html, sel, fname, wait_extra)
        browser.close()
    print("Done. Output:", OUT)


if __name__ == "__main__":
    main()
