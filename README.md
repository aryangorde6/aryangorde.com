# aryangorde.com

Personal portfolio for Aryan Gorde — backend & full-stack developer.
Built with Python. Served as static files from AWS (a private S3 bucket behind CloudFront).

**Design:** an engineering drawing. The page is a set of numbered drafting
sheets — warm paper with a fine grid, ink linework, mono annotation and a
single signal-orange accent that means "live". The stack is drawn as the
system it actually forms, with packets travelling along the wires.

---

## Build

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 build.py
```

That renders `build_src/` into a single self-contained `index.html`, plus
responsive image derivatives in `images/` and the self-hosted fonts in
`fonts/`.

| Command | What it does |
| --- | --- |
| `python3 build.py` | Build `index.html` + images + fonts |
| `python3 build.py --serve` | Build, serve on :5500, rebuild on file change |
| `python3 build.py --check` | Fail (non-zero exit) if `index.html` is stale — for CI |

## Why a build step for a static page

The content lives in `build_src/content.py` as plain Python data. Adding a
build to the changelog is appending a dict, not copy-pasting a `<div>`. The
stack diagram and the Teesri Shikayat ring are computed in
`build_src/drawings.py`, so the browser receives finished SVG. The build also enforces invariants that are easy to break by
hand and silent when broken:

1. every CSS class used in markup is actually defined in the stylesheet
2. every internal `#anchor` points at an id that exists
3. every nav entry matches a real section
4. exactly one `<h1>`, no skipped heading levels, no `<img>` without `alt`
5. nothing is *fetched* from a third-party origin (`src=`, `<link href>`, CSS
   `url()`); outbound `<a href>` links are fine, since clicking one isn't a
   request the page makes
6. every figure with a `check` key in `FIGURES` matches what it counts (builds
   in `CHANGELOG`, prizes in `RESULTS`, `CERTIFICATIONS`)

Any of those failing **fails the build** rather than shipping a subtly broken
page.

## Layout

```
build.py                     the build
requirements.txt             jinja2, pillow
build_src/
  content.py                 ← all the words live here
  drawings.py                geometry for the stack diagram and the ring
  templates/
    base.html.j2             page skeleton, <head>, fonts, inlining
    index.html.j2            section order
    macros.html.j2           sheet header, chips, external links
    sections/*.html.j2       one file per section, plus the ⌘K menu
  static/
    css/site.css             the design system
    js/site.js               behaviour (progressive enhancement only)
  fonts/*.woff2              Archivo, Instrument Serif, JetBrains Mono (OFL)
  images/aryan.jpg           source photo (build resizes it)
  images/awards/*.png        crops of the two winners graphics (header + own row only)

index.html                   ← GENERATED, do not edit
images/aryan-*.{webp,jpg}    ← GENERATED
images/award-*.{webp,jpg}    ← GENERATED
fonts/*.woff2                ← GENERATED (copied from build_src/fonts)
```

## The sheets

| § | Sheet | What's on it |
| --- | --- | --- |
| 00 | Index | Name in expanded type with the portrait set inline, a dimension line, then the year's two hackathon prizes as stamped plates — the centre of the first screen on desktop and phone — and a drawing note for the fixes merged upstream. Blurb, buttons and the drawing's title block follow. A CAD crosshair follows the cursor. |
| 01 | About | Lede, bio, spec table, four figures (each checked against the page by the build). |
| 02 | Results | The 2026 hackathon prizes as stamped cards (runner-up at WeMakeDevs × AWS Environmental Hacks; winner, 3rd place, at the Rote Playoffs Hackathon), and every other entry in a log. Each prize card carries a detail of the organisers' own winners graphic (header + Aryan's row only, joined by a break line; the other winners' photos are cut out). Between them, "Merged upstream": fixes accepted into NumPy (#32915) and Pillow (#10147, shipped in 13.0.0). The hero plates link here and to the case study. |
| 03 | Stack | Every tool, drawn as a request path: client → edge → application → data / async / AI, inside a runtime boundary, with CI/CD shipping into it. |
| 04 | Work | Teesri Shikayat on an ink sheet — the 250 m ring and the case flow; Teesra Kaan with a scam call drawn to scale (each predicted line, and how far ahead it came); Shaky Ground with how a citation chain is scored; Jaisa Kaha as a flow through its Discord room. |
| 05 | Changelog | Every 2026 build as a commit rail (prize tags on placed entries), with education and certifications alongside. |
| 06 | Contact | Headline, email with copy, live Mumbai time, link rows. The footer is the drawing's title block. |

