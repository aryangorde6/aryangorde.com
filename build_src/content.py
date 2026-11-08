"""
Every word on the site lives here.

Editing content should never mean editing markup. Add a build by appending a
dict to CHANGELOG; add a tool by appending a string to a STACK node. The
templates loop over these, so the page rebuilds around whatever you put in.

House rule (from the résumé accuracy pass): every claim on this page has to be
traceable to Aryan_Gorde_Resume.pdf, to Aryan's own hackathon records
(~/rote_hack/HACKATHON-HANDOFF.md and each project's README/overview), or to
the live app it describes. If you can't point at where a line came from,
don't add it. Diagrams on the page are
drawn as *schematics* and say so — they never carry invented numbers.

Inline markup is allowed in the prose fields. Wrap a word in <em> to set it in
the italic serif accent face.
"""

# --- identity ---------------------------------------------------------------

SITE = {
    "name": "Aryan Gorde",
    "role": "Backend & full-stack developer",
    "location": "Mumbai, India",
    "timezone": "Asia/Kolkata",     # drives the live local-time readout
    "tz_label": "IST",
    "domain": "https://aryangorde.com",
    "email": "aryangorde6@gmail.com",
    "github": "https://github.com/aryangorde6",
    "github_handle": "aryangorde6",
    "linkedin": "https://www.linkedin.com/in/aryan-gorde-6b660a264/",
    "resume": "/Aryan_Gorde_Resume.pdf",
    "title": "Aryan Gorde — Backend & Full-Stack Developer",
    "description": (
        "Aryan Gorde — backend and full-stack developer. Runner-up at the WeMakeDevs × "
        "AWS Environmental Hacks and a winner (3rd place) at the Rote Playoffs Hackathon in 2026, with fixes merged "
        "into NumPy and Pillow. Python, AWS, and AI only where code can check it."
    ),
    "og_description": (
        "Backends that have to be right, and the proof that they are — drawn as a system."
    ),
    "photo": "aryan.jpg",          # source file in build_src/images/
    "photo_alt": "Portrait of Aryan Gorde",
    "status": "Open to backend & full-stack roles",
}

# --- nav --------------------------------------------------------------------
# (id, label) — id must match a section id, and build.py verifies that. The
# order here is also the §-number each section is drawn with.

NAV = [
    ("about",     "About"),
    ("results",   "Results"),
    ("stack",     "Stack"),
    ("work",      "Work"),
    ("changelog", "Changelog"),
    ("contact",   "Contact"),
]

# --- hero -------------------------------------------------------------------

HERO = {
    "first_name": "Aryan",
    "last_name": "Gorde",
    "kicker": "Backend & full-stack developer",
    "blurb": (
        "I build the parts of a product that have to be <em>right</em> — warnings "
        "that quote the caller's own words, a tripwire that fails closed, tests frozen "
        "before the first result. Python on the server, AWS around it, and AI only "
        "where code can check its work."
    ),
    # The drawing's title block — the box in the corner of every engineering
    # sheet. Each row is (field, value); all of it is checkable elsewhere.
    "title_block": [
        ("Drawn by",  "A. Gorde"),
        ("Discipline", "Backend · Full-stack"),
        ("Studying",  "B.Tech CE · SPIT '27"),
        ("Based in",  "Mumbai, IN"),
    ],
}

# --- about ------------------------------------------------------------------

ABOUT = {
    "lede": "Server-side by preference, full-stack by necessity.",
    "paragraphs": [
        "I'm a computer engineering student who wandered onto the server side and never "
        "left. The work I like has a correct answer buried in it somewhere — a warning "
        "that has to quote what the caller actually said, a tripwire that fires on the "
        "third complaint and not the second, a chain of citations whose risk has to add up.",

        "Most of what I ship is Python, event-driven on AWS more often than not, with a "
        "small, sharp frontend on top. I'd rather spend the afternoon on the evaluation "
        "than the hover state. (This page is what happens when I get to do both.)",
    ],
    # Spec sheet rows: (field, value)
    "spec": [
        ("Currently", "B.Tech, Computer Engineering"),
        ("Latest",    "Jaisa Kaha · Nov 2026"),
        ("Learning",  "Distributed systems"),
        ("Status",    "Available"),
    ],
}

# Figures shown on the about sheet. Every one is checkable against the page,
# and build.py fails if a figure with a `check` key drifts from what it counts.
FIGURES = [
    {"value": 9, "suffix": "",  "label": "builds shipped in 2026", "check": "changelog_2026"},
    {"value": 2, "suffix": "",  "label": "hackathon prizes, solo", "check": "results"},
    {"value": 5, "suffix": "",  "label": "certifications",          "check": "certifications"},
    {"value": 3, "suffix": "+", "label": "years on Python"},
]

