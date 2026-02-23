#!/usr/bin/env python3
"""OpenClaw Skillforge

Small helper to scaffold, lint, and package AgentSkills/OpenClaw skills.

Usage:
  python skillforge.py init <skill-name> --path <dir> [--resources scripts,references,assets]
  python skillforge.py lint <skill-folder>
  python skillforge.py pack <skill-folder> [--out <dist-dir>]

Notes:
- Enforces OpenClaw parser constraints: single-line frontmatter keys and single-line JSON for metadata.
- Packaging delegates to OpenClaw's bundled package_skill.py when present.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$|^[a-z0-9]$")


def die(msg: str, code: int = 2) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def normalize_skill_name(name: str) -> str:
    name = name.strip().lower().replace("_", "-")
    name = re.sub(r"[^a-z0-9-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def ensure_skill_name(name: str) -> str:
    norm = normalize_skill_name(name)
    if not norm:
        die("skill name is empty after normalization")
    if not SKILL_NAME_RE.match(norm):
        die(f"invalid skill name '{norm}' (use lowercase letters, digits, hyphens; <=64 chars)")
    return norm


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def template_skill_md(skill_name: str) -> str:
    # Keep the body short; users should move long content into references/.
    return (
        "---\n"
        f"name: {skill_name}\n"
        f"description: TODO - Describe what this skill does and when to use it (include trigger phrases, filetypes, tools, and contexts).\n"
        "---\n\n"
        f"# {skill_name}\n\n"
        "## Quick start\n\n"
        "- TODO\n\n"
        "## Workflow\n\n"
        "1. TODO\n\n"
        "## Safety\n\n"
        "- Do not run destructive commands without confirmation.\n"
    )


def cmd_init(args: argparse.Namespace) -> None:
    skill_name = ensure_skill_name(args.skill_name)
    out_dir = Path(args.path).expanduser().resolve()
    skill_dir = out_dir / skill_name

    if skill_dir.exists() and any(skill_dir.iterdir()):
        die(f"target already exists and is not empty: {skill_dir}")

    resources = set()
    if args.resources:
        for part in args.resources.split(","):
            part = part.strip()
            if not part:
                continue
            resources.add(part)

    # Always create skill dir and SKILL.md
    skill_dir.mkdir(parents=True, exist_ok=True)
    write_text(skill_dir / "SKILL.md", template_skill_md(skill_name))

    for d in sorted(resources):
        if d not in {"scripts", "references", "assets"}:
            die(f"unknown resource dir '{d}' (expected scripts,references,assets)")
        (skill_dir / d).mkdir(parents=True, exist_ok=True)

    print(str(skill_dir))


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def lint_skill_md(skill_md: Path) -> list[str]:
    text = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return ["SKILL.md missing YAML frontmatter (must start with --- and include name/description)"]

    front = m.group(1)
    errors: list[str] = []

    # Basic required keys
    required = {"name": False, "description": False}

    for i, line in enumerate(front.splitlines(), start=1):
        if not line.strip():
            continue
        # Enforce single-line key:value (no multiline YAML, no indentation continuations)
        if line.startswith(" ") or line.startswith("\t"):
            errors.append(f"frontmatter line {i}: indented lines are not supported by OpenClaw parser")
            continue
        if ":" not in line:
            errors.append(f"frontmatter line {i}: expected 'key: value'")
            continue

        key = line.split(":", 1)[0].strip()
        if key in required:
            required[key] = True

        if key == "metadata":
            value = line.split(":", 1)[1].strip()
            if not value:
                errors.append("metadata: must be a single-line JSON object (not empty)")
            else:
                try:
                    obj = json.loads(value)
                    if not isinstance(obj, dict):
                        errors.append("metadata: JSON must be an object")
                except Exception as e:
                    errors.append(f"metadata: invalid JSON ({e})")

    for k, ok in required.items():
        if not ok:
            errors.append(f"frontmatter missing required key: {k}")

    return errors


def cmd_lint(args: argparse.Namespace) -> None:
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        die(f"SKILL.md not found: {skill_md}")

    errors = lint_skill_md(skill_md)
    if errors:
        for e in errors:
            print(f"lint: {e}", file=sys.stderr)
        raise SystemExit(1)

    print("OK")


def find_packager() -> Path | None:
    # Default install location on this host (Windows + npm global).
    candidate = Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules" / "openclaw" / "skills" / "skill-creator" / "scripts" / "package_skill.py"
    if candidate.exists():
        return candidate
    return None


def cmd_pack(args: argparse.Namespace) -> None:
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not (skill_dir / "SKILL.md").exists():
        die(f"not a skill folder (missing SKILL.md): {skill_dir}")

    # Lint first
    errors = lint_skill_md(skill_dir / "SKILL.md")
    if errors:
        for e in errors:
            print(f"lint: {e}", file=sys.stderr)
        raise SystemExit(1)

    packager = find_packager()
    if not packager:
        die("could not find OpenClaw package_skill.py; install/update OpenClaw or package manually as a .zip renamed to .skill")

    cmd = [sys.executable, str(packager), str(skill_dir)]
    if args.out:
        out_dir = Path(args.out).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd.append(str(out_dir))

    print("running:", " ".join(cmd))
    subprocess.check_call(cmd)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="skillforge")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_init = sub.add_parser("init", help="create a new skill skeleton")
    ap_init.add_argument("skill_name")
    ap_init.add_argument("--path", required=True, help="output directory that will contain the skill folder")
    ap_init.add_argument("--resources", default="scripts,references,assets")
    ap_init.set_defaults(fn=cmd_init)

    ap_lint = sub.add_parser("lint", help="lint a skill folder")
    ap_lint.add_argument("skill_dir")
    ap_lint.set_defaults(fn=cmd_lint)

    ap_pack = sub.add_parser("pack", help="package a skill folder into a .skill via OpenClaw packager")
    ap_pack.add_argument("skill_dir")
    ap_pack.add_argument("--out")
    ap_pack.set_defaults(fn=cmd_pack)

    args = ap.parse_args(argv)
    args.fn(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
