---
name: searxng-web-search
description: Use a self-hosted SearXNG instance for web search when Brave web_search is unavailable. Use to query SearXNG JSON endpoint (e.g., http://192.168.10.208:8087/) to gather sources, competitor research, SEO/UI/UX best practices, and documentation links; then optionally fetch full pages via web_fetch.
---

# SearXNG Web Search

Use this skill when you need web search but the built-in web_search tool isn’t configured.

## Endpoint

Default base URL (user-provided):
- `http://192.168.10.208:8087/`

SearXNG JSON API pattern:
- `GET /search?q=<query>&format=json` (optionally: `language`, `safesearch`, `time_range`, `categories`)

## How to search

Prefer the bundled script:

- Basic:
  - `python {baseDir}/scripts/searxng_search.py "your query"`
- With a custom base URL:
  - `python {baseDir}/scripts/searxng_search.py "your query" --base-url http://host:port/`
- Limit results:
  - `python {baseDir}/scripts/searxng_search.py "your query" --limit 8`

## After search

- Use the returned URLs as candidates.
- Pull key sources with `web_fetch` for readable text.
- Cross-check claims; prefer primary docs (Google/web.dev/WordPress) and reputable industry sources.

## Output format (recommended)

- Top 5–10 results: title + url + snippet
- Then: 3–7 actionable takeaways distilled from 2–4 best sources