# --- results (hackathons) ---------------------------------------------------
# Source: ~/rote_hack/HACKATHON-HANDOFF.md §1, §2, §10. Placed entries only.
# `stamp` is drawn as a rubber stamp: (top arc, centre band, bottom arc). Room, measured
# in the browser (viewBox units): top arc ≤ 124, bottom arc ≤ 150, band ≤ 132 —
# about 21 / 26 / 11 characters. Longer text runs under the band or off the arc.
# `rank_lead` goes on the line above the rank. Rote: WeMakeDevs titles its graphic
# "Hackathon Winners" (1st–3rd, above two runner-ups), so 3rd place is a winner.
# Never "winner" without the place next to it; Environmental Hacks stays "Runner-up".

RESULTS = [
    {
        "id": "env-hacks",
        "rank": "Runner-up",
        "event": "Environmental Hacks",
        "organizer": "WeMakeDevs × AWS · Bharat Builds Tour, event 02",
        "dates": "8–11 Oct 2026",
        "field": "9,146 registered · one of 4 runners-up across all three tracks",
        "track": "Heat and Water",
        "prize": "$1,000 AWS credits",
        "team": "Solo",
        "build": "Teesri Shikayat",
        "summary": (
            "a tripwire for dirty tap water. Hindi voice complaints on Telegram; when three "
            "homes close together report it, every home around them is warned, and only "
            "the residents can close the case."
        ),
        "links": [
            {"label": "Case study", "href": "#teesri"},
            {"label": "Demo video", "href": "https://youtu.be/L0UteWpltyw"},
        ],
        "short": "AWS Environmental Hacks",
        # The hero plate: the one-line version of this card.
        "plate": {
            "month": "Oct 2026",
            "org": "WeMakeDevs × AWS",
            "field": "9,146 registered",
            "what": "Built Teesri Shikayat",
            "href": "#teesri",
        },
        "stamp": ("Environmental Hacks", "Runner-up", "WeMakeDevs × AWS · 2026"),
        "rot": -7,
        # Crops of the organisers' runner-ups graphic: its header and Aryan's own
        # card only — the other teams' photos are left out (shown as a break line).
        "proof": {
            "caption": "From the official WeMakeDevs × AWS runner-ups graphic. "
                       "The other three teams are cut at the break.",
            # WeMakeDevs' own announcement post, checked 08 Nov 2026.
            "post": "https://www.linkedin.com/posts/the-environmental-hacks-runner-ups-are-here-share-7518274243164381184-WOrW/",
            "parts": [
                {"name": "env-head", "alt": "WeMakeDevs × AWS graphic: Bharat Builds event 02, "
                                            "Environmental Hacks runner-ups. Each team wins $1,000 AWS credits."},
                {"name": "env-row", "alt": "Heat and Water: Teesri Shikayat, solo, Aryan Gorde."},
            ],
        },
    },
    {
        "id": "rote",
        "rank_lead": "Winner",
        "rank": "3rd place",
        # "Hackathon" in the name: "Playoffs" alone reads like sport (WeMakeDevs' post:
        # "The Rote Playoffs hackathon winners are…"). Stamp says "Rote Playoffs Hack" (arc room).
        "event": "Rote Playoffs Hackathon",
        "organizer": "WeMakeDevs × Modiqo",
        "dates": "1–6 Sep 2026",
        "field": "of ~900 published plays",
        "track": "Open",
        "prize": "iPhone 17",
        "team": "Solo",
        "build": "Four plays + one platform defect",
        "summary": (
            "four read-only GitHub plays for Modiqo's Rote registry, and the finding that "
            "carried them: the runtime silently kept only the first 64 KiB of a step's "
            "output and still reported success. 221 of the 249 public plays that read "
            "that output (89%) never checked. Filed upstream; fixed in rote v0.83.0."
        ),
        "links": [
            {"label": "Write-up", "href": "https://aryangorde6.github.io/rote-stdout-truncation/"},
            {"label": "Upstream issue", "href": "https://github.com/modiqo/rote-releases/issues/10"},
        ],
        "short": "Rote Playoffs Hackathon",
        "plate": {
            "month": "Sep 2026",
            "org": "WeMakeDevs × Modiqo",
            "field": "~900 published plays",
            "what": "Found a 64 KiB output bug, fixed upstream",
            "href": "#rote",
        },
        # Band "Winner" like Env Hacks' "Runner-up". Top arc "Rote Playoffs Hack" (Aryan,
        # 08 Nov; the full "…Hackathon" is too long for the arc). No year: there has only
        # been one Rote Playoffs. Both organisers stay on the bottom arc;
        # "3rd place · WeMakeDevs × Modiqo" is too long for it, so the place is carried
        # by the big rank text right beside the stamp.
        "stamp": ("Rote Playoffs Hack", "Winner", "WeMakeDevs × Modiqo"),
        "rot": 6,
        "proof": {
            "caption": "From the official WeMakeDevs × Modiqo winners graphic. "
                       "The other winners are cut at the break.",
            # WeMakeDevs' own announcement post, checked 08 Nov 2026.
            "post": "https://www.linkedin.com/posts/the-rote-playoffs-hackathon-winners-are-share-7505295266309132288-6Rjf/",
            "parts": [
                {"name": "rote-head", "alt": "WeMakeDevs × Modiqo graphic: Rote Playoffs hackathon winners."},
                {"name": "rote-row", "alt": "3rd position, Apple iPhone 17: Aryan Gorde."},
            ],
        },
    },
]
# One-line rank, e.g. "Winner · 3rd place" (command palette, structured data).
for _r in RESULTS:
    _r["rank_full"] = " · ".join(x for x in (_r.get("rank_lead"), _r["rank"]) if x)

