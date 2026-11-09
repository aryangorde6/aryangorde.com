#!/usr/bin/env python3
"""
Build aryangorde.com.

Renders build_src/ into static pages: the home page, one page per feature
(/<slug>/index.html) and a 404, each self-contained (CSS and JS inlined), plus
responsive images, silent video loops, link-preview images and five
self-hosted fonts. No Node, no CDN, no runtime dependencies in the browser.

    python3 build.py              build
    python3 build.py --check      build into a temp dir and diff; non-zero
                                  exit if any page is stale (for CI)
    python3 build.py --serve      build, then serve on :5500 and rebuild on
                                  change

Why a build step for a static page: the content lives in content.py as plain
Python data, so adding a project is appending a dict rather than copy-pasting
a <div>. The build also enforces invariants that are easy to break by hand
and silent when broken:

  1. every class used in a template is actually defined in the CSS
  2. every internal #anchor points at an id that exists
  3. every nav entry matches a real section
  4. one <h1>, no skipped heading levels, no <img> without alt
  5. nothing is fetched from a third-party origin
  6. every figure on the page matches the list it counts
  7. every link to another page of the site lands on a page that exists
  8. every Devanagari letter in the content is in the font subset

Any of those failing fails the build rather than shipping a subtly broken page.
"""

from __future__ import annotations

import argparse
import importlib.util
import filecmp
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("jinja2 is not installed.  pip install -r requirements.txt")

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is not installed.  pip install -r requirements.txt")

ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "build_src"
TEMPLATES = SRC / "templates"
STATIC = SRC / "static"
SRC_IMAGES = SRC / "images"
OUT_IMAGES = ROOT / "images"
SRC_FONTS = SRC / "fonts"
OUT_FONTS = ROOT / "fonts"
REQUIRED_FONTS = [
    "big-shoulders-latin",
    "big-shoulders-symbols",
    "newsreader-latin",
    "newsreader-symbols",
    "anek-devanagari-names",
]
# The Devanagari font is a Google Fonts `text=` subset holding only these
# letters. Change a Hindi name and the subset has to be fetched again:
#   fonts.googleapis.com/css2?family=Anek+Devanagari:wdth,wght@75,700&text=<letters>
DEVANAGARI_SUBSET = "तीसरी शिकायत तीसरा कान जैसा कहा पुकार"
SRC_VIDEO = SRC / "video"
OUT_VIDEO = ROOT / "video"
SRC_OG = SRC / "og"
OUT_OG = ROOT / "og"

# Widths to emit for the portrait. The cover shows it at up to ~750 CSS px;
# the source is 1536 px wide, so the ladder tops out at 1200.
PHOTO_WIDTHS = [480, 760, 1000, 1200]
WEBP_QUALITY = 82
JPEG_QUALITY = 88


# ---------------------------------------------------------------------------
# images
# ---------------------------------------------------------------------------

