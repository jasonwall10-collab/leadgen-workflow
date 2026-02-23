---
name: openclaw-skillforge
description: Design, scaffold, lint, and package high-quality OpenClaw/AgentSkills-compatible skills (SKILL.md + optional scripts/references/assets). Use when creating or refactoring skills under <workspace>/skills or ~/.openclaw/skills, tuning frontmatter/metadata gating (requires.bins/env/config/os), writing trigger-friendly descriptions, validating AgentSkills/OpenClaw parser constraints (single-line frontmatter keys; metadata as single-line JSON), and packaging into .skill bundles.
---

# OpenClaw Skillforge

Build skills that are *small*, *trigger reliably*, and *don’t break OpenClaw’s loader/parser*.

## Workflow (use this order)

### 1) Pin the goal with concrete examples
Collect 3–8 example user prompts that **should** trigger the skill, plus 3–8 that **should not**.

Also capture:
- Expected tools to use (browser/exec/nodes/etc)
- Any required binaries (host + sandbox)
- Any secrets / env vars (and where they should be injected)

### 2) Choose the skill name + description (the trigger is everything)
- Name: lowercase + digits + hyphens; keep it short.
- Description: include *what it does* and *when to use it* with explicit triggers.

Good descriptions mention:
- filetypes (e.g. .docx)
- ecosystems (Coolify, GH, Terraform)
- workflows (triage, packaging, linting)
- what “done” looks like

### 3) Scaffold the folder
Preferred target: `{baseDir}` should be `<workspace>/skills/<skill-name>`.

Use the generator script bundled with this skill:

- Create a new skill skeleton:
  - `python {baseDir}/scripts/skillforge.py init <skill-name> --path <workspace>/skills`

If you need the upstream template initializer/packager (bundled with OpenClaw), it’s here:
- `C:\Users\admin\AppData\Roaming\npm\node_modules\openclaw\skills\skill-creator\scripts\init_skill.py`
- `C:\Users\admin\AppData\Roaming\npm\node_modules\openclaw\skills\skill-creator\scripts\package_skill.py`

### 4) Write SKILL.md (keep it lean)
Rules that matter in OpenClaw:
- Frontmatter keys should be **single-line**.
- `metadata:` must be a **single-line JSON object** (if present).
- Don’t add extra docs like README/CHANGELOG.

Recommended SKILL.md body structure:
1. **Quick start** (3–7 bullets)
2. **Decision points** (when to choose A vs B)
3. **Canonical workflow** (imperative steps)
4. **Safety/guardrails** (what not to do)
5. **References** (point to files in `references/` only when needed)

### 5) Add reusable resources
- `scripts/`: deterministic automation, tested via `python …`
- `references/`: long docs, schemas, API notes, examples
- `assets/`: templates or output artifacts (not meant to be read into context)

### 6) Lint + package
- Lint:
  - `python {baseDir}/scripts/skillforge.py lint <path-to-skill-folder>`
- Package (.skill zip):
  - `python {baseDir}/scripts/skillforge.py pack <path-to-skill-folder> --out <dist-dir>`

## OpenClaw gating cheat-sheet (metadata)

Use `metadata:` only when needed; keep it one line.

Example:

```yaml
metadata: {"openclaw":{"requires":{"bins":["uv"],"env":["GEMINI_API_KEY"],"config":["browser.enabled"]},"primaryEnv":"GEMINI_API_KEY","os":["win32","linux"]}}
```

Notes:
- `requires.bins` checks host PATH at load time.
- If you run sandboxed, the bin must exist in the container too.
- Secrets should go in `~/.openclaw/openclaw.json` under `skills.entries.<skillKey>.env` or `.apiKey`.

## Quality bar (don’t ship until these are true)
- Description includes clear trigger phrases + contexts.
- Body is under ~500 lines; big details moved into `references/`.
- Scripts (if any) run successfully at least once.
- Lint passes.
- Packaging succeeds.