# Fixes merged into other people's projects. Source: the PRs themselves
# (gh pr view) and Pillow 13.0.0's release notes, checked 08 Nov 2026. NumPy has
# not released since the merge, so it claims "merged into main" and no more.
UPSTREAM = [
    {
        "id": "pr-numpy",
        "project": "NumPy",
        "repo": "numpy/numpy",
        "number": 32915,
        "title": "BUG: close the file in np.load when an .npz is invalid",
        "summary": (
            "<code>np.load</code> left the file open when handed a broken <code>.npz</code> "
            "— an interrupted download, say — and Python warned about an unclosed file. "
            "The file is now handed over only once the archive has opened, so a failure "
            "closes it. With a regression test."
        ),
        "merged": "18 Oct 2026",
        "diff": "+29 −2 · 2 files",
        "status": "Merged into main",
        "href": "https://github.com/numpy/numpy/pull/32915",
    },
    {
        "id": "pr-pillow",
        "project": "Pillow",
        "repo": "python-pillow/Pillow",
        "number": 10147,
        "title": "Improve mmap buffer length check",
        "summary": (
            "Opening a truncated image by filename crashed with a bare <code>ValueError</code> "
            "and ignored <code>LOAD_TRUNCATED_IMAGES</code>: the length check used the tile's "
            "stride, which is 0 for PPM, TIFF, TGA and five other formats. It now falls back "
            "to the decoder, so a filename behaves exactly like a file object."
        ),
        "merged": "10 Oct 2026",
        "diff": "+30 −3 · 3 files",
        "status": "Shipped in Pillow 13.0.0",
        "release": "13.0.0",
        "href": "https://github.com/python-pillow/Pillow/pull/10147",
    },
]

# Every other hackathon entered in 2026, newest first. Outcome says only what
# is known: "Submitted" means submitted, nothing more is claimed.
ENTRIES = [
    {"when": "Nov 2026", "event": "Flip the Switch", "organizer": "WeMakeDevs × DevTools Academy × Switch",
     "build": "Jaisa Kaha — an AI scribe that won't invent a cook's quantities",
     "outcome": "Submitted · Track 02"},
    {"when": "Nov 2026", "event": "Global AI Developer Hackathon", "organizer": "Meta",
     "build": "Teesra Kaan — warns on a scam call and shows the caller's next line",
     "outcome": "Submitted · Indie track"},
    {"when": "Oct 2026", "event": "Graph Hacks", "organizer": "WeMakeDevs × FalkorDB",
     "build": "Shaky Ground — finds the science built on retracted research",
     "outcome": "Submitted · Track 01"},
    {"when": "Oct 2026", "event": "Dark Factory", "organizer": "WeAreDevelopers × Band",
     "build": "The Adversary Line — five coding-agent seats building and attacking a reservation service",
     "outcome": "Submitted"},
    {"when": "Sep 2026", "event": "IBM Bob 2.0 Hackathon", "organizer": "lablab.ai × IBM",
     "build": "Antibody — checks that fixed bugs stay fixed (team of 2)",
     "outcome": "Submitted"},
    {"when": "Sep 2026", "event": "First Commit", "organizer": "WeMakeDevs × AWS",
     "build": "Pukaar — one press pages the three people most likely to answer, at once",
     "outcome": "Submitted · 13,664 registered"},
    {"when": "Sep 2026", "event": "AI Trading Agents Hackathon", "organizer": "lablab.ai × Alpaca",
     "build": "Contour — an options agent that sells only the rich side of the skew",
     "outcome": "Submitted"},
]

