#!/usr/bin/env python3
"""SimpleSEO live site auditor (Python 3 stdlib, zero external dependencies)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from typing import Any

USER_AGENT = "SimpleSEO-Auditor/1.0 (+https://github.com/0xMinomus/SimpleSEO)"
DEPRECATED_SCHEMA_TYPES = {
    "HowTo",
    "SpecialAnnouncement",
    "CourseInfo",
    "EstimatedSalary",
    "LearningVideo",
    "ClaimReview",
    "VehicleListing",
    "PracticeProblem",
}
VALID_ROBOTS_DIRECTIVES = {
    "user-agent",
    "allow",
    "disallow",
    "sitemap",
    "crawl-delay",
    "host",
}
ARD_URN_RE = re.compile(r"^urn:air:([a-zA-Z0-9.-]+)(?::([a-zA-Z0-9._:-]+))?:([a-zA-Z0-9._-]+)$")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_chunks: list[str] = []
        self._in_title = False
        self.h1_chunks: list[str] = []
        self._in_h1 = False
        self.h1_count = 0
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.jsonld_blocks: list[str] = []
        self._in_jsonld = False
        self._jsonld_buf: list[str] = []
        self.lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        t = tag.lower()
        if t == "html":
            self.lang = attr_map.get("lang", "")
        elif t == "title":
            self._in_title = True
        elif t == "h1":
            self._in_h1 = True
            self.h1_count += 1
        elif t == "meta":
            self.meta.append(attr_map)
        elif t == "link":
            self.links.append(attr_map)
        elif t == "img":
            self.images.append(attr_map)
        elif t == "script" and attr_map.get("type", "").lower().startswith("application/ld+json"):
            self._in_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "title":
            self._in_title = False
        elif t == "h1":
            self._in_h1 = False
        elif t == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld_blocks.append("".join(self._jsonld_buf).strip())

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_chunks.append(data)
        if self._in_h1:
            self.h1_chunks.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)


def fetch_url(url: str, timeout: int = 20) -> tuple[int, str, dict[str, str], bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, resp.geturl(), headers, resp.read()
    except urllib.error.HTTPError as err:
        headers = {k.lower(): v for k, v in err.headers.items()} if err.headers else {}
        body = err.read() if hasattr(err, "read") else b""
        return err.code, err.geturl() or url, headers, body
    except Exception as exc:
        return 0, url, {"error": str(exc)}, b""


def validate_robots_txt(text: str) -> dict[str, Any]:
    invalid_lines: list[str] = []
    sitemaps: list[str] = []
    groups: dict[str, list[tuple[str, str]]] = {}
    current_agents: list[str] = []
    saw_directive_in_group = False

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            invalid_lines.append(raw_line.strip())
            continue
        key, val = [part.strip() for part in line.split(":", 1)]
        low_key = key.lower()
        if low_key not in VALID_ROBOTS_DIRECTIVES:
            invalid_lines.append(raw_line.strip())
            continue
        if low_key == "user-agent":
            if saw_directive_in_group:
                current_agents = []
                saw_directive_in_group = False
            current_agents.append(val)
            groups.setdefault(val.lower(), [])
        elif low_key == "sitemap":
            sitemaps.append(val)
        else:
            saw_directive_in_group = True
            for agent in current_agents:
                groups.setdefault(agent.lower(), []).append((low_key, val))

    ai_bots = {}
    for bot in ("googlebot", "oai-searchbot", "chatgpt-user", "claude-searchbot", "perplexitybot"):
        rules = groups.get(bot) or groups.get("*", [])
        blocked_root = any(d == "disallow" and p == "/" for d, p in rules) and not any(
            d == "allow" and p == "/" for d, p in rules
        )
        ai_bots[bot] = "blocked" if blocked_root else "allowed"

    return {
        "valid_rfc9309": len(invalid_lines) == 0,
        "invalid_lines": invalid_lines,
        "sitemaps": sitemaps,
        "ai_bots": ai_bots,
    }


def validate_llms_txt(text: str) -> dict[str, Any]:
    has_h1 = bool(re.search(r"(?m)^\s*#\s+.+", text))
    has_md_link = bool(re.search(r"\[[^\]]+\]\([^)]+\)", text))
    length_ok = len(text.strip()) >= 50
    return {
        "valid": has_h1 and has_md_link and length_ok,
        "has_h1": has_h1,
        "has_markdown_link": has_md_link,
        "length_ok": length_ok,
        "char_count": len(text.strip()),
    }


def validate_ai_catalog(raw_text: str) -> dict[str, Any]:
    errors: list[str] = []
    try:
        data = json.loads(raw_text)
    except Exception as exc:
        return {"valid": False, "errors": [f"Invalid JSON: {exc}"], "entries": 0}

    if not isinstance(data, dict):
        return {"valid": False, "errors": ["Root must be a JSON object"], "entries": 0}
    if data.get("specVersion") != "1.0":
        errors.append("Missing or non-1.0 specVersion")
    if "collections" in data:
        errors.append("Deprecated top-level 'collections' field present")
    entries = data.get("entries")
    if not isinstance(entries, list) or len(entries) == 0:
        errors.append("Missing non-empty 'entries' array")
        return {"valid": False, "errors": errors, "entries": 0}

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Entry #{i} is not an object")
            continue
        ident = entry.get("identifier", "")
        if not ARD_URN_RE.match(str(ident)):
            errors.append(f"Entry #{i}: invalid identifier '{ident}'")
        if not entry.get("displayName"):
            errors.append(f"Entry #{i}: missing displayName")
        if not entry.get("type"):
            errors.append(f"Entry #{i}: missing type")
        if ("url" in entry) == ("data" in entry):
            errors.append(f"Entry #{i}: provide exactly one of 'url' or 'data'")
        queries = entry.get("representativeQueries")
        if not isinstance(queries, list) or not (2 <= len(queries) <= 5):
            errors.append(f"Entry #{i}: recommend 2 to 5 representativeQueries")
        trust = entry.get("trustManifest")
        if not isinstance(trust, dict) or not trust.get("identity"):
            errors.append(f"Entry #{i}: trustManifest.identity is required")

    return {"valid": len(errors) == 0, "errors": errors, "entries": len(entries)}


def inspect_jsonld(blocks: list[str]) -> dict[str, Any]:
    parsed_types: list[str] = []
    deprecated: list[str] = []
    errors: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        t = node.get("@type")
        if isinstance(t, list):
            for item in t:
                parsed_types.append(str(item))
                if item in DEPRECATED_SCHEMA_TYPES:
                    deprecated.append(str(item))
        elif isinstance(t, str):
            parsed_types.append(t)
            if t in DEPRECATED_SCHEMA_TYPES:
                deprecated.append(t)
        if "@graph" in node:
            walk(node["@graph"])

    for idx, block in enumerate(blocks):
        try:
            obj = json.loads(block)
            if isinstance(obj, dict) and "@context" not in obj:
                errors.append(f"Block #{idx} missing @context")
            walk(obj)
        except Exception as exc:
            errors.append(f"Block #{idx} invalid JSON: {exc}")

    return {
        "block_count": len(blocks),
        "types": parsed_types,
        "deprecated_types": sorted(set(deprecated)),
        "errors": errors,
    }


def audit_html(html_bytes: bytes, final_url: str, headers: dict[str, str]) -> dict[str, Any]:
    html_text = html_bytes.decode("utf-8", errors="replace")
    parser = PageParser()
    parser.feed(html_text)

    title = " ".join("".join(parser.title_chunks).split())
    h1 = " ".join("".join(parser.h1_chunks).split())

    def get_meta(name: str | None = None, prop: str | None = None) -> str:
        for m in parser.meta:
            if name and m.get("name", "").lower() == name.lower():
                return m.get("content", "")
            if prop and m.get("property", "").lower() == prop.lower():
                return m.get("content", "")
        return ""

    canonicals = [l.get("href", "") for l in parser.links if "canonical" in l.get("rel", "").lower().split()]
    hreflangs = [l.get("hreflang", "") for l in parser.links if l.get("hreflang")]
    ai_catalog_links = [l.get("href", "") for l in parser.links if "ai-catalog" in l.get("rel", "").lower().split()]

    missing_wh = [
        img.get("src", "(inline)")
        for img in parser.images
        if not (img.get("width") and img.get("height"))
    ]
    missing_alt = [
        img.get("src", "(inline)")
        for img in parser.images
        if "alt" not in img and img.get("role", "").lower() != "presentation"
    ]

    sec_headers = {
        h: headers.get(h, "")
        for h in ("x-content-type-options", "x-frame-options", "referrer-policy", "strict-transport-security")
    }

    return {
        "final_url": final_url,
        "html_bytes": len(html_bytes),
        "within_2mb_googlebot_cap": len(html_bytes) <= 2 * 1024 * 1024,
        "lang": parser.lang,
        "title": title,
        "title_length": len(title),
        "description": get_meta(name="description"),
        "description_length": len(get_meta(name="description")),
        "robots_meta": get_meta(name="robots"),
        "canonical": canonicals[0] if canonicals else "",
        "canonical_matches_final_url": bool(canonicals and canonicals[0].rstrip("/") == final_url.rstrip("/")),
        "hreflangs": hreflangs,
        "ai_catalog_links": ai_catalog_links,
        "og_title": get_meta(prop="og:title"),
        "og_image": get_meta(prop="og:image"),
        "h1_count": parser.h1_count,
        "h1_text": h1,
        "image_count": len(parser.images),
        "images_missing_dimensions": missing_wh,
        "images_missing_alt": missing_alt,
        "jsonld": inspect_jsonld(parser.jsonld_blocks),
        "security_headers": sec_headers,
    }


def run_live_audit(url: str) -> dict[str, Any]:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urllib.parse.urlparse(url)
    status, final_url, headers, body = fetch_url(url)
    origin = f"{urllib.parse.urlparse(final_url).scheme}://{urllib.parse.urlparse(final_url).netloc}"

    page_report = audit_html(body, final_url, headers) if body else {"error": f"Failed to fetch {url}"}
    page_report["initial_status"] = status
    page_report["redirected"] = final_url.rstrip("/") != url.rstrip("/")

    # robots.txt
    r_status, _, _, r_body = fetch_url(origin + "/robots.txt")
    robots_report = (
        validate_robots_txt(r_body.decode("utf-8", errors="replace"))
        if r_status == 200
        else {"valid_rfc9309": False, "status": r_status}
    )
    robots_report["status"] = r_status

    # sitemaps
    sitemap_checks = {}
    for sm_path in ("/sitemap-index.xml", "/sitemap.xml"):
        sm_status, sm_final, _, sm_body = fetch_url(origin + sm_path)
        xml_valid = False
        url_count = 0
        if sm_status == 200 and sm_body:
            try:
                root = ET.fromstring(sm_body)
                xml_valid = True
                url_count = len(list(root))
            except ET.ParseError:
                xml_valid = False
        sitemap_checks[sm_path] = {
            "status": sm_status,
            "final_url": sm_final,
            "xml_valid": xml_valid,
            "entries": url_count,
        }

    # llms.txt
    l_status, _, _, l_body = fetch_url(origin + "/llms.txt")
    llms_report = (
        validate_llms_txt(l_body.decode("utf-8", errors="replace"))
        if l_status == 200
        else {"valid": False}
    )
    llms_report["status"] = l_status

    # ai-catalog.json
    a_status, _, _, a_body = fetch_url(origin + "/.well-known/ai-catalog.json")
    ard_report = (
        validate_ai_catalog(a_body.decode("utf-8", errors="replace"))
        if a_status == 200
        else {"valid": False, "errors": [f"HTTP {a_status}"], "entries": 0}
    )
    ard_report["status"] = a_status

    # 404 verification
    nf_status, _, _, _ = fetch_url(origin + "/simpleseo-not-found-verification-404")

    return {
        "target": url,
        "origin": origin,
        "page": page_report,
        "robots_txt": robots_report,
        "sitemaps": sitemap_checks,
        "llms_txt": llms_report,
        "ai_catalog": ard_report,
        "not_found_status": nf_status,
        "proper_404": nf_status == 404,
    }


def format_markdown(report: dict[str, Any]) -> str:
    page = report["page"]
    robots = report["robots_txt"]
    llms = report["llms_txt"]
    ard = report["ai_catalog"]

    lines = [
        f"# SimpleSEO Audit Report: {report['origin']}",
        "",
        "## Core Checks",
        f"- **HTTP Status / Final URL**: `{page.get('initial_status')}` -> `{page.get('final_url')}`",
        f"- **Canonical Match**: `{page.get('canonical_matches_final_url')}` (`{page.get('canonical')}`)",
        f"- **Title ({page.get('title_length')} chars)**: `{page.get('title')}`",
        f"- **Meta Description ({page.get('description_length')} chars)**: `{page.get('description')}`",
        f"- **H1 Count**: `{page.get('h1_count')}`",
        f"- **HTML Size**: `{round(page.get('html_bytes', 0) / 1024, 1)} KB` (Under 2 MB cap: `{page.get('within_2mb_googlebot_cap')}`)",
        f"- **Images**: `{page.get('image_count')}` total, `{len(page.get('images_missing_dimensions', []))}` missing width/height, `{len(page.get('images_missing_alt', []))}` missing alt",
        f"- **JSON-LD Types**: `{page.get('jsonld', {}).get('types', [])}` (Deprecated: `{page.get('jsonld', {}).get('deprecated_types', [])}`, Errors: `{page.get('jsonld', {}).get('errors', [])}`)",
        f"- **404 Status Check**: HTTP `{report.get('not_found_status')}` (Proper 404: `{report.get('proper_404')}`)",
        "",
        "## Crawl, Sitemaps & AI Readiness",
        f"- **robots.txt (HTTP {robots.get('status')})**: RFC 9309 valid=`{robots.get('valid_rfc9309')}`, AI bots=`{robots.get('ai_bots')}`",
        f"- **Sitemaps**: `{json.dumps(report['sitemaps'])}`",
        f"- **llms.txt (HTTP {llms.get('status')})**: valid=`{llms.get('valid')}` ({llms.get('char_count', 0)} chars)",
        f"- **ARD ai-catalog.json (HTTP {ard.get('status')})**: valid=`{ard.get('valid')}`, entries=`{ard.get('entries')}`, errors=`{ard.get('errors')}`",
        f"- **Security Headers**: `{json.dumps(page.get('security_headers', {}))}`",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="SimpleSEO live URL auditor")
    parser.add_argument("url", help="Target website URL (for example https://www.example.com)")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    report = run_live_audit(args.url)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(format_markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
