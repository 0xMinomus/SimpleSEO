# Sub-Skill 09: Live Production Verification & Scoring

Focus: Never assume an optimization worked locally. Verify every route, header, crawler response, and Lighthouse score against the live production domain.

## Verification Checklist

1. **Automated Structural & Live Audit**
   ```bash
   python3 scripts/simpleseo_audit.py https://www.example.com --format markdown
   ```
   Confirm:
   - Canonical host returns `HTTP 200` (zero redirect chains on canonical URLs)
   - `/sitemap.xml` redirects (`301`/`308`) cleanly or serves valid XML
   - `/sitemap-index.xml` and child sitemaps return `200` and list only canonical `200` URLs
   - `/robots.txt` returns `200` with zero syntax errors and allows target bots
   - `/llms.txt` returns `200` (`text/markdown`), valid H1 + links + >50 chars
   - `/.well-known/ai-catalog.json` returns `200` (`application/json`), passes ARD v1.0 checks
   - Unknown path `/this-page-does-not-exist-check` returns `404`
   - Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) present

2. **Bot User-Agent Verification**
   Test HTTP `200` response (no WAF/CAPTCHA challenge) for:
   - `Googlebot/2.1`
   - `OAI-SearchBot/1.0`
   - `ChatGPT-User/1.0`
   - `Claude-SearchBot/1.0`

3. **Live PageSpeed Insights / Lighthouse Audit**
   Run on Mobile and Desktop (via PSI API or `pagespeed.web.dev`):
   - Performance >= 90 (`CLS = 0`, fast LCP)
   - Accessibility = 100
   - Best Practices = 100
   - SEO = 100
   - Agentic Browsing = full pass (`4/4` or `N/N`)

4. **Mandatory Final PASS/FAIL Gate & Complete Report**
   - Run every check in the `SEO-01` through `SEO-10` Final Delivery Gate from `SKILL.md`.
   - Never deliver a report containing an unresolved `FAIL`. Fix any failure, redeploy, and re-measure first.
   - Always present the user with:
     1. Complete list of every SEO task executed (technical, schema, on-page/sitelinks, GEO/AI, performance, GSC, IndexNow)
     2. Concrete benefit of each change
     3. Exact `PASS` / `FAIL` status backed by live command/Lighthouse/GSC evidence
     4. Honest summary of off-page actions outside code (Google Business Profile, external brand mentions, genuine reviews)