# --- stack (drawn as a system diagram) --------------------------------------
# Each node is a box in the diagram. `x`, `y`, `w` place it on the desktop
# drawing (in a 1200 × 660 coordinate space); below ~1100px the drawing
# reflows into a simple vertical flow and those numbers are ignored.
# `edges` are drawn from this node to the named nodes. Connectors attach at
# each node's title bar, so a node can grow taller without breaking the lines.

STACK_NODES = [
    {"id": "client", "label": "Client", "x": 24, "y": 238, "w": 236,
     "note": "Enough frontend to ship the whole thing solo.",
     "items": ["React", "Next.js", "Tailwind", "Chart.js", "Vanilla JS"],
     "edges": ["edge"]},

    {"id": "edge", "label": "Edge", "x": 330, "y": 238, "w": 170,
     "note": "Off the laptop, and staying up.",
     "items": ["Nginx", "Gunicorn"],
     "edges": ["app"]},

    {"id": "app", "label": "Application", "x": 566, "y": 238, "w": 244,
     "note": "Where most of the time goes.",
     "items": ["Django", "DRF", "FastAPI", "Express", "Node.js"],
     "edges": ["data", "async", "ai"]},

    {"id": "data", "label": "Data", "x": 876, "y": 50, "w": 300,
     "note": "Storage, cache, and the queries between.",
     "items": ["PostgreSQL", "MongoDB Atlas", "Redis", "SQLite", "ChromaDB"],
     "edges": []},

    {"id": "async", "label": "Async", "x": 876, "y": 250, "w": 300,
     "note": "Work that shouldn't block a request.",
     "items": ["Celery", "Redis"],
     "edges": []},

    {"id": "ai", "label": "AI", "x": 876, "y": 416, "w": 300,
     "note": "Used where it earns its latency.",
     "items": ["Groq · Llama 3.3", "Vertex AI · Gemini", "Amazon Bedrock", "Ollama",
               "Hybrid retrieval"],
     "edges": []},
]

# The dashed boundary drawn around everything server-side.
STACK_BOUNDARY = {
    "label": "Runtime",
    "items": ["Docker", "AWS EC2", "Cloud Run"],
}

# The lane under the drawing that ships into the boundary.
STACK_CI = {
    "label": "CI / CD",
    "note": "Tests on every push; main deploys on green.",
    "items": ["GitHub Actions", "Jenkins"],
}

LANGUAGES = ["Python", "TypeScript", "JavaScript", "SQL", "Bash", "C"]

# --- work: featured case study ----------------------------------------------
# Source: ~/teesri-shikayat/README.md and HACKATHON-HANDOFF.md §10.2. The ring
# figure is a schematic of the recorded demo incident (simulated homes).

