# Final Verification Checklist

Run these checks after pushing changes to live production:

1. **Canonical & Redirects**
   - Canonical root URL returns `HTTP 200` with zero redirect hops.
   - Alternate host (apex or `www`) issues a single `301`/`308` to canonical.
   - `/sitemap.xml` redirects or resolves cleanly with zero `404`.
   - Unknown URLs return `HTTP 404` with `noindex`.
2. **Discovery & AI Files**
   - `/robots.txt` -> `HTTP 200`, valid RFC 9309 syntax.
   - `/sitemap-index.xml` and child sitemaps -> `HTTP 200`, only canonical `200` URLs.
   - `/llms.txt` -> `HTTP 200`, `text/markdown`, passes H1 + Markdown link checks.
   - `/.well-known/ai-catalog.json` -> `HTTP 200`, `application/json`, passes ARD v1.0 schema checks.
   - `/og-image.png` -> `HTTP 200`, `1200x630`.
3. **Security & Cache Headers**
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: SAMEORIGIN`
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - Immutable cache headers on static bundle assets and previews.
4. **Search Engine Submissions**
   - Google Search Console property verified (Domain property recommended).
   - Active sitemap submitted and showing `Success`.
   - Core URLs passed Live URL Test and queued via Request Indexing.
   - IndexNow ping returned `HTTP 200` or `HTTP 202`.
5. **Lighthouse / PageSpeed Insights**
   - Performance >= 90 (`CLS = 0`)
   - Accessibility = 100
   - Best Practices = 100
   - SEO = 100
   - Agentic Browsing = full pass (`N/N`)
