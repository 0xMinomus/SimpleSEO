#!/usr/bin/env python3
"""SimpleSEO asset generator for RFC 9309 robots.txt, llms.txt, and ARD v1.0 ai-catalog.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

AI_CRAWLERS = [
    "*",
    "Googlebot",
    "Google-Extended",
    "OAI-SearchBot",
    "ChatGPT-User",
    "GPTBot",
    "Claude-SearchBot",
    "Claude-User",
    "ClaudeBot",
    "PerplexityBot",
    "Applebot",
]


def build_robots_txt(origin: str, sitemap_path: str = "/sitemap-index.xml") -> str:
    blocks = []
    for agent in AI_CRAWLERS:
        blocks.append(f"User-agent: {agent}\nAllow: /")
    blocks.append(f"Sitemap: {origin.rstrip('/')}{sitemap_path}")
    return "\n\n".join(blocks) + "\n"


def build_llms_txt(brand: str, origin: str, summary: str, pages: list[tuple[str, str, str]]) -> str:
    base = origin.rstrip("/")
    lines = [
        f"# {brand}",
        "",
        f"> {summary}",
        "",
        "## Core Pages",
        "",
    ]
    for title, path, desc in pages:
        url = path if path.startswith("http") else f"{base}{path}"
        lines.append(f"- [{title}]({url}): {desc}")
    return "\n".join(lines) + "\n"


def build_ai_catalog(brand: str, domain: str, origin: str, queries: list[str]) -> dict:
    base = origin.rstrip("/")
    return {
        "specVersion": "1.0",
        "entries": [
            {
                "identifier": f"urn:air:{domain}:guides:llms",
                "displayName": f"{brand} Official AI Guide",
                "type": 'text/markdown; profile="urn:air:agent-skills"',
                "url": f"{base}/llms.txt",
                "representativeQueries": queries[:5],
                "trustManifest": {"identity": domain},
            }
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SEO & AI discovery files")
    parser.add_argument("--brand", required=True, help="Brand or website name")
    parser.add_argument("--domain", required=True, help="Root domain (e.g. example.com)")
    parser.add_argument("--origin", required=True, help="Canonical origin (e.g. https://www.example.com)")
    parser.add_argument("--summary", required=True, help="One-paragraph factual site summary")
    parser.add_argument("--public-dir", default="public", help="Target public directory")
    parser.add_argument("--sitemap-path", default="/sitemap-index.xml")
    args = parser.parse_args()

    pub = Path(args.public_dir)
    well_known = pub / ".well-known"
    well_known.mkdir(parents=True, exist_ok=True)

    (pub / "robots.txt").write_text(build_robots_txt(args.origin, args.sitemap_path), encoding="utf-8")
    (pub / "llms.txt").write_text(
        build_llms_txt(
            args.brand,
            args.origin,
            args.summary,
            [("Home", "/", f"Main website and service overview for {args.brand}.")],
        ),
        encoding="utf-8",
    )
    catalog = build_ai_catalog(
        args.brand,
        args.domain,
        args.origin,
        [
            f"{args.brand} official services and pricing",
            f"how to contact {args.brand}",
        ],
    )
    (well_known / "ai-catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Generated robots.txt, llms.txt, and .well-known/ai-catalog.json in {pub}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
