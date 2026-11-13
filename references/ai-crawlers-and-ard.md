# AI Crawlers, `llms.txt` & ARD v1.0 Reference

## AI Crawler Roles

| Token | Vendor | Purpose |
|---|---|---|
| `Googlebot` | Google | Google Search index and AI Overviews |
| `Google-Extended` | Google | Gemini grounding and generative training control |
| `OAI-SearchBot` | OpenAI | ChatGPT Search index and citations |
| `ChatGPT-User` | OpenAI | Live user-triggered fetches from ChatGPT |
| `GPTBot` | OpenAI | OpenAI model training |
| `Claude-SearchBot` | Anthropic | Claude search-result citability |
| `Claude-User` | Anthropic | Live user-triggered fetches from Claude |
| `ClaudeBot` | Anthropic | Anthropic model training |
| `PerplexityBot` | Perplexity | Perplexity search index |
| `Applebot` | Apple | Siri, Spotlight, and Safari discovery |

## `robots.txt` Compliance Note

Keep `public/robots.txt` strictly within RFC 9309 directives (`User-agent`, `Allow`, `Disallow`, `Sitemap`). Non-standard directives can trigger validation errors in Google Lighthouse's SEO audit.

## `llms.txt` Validation Rules

1. Served at `/llms.txt` (`Content-Type: text/markdown; charset=utf-8`).
2. Starts with an H1 heading (`# Brand Name`).
3. Includes a concise blockquote (`> ...`) summarizing what the site does.
4. Contains structured `##` sections with Markdown links (`- [Title](https://...): description`).
5. Total length is at least 50 characters.

## `/.well-known/ai-catalog.json` (ARD v1.0) Rules

1. Valid JSON object served with `Content-Type: application/json; charset=utf-8` and `Access-Control-Allow-Origin: *`.
2. Required root keys:
   - `"specVersion": "1.0"`
   - `"entries": [ ... ]` (must not contain deprecated top-level `"collections"`).
3. Each entry requires:
   - `"identifier"`: matches `^urn:air:<domain>[:<namespace>]:<name>$`
   - `"displayName"`: non-empty string
   - `"type"`: standard media type (for example `text/markdown; profile="urn:air:agent-skills"` or `application/ai-registry+json`)
   - Exactly one of `"url"` or `"data"` (never both in the same entry)
   - `"representativeQueries"`: array of 2 to 5 query strings
   - `"trustManifest": { "identity": "<domain>" }`