FEATURED = {
    "id": "teesri",
    "name": "Teesri Shikayat",
    "gloss": "“the third complaint”",
    "tag": "Featured build · Runner-up, AWS Environmental Hacks",
    "summary": (
        "A tripwire for dirty tap water, from my own monsoon tap in Mumbai. Residents "
        "complain with a Hindi voice note on Telegram. When three different homes within "
        "250 m report dirty water inside 72 hours, every enrolled home in the ring is "
        "warned in Hindi — and only the residents can close the case."
    ),
    "figures": [
        {"value": "20/23", "note": "homes warned in the demo incident had never complained."},
        {"value": "₹0.94", "note": "measured AWS cost of one real incident, end to end."},
        {"value": "66", "note": "tests, run in CI on every push."},
    ],
    "quote": ("The ward office said resolved. The AI believed them.", "Cedar didn’t."),
    "quote_note": (
        "The model chooses the words; code and policy choose the actions. A ward office’s "
        "“resolved” only asks to close the case — any resident’s “not clean” reopens it, "
        "and silence never closes it."
    ),
    # Drawn as a flow, left to right; `kind` styles the step.
    "flow": [
        ("Third report", "3 homes · 250 m · 72 h", ""),
        ("Volunteer", "approves with one tap", ""),
        ("Ring warned", "Hindi text + Polly voice", ""),
        ("Ward office", "replies “resolved”", ""),
        ("Cedar", "denies close_case", "deny"),
        ("Residents", "one says “not clean”", ""),
        ("Reopened", "silence never closes it", "end"),
    ],
    "detail": [
        ("Listening",
         "Hindi voice notes arrive on Telegram and go through Amazon Transcribe (hi-IN). "
         "Bedrock quota was zero, so an open model — Gemma 4 E4B in llama.cpp on our own "
         "EC2 Graviton4 instance — fills a fixed schema, and code validates every field."),
        ("The tripwire",
         "DynamoDB Streams feed an EventBridge Pipe into a rule written in plain code, not "
         "AI: three different homes, every pair within 250 m, within 72 hours. One "
         "DynamoDB transaction settles two “third” reports arriving at once."),
        ("The case",
         "One Step Functions execution per incident, waiting on three task tokens: the "
         "volunteer’s approval, the ward office’s reply and the residents’ check-ins. A Map "
         "state sends every warning as text and as an Amazon Polly voice note."),
        ("Guarded",
         "A Strands case agent whose every action is checked by Cedar policies that fail "
         "closed. The ward office gets one email with counts, never names or numbers. Own "
         "KMS key, CloudTrail, GuardDuty and alarms."),
    ],
    "tech": ["AWS CDK (Python)", "Lambda", "Transcribe", "Polly", "DynamoDB Streams",
             "EventBridge Pipes", "Step Functions", "Strands", "Cedar", "EC2 Graviton4"],
    "links": [
        {"label": "Watch the demo", "href": "https://youtu.be/L0UteWpltyw"},
        {"label": "Source", "href": "https://github.com/aryangorde6/teesri-shikayat"},
        {"label": "Build story", "href": "https://builder.aws.com/content/3KYOE7QsILh1qS2cN5fbcCJDLzy/three-complaints-one-warning-a-dirty-water-tripwire-on-aws"},
    ],
}

# --- work: case studies on paper -------------------------------------------------
# Only projects on github.com/aryangorde6 appear on this site (Aryan, 08 Nov 2026).
# Sources: each repo's README (fetched 08 Nov 2026) and the hackathon STATE files.
# `figure` picks the drawing: "timeline" (to scale, in seconds) or "chain".

