# SimpleSEO

**One skill call to take a deployed website from live URL to Google-ranked and AI-cited.**

Most SEO tools stop at giving you a long list of warnings you still have to fix by hand. **SimpleSEO** is a universal, end-to-end SEO skill pack designed to work across **any AI coding agent** (Oh My Pi, OpenAI Codex, Claude Code, Cursor, OpenCode, Gemini CLI, Windsurf, and Cline). Call it once, confirm two quick checkpoints, and let your agent audit, fix your codebase, submit sitemaps to Google and IndexNow, and verify real production scores.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/version-v1.0-green.svg)](https://github.com/0xMinomus/SimpleSEO/releases/tag/v1.0)
[![Python 3.10+ Stdlib](https://img.shields.io/badge/scripts-Python%203%20stdlib-yellow.svg)](scripts/)

---

## Why SimpleSEO Exists

Getting a website live is only half the job. Even well-built sites regularly miss traffic for basic reasons:
- `robots.txt` blocks AI crawlers or includes non-standard lines that fail Lighthouse SEO checks.
- Canonical URLs point to `example.com` while the host redirects `308` to `www.example.com`.
- Single-page sites never earn Google Sitelinks because all sections live on one URL hash.
- Images lack `width` and `height`, hurting Cumulative Layout Shift (CLS).
- Search engines like Bing and ChatGPT Search have zero indexed pages because nobody pinged IndexNow or submitted a clean sitemap.

SimpleSEO bundles all of those fixes, checks, and live submissions into **one structured skill package** with **nine specialized sub-skills** and **zero-dependency Python scripts**.

---

## Minimum Prerequisites

Before running SimpleSEO, your website only needs three things:

1. **Hosted and live over HTTPS** (Vercel, Cloudflare Pages, Netlify, VPS, etc.).
2. **A custom domain connected** (for example `yourdomain.com` or `www.yourdomain.com`).
3. **Registered in Google Search Console** (either as a Domain property or URL-prefix property).

Not there yet? Do not worry. When you invoke SimpleSEO and answer **No** at the first check, it pauses automatically and walks you through hosting, DNS, and Google Search Console verification step by step.

---

## How SimpleSEO Works (Two-Gate Flow)

SimpleSEO never edits your project or touches your Search Console property without asking first. Every session follows two clear gates:

```
You call /simpleseo (or mention SimpleSEO)
          |
          v
[Gate 1] Are you hosted, on a custom domain, and in Google Search Console?
    |-- No  --> Stops immediately and gives you a step-by-step setup guide.
    |-- Yes --> Moves to Gate 2.
          |
          v
[Gate 2] Shows all 9 sub-skills + their benefits and asks for confirmation.
    |-- Run all end-to-end --> Audits, fixes code, builds, submits GSC/IndexNow, verifies live scores.
    |-- Audit only         --> Read-only diagnostic report, zero files touched.
    |-- Pick modules       --> Runs only the sub-skills you choose.
```

---

## Included Sub-Skills & Benefits

SimpleSEO packs **9 sub-skills** inside one root skill so you do not have to install or coordinate separate plugins:

| # | Sub-Skill | What It Handles | Benefit to You |
|---|---|---|---|
| 1 | **Technical & Crawl Architecture** | Aligns canonicals across config/HTML/sitemap/JSON-LD, redirects `/sitemap.xml` to `/sitemap-index.xml`, enforces RFC 9309 `robots.txt`, adds security & immutable cache headers, and ships a `noindex` `404` page. | Search bots crawl the exact right URL with zero redirect loops, 404 traps, or wasted crawl budget. |
| 2 | **Structured Data & Schema.org** | Generates server-rendered JSON-LD `@graph` (`Organization` / `ProfessionalService` / `LocalBusiness`, `WebSite`, `WebPage`, `BreadcrumbList`, `SiteNavigationElement`, `OfferCatalog`, `Product`, `FAQPage`) using active Schema types only. | Eligible for Google rich results, clear entity recognition, and clean pricing/service parsing. |
| 3 | **On-Page, Sitelinks & Social Cards** | Sharpens titles and meta descriptions, adds `hreflang`, builds focused sub-pages linked cleanly from footer/nav, and updates `1200x630` Open Graph & Twitter share cards. | Higher click-through rates, multi-link Google Sitelinks under your brand, and accurate social previews. |
| 4 | **AI Search & Agent Readiness (GEO)** | Opens explicit crawl access for `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `PerplexityBot`, and `Google-Extended`; creates `llms.txt` and `/.well-known/ai-catalog.json` (ARD v1.0); structures direct answer passages. | Prepares your site to be crawled, understood, and cited by ChatGPT Search, Perplexity, Claude, and Google AI Overviews. |
| 5 | **Core Web Vitals & Image SEO** | Adds LCP `<link rel="preload">` + `fetchpriority="high"`, explicit `width` and `height` on all `<img>` tags, lazy loading below the fold, and accessible `alt` / `role="presentation"` handling. | Locks `CLS = 0`, improves mobile speed, and targets 100/100 Accessibility. |
| 6 | **Search Engine Submission (GSC + IndexNow)** | Verifies GSC Domain property via DNS `TXT`, cleans up old CMS sitemaps, submits live `sitemap-index.xml`, runs Live URL Inspection + Request Indexing, and pings `api.indexnow.org` for Bing/Copilot/ChatGPT Search. | Speeds up discovery across both Google and non-Google search indexes from weeks to hours. |
| 7 | **Local SEO, E-E-A-T & Off-Page Plan** | Configures `geo.region`, `geo.placename`, and `areaServed` schema, verifies truthful contact/portfolio signals, and maps out Google Business Profile, backlinks, and brand mentions. | Boosts local map pack relevance and builds off-site proof without fabricating fake reviews or stats. |
| 8 | **Content Quality & Topic Clusters** | Audits thin routes, heading hierarchy (`H1` to `H3`), duplicate metadata, and internal cross-linking across services. | Prevents keyword cannibalization and strengthens topical authority. |
| 9 | **Live Production Verification** | Runs live HTTP checks, tests bot User-Agents (`Googlebot`, `OAI-SearchBot`, `ChatGPT-User`), validates `llms.txt` and `ai-catalog.json`, and checks PageSpeed Insights / Lighthouse scores. | Proves everything works in production with real measured scores. |

---

## Installation (Any Coding Agent)

SimpleSEO follows the open `SKILL.md` + `AGENTS.md` standard and ships manifests for major coding agents. Pick the option that matches your tool:

### Option 1: Universal Skills CLI (`npx skills`)
Works with Oh My Pi, Codex, Claude Code, Cursor, OpenCode, Windsurf, and more:

```bash
npx skills add 0xMinomus/SimpleSEO
```

### Option 2: Direct Clone into Your Agent's Global Skills Folder

```bash
# Oh My Pi
git clone https://github.com/0xMinomus/SimpleSEO.git ~/.omp/agent/skills/SimpleSEO

# Claude Code
git clone https://github.com/0xMinomus/SimpleSEO.git ~/.claude/skills/SimpleSEO

# OpenAI Codex
git clone https://github.com/0xMinomus/SimpleSEO.git ~/.codex/skills/SimpleSEO

# Cursor
git clone https://github.com/0xMinomus/SimpleSEO.git ~/.cursor/skills/SimpleSEO
```

### Option 3: Project-Level Use
Clone or copy `SimpleSEO` into your repository or workspace and point your agent to `SKILL.md` or `AGENTS.md`.

---

## How to Use It

1. Open your website repository in any supported AI coding agent.
2. Invoke the skill explicitly:
   ```text
   /simpleseo https://www.yourdomain.com
   ```
   Or simply mention it in your prompt:
   ```text
   Run SimpleSEO on this project and https://www.yourdomain.com
   ```
3. Answer **Gate 1** (confirm you have hosting, a custom domain, and Google Search Console, or follow the guided setup if not).
4. Review the sub-skills and benefits in **Gate 2**, then confirm **Yes, run all SimpleSEO sub-skills end to end**.
5. Let the agent inspect, apply changes, build, deploy, submit sitemaps/IndexNow, and deliver the final live verification report.

---

## Standalone CLI Tools (Python 3 Stdlib, No Pip Install Needed)

You or your agent can also run SimpleSEO's bundled utilities directly from the terminal:

### 1. Live Site & AI Readiness Auditor
Checks canonical alignment, HTML size vs Googlebot's 2 MB cap, headers, JSON-LD types, deprecated schema, image dimensions, `robots.txt` RFC 9309 compliance, sitemaps, `llms.txt`, `/.well-known/ai-catalog.json`, and `404` status:

```bash
python3 scripts/simpleseo_audit.py https://www.yourdomain.com --format markdown
python3 scripts/simpleseo_audit.py https://www.yourdomain.com --format json
```

### 2. Asset Generator (`robots.txt`, `llms.txt`, `ai-catalog.json`)
Generates Lighthouse-compliant starter files inside `public/`:

```bash
python3 scripts/generate_assets.py \
  --brand "YourBrand" \
  --domain "yourdomain.com" \
  --origin "https://www.yourdomain.com" \
  --summary "Clear one-paragraph overview of your business and services." \
  --public-dir ./public
```

### 3. IndexNow Key Creator & Instant Ping
Creates a 32-char hex verification key in `public/`, verifies it live over HTTPS, and submits URLs to Bing, Copilot, DuckDuckGo, and ChatGPT Search via IndexNow:

```bash
python3 scripts/indexnow_ping.py \
  --host www.yourdomain.com \
  --public-dir ./public \
  --urls https://www.yourdomain.com/ https://www.yourdomain.com/services/
```

---

## Running Tests

SimpleSEO includes a unit test suite covering HTML parsing, deprecated schema detection, RFC 9309 `robots.txt` validation, `llms.txt`, ARD `ai-catalog.json`, and IndexNow key management:

```bash
python3 -m unittest discover -s tests -v
```

---

## Repository Layout

```text
SimpleSEO/
├── SKILL.md                        # Universal orchestrator & 2-gate prompt protocol
├── AGENTS.md                       # Universal agent entrypoint
├── .claude-plugin/                 # Claude Code plugin & marketplace manifests
├── .codex-plugin/                  # OpenAI Codex plugin manifest
├── .cursor-plugin/                 # Cursor plugin manifest
├── subskills/                      # 9 modular execution guides
├── references/                     # Setup guide, Schema templates, ARD & QA checklists
├── scripts/                        # Zero-dependency Python 3 audit, generator, and IndexNow CLIs
├── tests/                          # Unit tests for all bundled scripts
├── LICENSE                         # MIT License
├── SECURITY.md                     # Security & vulnerability disclosure policy
├── CODE_OF_CONDUCT.md              # Contributor Covenant v2.1
├── CONTRIBUTING.md                 # Contribution workflow
└── CHANGELOG.md                    # Release history
```

---

## Honest Scope Note

SimpleSEO maximizes everything controllable in your website codebase, server headers, structured data, performance, Google Search Console, and IndexNow. Off-page signals like Google Business Profile registration, genuine customer reviews, and third-party backlinks/brand mentions still require your own real-world accounts and outreach, and SimpleSEO will clearly hand you that action list at the end instead of inventing fake metrics.

---

## License

Released under the [MIT License](LICENSE). Built by [Andika Putra (0xMinomus)](https://github.com/0xMinomus).
