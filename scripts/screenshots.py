"""Full-page screenshots at 4 widths x 2 themes, with overflow check.
Usage: python scripts/screenshots.py [url] [out_dir] [widths]
Default url is the local index.html."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
url = sys.argv[1] if len(sys.argv) > 1 else (ROOT / "index.html").as_uri()
out = Path(sys.argv[2] if len(sys.argv) > 2 else ROOT / "screenshots")
widths = [int(w) for w in sys.argv[3].split(",")] if len(sys.argv) > 3 else [1440, 1024, 768, 390]
out.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        for w in widths:
            page = browser.new_page(viewport={"width": w, "height": 900})
            page.add_init_script(f"localStorage.setItem('theme','{theme}')")
            page.goto(url, wait_until="networkidle")
            page.add_style_tag(content=".reveal{opacity:1!important;transform:none!important;transition:none!important}")
            page.evaluate("document.fonts.ready")
            sw = page.evaluate("document.documentElement.scrollWidth")
            flag = "  <-- HORIZONTAL OVERFLOW" if sw > w else ""
            page.screenshot(path=str(out / f"{theme}-{w}.png"), full_page=True)
            print(f"{theme}-{w}: scrollWidth={sw}{flag}")
            page.close()
    browser.close()
