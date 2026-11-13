# Sub-Skill 03: On-Page SEO, Sitelinks & Social Cards

Focus: Structure pages, headings, metadata, and internal links so single-page or small sites earn multi-link Google Sitelinks and rank for high-intent commercial keywords.

## Checks & Fixes

1. **Title & Meta Description Discipline**
   - Keep `<title>` between 50 and 65 characters with brand + primary keyword front-loaded cleanly.
   - Keep `<meta name="description">` between 140 and 160 characters with real value proposition, pricing/offer anchor (when applicable), and clear scope.
   - Ensure every route has a **unique** `<title>`, `<meta name="description">`, and `<h1>`.

2. **Sitelinks Architecture**
   - Single-page anchor links (`/#pricing`, `/#faq`) rarely qualify for standalone Google Sitelinks.
   - Build 3 to 6 focused, static sub-pages targeting each core customer intent (for example: main service page, pricing page, portfolio/case-studies page, and 1 to 3 niche vertical landing pages).
   - Link every sub-page clearly from the global `<footer>` (and/or header navigation) with descriptive anchor text, plus include `ItemList` of `SiteNavigationElement` in JSON-LD and visible breadcrumb navigation (`BreadcrumbList`).
   - Add cross-links between related sub-pages and back to `/#pricing` or `/`.

3. **Language, Region & Social Metadata**
   - Set `<html lang="...">` accurately (for example `id` or `en`).
   - Add `<link rel="alternate" hreflang="..." href="..." />` and `hreflang="x-default"` matching the canonical URL.
   - Include full Open Graph (`og:type`, `og:site_name`, `og:locale`, `og:title`, `og:description`, `og:url`, `og:image`, `og:image:width="1200"`, `og:image:height="630"`, `og:image:alt`) and `twitter:card="summary_large_image"`.
   - Verify `public/og-image.png` exists at `1200x630` and reflects current brand identity, pricing, and messaging (no stale copy or old logos).
