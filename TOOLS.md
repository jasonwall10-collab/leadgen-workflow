# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Installed CLI Tools

### Coding Agents
- **Claude Code** v2.1.50 — `C:\Users\admin\.local\bin\claude.exe`
  - Latest features: worktree isolation (`--worktree`/`-w`), agent teams, plan mode, 1M context window (Opus 4.6 fast mode), `claude agents` command, MCP progress updates
  - New flags: `--worktree` for isolated git worktrees, `CLAUDE_CODE_SIMPLE` mode, `CLAUDE_CODE_DISABLE_1M_CONTEXT`
  - Hooks: `WorktreeCreate`, `WorktreeRemove`, `ConfigChange` events
  - Agents: `isolation: "worktree"` in agent definitions, `background: true` for always-background tasks
- **Codex CLI** — NOT installed. Now has a Rust rewrite (legacy TS is superseded). Install via `npm i -g @openai/codex` or `brew install --cask codex`. Can sign in with ChatGPT account.
  - New: Desktop app via `codex app`, IDE support (VS Code/Cursor/Windsurf), `--approval-mode` flag (suggest/auto-edit/full-auto)
  - Providers: openai, openrouter, azure, gemini, ollama, mistral, deepseek, xai, groq, arceeai
- **Pi Coding Agent** — NOT installed. Install via `npm install -g @mariozechner/pi-coding-agent`

### Gemini CLI
- **Gemini CLI** v0.19.4 (latest stable: ~v0.29.0+) — `C:\Users\admin\AppData\Roaming\npm\gemini.ps1`
  - ⚠️ OUTDATED — consider `npm update -g @google/gemini-cli`
  - Latest features: Plan mode, `--resume` for session resumption, MCP progress updates, Google Search grounding, macOS notifications, GitHub Action integration
  - Free tier: 60 req/min, 1000 req/day with Google account
  - Now uses Gemini 3 models with 1M token context
  - Install channels: `@latest` (stable weekly), `@preview` (weekly preview), `@nightly`

### GitHub CLI
- **gh** v2.85.0 (latest: v2.87.2) — `C:\Program Files\GitHub CLI\gh.exe`
  - ⚠️ SLIGHTLY OUTDATED — consider updating
  - New in v2.87: `gh workflow run` now immediately returns workflow run URL, Copilot Code Review via `--add-reviewer @copilot`, `--query` flag for `gh project item-list`, improved auth in WSL/VM environments
  - New interactive search for reviewer/assignee selection in `gh pr edit`

### Web Search
- **Primary:** `functions.web_search` (Brave Search API) — currently **NOT configured** (no BRAVE_API_KEY). Run `openclaw configure --section web` to set up.
- **Failover (always use if Brave fails/unavailable):** **SearXNG** via the `searxng-web-search` skill.
  - Endpoint: `http://192.168.10.208:8087/`
  - Script: `python C:\Users\admin\.openclaw\workspace\skills\searxng-web-search\scripts\searxng_search.py "<query>" --limit 8`

## Skill Update Notes (2026-02-23)

### coding-agent skill
- Codex CLI has been rewritten in Rust — the skill references the legacy TS version
- Codex now supports `--approval-mode full-auto` (replaces `--full-auto` flag)
- Codex supports `codex review` for code review (renamed from vanilla mode)
- Claude Code v2.1.50 now supports `--worktree` for isolated git worktrees (can replace manual worktree setup)
- Claude Code now has agent teams, background agents, and plan mode
- Gemini CLI can also be used as a coding agent now (not just Q&A)

### gemini skill
- Gemini CLI is now much more than "one-shot Q&A" — it's a full coding agent
- Supports MCP, Google Search grounding, plan mode, session checkpointing
- Custom context via GEMINI.md files (like CLAUDE.md)
- GitHub Action available: `google-github-actions/run-gemini-cli`
- Free tier generous: 60 req/min, 1000 req/day

### github skill
- gh v2.87+ adds Copilot Code Review support (`gh pr edit --add-reviewer @copilot`)
- `gh workflow run` now returns the workflow run URL immediately
- `gh project item-list --query` for filtering project items
- Improved WSL/VM auth flow

### healthcheck skill
- Looks comprehensive and current. No major updates needed.

### gh-issues skill
- Comprehensive and self-contained. No major updates needed.
- Consider adding `gh pr edit --add-reviewer @copilot` for automated AI review

### skill-creator skill
- Generic documentation — no external dependencies to update

### weather skill
- wttr.in still operational and unchanged
- Consider adding Open-Meteo API as alternative (mentioned in description but not in instructions)

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
