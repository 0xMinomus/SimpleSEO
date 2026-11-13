# Sub-Skill 01: Technical & Crawl Architecture

Focus: Make sure search engines and AI crawlers reach your exact canonical URL cleanly with fast edge caching, proper security headers, and zero dead links.

## Checks & Fixes

1. **Apex vs `www` Canonical Lock**
   - Test both `https://example.com/` and `https://www.example.com/` using `curl -sI`.
   - Identify which host returns `200 OK` and which issues a `301`/`308` redirect.
   - Lock the `200 OK` host everywhere:
     - Framework config (`astro.config.*` `site`, Next.js `metadataBase`, etc.)
     - `<link rel="canonical" href="...">`
     - `<meta property="og:url" content="...">`
     - XML sitemaps (`sitemap-index.xml`, `sitemap-0.xml`)
     - `public/robots.txt` `Sitemap:` line
     - JSON-LD `@id` and `url` fields
   - Never let canonical tags or sitemaps point to a redirecting host.

2. **`/sitemap.xml` Alias & Sitemap Quality**
   - If your framework emits `/sitemap-index.xml` (such as Astro `@astrojs/sitemap`), add a permanent redirect `/sitemap.xml -> /sitemap-index.xml` in `vercel.json` / `netlify.toml` / server config so crawlers probing `/sitemap.xml` never hit `404`.
   - Include `<lastmod>` timestamps where meaningful and exclude `noindex`, `404`, and utility routes from sitemaps.

3. **`robots.txt` Strict RFC 9309 Compliance**
   - Only use standard directives: `User-agent`, `Allow`, `Disallow`, `Sitemap`.
   - Avoid experimental or unrecognized tokens inside `robots.txt` because Google Lighthouse flags invalid lines under `robots.txt is not valid`, dropping the SEO score.
   - Verify no CSS, JS, fonts, or public preview images required for rendering are blocked.

4. **HTML Size & Initial Payload**
   - Keep critical copy, headings, internal links, and JSON-LD within the first 2 MB of uncompressed HTML so crawlers never truncate structured data or main content.
   - Never rely purely on client-side rendering for primary titles, descriptions, headings, or JSON-LD.

5. **Security & Edge Cache Headers**
   - Configure on your hosting platform (for example `vercel.json`):
     - `X-Content-Type-Options: nosniff`
     - `X-Frame-Options: SAMEORIGIN`
     - `Referrer-Policy: strict-origin-when-cross-origin`
     - `Permissions-Policy: camera=(), microphone=(), geolocation=()`
     - Long-lived immutable caching (`Cache-Control: public, max-age=31536000, immutable`) on fingerprinted JS/CSS bundles and static preview images.

6. **Real `404` Handling**
   - Ship a branded `404` page (`src/pages/404.astro`, `app/not-found.tsx`, etc.) with `<meta name="robots" content="noindex, nofollow">` and links back to the homepage and main service routes.
   - Verify unknown paths return HTTP `404` (not a soft-404 `200 OK` fallback).
