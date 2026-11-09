# aryangorde.com

Personal portfolio for Aryan Gorde, backend and full-stack developer.
Built with Python. Served as static files from AWS (a private S3 bucket behind CloudFront).

**Design:** a magazine. Black pages with white type, a cool white "paper" for the record
(prizes, open source, everything shipped) and a yellow back cover. The home page is the
cover: the name set huge over a colour portrait, three cover lines and a deck. Each build
gets its own feature page, with its Hindi name set big in the headline.

---

## Build

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 build.py
```

That renders `build_src/` into static pages, each self-contained (CSS and JS inlined):
`index.html`, one `<slug>/index.html` per feature and `404.html`. Alongside them: responsive
photo derivatives in `images/`, the self-hosted fonts in `fonts/`, the silent loops in
`video/` and the link-preview images in `og/`.

| Command | What it does |
| --- | --- |
| `python3 build.py` | Build every page + images + fonts + loops + link previews |
| `python3 build.py --serve` | Build, serve on :5500, rebuild on file change |
| `python3 build.py --check` | Fail (non-zero exit) if any page is stale (for CI) |
| `python3 og.py` | Re-render the link-preview images with headless Chrome |

## Why a build step for a static page

The content lives in `build_src/content.py` as plain Python data. Adding a build to the
changelog is appending a dict; adding a feature page is appending a dict to `FEATURES`. The
build also enforces invariants that are easy to break by hand and silent when broken:

1. every CSS class used in markup is actually defined in the stylesheet
2. every internal `#anchor` points at an id that exists
3. every nav entry matches a real section
4. exactly one `<h1>`, no skipped heading levels, no `<img>` without `alt`
5. nothing is *fetched* from a third-party origin (`src=`, `<link href>`, CSS
   `url()`); outbound `<a href>` links are fine, since clicking one isn't a
   request the page makes
6. every figure with a `check` key in `FIGURES` matches what it counts (builds
   in `CHANGELOG`, prizes in `RESULTS`, `CERTIFICATIONS`)
7. every link to another page of the site (`/slug/`, `/#id`) lands on a page and an id that exist
8. every Devanagari letter on the site is in the Hindi font subset

Any of those failing **fails the build** rather than shipping a subtly broken page.

## Layout

```
build.py                     the build
og.py                        renders the link-preview images (run by hand, output committed)
requirements.txt             jinja2, pillow
build_src/
  content.py                 ← all the words live here
  drawings.py                the simulated homes for the tripwire demo
  templates/
    base.html.j2             page skeleton, <head>, fonts, inlining
    index.html.j2            the home page: section order
    feature.html.j2          one page per build
    404.html.j2              "Not in this issue."
    macros.html.j2           department header, buttons, video loop, project name
    sections/*.html.j2       one file per section, plus the two hands-on demos
  static/
    css/site.css             the design system
    js/site.js               behaviour (progressive enhancement only)
  fonts/*.woff2              Big Shoulders Display, Newsreader, Anek Devanagari (OFL)
  images/aryan.jpg           source photo (build resizes it)
  images/awards/*.png        crops of the two winners graphics (header + own row only)
  video/*.mp4, *.jpg         8-second silent loops and their posters
  og/*.jpg                   link-preview images (made by og.py)

index.html, 404.html         ← GENERATED, do not edit
<slug>/index.html            ← GENERATED (one per feature)
images/, fonts/, video/, og/ ← GENERATED (resized or copied from build_src)
```

## The pages

**Home**, in order:

