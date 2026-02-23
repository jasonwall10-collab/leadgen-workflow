#!/usr/bin/env python3
"""Query a SearXNG instance and print results.

Examples:
  python searxng_search.py "wordpress ecommerce ux checklist" --limit 8
  python searxng_search.py "core web vitals lcp inp cls" --base-url http://192.168.10.208:8087/

SearXNG JSON endpoint:
  <base>/search?q=...&format=json

Notes:
- Designed for quick research inside OpenClaw where Brave web_search may be unavailable.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


def build_url(base_url: str, query: str, **params: str) -> str:
    base = base_url.rstrip("/")
    q = {"q": query, "format": "json"}
    q.update({k: v for k, v in params.items() if v is not None})
    return f"{base}/search?{urllib.parse.urlencode(q)}"


def fetch(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-searxng/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    return json.loads(data)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--base-url", default="http://192.168.10.208:8087/")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--language", default=None)
    ap.add_argument("--time-range", default=None, dest="time_range")
    ap.add_argument("--safesearch", default=None)

    args = ap.parse_args(argv)

    url = build_url(
        args.base_url,
        args.query,
        language=args.language,
        time_range=args.time_range,
        safesearch=args.safesearch,
    )

    try:
        obj = fetch(url)
    except Exception as e:
        print(f"error: failed to query SearXNG: {e}", file=sys.stderr)
        print(f"url: {url}", file=sys.stderr)
        return 2

    results = obj.get("results") or []
    results = results[: max(0, args.limit)]

    out = []
    for r in results:
        out.append(
            {
                "title": (r.get("title") or "").strip(),
                "url": (r.get("url") or "").strip(),
                "snippet": (r.get("content") or "").strip(),
                "engine": r.get("engine"),
            }
        )

    print(json.dumps({"query": args.query, "count": len(out), "results": out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