CASES = [
    {
        "id": "teesra-kaan",
        "name": "Teesra Kaan",
        "tag": "Scam-call guardian · Meta Global AI Developer Hackathon",
        "summary": (
            "The third ear on a scam call. Put a suspicious call on speaker and it listens "
            "in Hindi, Marathi or English. The moment the caller starts a known scam it warns "
            "you in your language, quoting his own words — then shows his next line before "
            "he says it."
        ),
        "figures": [
            {"value": "131/132", "note": "real US scam robocalls from the FTC warned on, in a test "
                                         "fixed before any result existed."},
            {"value": "9/9", "note": "scam calls still caught with every keyword rewritten out. "
                                     "A keyword list caught none."},
            {"value": "0/15", "note": "genuine test calls warned on, amber or red (synthetic voices)."},
        ],
        "figure": "timeline",
        # The one call re-enacted by people on a real phone line (README, "Does it
        # work?"). Outside the frozen test: an example, not a measurement.
        "timeline": {
            "span": 50,
            "events": [
                {"t": 0,  "time": "0:00", "lane": "caller", "row": 1, "what": "First false claim"},
                {"t": 17, "time": "0:17", "lane": "tk", "row": 1, "kind": "amber",
                 "what": "Amber. Next line shown: “Come on a video call.”"},
                {"t": 38, "time": "0:38", "lane": "caller", "row": 2, "kind": "hit",
                 "what": "“Come on a video call.”", "note": "21 s after it was shown"},
                {"t": 40, "time": "0:40", "lane": "tk", "row": 1, "kind": "red",
                 "what": "Red. Next line shown: “Transfer the money for verification.”"},
                {"t": 45, "time": "0:45", "lane": "caller", "row": 1, "kind": "hit",
                 "what": "Asks for the money", "note": "5 s after the red warning"},
            ],
            "dims": [{"a": 17, "b": 38, "label": "21 s ahead"}, {"a": 40, "b": 45, "label": "5 s"}],
            "caption": "The one call re-enacted by people on a real phone line, heard at real-time "
                       "speed. Outside the frozen test: an example, not a measurement.",
        },
        "detail": [
            ("The next line",
             "Ten scam scripts from police, RBI and DoT advisories, written as ordered steps. "
             "Once two steps are heard it shows the next one, but only when every script that "
             "fits the call agrees. Fixed scripts make the prediction, not a model."),
            ("Proof, not say-so",
             "Muse Spark answers 13 fixed yes/no questions about the caller, quoting his exact "
             "words for every yes, and a quote that isn't in the transcript is thrown away. A "
             "warning needs a quoted sign; red waits for an ask for money, an OTP, an app or a link."),
            ("Measured",
             "The test was fixed before any result existed and run once: 150 real FTC robocalls "
             "and Hindi, Marathi and English calls in synthetic voices, against a keyword list "
             "and against the model asked plainly. Every transcript is committed; the run "
             "replays offline."),
            ("Ten people",
             "Ten people, five of them elderly, used it in their own language. One elder had "
             "lost ₹20,000 to a “sent too much by mistake” call; it became the tenth script "
             "before the test was frozen."),
        ],
        "tech": ["Muse Voice Transcribe", "Muse Spark 1.3", "FastAPI", "WebSockets", "Python"],
        "links": [
            {"label": "Read the source", "href": "https://github.com/aryangorde6/teesra-kaan"},
        ],
    },
    {
        "id": "shaky-ground",
        "name": "Shaky Ground",
        "tag": "Citation graph · Graph Hacks 2026, Track 01",
        "summary": (
            "Finds the science built on retracted research, not just the papers that cite it. "
            "Every citation is weighted by how much the citing paper relies on the cited one, "
            "a chain's risk is computed in Cypher, and an agent decides which branches to "
            "explore — returning every answer with its evidence."
        ),
        "figures": [
            {"value": "45", "note": "papers found building on Lesné et al. 2006 (Nature, retracted "
                                    "2024). Two of them were retracted themselves."},
            {"value": "0.45 s", "note": "to score every chain of up to three citations across 10,852 "
                                        "papers. Brute force took 287.8 s, with 0 mismatches."},
            {"value": "27/30", "note": "links a third model, from another family, classed exactly as "
                                       "the judges did."},
        ],
        "figure": "chain",
        # Schematic: the weights and the 0.2 threshold are the README's; the papers
        # are illustrative.
        "chain": {
            "nodes": [("Retracted paper", "1.0"), ("Paper A", "1.0"), ("Paper B", "0.6"),
                      ("Paper C", "0.36")],
            "links": [("Foundational", "× 1.0", "uses its method"),
                      ("Supporting", "× 0.6", "relies on its finding"),
                      ("Supporting", "× 0.6", "relies on its finding")],
            "verdict": "Builds on it",
            "branch": (("Background", "× 0.15", "mentions it in passing"), ("Paper D", "0.15"), "In passing"),
            "rule": "Builds on ⇔ risk ≥ 0.2: three supporting links score 0.6³ = 0.216, and any "
                    "background link caps a chain at 0.15.",
            "caption": "Schematic: how a chain is scored, in Cypher. Weights and threshold are the "
                       "project's; the papers are illustrative.",
        },
        "detail": [
            ("Reliance, not citation",
             "The model never picks a number. It reads only the citation sentences and answers "
             "yes/no questions; fixed rules turn the answers into a class and a weight, and the "
             "deciding sentence is stored verbatim on the edge."),
            ("Risk in Cypher",
             "Risk flows back from the retracted paper one hop per query, so the cost grows with "
             "edges, not chains. A variable-length path with <code>reduce()</code> returns one "
             "paper's riskiest chain, evidence on every link, in about 20 ms."),
            ("Two models must agree",
             "A second link counts only if it relies on the part that came from the retracted "
             "paper. One model wasn't reliable enough, so two model families vote: a link "
             "carries only if both say yes."),
            ("For people and agents",
             "A web UI, a foundation check for any paper or a whole reference list, and an MCP "
             "server so an AI agent can check a paper before citing it. Unchecked is never "
             "shown as clean."),
        ],
        "tech": ["FalkorDB", "Cypher", "OpenAlex", "Semantic Scholar", "Retraction Watch",
                 "Gemini", "Groq", "MCP", "Railway"],
        "links": [
            {"label": "Open the live demo", "href": "https://shaky-ground-production.up.railway.app"},
            {"label": "Demo video", "href": "https://youtu.be/64SxLfHHHHY"},
            {"label": "Build story", "href": "https://aryangorde.hashnode.dev/how-far-does-a-retraction-reach"},
            {"label": "Source", "href": "https://github.com/aryangorde6/shaky-ground"},
        ],
    },
]

# --- work: builds drawn as a flow -------------------------------------------------
# `pipeline` is drawn as a left-to-right flow; each step is (label, sub-label).

