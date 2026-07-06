import os
from playwright.sync_api import sync_playwright

base_dir = r"d:\Work\Source\RMSelection Hijrah\NewRMSelection"
out_dir  = os.path.join(base_dir, "Document", "FSD", "screenshots")
os.makedirs(out_dir, exist_ok=True)

pages = [
    ("ProjectIdentityIndex.html",           "ss_index.png"),
    ("ProjectIdentityDetail.html",          "ss_detail.png"),
    ("ProjectIdentityDocumentApproval.html","ss_approval.png"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()
    for html, fname in pages:
        url = "file:///" + os.path.join(base_dir, html).replace("\\", "/")
        page.goto(url)
        page.wait_for_timeout(3000)
        out_path = os.path.join(out_dir, fname)
        page.screenshot(path=out_path, full_page=True)
        print(f"Saved: {out_path}")
    browser.close()

print("Done.")
