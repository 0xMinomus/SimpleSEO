# Sub-Skill 06: Search Engine Submission (GSC + IndexNow)

Focus: Put your updated sitemaps and pages straight into Google and Bing/ChatGPT/Copilot discovery queues instead of waiting passively for crawlers.

## Workflow

1. **Google Search Console (GSC)**
   - Check whether the user only has a URL-prefix property (`https://www.example.com/`) or also a **Domain property** (`example.com`).
   - If Domain property is unverified and DNS CLI/access is available (for example Vercel DNS, Cloudflare, or user's registrar):
     - Retrieve the `google-site-verification=...` TXT token from GSC.
     - Add the TXT record at root (`@`) and confirm propagation with `dig +short TXT example.com @8.8.8.8`.
     - Trigger **Verify Ownership** in GSC.
   - Open **Sitemaps** in GSC:
     - Remove any legacy dead sitemaps left behind by older CMS installations (such as old WordPress `post-sitemap.xml` or `product-sitemap.xml` files returning 404/stale URLs).
     - Submit the live canonical sitemap (`https://www.example.com/sitemap-index.xml`) and confirm status **`Success`**.
   - Open **URL Inspection** for the homepage and key landing pages:
     - Run **Test Live URL** (`URL is available to Google`, `Page can be indexed`, valid structured data items detected).
     - Click **Request Indexing** on each core URL until done (respecting daily quota).

2. **IndexNow Instant Submission (Bing, Copilot, DuckDuckGo, ChatGPT Search)**
   - Run `scripts/indexnow_ping.py`:
     ```bash
     python3 scripts/indexnow_ping.py --host www.example.com --public-dir public --urls https://www.example.com/ https://www.example.com/services/
     ```
   - Verify the `<key>.txt` file deploys and returns `HTTP 200`, then confirm `https://api.indexnow.org/indexnow` returns **`HTTP 200` or `HTTP 202`**.

3. **Optional Bing Webmaster Tools Sync**
   - Note that Bing Webmaster Tools offers 1-click import from verified Google Search Console accounts. Only perform browser actions on third-party accounts with explicit user consent.