PROJECTS = [
    {
        "id": "jaisa-kaha",
        "name": "Jaisa Kaha",
        "tag": "Agents with owners · Flip the Switch, Track 02",
        "blurb": (
            "An AI scribe that refuses to make up a cook's quantities. It writes down only the "
            "amounts that were said and keeps a gap where none was — or where the cook said "
            "“by feel” — and only the cook's own account can fill it. On a test sentence, four "
            "models out of four turned “ghee, by feel” into a number."
        ),
        "pipeline": [
            ("Voice note",  "the cook, in Marathi"),
            ("Tape",        "Transcribe mr-IN · every word, with its second"),
            ("Lekhak",      "Qwen3 on Bedrock · each amount cites the tape"),
            ("Pothi",       "the cook's own agent · asks about gaps only"),
            ("Cook",        "fills a gap, then “page pakka”"),
            ("Page",        "only Pothi can change it"),
        ],
        "caption": "One dish through the Discord room. Switch checks every message against its "
                   "addressee's rule, so Pothi refuses everyone but the cook and Tape — the AI, and me.",
        "tech": ["Switch", "Discord", "AWS Transcribe", "Amazon Bedrock", "Python (stdlib)"],
        "links": [
            {"label": "Demo video", "href": "https://youtu.be/fnLvEMvr4IU",
             "aria": "Jaisa Kaha demo video"},
            {"label": "Source", "href": "https://github.com/aryangorde6/jaisa-kaha",
             "aria": "Jaisa Kaha source on GitHub"},
        ],
    },
]

# --- changelog --------------------------------------------------------------
# Every build on github.com/aryangorde6, from each repo's README and the
# hackathon STATE files. NOTE: there is no employment to list, so this is a
# dated log of real shipped work, not a job history. Do not add invented roles.
# `tech` only lists things named in that entry's own `detail`.
# `anchor` (optional) links the entry to its write-up further up the page.

CHANGELOG = [
    {"period": "Nov 2026", "name": "Jaisa Kaha", "anchor": "jaisa-kaha",
     "context": "Flip the Switch · WeMakeDevs × DevTools Academy × Switch · solo",
     "detail": "An AI scribe for a family's recipes that writes down only the amounts the cook "
               "said and keeps a gap where none was. Three agents share one Discord room "
               "through Switch, and the cook's own agent refuses anyone else who tries to fill "
               "a gap — the AI, and me.",
     "tech": ["Switch", "Discord", "AWS Transcribe", "Amazon Bedrock"]},

    {"period": "Oct–Nov 2026", "name": "Teesra Kaan", "anchor": "teesra-kaan",
     "context": "Meta Global AI Developer Hackathon · Indie track",
     "detail": "A scam-call guardian in Hindi, Marathi and English that warns in the caller's "
               "own words and shows his next line before he says it. Tested once, on a set "
               "fixed before any result: 131 of 132 real FTC impersonation robocalls warned on.",
     "tech": ["Muse Voice Transcribe", "Muse Spark", "FastAPI"]},

    {"period": "Oct 2026", "name": "Shaky Ground", "anchor": "shaky-ground",
     "context": "Graph Hacks · WeMakeDevs × FalkorDB · solo",
     "detail": "Finds the science built on retracted research: a FalkorDB citation graph where "
               "every citation is weighted by reliance and a chain's risk is computed in "
               "Cypher, with an agent that decides where to dig and an MCP server for other agents.",
     "tech": ["FalkorDB", "Cypher", "MCP"]},

    {"period": "Oct 2026", "name": "Teesri Shikayat", "anchor": "teesri",
     "context": "WeMakeDevs × AWS Environmental Hacks · solo", "prize": "Runner-up",
     "detail": "A dirty-water tripwire for Mumbai: Hindi voice complaints on Telegram, a "
               "plain-code rule for three homes within 250 m inside 72 hours, and one Step "
               "Functions case per incident that only residents can close, guarded by a "
               "Strands agent checked with Cedar. One real incident cost ₹0.94.",
     "tech": ["Transcribe", "Polly", "EventBridge Pipes", "Step Functions", "Strands",
              "Cedar", "CDK"]},

    {"period": "Oct 2026", "name": "The Adversary Line", "anchor": None,
     "context": "Dark Factory · WeAreDevelopers × Band · solo",
     "detail": "A dark software factory: five coding-agent seats in Band Desktop building a "
               "reservation service in stages, each a complete container, while one seat "
               "plants known bugs to test the checker. Run on free models, for $0.",
     "tech": ["Band Desktop", "Docker"],
     "links": [{"label": "Source", "href": "https://github.com/aryangorde6/the-adversary-line"}]},

    {"period": "Sep 2026", "name": "Antibody", "anchor": None,
     "context": "IBM Bob 2.0 Hackathon · lablab.ai · team of 2",
     "detail": "Do fixed bugs stay fixed? Antibody puts a project's past bug fixes back, one at "
               "a time, and runs its own tests. On sqlparse, 13 of 20 fixes were caught before "
               "and 18 of 20 after. Before the event: 479 fixes undone across 18 Python "
               "libraries, and 139 times every test still passed.",
     "tech": ["IBM Bob", "pytest", "GitHub Actions"],
     "links": [{"label": "Ledger", "href": "https://antibody-ledger.vercel.app/sqlparse/"},
               {"label": "Source", "href": "https://github.com/aryangorde6/antibody"}]},

    {"period": "Sep 2026", "name": "Pukaar", "anchor": None,
     "context": "WeMakeDevs × AWS First Commit · solo",
     "detail": "Help for an older person living alone: one press pages the three people most "
               "likely to answer, at the same time; the first to say “I'm going” wins, and "
               "the circle widens if nobody answers within a minute. Eleven languages, AAA "
               "contrast, 21 live checks.",
     "tech": ["Step Functions task tokens", "DynamoDB", "Terraform"],
     "links": [{"label": "Source", "href": "https://github.com/aryangorde6/pukaar"},
               {"label": "Demo", "href": "https://youtu.be/GaQZs1yBAyU"}]},

    {"period": "Sep 2026", "name": "Rote plays", "anchor": "rote",
     "context": "WeMakeDevs × Modiqo Rote Playoffs Hackathon · solo", "prize": "Winner · 3rd place",
     "detail": "Four read-only plays for pull-request review — unresolved threads, flaky CI, "
               "who should review, and a truncation audit — plus a measured platform defect: "
               "step output silently cut at 64 KiB, unchecked by 89% of public plays. Filed "
               "upstream and fixed in rote v0.83.0.",
     "tech": ["TypeScript", "GitHub GraphQL", "gh CLI"]},

    {"period": "Aug–Sep 2026", "name": "Contour", "anchor": None,
     "context": "AI Trading Agents Hackathon · lablab.ai × Alpaca",
     "detail": "An autonomous options agent that measures the volatility surface every 15 "
               "minutes and sells only the rich side of the skew, on paper. A 387-cycle "
               "backtest found no edge (t = +0.37), so none is claimed. 302 tests, and every "
               "decision recorded in a SHA-256 hash chain.",
     "tech": ["alpaca-py", "Alpaca CLI", "pytest"],
     "links": [{"label": "Write-up", "href": "https://aryangorde6.github.io/contour/"},
               {"label": "Source", "href": "https://github.com/aryangorde6/contour"}]},
]

