# HEARTBEAT.md

## Nightly prompt: Reddit opportunity scan

Goal: **each night** ask the user if they want to run the Reddit scan. The user will reply **yes/no**.

### When to ask
- Time window (Adelaide time): **20:30–22:30**
- Ask **once per date**.
- If it’s outside the window, do nothing.

### State tracking
- Use `memory/heartbeat-state.json`:
  - `nightlyRedditScan.lastAskedDate` (YYYY-MM-DD)

### Message template
"Want me to run the Reddit scan tonight? (yes/no)"

### Scan freshness filter
When running the scan, prefer recent posts:
- Default: **last year**
- If results feel thin/noisy, relax to **2 years**
- If results are too broad, tighten to **last month**

