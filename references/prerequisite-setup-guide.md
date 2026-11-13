# Prerequisite Setup Guide (Gate 1 Fallback)

Use this guide when the user answers **No** at Gate 1 (not yet hosted, missing custom domain, or not yet registered in Google Search Console).

---

## Step 1: Deploy Your Website Live Over HTTPS

1. Build your site locally first to confirm zero build errors (`npm run build` or equivalent).
2. Deploy to a fast static/edge host with automatic HTTPS:
   - **Vercel**: Connect your Git repository or run `npx vercel --prod`.
   - **Cloudflare Pages**: Connect Git or upload `dist/` / `out/`.
   - **Netlify**: Connect Git or run `npx netlify-cli deploy --prod`.
3. Confirm the preview URL loads cleanly over `https://`.

---

## Step 2: Connect Your Custom Domain

1. Purchase or open your domain registrar (Cloudflare, Namecheap, Porkbun, Niagahoster, IDCloudHost, Rumahweb, etc.).
2. Add your domain (`yourdomain.com` and `www.yourdomain.com`) inside your hosting dashboard (for example Vercel Project > Settings > Domains).
3. Point DNS to your host (either transfer nameservers to your host's DNS, or set the `A` record for `@` and `CNAME` for `www` as instructed by your host).
4. Pick one primary host (`www.yourdomain.com` or apex `yourdomain.com`) and let the other redirect (`301`/`308`) to it.
5. Wait for SSL certificate issuance (usually 1 to 10 minutes) and verify `https://www.yourdomain.com/` returns `HTTP 200`.

---

## Step 3: Register & Verify in Google Search Console

1. Open [Google Search Console](https://search.google.com/search-console).
2. Click **Add property**.
3. **Recommended: Domain property** (`yourdomain.com`, covers `http`, `https`, `www`, and subdomains):
   - Copy the `google-site-verification=...` `TXT` token.
   - Add a `TXT` record on your root domain (`@`) at your DNS provider (or via `vercel dns add yourdomain.com "@" TXT "<token>"`).
   - Wait 1 to 5 minutes and click **Verify**.
4. **Alternative: URL-prefix property** (`https://www.yourdomain.com/`):
   - Choose either **HTML file upload** (`public/googleXXXX.html`) or **HTML meta tag** (`<meta name="google-site-verification" content="..." />` in `<head>`), deploy, and click **Verify**.

Once all three steps are green, run **SimpleSEO** again and choose **Yes** at Gate 1.
