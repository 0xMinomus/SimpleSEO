#!/usr/bin/env python3
"""SimpleSEO IndexNow key generator, verifier, and URL submission script."""

from __future__ import annotations

import argparse
import json
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path


def resolve_or_create_key(public_dir: Path, explicit_key: str | None) -> tuple[str, Path]:
    public_dir.mkdir(parents=True, exist_ok=True)
    if explicit_key:
        key = explicit_key.strip()
        key_file = public_dir / f"{key}.txt"
        key_file.write_text(key + "\n", encoding="utf-8")
        return key, key_file

    # Reuse existing 32-char hex key file if present
    for candidate in sorted(public_dir.glob("*.txt")):
        stem = candidate.stem
        if len(stem) == 32 and all(c in "0123456789abcdef" for c in stem.lower()):
            content = candidate.read_text(encoding="utf-8").strip()
            if content == stem:
                return stem, candidate

    key = secrets.token_hex(16)
    key_file = public_dir / f"{key}.txt"
    key_file.write_text(key + "\n", encoding="utf-8")
    return key, key_file


def verify_live_key(host: str, key: str) -> tuple[int, str]:
    url = f"https://{host}/{key}.txt"
    req = urllib.request.Request(url, headers={"User-Agent": "SimpleSEO-IndexNow/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace").strip()
    except urllib.error.HTTPError as err:
        return err.code, ""


def submit_indexnow(host: str, key: str, urls: list[str]) -> tuple[int, str]:
    payload = json.dumps(
        {
            "host": host,
            "key": key,
            "keyLocation": f"https://{host}/{key}.txt",
            "urlList": urls,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate IndexNow key and submit URLs")
    parser.add_argument("--host", required=True, help="Canonical host (e.g. www.example.com)")
    parser.add_argument("--public-dir", default="public", help="Directory for <key>.txt")
    parser.add_argument("--key", default=None, help="Optional 32-hex IndexNow key")
    parser.add_argument("--urls", nargs="+", required=True, help="Canonical URLs to submit")
    parser.add_argument("--dry-run", action="store_true", help="Create key file without network calls")
    args = parser.parse_args()

    key, key_file = resolve_or_create_key(Path(args.public_dir), args.key)
    print(f"IndexNow key file: {key_file} (key={key})")
    if args.dry_run:
        return 0

    status, live_body = verify_live_key(args.host, key)
    if status != 200 or live_body != key:
        print(
            f"Live key check failed at https://{args.host}/{key}.txt (HTTP {status}). Deploy first, then re-run.",
            file=sys.stderr,
        )
        return 1

    ping_status, ping_body = submit_indexnow(args.host, key, args.urls)
    print(f"IndexNow response: HTTP {ping_status} {ping_body}".strip())
    return 0 if ping_status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main())