| Section | What's on it |
| --- | --- |
| Cover | The name over a colour portrait. Three cover lines (runner-up at WeMakeDevs × AWS Environmental Hacks; winner, 3rd place, at the Rote Playoffs Hackathon; fixes merged into NumPy and Pillow), each linking to its proof, then the deck. |
| Work | The four builds: Teesri Shikayat as the lead story with its loop, then Teesra Kaan, Shaky Ground and Jaisa Kaha. Each links to its feature page. |
| Prizes | One spread per prize, each with a detail of the organisers' own winners graphic (header + Aryan's row only, joined by a break line; the other winners are cut out). The Rote spread has a 64 KiB slider: drag the output size and watch what the runtime kept while it reported success. |
| Open source | The fixes merged into NumPy (#32915) and Pillow (#10147, shipped in 13.0.0), then every other 2026 entry in a table. |
| About | Lede, bio, facts, four figures (each checked against the page by the build). |
| Stack | The tools by where they sit in a request, as a list. |
| Everything shipped | Every 2026 build, newest first, with education and certifications alongside. |
| Contact | The yellow back cover: headline, email with copy, link rows. |

**Feature pages** (`/teesri-shikayat/`, `/teesra-kaan/`, `/shaky-ground/`, `/jaisa-kaha/`):
the name (Devanagari over the Latin when it has one) and what it means, the deck, the loop,
three numbers, then the project's own figure: the **tripwire demo** (tap simulated homes;
the rule is the project's: three homes, every pair within 250 m, inside 72 hours), a call
drawn to scale, a citation chain scored, or a flow through a Discord room. Four short
sections on how it works, what it's built with, and the next feature.

Hackathon facts come from `~/rote_hack/HACKATHON-HANDOFF.md` and each project's own README
or overview (fetched from GitHub). Upstream facts come from the pull requests themselves and
the projects' release notes. An entry's outcome says only what is known ("Submitted" claims
nothing more).

The tripwire demo uses **simulated homes**, seeded so the build stays deterministic; the
rule is the project's own. The Teesra Kaan timeline is the one call re-enacted by people on
a real phone line, captioned as an example outside the frozen test. The Shaky Ground chain
is a **schematic**: the weights and threshold are the project's, the papers are
illustrative.

The loops are cut from Aryan's own demo recordings: 8 seconds, muted, H.264. Every distinct
frame was checked for phone numbers and for other people's faces or names before a clip was
added. They load nothing until they're on screen.

**Only projects from [github.com/aryangorde6](https://github.com/aryangorde6)
appear on the site.**

## Type and colour

Fonts are self-hosted from `fonts/` (same origin), so the pages make zero third-party
requests.

- **Big Shoulders Display**: headlines, uppercase, 700 to 900
- **Newsreader**: text
- **Anek Devanagari** (condensed, bold): the Hindi names only. The file is a subset holding
  just their letters (3 KB); change a Hindi name and fetch a new subset (see
  `DEVANAGARI_SUBSET` in build.py).

| Pair | Ratio |
| --- | --- |
| white `#f4f4f4` on black `#0b0b0b` | 17.9 : 1 |
| body `#d6d6d6` on black | 13.5 : 1 |
| dim `#9a9a9a` on black | 7.0 : 1 |
| yellow `#ffd60a` on black | 13.9 : 1 |
| black on paper `#f4f4f4` | 17.9 : 1 |
| dim `#5a5a5a` on paper | 6.3 : 1 |
| black on yellow | 13.9 : 1 |
| dim `#4d4300` on yellow | 7.0 : 1 |

Yellow is never used for text on the white paper.

## Output

The home page is ~95 KB (~23 KB gzipped) with CSS and JS inlined; a feature page ~65 KB
(~17 KB gzipped). Fonts are ~180 KB. The loops (100 to 310 KB each) and the award details load
only when they come on screen.

## Accessibility

- Motion is decided before first paint from `prefers-reduced-motion`. With reduced motion
  no loop plays until its Play button is pressed.
- Every loop has a visible Pause button (WCAG 2.2.2) and only plays while at least 40% on
  screen. Without JS, the poster is shown.
- Both demos are real HTML controls (a range input; buttons for the homes) with a live
  status line, and read correctly before any script runs. On a phone the tripwire map
  stands upright so the homes stay far enough apart to tap.
- Skip link, semantic landmarks, one `h1` per page, no skipped heading levels.

## Deployment

AWS, defined in [`infra/site.yaml`](infra/site.yaml) (CloudFormation, stack
`aryangorde-site` in ap-south-1):

- a **private S3 bucket** in Mumbai: no public access, versioned (old versions kept 30 days);
- **CloudFront** in front of it: HTTPS with a free ACM certificate (us-east-1), HTTP/2 and
  HTTP/3, gzip/brotli, security headers, `www` → bare-domain 301 redirect (a CloudFront
  Function, which also serves `/slug/` from `/slug/index.html` and sends `/slug` to
  `/slug/`), and unknown paths answered with the "Not in this issue" page and a 404 status.

DNS stays at Hostinger: `@` is an ALIAS and `www` a CNAME to the distribution's
`*.cloudfront.net` name (see [`infra/HOSTINGER_DNS.md`](infra/HOSTINGER_DNS.md)).

To publish a change:

```bash
python3 build.py && infra/deploy.sh
```

`deploy.sh` checks that every page matches `build_src/` and that the public résumé is the
copy without the phone number, uploads **only** the pages (`index.html`, `404.html`, the
feature folders), the résumé PDF, `images/`, `fonts/`, `video/` and `og/`, sets cache headers
(pages and PDF 5 minutes, everything else a week) and clears CloudFront's cache. Nothing else in the repo is ever served.

Cost: CloudFront's always-free allowance (1 TB and 10 million requests a month) covers a
portfolio; S3 storage for a few MB is a fraction of a cent.
