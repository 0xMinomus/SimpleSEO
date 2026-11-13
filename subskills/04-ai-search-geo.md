# Sub-Skill 04: AI Search & Agent Readiness (GEO)

Focus: Ensure AI answer engines (Google AI Overviews, AI Mode, ChatGPT Search, Perplexity, Claude, and Gemini) can crawl, parse, trust, and accurately cite your site.

## Checks & Fixes

1. **Explicit AI Crawler Access (`robots.txt`)**
   - Decide intentionally between Search/Citability bots and Training bots, and declare groups explicitly using standard RFC 9309 directives:
     - Google: `Googlebot`, `Google-Extended`
     - OpenAI: `OAI-SearchBot` (ChatGPT Search index), `ChatGPT-User` (live user browsing), `GPTBot`
     - Anthropic: `Claude-SearchBot`, `Claude-User`, `ClaudeBot`
     - Perplexity: `PerplexityBot`
     - Apple: `Applebot`
   - Never block `OAI-SearchBot` or `Claude-SearchBot` if the user wants AI search citations.

2. **`public/llms.txt` (`llmstxt.org` Standard)**
   - Serve at `/llms.txt` with `Content-Type: text/markdown; charset=utf-8`.
   - Follow the exact structural rules required by Lighthouse `llms-txt`:
     - Starts with an H1 (`# Brand Name`)
     - Followed by a concise blockquote (`> One-paragraph factual overview...`)
     - Organized `##` sections containing Markdown links (`- [Page Title](https://...): description`)
     - Minimum 50+ characters, clean UTF-8, no HTML soup.
   - Link in `<head>`: `<link rel="alternate" type="text/plain" title="AI Guide" href="/llms.txt" />`.

3. **`public/.well-known/ai-catalog.json` (ARD v1.0)**
   - Serve valid JSON at `/.well-known/ai-catalog.json` with `Content-Type: application/json; charset=utf-8` and `Access-Control-Allow-Origin: *`.
   - Include `"specVersion": "1.0"`, an `"entries"` array using `"urn:air:<domain>:<namespace>:<name>"` identifiers, `"displayName"`, `"type"`, `"url"` or `"data"`, 2 to 5 `"representativeQueries"`, and `"trustManifest": { "identity": "<domain>" }`.
   - Link in `<head>`: `<link rel="ai-catalog" href="/.well-known/ai-catalog.json" />`.

4. **Entity Clarity & Front-Loaded Citable Answers**
   - Define what your brand is in clear `"X is..."` phrasing in the first 30% of the page so AI models never confuse your brand with similarly named hosting providers, competitors, or foreign domains.
   - Structure service explanations, pricing tiers, and FAQs as self-contained factual statements with concrete deliverables, turnaround times, and currency.

See `references/ai-crawlers-and-ard.md` for full validation rules.
