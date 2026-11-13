# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in **SimpleSEO** (such as unsafe URL handling, shell injection risks in helper scripts, or improper handling of user credentials), please report it privately instead of opening a public GitHub issue.

- **Contact**: Email `beliweb@gmail.com` or message the maintainer via GitHub (`0xMinomus`).
- **What to include**: Steps to reproduce, affected file or script, and potential impact.
- **Response window**: You can expect an acknowledgment within 48 hours and a fix or mitigation plan shortly after verification.

## Operational Security Guidelines for Agents

When running SimpleSEO against a user project:
1. Never expose private repository URLs, API tokens, or local environment secrets in public files (`llms.txt`, `ai-catalog.json`, `robots.txt`, JSON-LD, or HTML meta tags).
2. Always confirm before modifying DNS records or submitting URLs through an authenticated browser session.
3. Keep all helper scripts limited to standard library HTTP/HTML/JSON operations with no hidden telemetry.
