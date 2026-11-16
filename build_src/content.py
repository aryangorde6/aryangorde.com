"""
Every word on the site lives here.

Editing content should never mean editing markup. Add a build by appending a
dict to CHANGELOG; add a feature page by appending a dict to FEATURES. The
templates loop over these, so the pages rebuild around whatever you put in.

House rule: every claim on this site has to trace to a source: each project's
README on github.com/aryangorde6, Aryan's hackathon records (the STATE.md and
handoff files in each hackathon folder), the pull requests themselves, the
organisers' winners graphics, or the live app. If you can't point at where a
line came from, don't add it. Schematic drawings say they are schematic.

Inline markup is allowed in prose fields: <b>, <code>, and <mark> (the yellow
highlighter, used sparingly).

Writing: plain sentences. No em dashes in copy; use a colon, a comma, brackets
or a full stop.
"""

# --- identity ---------------------------------------------------------------

SITE = {
    "name": "Aryan Gorde",
    "role": "Backend & full-stack developer",
    "location": "Mumbai, India",
    "domain": "https://www.aryangorde.com",
    "email": "aryangorde6@gmail.com",
    "github": "https://github.com/aryangorde6",
    "github_handle": "aryangorde6",
    "linkedin": "https://www.linkedin.com/in/aryan-gorde-6b660a264/",
    "resume": "/Aryan_Gorde_Resume.pdf",
    "title": "Aryan Gorde · Backend and full-stack developer",
    "description": (
        "Aryan Gorde, backend and full-stack developer in Mumbai. Runner-up at the WeMakeDevs × "
        "AWS Environmental Hacks and a winner (3rd place) at the Rote Playoffs Hackathon in 2026, "
        "with fixes merged into NumPy and Pillow. Python, AWS, and AI only where code can check it."
    ),
    "og_description": "Backends that have to be right, and the proof that they are.",
    "photo": "aryan.jpg",          # source file in build_src/images/
    "photo_alt": "Portrait of Aryan Gorde",
}

# --- nav --------------------------------------------------------------------
# (id, label). Each id must be a <section id> on the home page; build.py checks.

NAV = [
    ("work",        "Work"),
    ("prizes",      "Prizes"),
    ("open-source", "Open source"),
    ("about",       "About"),
    ("contact",     "Contact"),
]

# --- the cover ----------------------------------------------------------------

HERO = {
    "first_name": "Aryan",
    "last_name": "Gorde",
    # Three cover lines: a yellow chip, a headline, one sentence. Each links to
    # the part of the page that proves it.
    "lines": [
        {"chip": "Runner-up", "head": "Environmental Hacks", "href": "#env-hacks",
         "text": "WeMakeDevs × AWS. One of 4 runners-up out of 9,146 registered, solo, "
                 "with Teesri Shikayat."},
        {"chip": "Winner · 3rd place", "head": "Rote Playoffs Hackathon", "href": "#rote",
         "text": "WeMakeDevs × Modiqo. Found the runtime silently cutting output at 64 KiB; "
                 "fixed upstream."},
        {"chip": "Merged", "head": "NumPy and Pillow", "href": "#open-source",
         "text": "Two fixes accepted upstream. Pillow's shipped in 13.0.0."},
    ],
    "deck": (
        "Backend and full-stack developer. I build the parts of a product that "
        "<mark>have to be right</mark>: Python on the server, AWS around it, and AI only "
        "where code can check its work."
    ),
}

# --- about ------------------------------------------------------------------

ABOUT = {
    "lede": "Server-side by preference, full-stack by necessity.",
    "paragraphs": [
        "I'm a computer engineering student who wandered onto the server side and never "
        "left. The work I like has a correct answer buried in it somewhere: a warning that "
        "has to quote what the caller actually said, a tripwire that fires on the third "
        "complaint and not the second, a chain of citations whose risk has to add up.",

        "Most of what I ship is Python, event-driven on AWS more often than not, with a "
        "small, sharp frontend on top. I'd rather spend the afternoon on the evaluation "
        "than the hover state. (This site is what happens when I get to do both.)",
    ],
    "spec": [
        ("Studying",  "B.Tech, Computer Engineering, SPIT (2027)"),
        ("Latest",    "CareCircle, Nov 2026"),
        ("Learning",  "Distributed systems"),
        ("Based in",  "Mumbai"),
    ],
}

