# Sub-Skill 05: Core Web Vitals & Image SEO

Focus: Keep Largest Contentful Paint (LCP) fast, Total Blocking Time (TBT) near zero, and Cumulative Layout Shift (CLS) locked at `0`.

## Checks & Fixes

1. **Zero Cumulative Layout Shift (`CLS = 0`)**
   - Add explicit `width` and `height` attributes on every `<img>` element across the homepage, portfolio cards, sub-pages, and header/footer logos.
   - Verify actual image dimensions on disk match declared aspect ratios.

2. **LCP Optimization**
   - Add `<link rel="preload" as="image" href="/path/to/hero-image.webp" fetchpriority="high" />` in `<head>` for pages that display a hero image above the fold.
   - Set `loading="eager"`, `decoding="async"`, and `fetchpriority="high"` on the hero/LCP `<img>`.
   - Set `loading="lazy"` and `decoding="async"` on below-the-fold images.

3. **Modern Formats & Asset Weight**
   - Prefer `.webp` or `.avif` for photographic previews and `.svg` for geometric marks and icons.
   - Flag oversized raster assets (>200 KB for hero/banner images, >100 KB for content cards, >50 KB for thumbnails).

4. **Accessibility & Semantic Cleanliness**
   - Ensure every meaningful `<img>` has descriptive, natural `alt` text (10 to 125 chars, no keyword stuffing).
   - Mark purely decorative avatars/ornaments with `alt=""` and `role="presentation"` or `aria-hidden="true"` so screen readers and Lighthouse Accessibility score `100/100`.
   - Keep external font requests minimal with `preconnect` and `display=swap`.
