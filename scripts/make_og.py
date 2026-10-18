"""Generate og.png (1200x630) in the site's light theme. Run: python scripts/make_og.py"""
from pathlib import Path
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parent / "fonts"  # gitignored download cache
SRC = "https://github.com/google/fonts/raw/main/ofl/"
FILES = {"InterTight[wght].ttf": "intertight/", "JetBrainsMono[wght].ttf": "jetbrainsmono/"}

BG, TEXT, MUTED, LINE = "#fafaf8", "#111110", "#6b6a66", "#e6e4df"
ACCENT, ACCENT_SOFT = "#2f5bea", "#eef2fe"


def font(name, size, weight):
    path = FONTS / name
    if not path.exists():
        FONTS.mkdir(exist_ok=True)
        urlretrieve(SRC + FILES[name] + name.replace("[", "%5B").replace("]", "%5D"), path)
    f = ImageFont.truetype(str(path), size)
    f.set_variation_by_axes([weight])
    return f


def tracked(draw, xy, text, f, fill, tracking):
    """Draw text with letter-spacing (em), like the site's tight headings."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking * f.size
    return x


img = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(img)
M = 88

# monogram, same as the favicon
d.rounded_rectangle((M, 80, M + 64, 144), radius=14, fill=ACCENT)
d.text((M + 32, 112), "AR", font=font("InterTight[wght].ttf", 30, 700), fill="#fff", anchor="mm")
d.text((M + 88, 112), "Automation, AI tools and web apps", font=font("JetBrainsMono[wght].ttf", 22, 400), fill=MUTED, anchor="lm")

tracked(d, (M - 4, 220), "Aditya Ranjith", font("InterTight[wght].ttf", 128, 700), TEXT, -0.045)
tracked(d, (M, 384), "Developer", font("InterTight[wght].ttf", 52, 500), MUTED, -0.03)

d.line((M, 478, 1200 - M, 478), fill=LINE, width=2)
badge = "USAII Global AI Hackathon winner · SIH 2026 finalist"
bf = font("JetBrainsMono[wght].ttf", 24, 500)
w = bf.getlength(badge)
d.rounded_rectangle((M, 512, M + w + 40, 560), radius=24, fill=ACCENT_SOFT)
d.text((M + 20, 536), badge, font=bf, fill=ACCENT, anchor="lm")

img.save(ROOT / "og.png", optimize=True)
print("wrote", ROOT / "og.png")
