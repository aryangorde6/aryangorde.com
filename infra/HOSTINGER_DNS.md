# Hostinger DNS changes for the AWS move

hPanel → **Domains** → aryangorde.com → **DNS / Nameservers** → **DNS records**.
In hPanel the **Name** field is the part before `.aryangorde.com` (`@` means the domain itself).

## Step 1: prove you own the domain (for the free HTTPS certificate)

These two records are harmless. They don't change the live site. (Added 08 Nov 2026.)

| Type  | Name | Points to (target) | TTL |
|-------|------|--------------------|-----|
| CNAME | `_7e9b4fac1011b99b3535ec88eb407fd0` | `_c8b914caa3950df940937c6251f68dbe.wzccmgtwzk.acm-validations.aws` | 300 |
| CNAME | `_12e8d45e39c0221f79da6203817145e6.www` | `_5cb63c3cf08951a48c0afe11816700cc.wzccmgtwzk.acm-validations.aws` | 300 |

Keep them afterwards. The certificate in use (08 Nov) covers `aryangorde.com` + `*.aryangorde.com`;
AWS renews it every year through the **first** record (`_7e9b…`), which must never be deleted.
The `www` one is spare (only needed if a www-specific certificate is ever requested).

The first certificate request **failed for www** (`CAA_ERROR`, 08 Nov 16:14): `www` was a CNAME to
`aryangorde8.github.io`, and a CAA check follows a CNAME, so AWS read GitHub's CAA records
(`github.io` allows only DigiCert, Let's Encrypt and Sectigo — not Amazon). The bare domain has no
CAA record and passed. Hence Step 1b.

## Step 1b: move `www` off the github.io name (no visible change) — done 08 Nov 16:33

Point `www` at GitHub Pages' four IP addresses directly instead of through `aryangorde8.github.io`.
GitHub still serves www exactly as before (301 → https://aryangorde.com, its certificate covers
www until 11 Dec 2026 — checked 08 Nov), but the CAA lookup no longer lands on github.io.

| Action | Type | Name | Value | TTL |
|--------|------|------|-------|-----|
| Delete | CNAME | `www` | `aryangorde8.github.io` | |
| Add | A | `www` | `185.199.108.153` | 300 |
| Add | A | `www` | `185.199.109.153` | 300 |
| Add | A | `www` | `185.199.110.153` | 300 |
| Add | A | `www` | `185.199.111.153` | 300 |

Then a new certificate is requested for both names (a failed one can't be retried). AWS's own DNS
cache still remembered the old CNAME (TTL 14400 s), so www failed CAA once more at 16:35.
**Workaround used (16:48):** a certificate for `aryangorde.com` + `*.aryangorde.com`. For a wildcard
name AWS reads the CAA of the bare domain (none), not of `www`, so the stale cache didn't matter;
the wildcard covers www.

## Step 2: switch the site to AWS (only after the certificate is issued)

**Only after the new certificate is issued and attached to CloudFront**; switching earlier makes
the site show an error.

**2a — bare domain** (done 08 Nov 16:43):

| Action | Type | Name | Value |
|--------|------|------|-------|
| Delete | A | `@` | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` (GitHub Pages, 4 records) |
| Add | CNAME (hPanel shows it as **ALIAS**) | `@` | `d3enmg35mhhoy0.cloudfront.net` |

**2b — www** (done 08 Nov 16:56, after the wildcard certificate was attached with `IncludeWww=true`):

| Action | Type | Name | Value |
|--------|------|------|-------|
| Delete | A | `www` | the 4 GitHub Pages addresses from Step 1b |
| Add | CNAME | `www` | `d3enmg35mhhoy0.cloudfront.net` |

TTL: 300 for the new records, so a mistake can be undone quickly. Visitors move over as the old
records expire (the apex A records have TTL 14400 s, so up to about 4 hours).

**To roll back:** delete the ALIAS and the `www` CNAME, put the four `@` A records back and point
`www` at GitHub again (CNAME `aryangorde8.github.io`, or the four A records). GitHub Pages keeps
serving the old site until it is turned off.

## Do not touch

Everything else in the zone stays exactly as it is:

| Type | Name | Value | Why |
|------|------|-------|-----|
| A | `teesrakaan` | 3.111.63.35 | Teesra Kaan server |
| A | `debtclear` | 13.200.237.92 | DebtClear server |
| A | `mnemos`, `mnemos-agent` | 13.205.64.168 | Mnemos server |
| A | `syshealth` | 13.202.179.37 | SysHealth server |
| CNAME | `_0031f0c60a9c013e56d87dd3596a84b8.syshealth` | …acm-validations.aws | SysHealth's certificate |
| A | `ticketforge` | 13.51.146.161 | TicketForge server |
| A | `mittiguard` | 98.91.44.205 | MittiGuard server |
| A | `devsync` | 3.108.36.149 | DevSync server |
| CNAME | three `…._domainkey` | `….dkim.amazonses.com` | Amazon SES email signing (DKIM) |
| TXT | `mail` | v=spf1 include:amazonses.com ~all | Amazon SES sender policy (SPF) |
| TXT | `@` | google-site-verification=… | Google Search Console |
| TXT | `_dmarc` | v=DMARC1; p=none; … | email policy |
