# Sub-Skill 02: Structured Data & Schema.org

Focus: Emit clean, valid, server-rendered JSON-LD `@graph` markup so Google and AI systems understand your business entity, services, pricing, navigation, and FAQs without guesswork.

## Rules

1. **Always Server-Render JSON-LD**: Inject `<script type="application/ld+json">` in the initial HTML document (`is:inline` in Astro, SSR in Next.js/Remix). Safely escape `<` as `\u003c`.
2. **Use `@graph` with Linked `@id` URIs**:
   - Declare `"@context": "https://schema.org"` once at the root.
   - Link entities cleanly (`#organization`, `#website`, `#webpage`, `#breadcrumb`, `#sitenav`, `#faq`).
   - Use full absolute canonical URLs for every `url`, `@id`, `logo`, and `image` field.
3. **Choose Active Schema Types Only**:
   - **Recommended core**: `Organization`, `LocalBusiness` / `ProfessionalService`, `WebSite`, `WebPage`, `BreadcrumbList`, `ItemList` + `SiteNavigationElement`, `OfferCatalog`, `Offer`, `Service`, `Product`, `SoftwareApplication`, `Article` / `BlogPosting`, `Person`, `ContactPage`.
   - **Keep if helpful on-page**: `FAQPage` (useful for AI/entity parsing even without Google FAQ rich-result cards).
   - **Never emit deprecated types**: `HowTo`, `SpecialAnnouncement`, `CourseInfo`, `EstimatedSalary`, `LearningVideo`, `ClaimReview` (for SERP rich results), `VehicleListing`, or `PracticeProblem`.
4. **Truth & Integrity**:
   - Only include `price` when an explicit numeric price exists on the page (omit numeric `price` on "Custom" tiers).
   - Never add fabricated `AggregateRating` or `Review` schema without real, visible, verifiable reviews on the page.

See `references/schema-templates.md` for copy-ready JSON-LD `@graph` blocks.