Hackathon facts come from `~/rote_hack/HACKATHON-HANDOFF.md` and each
project's own README or overview (fetched from GitHub). Upstream facts come from the pull requests
themselves and the projects' release notes. An entry's outcome says only what is known
("Submitted" claims nothing more).

The Teesri Shikayat ring is a **schematic** of the recorded demo incident: the
counts (3 reported, 23 warned, 20 of them never complained) are the demo's,
the positions are illustrative and seeded so the build stays deterministic.

The Teesra Kaan timeline is the one call re-enacted by people on a real phone
line, captioned as an example outside the frozen test. The Shaky Ground chain
is a **schematic**: the weights and threshold are the project's, the papers are
illustrative.

**Only projects from [github.com/aryangorde6](https://github.com/aryangorde6)
appear on the site.**

## Type and colour

Fonts are self-hosted from `fonts/` (same origin), so the page still makes
zero third-party requests.

- **Archivo** (variable width + weight) — titles at 120–125% width, body at 100%
- **JetBrains Mono** — annotation, labels, chips
- **Instrument Serif italic** — emphasis only (`<em>` in content.py)

| Pair | Ratio |
| --- | --- |
| ink `#121211` on paper `#f1efe8` | 16.3 : 1 |
| muted `#5b5951` on paper | 6.1 : 1 |
| accent-ink `#b8320a` on paper | 5.2 : 1 |
| accent `#ff4f1a` on ink | 5.7 : 1 |
| ink on accent | 5.7 : 1 |
| on-ink-muted `#a9a69c` on ink | 7.7 : 1 |

The bright accent is never used for small text on paper; that's what
`--accent-ink` is for.

## Output

`index.html` is ~152 KB (~36 KB gzipped) with CSS and JS inlined. First load is
roughly 200 KB including one photo derivative and ~140 KB of fonts.

## Accessibility

- Motion is decided before first paint from `prefers-reduced-motion`. With
  reduced motion nothing animates; the diagram starts paused and offers Play.
- The looping diagram has a visible Pause control (WCAG 2.2.2) and only runs
  while on screen. The Jaisa Kaha flow sweeps once (~2.5 s) and stops.
- Scroll reveals disarm themselves if `IntersectionObserver` never delivers,
  so content can never be stranded at `opacity: 0`.
- The diagram's boxes are real HTML, not SVG text, and reflow into a vertical
  flow on small screens.
- The ⌘K / Ctrl-K / `/` menu is a native `<dialog>` with a combobox + listbox.
  It is JS-only; without JS the nav links scroll horizontally on phones.
- Skip link, semantic landmarks, one `h1`, no skipped heading levels.

## Deployment

AWS, defined in [`infra/site.yaml`](infra/site.yaml) (CloudFormation, stack
`aryangorde-site` in ap-south-1):

- a **private S3 bucket** in Mumbai: no public access, versioned (old versions kept 30 days);
- **CloudFront** in front of it: HTTPS with a free ACM certificate (us-east-1), HTTP/2 and
  HTTP/3, gzip/brotli, security headers, `www` → bare-domain 301 redirect (a CloudFront
  Function), and unknown paths answered with the home page and a 404 status.

DNS stays at Hostinger: `@` is an ALIAS and `www` a CNAME to the distribution's
`*.cloudfront.net` name (see [`infra/HOSTINGER_DNS.md`](infra/HOSTINGER_DNS.md)).

To publish a change:

```bash
python3 build.py && infra/deploy.sh
```

`deploy.sh` checks that `index.html` matches `build_src/` and that the public résumé is the
copy without the phone number, uploads **only** `index.html`, the résumé PDF, `images/` and
`fonts/`, sets cache headers (page and PDF 5 minutes, images and fonts a week) and clears
CloudFront's cache. Nothing else in the repo is ever served.

Cost: CloudFront's always-free allowance (1 TB and 10 million requests a month) covers a
portfolio; S3 storage for a few MB is a fraction of a cent.