# Figures on the about spread. build.py fails if a figure with a `check` key
# drifts from what it counts.
FIGURES = [
    {"value": 10, "suffix": "", "label": "builds shipped in 2026", "check": "changelog_2026"},
    {"value": 2, "suffix": "",  "label": "hackathon prizes, solo", "check": "results"},
    {"value": 5, "suffix": "",  "label": "certifications",          "check": "certifications"},
    {"value": 3, "suffix": "+", "label": "years on Python"},
]

# --- prizes -------------------------------------------------------------------
# Placed entries only. Wording rule: Rote is "Winner · 3rd place" (WeMakeDevs titles
# its graphic "Hackathon Winners", 1st to 3rd, above two runner-ups). Never "winner"
# without the place next to it. Environmental Hacks is always "Runner-up".

RESULTS = [
    {
        "id": "env-hacks",
        "rank": "Runner-up",
        "event": "Environmental Hacks",
        "organizer": "WeMakeDevs × AWS · Bharat Builds Tour, event 02",
        "dates": "8–11 Oct 2026",
        "field": "9,146 registered. One of 4 runners-up across all three tracks.",
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
            {"label": "Read the feature", "href": "/teesri-shikayat/"},
            {"label": "Demo video", "href": "https://youtu.be/L0UteWpltyw"},
        ],
        # Crops of the organisers' runner-ups graphic: its header and Aryan's own
        # card only. The other teams' photos are left out (shown as a break line).
        "proof": {
            "caption": "From the official WeMakeDevs × AWS runner-ups graphic. "
                       "The other three teams are cut at the break.",
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
        # "The Rote Playoffs hackathon winners are…").
        "event": "Rote Playoffs Hackathon",
        "organizer": "WeMakeDevs × Modiqo",
        "dates": "1–6 Sep 2026",
        "field": "Of ~900 published plays.",
        "track": "Open",
        "prize": "iPhone 17",
        "team": "Solo",
        "build": "Four plays and one platform defect",
        "summary": (
            "four read-only GitHub plays for Modiqo's Rote registry, and the finding that "
            "carried them: the runtime silently kept only the first 64 KiB of a step's "
            "output and still reported success. 221 of the 249 public plays that read "
            "that output (89%) never checked. Filed upstream; fixed in rote v0.83.0."
        ),
        "demo": "truncation",
        "links": [
            {"label": "Write-up", "href": "https://aryangorde6.github.io/rote-stdout-truncation/"},
            {"label": "Upstream issue", "href": "https://github.com/modiqo/rote-releases/issues/10"},
        ],
        "proof": {
            "caption": "From the official WeMakeDevs × Modiqo winners graphic. "
                       "The other winners are cut at the break.",
            "post": "https://www.linkedin.com/posts/the-rote-playoffs-hackathon-winners-are-share-7505295266309132288-6Rjf/",
            "parts": [
                {"name": "rote-head", "alt": "WeMakeDevs × Modiqo graphic: Rote Playoffs hackathon winners."},
                {"name": "rote-row", "alt": "3rd position, Apple iPhone 17: Aryan Gorde."},
            ],
        },
    },
]
# One-line rank, e.g. "Winner · 3rd place" (structured data, chips).
for _r in RESULTS:
    _r["rank_full"] = " · ".join(x for x in (_r.get("rank_lead"), _r["rank"]) if x)

# The 64 KiB slider on the Rote spread. Numbers from ~/rote_hack/HACKATHON-HANDOFF.md
# and the write-up: output past 64 KiB was dropped while the step still reported
# success; 221 of the 249 registry plays that read step output never checked.
TRUNCATION = {
    "limit_kib": 64,
    "max_kib": 256,
    "start_kib": 120,   # past the limit, so the page shows a loss before any script runs
    "plays_reading": 249,
    "plays_unchecked": 221,
}

