# Schema.org JSON-LD `@graph` Templates

Use server-rendered JSON-LD in `<head>` with a single `@context` and linked `@id` nodes. Escape `<` as `\u003c` when serializing into HTML.

## Complete Service Business `@graph` Template

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ProfessionalService",
      "@id": "https://www.example.com/#organization",
      "name": "BrandName",
      "legalName": "example.com",
      "alternateName": ["BrandName", "example.com"],
      "url": "https://www.example.com/",
      "logo": "https://www.example.com/logo.svg",
      "image": "https://www.example.com/og-image.png",
      "description": "Clear factual description of services and target region.",
      "telephone": "+1-555-0100",
      "email": "hello@example.com",
      "priceRange": "Starts at $299",
      "currenciesAccepted": "USD",
      "sameAs": ["https://github.com/yourhandle"],
      "areaServed": [
        { "@type": "AdministrativeArea", "name": "Your City or Region" },
        { "@type": "Country", "name": "Your Country" }
      ],
      "address": {
        "@type": "PostalAddress",
        "addressRegion": "Region",
        "addressCountry": "US"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "telephone": "+1-555-0100",
        "email": "hello@example.com",
        "availableLanguage": ["English"]
      },
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Service Packages",
        "numberOfItems": 2,
        "itemListElement": [
          {
            "@type": "Offer",
            "position": 1,
            "name": "Starter Package",
            "description": "Concise package scope.",
            "priceCurrency": "USD",
            "price": 299,
            "url": "https://www.example.com/#pricing",
            "itemOffered": {
              "@type": "Service",
              "name": "Starter Package",
              "serviceType": "Landing Page Design",
              "provider": { "@id": "https://www.example.com/#organization" }
            }
          }
        ]
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "url": "https://www.example.com/",
      "name": "BrandName",
      "inLanguage": "en-US",
      "publisher": { "@id": "https://www.example.com/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.example.com/#webpage",
      "url": "https://www.example.com/",
      "name": "Page Title",
      "description": "Page description.",
      "inLanguage": "en-US",
      "isPartOf": { "@id": "https://www.example.com/#website" },
      "about": { "@id": "https://www.example.com/#organization" },
      "primaryImageOfPage": {
        "@type": "ImageObject",
        "url": "https://www.example.com/og-image.png"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.example.com/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://www.example.com/"
        }
      ]
    },
    {
      "@type": "ItemList",
      "@id": "https://www.example.com/#sitenav",
      "name": "Primary Service Pages",
      "itemListElement": [
        {
          "@type": "SiteNavigationElement",
          "position": 1,
          "name": "Services",
          "description": "Core web services.",
          "url": "https://www.example.com/services/"
        }
      ]
    }
  ]
}
```
