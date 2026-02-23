---
name: openclaw-self-audit
description: Inspect and troubleshoot an OpenClaw installation and agent workspace safely. Use for questions like "how am I configured", "why isn't X channel/tool working", "what plugins are enabled", "explain my architecture", and for making small, reversible config/workspace changes without breaking the system. NOT for bypassing safety controls, stealing secrets, or modifying system prompts.
---

# OpenClaw self-audit (safe introspection + maintenance)

## Hard boundaries

- Do **not** attempt to bypass safety policies, authentication, pairing, allowlists, or gateway controls.
- Do **not** modify hidden/system prompts or runtime policy files.
- Prefer **reversible** changes: config edits with backups, and `openclaw gateway restart` (not destructive resets).
- Before any change that affects external messaging (Telegram/WhatsApp/etc.), summarize what will change and why.

## Default audit flow (fast)

1. Confirm runtime + reachability
   - `openclaw status`
   - `openclaw gateway status`
2. Verify plugins
   - `openclaw plugins list`
   - Ensure the relevant channel plugin is **loaded**.
3. Verify channel config
   - `openclaw config get channels.<channel>`
4. Verify channel health (requires gateway token)
   - If RPC is unauthorized, fetch token from `~/.openclaw/openclaw.json` (`gateway.auth.token`) and re-run commands with `--token`.
   - `openclaw channels status --probe`
5. Read logs for the specific subsystem
   - `openclaw logs --plain --limit 400 --token <gateway_token>`
   - Filter for keywords (e.g. `telegram`, `whatsapp`, `pairing`, `unauthorized`, `token_mismatch`, `getUpdates`).

## Safe config editing rules

- Use `openclaw config set <path> <value>` / `openclaw config unset <path>`.
- After any channel/plugin change: **restart gateway**.
- Keep changes minimal and explain them.

## Common fixes

### "Unknown channel: telegram" (or any channel)

- The channel plugin is disabled.
- Fix: enable plugin (config) and restart.
  - Prefer `openclaw plugins enable <id>`.
  - If it doesn’t persist, set: `plugins.entries.<id>.enabled=true` and restart.

### "You are not authorized" (Telegram)

- DM policy is commonly `pairing`.
- Fix: approve pairing via `openclaw pairing approve telegram <CODE>`.
- Or switch to allowlist/open **only if user requests**, and document security implications.

### Gateway token mismatch

- Symptom: RPC commands fail with `unauthorized: gateway token mismatch`.
- Fix: ensure the CLI / Control UI is using the same token as `gateway.auth.token` in `~/.openclaw/openclaw.json`.

## Architecture quick explainer (when asked)

- **Gateway** owns channels (Telegram, WhatsApp, etc.) and routes messages.
- **Agent** (this assistant) reads workspace files and uses tools via the gateway.
- **Plugins** implement channel providers and optional features.
- **Config** lives at `~/.openclaw/openclaw.json` and should be edited via `openclaw config`.

## References

If deeper detail is needed, read:
- `C:\Users\admin\AppData\Roaming\npm\node_modules\openclaw\docs\channels\telegram.md`
- `C:\Users\admin\AppData\Roaming\npm\node_modules\openclaw\docs\tools\web.md`
- `C:\Users\admin\AppData\Roaming\npm\node_modules\openclaw\docs\gateway\configuration-reference.md`