def build_images(content, out_dir: Path, quiet=False) -> dict:
    """Emit WebP + JPEG derivatives and return the data the template needs.

    Upscaling is deliberately refused: if the source is narrower than a target
    width we skip that width rather than invent detail that isn't there.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    src_path = SRC_IMAGES / content.SITE["photo"]
    if not src_path.exists():
        sys.exit(f"source photo missing: {src_path}")

    im = Image.open(src_path)
    im = im.convert("RGB")
    sw, sh = im.size
    stem = Path(content.SITE["photo"]).stem

    widths = [w for w in PHOTO_WIDTHS if w <= sw]
    # If the source is smaller than every rung, emit its native width so we
    # don't throw away real pixels. If it's larger, the ladder already covers
    # what the layout can use and a source-sized rung would just be dead weight
    # nobody downloads.
    if sw < max(PHOTO_WIDTHS) and sw not in widths:
        widths.append(sw)
    widths = sorted(set(widths))

    if not quiet and max(PHOTO_WIDTHS) > sw:
        skipped = [w for w in PHOTO_WIDTHS if w > sw]
        print(f"  photo source is only {sw}x{sh}px — skipping {skipped} rather than "
              f"upscaling (would invent detail).")
        print("  → a larger original would look sharper on retina screens.")

    webp, jpg, written = [], [], []
    for w in widths:
        h = round(sh * w / sw)
        resized = im.resize((w, h), Image.LANCZOS)

        wp = out_dir / f"{stem}-{w}.webp"
        resized.save(wp, "WEBP", quality=WEBP_QUALITY, method=6)
        webp.append(f"/images/{wp.name} {w}w")
        written.append(wp)

        jp = out_dir / f"{stem}-{w}.jpg"
        resized.save(jp, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        jpg.append(f"/images/{jp.name} {w}w")
        written.append(jp)

    largest = max(widths)
    if not quiet:
        total = sum(p.stat().st_size for p in written)
        print(f"  images: {len(written)} files, {total/1024:.0f} KB total "
              f"({', '.join(str(w) for w in widths)}px)")

    initials = "".join(part[0] for part in content.SITE["name"].split()[:2]).upper()
    return {
        "webp_srcset": ", ".join(webp),
        "jpg_srcset": ", ".join(jpg),
        "fallback": f"images/{stem}-{largest}.jpg",
        "og": f"images/{stem}-{largest}.jpg",
        "width": sw,
        "height": sh,
        "alt": content.SITE["photo_alt"],
        "initials": initials,
    }


def build_award_images(content, out_dir: Path, quiet=False) -> dict:
    """WebP + JPEG of each award detail (crops of the organisers' graphics).

    Native size only: the crops are small, and upscaling would invent detail.
    `pct` is each part's width relative to the first part of its figure, so the
    header and the row keep the graphic's own scale on the page.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    awards, written = {}, []
    for r in content.RESULTS:
        proof = r.get("proof")
        if not proof:
            continue
        ref_w = None
        for part in proof["parts"]:
            name = part["name"]
            src = SRC_IMAGES / "awards" / f"{name}.png"
            if not src.exists():
                sys.exit(f"award image missing: {src}")
            im = Image.open(src).convert("RGB")
            w, h = im.size
            ref_w = ref_w or w
            wp, jp = out_dir / f"award-{name}.webp", out_dir / f"award-{name}.jpg"
            im.save(wp, "WEBP", quality=WEBP_QUALITY, method=6)
            im.save(jp, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            written += [wp, jp]
            awards[name] = {"webp": f"images/{wp.name}", "jpg": f"images/{jp.name}",
                            "w": w, "h": h, "pct": round(100 * w / ref_w, 2)}
    if not quiet and written:
        total = sum(p.stat().st_size for p in written)
        print(f"  award details: {len(written)} files, {total/1024:.0f} KB total")
    return awards


# ---------------------------------------------------------------------------
# video loops and link previews
# ---------------------------------------------------------------------------

def build_videos(out_dir: Path) -> dict:
    """Copy the silent loops and their posters; return {name: paths + size}.

    The clips are cut by hand from Aryan's own demo recordings (see README):
    8 s, muted, H.264, every distinct frame checked for phone numbers and for
    other people's faces or names before it was added.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    videos = {}
    for mp4 in sorted(SRC_VIDEO.glob("*.mp4")):
        poster = mp4.with_suffix(".jpg")
        if not poster.exists():
            sys.exit(f"poster missing for {mp4.name}: {poster}")
        for f in (mp4, poster):
            dest = out_dir / f.name
            if not dest.exists() or not filecmp.cmp(f, dest, shallow=False):
                shutil.copyfile(f, dest)
        w, h = Image.open(poster).size
        videos[mp4.stem] = {"mp4": f"video/{mp4.name}", "poster": f"video/{poster.name}", "w": w, "h": h}
    return videos


def copy_og(out_dir: Path, needed: list[str]) -> None:
    """Copy the link-preview images (made by og.py, committed) and insist on
    one for every page."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in needed:
        src = SRC_OG / f"{name}.jpg"
        if not src.exists():
            sys.exit(f"link-preview image missing: {src}  (run: python3 og.py)")
        dest = out_dir / src.name
        if not dest.exists() or not filecmp.cmp(src, dest, shallow=False):
            shutil.copyfile(src, dest)


def prune(out_dir: Path, keep: set[str], pattern: str) -> None:
    """Delete generated files the build no longer makes, so deploy.sh's
    `--delete` doesn't keep serving them."""
    for f in out_dir.glob(pattern):
        if f.name not in keep:
            f.unlink()


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def defined_css_classes(css: str) -> set[str]:
    """Class names the stylesheet defines, un-escaping CSS identifier escapes."""
    found = set()
    for m in re.finditer(r"\.((?:[A-Za-z0-9_-]|\\.)+)", css):
        found.add(re.sub(r"\\(.)", r"\1", m.group(1)))
    return found


def used_html_classes(html: str) -> set[str]:
    body = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    used = set()
    for m in re.finditer(r'class="([^"]*)"', body):
        used.update(m.group(1).split())
    return used


def page_ids(html: str) -> set[str]:
    return set(re.findall(r'\bid="([^"]+)"', html))


def check_page(name: str, html: str, css: str) -> list[str]:
    """Checks that hold for every page on its own."""
    problems = []
    for cls in sorted(used_html_classes(html) - defined_css_classes(css)):
        problems.append(f"{name}: class '{cls}' is used in markup but not defined in CSS")

    ids = page_ids(html)
    for href in set(re.findall(r'href="#([^"]+)"', html)):
        if href not in ids:
            problems.append(f"{name}: anchor '#{href}' points at an id that doesn't exist")

    levels = [int(m) for m in re.findall(r"<h([1-6])\b", html)]
    if levels.count(1) != 1:
        problems.append(f"{name}: expected exactly one <h1>, found {levels.count(1)}")
    for a, b in zip(levels, levels[1:]):
        if b - a > 1:
            problems.append(f"{name}: heading level jumps from h{a} to h{b}")
            break

    for tag in re.findall(r"<img\b[^>]*>", html):
        if "alt=" not in tag:
            problems.append(f"{name}: <img> without alt: {tag[:70]}")

    # Nothing the browser loads by itself (src=, <link href>, CSS url()) may
    # come from another origin. Outbound <a href> links are fine.
    loaded = re.findall(r'\bsrc="(https?://[^"]+)"', html)
    loaded += [m.group(1) for m in re.finditer(r'<link\b[^>]*\bhref="(https?://[^"]+)"[^>]*>', html)
               if 'rel="canonical"' not in m.group(0)]
    loaded += re.findall(r'url\(\s*["\']?(https?://[^)"\']+)', html)
    for url in loaded:
        if "aryangorde.com" not in url:
            problems.append(f"{name}: page would fetch a third-party resource: {url}")
    return problems


def check_site(pages: dict, content) -> list[str]:
    """Checks across pages: nav, cross-page links, figures, the font subset."""
    problems = []
    home = pages["index.html"]
    home_ids = page_ids(home)
    section_ids = set(re.findall(r'<section[^>]*\bid="([^"]+)"', home))
    for nav_id, label in content.NAV:
        if nav_id not in section_ids:
            problems.append(f"nav entry '{label}' -> #{nav_id} has no matching section")

    # Links to other pages of this site: "/", "/slug/", "/#id", "/slug/#id".
    for name, html in pages.items():
        for path, frag in re.findall(r'href="(/[a-z0-9-]*/?)(?:#([^"]+))?"', html):
            if path == "/":
                target = "index.html"
            elif path.endswith("/"):
                target = path.strip("/") + "/index.html"
            else:
                continue                            # a file: /Aryan_Gorde_Resume.pdf
            if target not in pages:
                problems.append(f"{name}: link to {path} but no page is built there")
            elif frag and frag not in page_ids(pages[target]):
                problems.append(f"{name}: link to {path}#{frag} but that page has no such id")
    for path in re.findall(r'href="(/[^"#]+\.[a-z0-9]+)"', "".join(pages.values())):
        if not (ROOT / path.lstrip("/")).exists():
            problems.append(f"link to {path} but there is no such file")

    year = "2026"
    counts = {
        "changelog_2026": sum(1 for e in content.CHANGELOG if e["period"].endswith(year)),
        "results": len(content.RESULTS),
        "certifications": len(content.CERTIFICATIONS),
    }
    for f in content.FIGURES:
        key = f.get("check")
        if key and f["value"] != counts[key]:
            problems.append(f"figure '{f['label']}' says {f['value']} but {key} counts {counts[key]}")

    used = set(re.findall(r"[ऀ-ॿ]", "".join(pages.values())))
    missing = used - set(DEVANAGARI_SUBSET)
    if missing:
        problems.append("Devanagari letters not in the font subset: " + " ".join(sorted(missing))
                        + " (fetch a new subset, see DEVANAGARI_SUBSET)")
    return problems


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------

def load_module(name: str, src: Path):
    """Import a build_src module fresh, every time.

    Deliberately bypasses __pycache__. Python invalidates bytecode on
    (mtime, size), and content edits that keep the byte length identical can
    slip through that check and silently rebuild from the previous version's
    data. A build tool must never do that.
    """
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, src)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_content():
    return load_module("site_content", SRC / "content.py")


def copy_fonts(out_dir: Path) -> dict:
    """Copy the self-hosted webfonts; return {stem: "fonts/<file>"}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    found = {}
    for f in sorted(SRC_FONTS.glob("*.woff2")):
        dest = out_dir / f.name
        if not dest.exists() or not filecmp.cmp(f, dest, shallow=False):
            shutil.copyfile(f, dest)
        found[f.stem] = f"fonts/{f.name}"
    for need in REQUIRED_FONTS:
        if need not in found:
            sys.exit(f"font missing: build_src/fonts/{need}.woff2")
    prune(out_dir, {Path(v).name for v in found.values()}, "*.woff2")
    return found


def build(out_root: Path, quiet=False) -> dict:
    """Render every page into out_root. Returns {relative path: html}."""
    content = load_content()
    drawings = load_module("site_drawings", SRC / "drawings.py")

    css = (STATIC / "css" / "site.css").read_text(encoding="utf-8")
    js = (STATIC / "js" / "site.js").read_text(encoding="utf-8")

    out_images = out_root / "images"
    photo = build_images(content, out_images, quiet=quiet)
    awards = build_award_images(content, out_images, quiet=quiet)
    prune(out_images, {Path(x.split()[0]).name for x in (photo["webp_srcset"] + ", " + photo["jpg_srcset"]).split(", ")}
          | {Path(a[k]).name for a in awards.values() for k in ("webp", "jpg")}, "*.*")
    videos = build_videos(out_root / "video")
    fonts = copy_fonts(out_root / "fonts")
    features = content.FEATURES
    copy_og(out_root / "og", ["home"] + [f["slug"] for f in features])

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        undefined=StrictUndefined,      # a typo'd variable fails the build
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,               # content.py holds intentional markup
    )
    common = dict(
        site=content.SITE, nav=content.NAV, hero=content.HERO, about=content.ABOUT,
        figures=content.FIGURES, results=content.RESULTS, truncation=content.TRUNCATION,
        upstream=content.UPSTREAM, entries=content.ENTRIES, stack=content.STACK,
        languages=content.LANGUAGES, features=features, changelog=content.CHANGELOG,
        education=content.EDUCATION, certifications=content.CERTIFICATIONS,
        contact=content.CONTACT, colophon=content.COLOPHON, fonts=fonts, photo=photo,
        awards=awards, videos=videos, tripwire=drawings.tripwire_homes(),
        css=css, js=js, year=datetime.now().year,
    )
    site = content.SITE
    pages = {}

    home = {"title": site["title"], "description": site["description"],
            "og_description": site["og_description"], "path": "/", "og": "/og/home.jpg",
            "og_alt": f"{site['name']}, {site['role'].lower()}", "hindi": True}
    pages["index.html"] = env.get_template("index.html.j2").render(page=home, **common)

    for i, f in enumerate(features):
        page = {"title": f"{f['name']} · {site['name']}", "description": f["teaser"],
                "og_description": f["teaser"], "path": f"/{f['slug']}/",
                "og": f"/og/{f['slug']}.jpg", "og_alt": f"{f['name']}, a build by {site['name']}",
                "hindi": bool(f.get("hindi"))}
        pages[f"{f['slug']}/index.html"] = env.get_template("feature.html.j2").render(
            page=page, feature=f, feature_index=i, **common)

    nf = {"title": f"Not in this issue · {site['name']}", "description": site["description"],
          "og_description": site["og_description"], "path": "/404.html", "og": "/og/home.jpg",
          "og_alt": home["og_alt"], "hindi": False}
    pages["404.html"] = env.get_template("404.html.j2").render(page=nf, **common)

    problems = []
    for name, html in pages.items():
        problems += check_page(name, html, css)
    problems += check_site(pages, content)
    if problems:
        print("\n  BUILD FAILED: the site would be subtly broken:\n", file=sys.stderr)
        for p in problems:
            print(f"    ✗ {p}", file=sys.stderr)
        print(file=sys.stderr)
        sys.exit(1)

    for name, html in pages.items():
        dest = out_root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
    return pages


def report(pages: dict):
    for name, html in pages.items():
        raw = html.encode()
        gz = len(subprocess.run(["gzip", "-c"], input=raw, capture_output=True).stdout)
        print(f"  {name}: {len(raw)/1024:.1f} KB ({gz/1024:.1f} KB gzipped)")
    font_kb = sum(p.stat().st_size for p in (ROOT / "fonts").glob("*.woff2")) / 1024
    vid_kb = sum(p.stat().st_size for p in (ROOT / "video").glob("*.mp4")) / 1024
    print(f"  fonts {font_kb:.0f} KB · video loops {vid_kb:.0f} KB (loaded only when on screen)")
    print("  checks passed: classes, anchors, cross-page links, nav, headings, alt text, "
          "no third-party fetches, figures, Devanagari subset")


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Build aryangorde.com")
    ap.add_argument("--check", action="store_true",
                    help="verify the built pages are up to date; non-zero exit if stale")
    ap.add_argument("--serve", action="store_true",
                    help="build, serve on :5500, rebuild on file change")
    args = ap.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as td:
            pages = build(Path(td), quiet=True)
            stale = [n for n in pages
                     if not (ROOT / n).exists() or not filecmp.cmp(Path(td) / n, ROOT / n, shallow=False)]
            if stale:
                sys.exit("STALE: " + ", ".join(stale) + "  (rebuild with: python3 build.py)")
            print(f"all {len(pages)} pages are up to date with build_src/")
            return

    print("building…")
    pages = build(ROOT)
    report(pages)
    print("done.")

    if args.serve:
        import http.server, socketserver, threading, time
        watched = [p for p in SRC.rglob("*") if p.suffix in {".j2", ".css", ".js", ".py"}]

        def watch():
            stamps = {p: p.stat().st_mtime for p in watched if p.exists()}
            while True:
                time.sleep(0.5)
                for p in watched:
                    if not p.exists():
                        continue
                    m = p.stat().st_mtime
                    if stamps.get(p) != m:
                        stamps[p] = m
                        print(f"\n{p.relative_to(ROOT)} changed, rebuilding…")
                        try:
                            report(build(ROOT, quiet=True))
                        except SystemExit as e:
                            print(f"  build failed: {e}")

        threading.Thread(target=watch, daemon=True).start()
        handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
            *a, directory=str(ROOT), **kw)
        with socketserver.TCPServer(("", 5500), handler) as httpd:
            print("\nserving http://localhost:5500  (ctrl-c to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nstopped.")


if __name__ == "__main__":
    main()