# Fixes merged into other people's projects. Source: the PRs (gh pr view) and
# Pillow 13.0.0's release notes, checked 08 Nov 2026. NumPy has not released
# since the merge, so it claims "merged into main" and no more.
UPSTREAM = [
    {
        "id": "pr-numpy",
        "project": "NumPy",
        "repo": "numpy/numpy",
        "number": 32915,
        "title": "BUG: close the file in np.load when an .npz is invalid",
        "summary": (
            "<code>np.load</code> left the file open when handed a broken <code>.npz</code> "
            "(an interrupted download, say), and Python warned about an unclosed file. "
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
        "href": "https://github.com/python-pillow/Pillow/pull/10147",
    },
]

# Every other hackathon entered in 2026, newest first. Outcome says only what is
# known: "Submitted" means submitted, nothing more is claimed.
ENTRIES = [
    {"when": "Nov 2026", "event": "Catalyst Solo AI Hackathon", "organizer": "Makers Need More × PromptWars",
     "build": "CareCircle", "what": "a shared care book where missed doses climb from the elder to the family",
     "outcome": "Round 1: 35th of 1,225"},
    {"when": "Nov 2026", "event": "Flip the Switch", "organizer": "WeMakeDevs × DevTools Academy × Switch",
     "build": "Jaisa Kaha", "what": "an AI scribe that won't invent a cook's quantities",
     "outcome": "Submitted · Track 02"},
    {"when": "Nov 2026", "event": "Global AI Developer Hackathon", "organizer": "Meta",
     "build": "Teesra Kaan", "what": "warns on a scam call and shows the caller's next line",
     "outcome": "Submitted · Indie track"},
    {"when": "Oct 2026", "event": "Graph Hacks", "organizer": "WeMakeDevs × FalkorDB",
     "build": "Shaky Ground", "what": "finds the science built on retracted research",
     "outcome": "Submitted · Track 01"},
    {"when": "Oct 2026", "event": "Dark Factory", "organizer": "WeAreDevelopers × Band",
     "build": "The Adversary Line", "what": "five coding-agent seats building and attacking a reservation service",
     "outcome": "Submitted"},
    {"when": "Sep 2026", "event": "IBM Bob 2.0 Hackathon", "organizer": "lablab.ai × IBM",
     "build": "Antibody", "what": "checks that fixed bugs stay fixed (team of 2)",
     "outcome": "Submitted"},
    {"when": "Sep 2026", "event": "First Commit", "organizer": "WeMakeDevs × AWS",
     "build": "Pukaar", "what": "one press pages the three people most likely to answer, at once",
     "outcome": "Submitted · 13,664 registered"},
    {"when": "Sep 2026", "event": "AI Trading Agents Hackathon", "organizer": "lablab.ai × Alpaca",
     "build": "Contour", "what": "an options agent that sells only the rich side of the skew",
     "outcome": "Submitted"},
]

# --- stack ------------------------------------------------------------------
# The tools, by the hop where they do their job in a request. Only tools that a
# public aryangorde6 repo (or this site) actually uses: checked repo by repo on
# 16 Nov 2026 (dependency files, workflows, READMEs). Add a tool only with a repo
# that shows it.
STACK = [
    {"label": "Client", "note": "Enough frontend to ship the whole thing solo.",
     "items": ["Vanilla JS", "Jinja2", "WebSockets"]},                        # carecircle, teesra-kaan, this site
    {"label": "Edge", "note": "Where a request comes in.",
     "items": ["CloudFront", "Telegram bots", "Discord"]},                     # this site; pukaar, teesri-shikayat; jaisa-kaha
    {"label": "Voice", "note": "Speech in, speech out, Hindi included.",
     "items": ["AWS Transcribe", "Muse Voice Transcribe", "Polly", "Cloud Text-to-Speech"]},
    {"label": "Application", "note": "Where most of the time goes.",
     "items": ["FastAPI", "Uvicorn", "Pydantic"]},                             # carecircle, teesra-kaan, contour
    {"label": "Data", "note": "Storage, and the queries between.",
     "items": ["DynamoDB", "Firestore", "FalkorDB", "S3"]},                    # pukaar, teesri; carecircle; shaky-ground
    {"label": "Async", "note": "Work that shouldn't block a request.",
     "items": ["Step Functions", "EventBridge", "SQS", "Cloud Scheduler"]},    # pukaar, teesri; carecircle
    {"label": "AI", "note": "Used where it earns its latency.",
     "items": ["Amazon Bedrock", "Gemini on Vertex AI", "Muse Spark", "Groq",
               "Gemma 4 on llama.cpp", "Strands", "Cedar", "MCP"]},
    {"label": "Runtime", "note": "Where it all runs.",
     "items": ["Docker", "AWS Lambda", "Amazon EC2", "Cloud Run"]},
    {"label": "Infrastructure", "note": "Written down, so it can be rebuilt.",
     "items": ["Terraform", "AWS CDK", "CloudFormation"]},                     # pukaar; teesri-shikayat; this site
    {"label": "CI / CD", "note": "Tests on every push. This site deploys itself from main.",
     "items": ["GitHub Actions", "pytest"]},
]

# TypeScript: the Rote plays. HCL: pukaar's Terraform. Cypher: shaky-ground.
LANGUAGES = ["Python", "TypeScript", "JavaScript", "Bash", "Cypher", "HCL"]

# --- features: one page each ----------------------------------------------------
# Only projects on github.com/aryangorde6 (Aryan, 08 Nov 2026). Sources: each repo's
# README (fetched 08 Nov 2026) and the hackathon STATE files.
#   slug     the page lives at /<slug>/
#   hindi    the Devanagari name, set big in the headline. Every character used here
#            must be in fonts/anek-devanagari-names.woff2 (a subset): build.py checks.
#   gloss    what the name means, from the project's own README or summary
#   video    a silent 8 s loop cut from Aryan's own demo recording (build_src/video/)
#   demo     an interactive figure drawn by the template ("tripwire")
#   teaser   the line under the name on the home page

FEATURES = [
    {
        "slug": "teesri-shikayat",
        "name": "Teesri Shikayat",
        "hindi": "तीसरी शिकायत",
        "gloss": "the third complaint",
        "kicker": "Runner-up · WeMakeDevs × AWS Environmental Hacks",
        "teaser": "Three complaints, one warning. A dirty-water tripwire on AWS that only "
                  "residents can switch off.",
        "dek": (
            "A tripwire for dirty tap water, from my own monsoon tap in Mumbai. Residents "
            "complain with a Hindi voice note on Telegram. When three different homes within "
            "250 m report dirty water inside 72 hours, every enrolled home in the ring is "
            "warned in Hindi, and only the residents can close the case."
        ),
        "video": "teesri-shikayat",
        "video_caption": "The demo console, recorded: the third report lands and the ring "
                         "is drawn. Simulated homes. Map © OpenStreetMap contributors.",
        "demo": "tripwire",
        "figures": [
            {"value": "20/23", "note": "homes warned in the demo incident had never complained."},
            {"value": "₹0.94", "note": "measured AWS cost of one real incident, end to end."},
            {"value": "66", "note": "tests, run in CI on every push."},
        ],
        "quote": ("The ward office said resolved. The AI believed them.", "Cedar didn’t."),
        "quote_note": (
            "The model chooses the words; code and policy choose the actions. A ward office’s "
            "“resolved” only asks to close the case. Any resident’s “not clean” reopens it, "
            "and silence never closes it."
        ),
        "flow_title": "One case, as the demo recorded it",
        "flow_caption": "A single Step Functions execution, waiting on people, never on a timer.",
        "flow": [
            ("Third report", "3 homes · 250 m · 72 h"),
            ("Volunteer", "approves with one tap"),
            ("Ring warned", "Hindi text + Polly voice"),
            ("Ward office", "replies “resolved”"),
            ("Cedar", "denies close_case"),
            ("Residents", "one says “not clean”"),
            ("Reopened", "silence never closes it"),
        ],
        "detail": [
            ("Listening",
             "Hindi voice notes arrive on Telegram and go through Amazon Transcribe (hi-IN). "
             "Bedrock quota was zero, so an open model fills a fixed schema instead: Gemma 4 "
             "E4B in llama.cpp on an EC2 Graviton4 instance. Code validates every field."),
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
    },
    {
        "slug": "teesra-kaan",
        "name": "Teesra Kaan",
        "hindi": "तीसरा कान",
        "gloss": "the third ear",
        "kicker": "Scam-call guardian · Meta Global AI Developer Hackathon, Indie track",
        "teaser": "The third ear on a scam call. It warns in the caller's own words, then "
                  "shows his next line before he says it.",
        "dek": (
            "Put a suspicious call on speaker and it listens in Hindi, Marathi or English. "
            "The moment the caller starts a known scam it warns you in your language, quoting "
            "his own words. Then it shows his next line before he says it."
        ),
        # Aryan, 08 Nov: link the live page. The meta STATE planned to stop the server
        # after 16 Nov: re-check then and drop this if it's down.
        "live": {"label": "Try it live", "href": "https://teesrakaan.aryangorde.com"},
        "figures": [
            {"value": "131/132", "note": "real US scam robocalls from the FTC warned on, in a test "
                                         "fixed before any result existed."},
            {"value": "9/9", "note": "scam calls still caught with every keyword rewritten out. "
                                     "A keyword list caught none."},
            {"value": "0/15", "note": "genuine test calls warned on, amber or red (synthetic voices)."},
        ],
        # The one call re-enacted by people on a real phone line (README, "Does it
        # work?"). Outside the frozen test: an example, not a measurement.
        "timeline": {
            "title": "One call, to scale",
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
        "slug": "shaky-ground",
        "name": "Shaky Ground",
        "kicker": "Citation graph · Graph Hacks (WeMakeDevs × FalkorDB), Track 01",
        "teaser": "Finds the science built on retracted research, not just the papers "
                  "that cite it.",
        "dek": (
            "Finds the science built on retracted research, not just the papers that cite it. "
            "Every citation is weighted by how much the citing paper relies on the cited one, "
            "a chain's risk is computed in Cypher, and an agent decides which branches to "
            "explore. Every answer comes back with its evidence."
        ),
        "video": "shaky-ground",
        # README, "Blast radius": ring k = strongest chain has k links; orange = builds on it.
        "video_caption": "The live demo, recorded: the retracted 2006 paper at the centre, each "
                         "ring one more citation away, and the papers that build on it in orange.",
        "figures": [
            {"value": "45", "note": "papers found building on Lesné et al. 2006 (Nature, retracted "
                                    "2024). Two of them were retracted themselves."},
            {"value": "0.45 s", "note": "to score every chain of up to three citations across 10,852 "
                                        "papers. Brute force took 287.8 s, with 0 mismatches."},
            {"value": "27/30", "note": "links a third model, from another family, classed exactly as "
                                       "the judges did."},
        ],
        # Schematic: the weights and the 0.2 threshold are the README's; the papers
        # are illustrative.
        "chain": {
            "title": "How a chain is scored",
            "nodes": [("Retracted paper", "1.0"), ("Paper A", "1.0"), ("Paper B", "0.6"),
                      ("Paper C", "0.36")],
            "links": [("Foundational", "× 1.0", "uses its method"),
                      ("Supporting", "× 0.6", "relies on its finding"),
                      ("Supporting", "× 0.6", "relies on its finding")],
            "verdict": "Builds on it",
            "branch": (("Background", "× 0.15", "mentions it in passing"), ("Paper D", "0.15"), "In passing"),
            "rule": "Builds on it when risk ≥ 0.2: three supporting links score 0.6³ = 0.216, and "
                    "any background link caps a chain at 0.15.",
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
    {
        "slug": "jaisa-kaha",
        "name": "Jaisa Kaha",
        "hindi": "जैसा कहा",
        "gloss": "as she said it",
        "kicker": "Agents with owners · Flip the Switch, Track 02",
        "teaser": "An AI scribe that refuses to make up a cook's quantities. Only the cook's "
                  "own account can fill a gap.",
        "dek": (
            "An AI scribe that refuses to make up a cook's quantities. It writes down only the "
            "amounts that were said and keeps a gap where none was (or where the cook said "
            "“by feel”), and only the cook's own account can fill it. On a test sentence, four "
            "models out of four turned “ghee, by feel” into a number."
        ),
        "video": "jaisa-kaha",
        "video_caption": "From the demo: I answer for the cook, and Switch refuses me under "
                         "Pothi's name. In the demo I play the cook on a second, labelled account.",
        "figures": [
            {"value": "7/8", "note": "missing amounts four models turned into numbers on a plain "
                                     "prompt, on the demo dish."},
            {"value": "0", "note": "numbers on Pothi's page that aren't a quote from the tape or "
                                   "typed by the cook."},
            {"value": "87", "note": "tests, Python standard library only."},
        ],
        "flow_title": "One dish through the Discord room",
        "flow_caption": "Switch checks every message against its addressee's rule, so Pothi "
                        "refuses everyone but the cook and Tape. That includes the AI, and me.",
        "flow": [
            ("Voice note",  "the cook, in Marathi"),
            ("Tape",        "Transcribe mr-IN · every word, with its second"),
            ("Lekhak",      "Qwen3 on Bedrock · each amount cites the tape"),
            ("Pothi",       "the cook's own agent · asks about gaps only"),
            ("Cook",        "fills a gap, then “page pakka”"),
            ("Page",        "only Pothi can change it"),
        ],
        "detail": [
            ("It never types a quantity",
             "Lekhak (“writer”), an LLM on Amazon Bedrock in Mumbai, writes the draft as JSON, "
             "and every amount is a range of words on the tape. Pothi (“the book”) is plain code "
             "with no model: it reads the cited words off the tape and marks each line said, a "
             "gap for the cook, or struck."),
            ("Switch writes the refusal",
             "Pothi belongs to the cook in Switch's records. When I or the AI try to give it a "
             "number, Switch's server refuses under Pothi's name, and Pothi's code never "
             "receives the message."),
            ("Measured before the first recording",
             "Both prompts were committed with their SHA-256 before the first real recording, "
             "then run on four models on Bedrock. On the demo dish the plain prompt made up 7 "
             "of 8 missing amounts. One recipe is a tiny sample, and the README says so."),
            ("For Mom's recipes",
             "Built for my mother's recipes; the page is for my sister, who is learning them. "
             "In the demo I play the cook on a second account, and the voice note is a "
             "synthetic voice. Both are labelled on screen."),
        ],
        "tech": ["Switch", "Discord", "AWS Transcribe", "Amazon Bedrock", "Python (stdlib)"],
        "links": [
            {"label": "Demo video", "href": "https://youtu.be/fnLvEMvr4IU"},
            {"label": "Source", "href": "https://github.com/aryangorde6/jaisa-kaha"},
        ],
    },
]

# --- changelog --------------------------------------------------------------
# Every build on github.com/aryangorde6, newest first. There is no employment to
# list, so this is a dated log of shipped work, not a job history.
# `href` (optional) links to the build's feature page or its prize.

CHANGELOG = [
    {"period": "Nov 2026", "name": "CareCircle",
     "context": "Catalyst Solo AI Hackathon · Makers Need More × PromptWars · solo",
     "detail": "A care book shared by an elder, their caretakers and family, built in 7 hours. "
               "Each person has their own passcode and only the elder decides who sees what. "
               "Doses are stamped like a bank passbook, a missed one emails the caretakers at "
               "30 minutes and the family at 60, and Gemini turns a prescription photo or a "
               "Hindi voice note into a draft the elder confirms. Ranked 35th of 1,225 in the "
               "automated Round 1 review, 96.62/100.",
     "tech": ["Cloud Run", "Firestore", "Gemini", "Cloud Text-to-Speech", "Cloud Scheduler",
              "FastAPI"],
     "links": [{"label": "Try it live", "href": "https://carecircle-641776536530.asia-south1.run.app"},
               {"label": "Source", "href": "https://github.com/aryangorde6/carecircle"}]},

    {"period": "Nov 2026", "name": "Jaisa Kaha", "hindi": "जैसा कहा", "href": "/jaisa-kaha/",
     "context": "Flip the Switch · WeMakeDevs × DevTools Academy × Switch · solo",
     "detail": "An AI scribe for a family's recipes that writes down only the amounts the cook "
               "said and keeps a gap where none was. Three agents share one Discord room "
               "through Switch, and the cook's own agent refuses anyone else who tries to fill "
               "a gap, the AI and me included.",
     "tech": ["Switch", "Discord", "AWS Transcribe", "Amazon Bedrock"]},

    {"period": "Oct–Nov 2026", "name": "Teesra Kaan", "hindi": "तीसरा कान", "href": "/teesra-kaan/",
     "context": "Meta Global AI Developer Hackathon · Indie track",
     "detail": "A scam-call guardian in Hindi, Marathi and English that warns in the caller's "
               "own words and shows his next line before he says it. Tested once, on a set "
               "fixed before any result: 131 of 132 real FTC impersonation robocalls warned on.",
     "tech": ["Muse Voice Transcribe", "Muse Spark", "FastAPI"]},

    {"period": "Oct 2026", "name": "Shaky Ground", "href": "/shaky-ground/",
     "context": "Graph Hacks · WeMakeDevs × FalkorDB · solo",
     "detail": "Finds the science built on retracted research: a FalkorDB citation graph where "
               "every citation is weighted by reliance and a chain's risk is computed in "
               "Cypher, with an agent that decides where to dig and an MCP server for other agents.",
     "tech": ["FalkorDB", "Cypher", "MCP"]},

    {"period": "Oct 2026", "name": "Teesri Shikayat", "hindi": "तीसरी शिकायत", "href": "/teesri-shikayat/",
     "context": "WeMakeDevs × AWS Environmental Hacks · solo", "prize": "Runner-up",
     "detail": "A dirty-water tripwire for Mumbai: Hindi voice complaints on Telegram, a "
               "plain-code rule for three homes within 250 m inside 72 hours, and one Step "
               "Functions case per incident that only residents can close, guarded by a "
               "Strands agent checked with Cedar. One real incident cost ₹0.94.",
     "tech": ["Transcribe", "Polly", "EventBridge Pipes", "Step Functions", "Strands",
              "Cedar", "CDK"]},

    {"period": "Oct 2026", "name": "The Adversary Line",
     "context": "Dark Factory · WeAreDevelopers × Band · solo",
     "detail": "A dark software factory: five coding-agent seats in Band Desktop building a "
               "reservation service in stages, each a complete container, while one seat "
               "plants known bugs to test the checker. Run on free models, for $0.",
     "tech": ["Band Desktop", "Docker"],
     "links": [{"label": "Source", "href": "https://github.com/aryangorde6/the-adversary-line"}]},

    {"period": "Sep 2026", "name": "Antibody",
     "context": "IBM Bob 2.0 Hackathon · lablab.ai · team of 2",
     "detail": "Do fixed bugs stay fixed? Antibody puts a project's past bug fixes back, one at "
               "a time, and runs its own tests. On sqlparse, 13 of 20 fixes were caught before "
               "and 18 of 20 after. Before the event: 479 fixes undone across 18 Python "
               "libraries, and 139 times every test still passed.",
     "tech": ["IBM Bob", "pytest", "GitHub Actions"],
     "links": [{"label": "Ledger", "href": "https://antibody-ledger.vercel.app/sqlparse/"},
               {"label": "Source", "href": "https://github.com/aryangorde6/antibody"}]},

    {"period": "Sep 2026", "name": "Pukaar", "hindi": "पुकार",
     "context": "WeMakeDevs × AWS First Commit · solo",
     "detail": "Help for an older person living alone: one press pages the three people most "
               "likely to answer, at the same time; the first to say “I'm going” wins, and "
               "the circle widens if nobody answers within a minute. Eleven languages, AAA "
               "contrast, 21 live checks.",
     "tech": ["Step Functions task tokens", "DynamoDB", "Terraform"],
     "links": [{"label": "Source", "href": "https://github.com/aryangorde6/pukaar"},
               {"label": "Demo", "href": "https://youtu.be/GaQZs1yBAyU"}]},

    {"period": "Sep 2026", "name": "Rote plays", "href": "#rote",
     "context": "WeMakeDevs × Modiqo Rote Playoffs Hackathon · solo", "prize": "Winner · 3rd place",
     "detail": "Four read-only plays for pull-request review (unresolved threads, flaky CI, "
               "who should review, and a truncation audit), plus a measured platform defect: "
               "step output silently cut at 64 KiB, unchecked by 89% of public plays. Filed "
               "upstream and fixed in rote v0.83.0.",
     "tech": ["TypeScript", "GitHub GraphQL", "gh CLI"]},

    {"period": "Aug–Sep 2026", "name": "Contour",
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
    "status": "Aug 2023 to June 2027",
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
    "headline_mark": "has to work.",
    "body": (
        "I'm after backend or full-stack work where the hard part is the system design, "
        "the data model, or keeping a deploy boring. If that's what you've got, I'd like "
        "to hear about it. Email is fastest, and I reply to everything that isn't a "
        "recruiter template."
    ),
    "links": [
        {"title": "GitHub",   "note": "@" + SITE["github_handle"], "href": SITE["github"]},
        {"title": "LinkedIn", "note": "the formal version", "href": SITE["linkedin"]},
        {"title": "Résumé",   "note": "PDF, one page",      "href": SITE["resume"]},
    ],
}

# --- colophon ---------------------------------------------------------------

COLOPHON = (
    "Set in Big Shoulders Display, Newsreader and Anek Devanagari, all self-hosted. Built by "
    "a small Python script (Jinja2 templates, content as Python data, a Pillow image "
    "pipeline) into static pages that make no third-party requests."
)
# Follows the colophon on every page. build.py fills in {kb}, that page's own size.
PAGE_WEIGHT = "This page’s HTML, with its styles and scripts inside, is {kb} KB. It sets no cookies."
