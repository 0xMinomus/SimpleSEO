# Changelog

All notable changes to **SimpleSEO** are documented in this file.

## [1.0.0] - 2026-11-14

### Added
- Universal `SKILL.md` orchestrator and `AGENTS.md` entrypoint compatible across Oh My Pi, OpenAI Codex, Claude Code, Cursor, OpenCode, Gemini CLI, Windsurf, and Cline.
- Mandatory Two-Gate workflow: Gate 1 checks minimal prerequisites (live HTTPS host, custom domain, Google Search Console) with a built-in setup fallback guide; Gate 2 shows every sub-skill and benefit before asking confirmation to execute end to end.
- Nine modular sub-skills covering technical crawlability, JSON-LD `@graph` schema, Sitelinks landing architecture, AI Search / GEO (`llms.txt`, ARD `ai-catalog.json`, AI crawler rules), Core Web Vitals (`CLS = 0`, LCP preload), GSC + IndexNow submissions, Local E-E-A-T authority, content clustering, and live Lighthouse verification.
- Zero-dependency Python 3 CLI scripts (`simpleseo_audit.py`, `indexnow_ping.py`, `generate_assets.py`) plus unit test suite (`tests/test_simpleseo.py`).
- Plugin manifests for `.claude-plugin`, `.codex-plugin`, and `.cursor-plugin`.