EDUCATION = {
    "degree": "B.Tech, Computer Engineering",
    "institution": "Sardar Patel Institute of Technology",
    "affiliation": "Mumbai University · Mumbai, India",
    "status": "Aug 2023 – June 2027",
    "detail": "Computer-science fundamentals with a practical bias: data structures, "
              "operating systems, databases, and machine learning, applied to things "
              "that actually get deployed.",
}

CERTIFICATIONS = [
    ("Meta Back-End Developer Professional Certificate", "Meta · Coursera",   "Dec 2025"),
    ("CI/CD: Continuous Integration and Continuous Delivery", "IBM · Coursera", "Jan 2026"),
    ("AWS Cloud Technical Essentials", "Amazon Web Services · Coursera",       "Jan 2026"),
    ("Docker for Beginners", "KodeKloud",                                       "Jan 2026"),
    ("Kubernetes for Absolute Beginners", "KodeKloud",                          "Jan 2026"),
]

# --- contact ----------------------------------------------------------------

CONTACT = {
    "headline_pre": "Let's build something that",
    "headline_em": "has to work.",
    "body": (
        "I'm after backend or full-stack work where the hard part is the system design, "
        "the data model, or keeping a deploy boring. If that's what you've got, I'd like "
        "to hear about it. Fastest route is email — I reply to everything that isn't a "
        "recruiter template."
    ),
    "links": [
        {"title": "GitHub",   "note": "@" + SITE["github_handle"], "href": SITE["github"], "icon": "↗"},
        {"title": "LinkedIn", "note": "the formal version", "href": SITE["linkedin"], "icon": "↗"},
        {"title": "Résumé",   "note": "PDF, one page",      "href": SITE["resume"],   "icon": "↓"},
    ],
}

# --- colophon ---------------------------------------------------------------

COLOPHON = (
    "Set in Archivo, Instrument Serif and JetBrains Mono, all self-hosted. Generated by "
    "a small Python build — Jinja2 templates, content as Python data, a Pillow image "
    "pipeline — into one HTML file that makes zero third-party requests."
)
