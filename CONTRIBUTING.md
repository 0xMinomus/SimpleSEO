# Contributing to SimpleSEO

Thank you for helping improve **SimpleSEO**. Contributions that make SEO, Schema, Core Web Vitals, and AI Search readiness simpler and more reliable across coding agents are always welcome.

## How You Can Contribute

- Report bugs in the audit, IndexNow, or asset generator scripts
- Improve sub-skill instructions for additional frameworks (Astro, Next.js, SvelteKit, Remix, Hugo, WordPress, plain HTML)
- Add unit tests for edge cases in HTML, JSON-LD, `robots.txt`, `llms.txt`, or ARD validation
- Keep documentation clear, practical, and free of hype

## Local Setup

SimpleSEO scripts require only **Python 3.10+** using the standard library (zero pip dependencies).

```bash
git clone https://github.com/0xMinomus/SimpleSEO.git
cd SimpleSEO
python3 -m unittest discover -s tests -v
```

## Contribution Rules

1. Keep `scripts/` dependency-free (Python 3 standard library only) so any user or agent can run them immediately without virtualenvs.
2. Keep all prompts, docs, and skills **agent-agnostic** (do not lock workflows to a single proprietary IDE or CLI tool).
3. Avoid em-dashes in documentation and copy, and never recommend deprecated Schema.org types or spammy SEO tactics.
4. Include or update unit tests in `tests/` whenever modifying script logic.
5. Open a concise pull request explaining what changed and how you verified it.
