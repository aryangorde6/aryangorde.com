#!/usr/bin/env python3
"""
Make the link-preview images (Open Graph, 1200 × 630) for every page.

    python3 og.py

Each one is a magazine cover: black, the colour portrait on the right, a
yellow chip, and the page's name set big (the Devanagari name over the Latin
one for a feature that has it). Headless Chrome renders them from the same
fonts and content as the site, into build_src/og/<page>.jpg. They're
committed, and build.py copies them into og/ and fails if one is missing.

Run it again after changing a name, a kicker or the portrait. It's separate
from build.py because Chrome's output isn't byte-identical between versions,
and `build.py --check` has to be.

Needs: google-chrome (or chromium) on PATH, Pillow.
"""

from __future__ import annotations

import base64
import html
import io
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "build_src"
OUT = SRC / "og"
W, H = 1200, 630

sys.path.insert(0, str(SRC))
sys.dont_write_bytecode = True
import content  # noqa: E402


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def portrait_uri() -> str:
    im = Image.open(SRC / "images" / content.SITE["photo"]).convert("RGB")
    im = im.resize((760, round(im.height * 760 / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# Fonts go in as data: URIs. A file:// page may not load fonts from other
# file:// URLs in Chrome.
FONTS = {name: data_uri(SRC / "fonts" / f"{name}.woff2", "font/woff2") for name in (
    "big-shoulders-latin", "big-shoulders-symbols", "newsreader-latin", "anek-devanagari-names")}

CSS = """
@font-face { font-family: "BS"; src: url(%(big-shoulders-latin)s) format("woff2"); font-weight: 600 900; }
@font-face { font-family: "BS"; src: url(%(big-shoulders-symbols)s) format("woff2"); font-weight: 600 900;
             unicode-range: U+20B9, U+2190-2193, U+2197, U+2212; }
@font-face { font-family: "NR"; src: url(%(newsreader-latin)s) format("woff2"); font-weight: 400 700; }
@font-face { font-family: "AD"; src: url(%(anek-devanagari-names)s) format("woff2"); font-weight: 700; font-stretch: 75%%; }
* { margin: 0; box-sizing: border-box; }
html, body { width: 1200px; height: 630px; overflow: hidden; background: #0b0b0b; color: #f4f4f4; }
body { position: relative; font-family: "NR", Georgia, serif; -webkit-font-smoothing: antialiased; }
.photo { position: absolute; top: 0; right: 0; bottom: 0; width: 600px;
         background: url(%(photo)s) center 20%% / cover no-repeat;
         filter: contrast(1.06) saturate(1.08);
         -webkit-mask-image: linear-gradient(90deg, transparent 0%%, rgba(0,0,0,.6) 22%%, #000 50%%); }
.fade { position: absolute; top: 0; right: 0; bottom: 0; width: 600px;
        background: linear-gradient(0deg, #0b0b0b 0%%, rgba(11,11,11,0) 34%%); }
.body { position: absolute; left: 64px; top: 56px; right: 64px; bottom: 52px; display: flex; flex-direction: column; }
.site { font: 800 22px/1 "BS"; letter-spacing: .08em; text-transform: uppercase; color: #ececec; }
.chip { align-self: flex-start; margin-top: 28px; padding: 6px 11px 5px; background: #ffd60a; color: #0b0b0b;
        font: 800 22px/1 "BS"; letter-spacing: .08em; text-transform: uppercase; }
.hi { margin-top: 20px; font: 700 132px/1.12 "AD"; font-stretch: 75%%; }
.en { max-width: 560px; font: 900 150px/.82 "BS"; text-transform: uppercase; letter-spacing: -.01em; margin-top: 22px; }
.hi + .en { margin-top: 0; font-size: 50px; line-height: 1; font-weight: 800; letter-spacing: .05em; color: #ffd60a; }
.name { font: 900 196px/.8 "BS"; text-transform: uppercase; letter-spacing: -.01em; margin-top: 30px; }
.name span { display: block; }
.name span + span { padding-left: .32em; }
.line { margin-top: auto; max-width: 640px; font-size: 27px; line-height: 1.3; color: #d6d6d6; }
.line b { font-weight: 600; color: #f4f4f4; }
"""


def page(inner: str, photo: str) -> str:
    css = CSS % dict(FONTS, photo=photo)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head>"
            f"<body><div class='photo'></div><div class='fade'></div><div class='body'>{inner}</div>"
            f"</body></html>")


def covers() -> dict[str, str]:
    e = html.escape
    out = {}
    r = {x["id"]: x for x in content.RESULTS}
    out["home"] = (
        f"<p class='site'>aryangorde.com</p>"
        f"<p class='chip'>{e(content.SITE['role'])}</p>"
        f"<h1 class='name'><span>{e(content.HERO['first_name'])}</span><span>{e(content.HERO['last_name'])}</span></h1>"
        f"<p class='line'><b>{e(r['env-hacks']['rank'])}</b>, {e(r['env-hacks']['event'])}. "
        f"<b>{e(r['rote']['rank_full'].replace(' · ', ', '))}</b>, {e(r['rote']['event'])}. "
        f"Fixes merged into NumPy and Pillow.</p>"
    )
    for f in content.FEATURES:
        kicker = f["kicker"].split(" · ")[0]
        names = (f"<p class='hi' lang='hi'>{e(f['hindi'])}</p>" if f.get("hindi") else "")
        names += f"<p class='en'>{e(f['name'])}</p>"
        fig = f["figures"][0]
        out[f["slug"]] = (
            f"<p class='site'>aryangorde.com · {e(content.SITE['name'])}</p>"
            f"<p class='chip'>{e(kicker)}</p>{names}"
            f"<p class='line'><b>{e(fig['value'])}</b> {e(fig['note'])}</p>"
        )
    return out


def chrome() -> str:
    for exe in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(exe):
            return exe
    sys.exit("og.py needs Chrome or Chromium on PATH")


def main():
    exe = chrome()
    photo = portrait_uri()
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for name, inner in covers().items():
            src = td / f"{name}.html"
            png = td / f"{name}.png"
            src.write_text(page(inner, photo), encoding="utf-8")
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size={W},{H}",
                            "--virtual-time-budget=4000", f"--screenshot={png}", src.as_uri()],
                           check=True, capture_output=True)
            im = Image.open(png).convert("RGB")
            if im.size != (W, H):
                im = im.crop((0, 0, W, H))
            dest = OUT / f"{name}.jpg"
            im.save(dest, "JPEG", quality=86, optimize=True, progressive=True)
            print(f"  {dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
