#!/usr/bin/env python3
"""Validate the pm-agents repo. Standard library only.

Checks:
  1. Every .agents/skills/*/SKILL.md has YAML front matter with `name` equal to its folder name
     and a non-empty `description` of at most 1024 characters.
  2. Required templates exist.
  3. Relative markdown links in repo .md files resolve (http(s)/mailto links, anchor-only links,
     links inside code, and files under templates/brain/ are ignored).
  4. .gitignore ignores the top-level brain folder with `/brain/`.

Usage:  python3 scripts/validate.py
Exit code 0 = all good, 1 = problems found (listed).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_DESCRIPTION = 1024

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "CONVENTIONS.md",
    "CHANGELOG.md",
    ".gitignore",
    ".devin/config.json",
    ".devin/mcp_config.json",
    "docs/HANDOFF.md",
    "templates/meeting-note.md",
    "templates/decision.md",
    "templates/stakeholder.md",
    "templates/user-story.md",
    "templates/weekly-status.md",
    "templates/release-notes.html",
    "templates/persona.md",
    "templates/brain/brain.yaml",
    "templates/brain/preferences/README.md",
    "templates/brain/inbox/.gitkeep",
    "templates/brain/inbox/processed/.gitkeep",
    "templates/brain/stakeholders/.gitkeep",
    "templates/brain/products/_example/README.md",
]

EXPECTED_SKILLS = ["onboard", "ingest", "ask", "user-story", "release-notes", "weekly-status"]
HTML_PLACEHOLDERS = ["{{product_name}}", "{{version}}", "{{date}}", "{{intro}}", "{{sections}}"]

SKIP_DIRS = {".git", "brain", "node_modules", "__pycache__"}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------- front matter

def parse_front_matter(text: str) -> dict[str, str] | None:
    """Minimal YAML front matter parser: top-level `key: value` pairs, incl. folded/literal blocks."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    data: dict[str, str] = {}
    key = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            key, value = m.group(1), m.group(2).strip()
            if value in (">", "|", ">-", "|-"):
                value = ""
            data[key] = value.strip("\"'")
        elif key is not None:
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def check_skills() -> None:
    skills_dir = ROOT / ".agents" / "skills"
    if not skills_dir.is_dir():
        err(".agents/skills/ folder is missing")
        return
    found = []
    for folder in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill = folder / "SKILL.md"
        if not skill.is_file():
            err(f"{rel(folder)}: missing SKILL.md")
            continue
        found.append(folder.name)
        fm = parse_front_matter(skill.read_text(encoding="utf-8"))
        if fm is None:
            err(f"{rel(skill)}: no YAML front matter (file must start with '---' and close it with '---')")
            continue
        name = fm.get("name", "")
        if name != folder.name:
            err(f"{rel(skill)}: front matter name '{name}' must equal folder name '{folder.name}'")
        desc = fm.get("description", "")
        if not desc:
            err(f"{rel(skill)}: description is missing or empty")
        elif len(desc) > MAX_DESCRIPTION:
            err(f"{rel(skill)}: description is {len(desc)} chars (max {MAX_DESCRIPTION})")
    for name in EXPECTED_SKILLS:
        if name not in found:
            err(f"expected skill '{name}' not found in .agents/skills/")


# ---------------------------------------------------------------- required files

def check_required_files() -> None:
    for f in REQUIRED_FILES:
        if not (ROOT / f).is_file():
            err(f"required file missing: {f}")
    html = ROOT / "templates" / "release-notes.html"
    if html.is_file():
        text = html.read_text(encoding="utf-8")
        for ph in HTML_PLACEHOLDERS:
            if ph not in text:
                err(f"templates/release-notes.html: placeholder {ph} missing")


# ---------------------------------------------------------------- links

LINK_RE = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.S | re.M)  # fenced code, even indented
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def iter_markdown_files():
    for path in ROOT.rglob("*.md"):
        parts = path.relative_to(ROOT).parts
        if parts[0] in SKIP_DIRS or any(p in {".git", "node_modules", "__pycache__"} for p in parts):
            continue  # .git/, the personal top-level brain/, caches
        if parts[:2] == ("templates", "brain"):
            continue
        yield path


def check_links() -> None:
    for md in iter_markdown_files():
        text = md.read_text(encoding="utf-8")
        text = FENCE_RE.sub("", text)
        text = HTML_COMMENT_RE.sub("", text)
        text = INLINE_CODE_RE.sub("", text)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):  # http:, https:, mailto:, ...
                continue
            if target.startswith("#") or target.startswith("<"):
                continue
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                err(f"{rel(md)}: broken link -> {target}")


# ---------------------------------------------------------------- gitignore

def check_gitignore() -> None:
    gi = ROOT / ".gitignore"
    if not gi.is_file():
        return  # already reported as missing
    lines = [l.strip() for l in gi.read_text(encoding="utf-8").splitlines()]
    if "/brain/" not in lines:
        err(".gitignore must contain the line '/brain/' (leading slash keeps templates/brain/ committed)")
    if "brain/" in lines or "brain" in lines:
        err(".gitignore has an unanchored 'brain' rule; it would also ignore templates/brain/. Use '/brain/'.")


def main() -> int:
    check_skills()
    check_required_files()
    check_links()
    check_gitignore()
    if errors:
        print(f"validate.py: {len(errors)} problem(s) found\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    skills = len(list((ROOT / ".agents" / "skills").glob("*/SKILL.md")))
    print(f"validate.py: OK ({skills} skills, {len(REQUIRED_FILES)} required files, links and .gitignore checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
