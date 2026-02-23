# MEMORY.md (curated)

## Non-negotiable operating rules
- Web research: try Brave `functions.web_search` first; if it errors/unconfigured/rate-limited/unusable, immediately fall back to SearXNG via `skills/searxng-web-search/scripts/searxng_search.py`, then `web_fetch` the best URLs.
- Coolify: only create/test/deploy inside the dedicated Coolify Project named **OpenClaw** unless explicitly asked to touch other projects.

## Current environment
- Docker Desktop is available locally. Running containers include `searxng` (8087), `chromadb` (8000), and `ollama` (11434).

## Business context
- User runs Charge Wise (https://chargewise.com.au) and wants ongoing help with UI/UX, SEO, WordPress performance, analytics/GA, and visibility.
