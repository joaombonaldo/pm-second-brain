#!/usr/bin/env python3
"""Build CATALOG.md (the skills marketplace list) from .agents/skills/*/SKILL.md front matter. Stdlib only.

Each skill's front matter has `name`, `description` and a `metadata:` map with the marketplace fields
(category, role, owner, version, status, brain, reads, writes, preferences, requires). See docs/SKILL-STANDARD.md.

Usage:
  python3 scripts/catalog.py           # write CATALOG.md
  python3 scripts/catalog.py --check   # exit 1 if CATALOG.md is out of date (used by validate.py)
  python3 scripts/catalog.py --stdout  # print instead of writing

Output is deterministic: categories in a fixed order, skills sorted by name.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".agents" / "skills"
CATALOG = ROOT / "CATALOG.md"

CATEGORIES = ["brain", "backlog", "release", "reporting", "team", "comms", "research", "other"]
CATEGORY_TITLES = {
    "brain": "Brain — remember, answer, tidy",
    "backlog": "Backlog — stories and refinement",
    "release": "Release — what shipped",
    "reporting": "Reporting — status for stakeholders",
    "team": "Team — hub, roll-ups, connections",
    "comms": "Comms — messages and updates",
    "research": "Research — discovery and analysis",
    "other": "Other",
}
LIST_FIELDS = ["reads", "writes", "preferences", "requires"]


# ---------------------------------------------------------------- parsing (shared with validate.py)

def _clean(value: str) -> str:
    """Strip quotes, or a trailing ` # comment` from an unquoted value."""
    value = value.strip()
    quoted = re.match(r"""^(["'])(.*?)\1\s*(#.*)?$""", value)
    if quoted:
        return quoted.group(2)
    return re.sub(r"\s+#.*$", "", value).strip()


def parse_skill(text: str) -> dict | None:
    """Parse SKILL.md front matter: top-level `key: value` (incl. folded blocks) and one level of `metadata:`.

    Returns {"keys": [top-level keys in order], "fields": {key: str}, "metadata": {key: str},
    "raw_values": [(key, raw value)]} or None when there is no front matter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    keys: list[str] = []
    fields: dict[str, str] = {}
    meta: dict[str, str] = {}
    raw: list[tuple[str, str]] = []
    key = None
    in_meta = False
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if top:
            key, value = top.group(1), top.group(2)
            keys.append(key)
            raw.append((key, value))
            in_meta = key == "metadata" and not value.strip()
            if value.strip() in (">", "|", ">-", "|-"):
                value = ""
            fields[key] = _clean(value)
            continue
        sub = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
        if in_meta and sub:
            meta[sub.group(1)] = _clean(sub.group(2))
            raw.append((f"metadata.{sub.group(1)}", sub.group(2)))
        elif key is not None and not in_meta:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return {"keys": keys, "fields": fields, "metadata": meta, "raw_values": raw}


def split_list(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()] if value else []


def first_sentence(text: str) -> str:
    m = re.match(r"^(.+?[.!?])(\s|$)", text.strip())
    return (m.group(1) if m else text).strip()


def load_skills() -> list[dict]:
    """All skills with parsed front matter, sorted by folder name. Unparseable ones get fm=None."""
    out = []
    if not SKILLS_DIR.is_dir():
        return out
    for folder in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        f = folder / "SKILL.md"
        if not f.is_file():
            continue
        out.append({"folder": folder.name, "path": f, "fm": parse_skill(f.read_text(encoding="utf-8"))})
    return out


# ---------------------------------------------------------------- rendering

def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def _code_list(value: str) -> str:
    items = split_list(value)
    return ", ".join(f"`{i}`" for i in items) if items else "—"


def render(skills: list[dict]) -> str:
    rows = []
    for s in skills:
        fm = s["fm"]
        if fm is None:
            continue
        m = fm["metadata"]
        cat = m.get("category", "other")
        rows.append({
            "name": fm["fields"].get("name", s["folder"]),
            "folder": s["folder"],
            "description": fm["fields"].get("description", ""),
            "category": cat if cat in CATEGORIES else "other",
            **{k: m.get(k, "") for k in ["role", "owner", "version", "status", "brain", *LIST_FIELDS]},
        })
    rows.sort(key=lambda r: (CATEGORIES.index(r["category"]), r["name"]))

    out = [
        "# Skills catalog",
        "",
        "<!-- Generated by scripts/catalog.py from each skill's front matter. Do not edit by hand: "
        "change the SKILL.md, then run `python3 scripts/catalog.py`. -->",
        "",
        "This is the **skills marketplace** of pm-agents: every skill the team can use, who owns it and how far you "
        "can trust it. Every skill is *brain-aware*: it reads your `brain/brain.yaml` and your `brain/preferences/`, so "
        "it works on your product without changes ([docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md)).",
        "",
        "- **Use a skill:** in Devin CLI type `/<name>` (for example `/weekly-status`), or just ask in plain words and "
        "the right skill is picked.",
        "- **Add or improve one:** see [CONTRIBUTING.md](CONTRIBUTING.md).",
        "- **Status:** `stable` = tested and used for real; `experimental` = new or not yet tested in real use, check "
        "its output; `deprecated` = being replaced.",
        "- **Brain:** `required` = needs your brain (run `/onboard` first); `optional` = works without it; `none` = "
        "never touches it.",
        "",
        f"{len(rows)} skills.",
        "",
        "## At a glance",
        "",
    ]
    for cat in CATEGORIES:
        group = [r for r in rows if r["category"] == cat]
        if not group:
            continue
        out += [f"### {CATEGORY_TITLES[cat]} ({len(group)})", "",
                "| Skill | What it does | Role | Status | Brain | Requires | Version | Owner |",
                "|-------|--------------|------|--------|-------|----------|---------|-------|"]
        for r in group:
            out.append("| " + " | ".join([
                f"[`/{r['name']}`](#{r['name']})",
                _cell(first_sentence(r["description"])),
                _cell(r["role"]), r["status"], r["brain"],
                ", ".join(split_list(r["requires"])) or "—",
                r["version"], _cell(r["owner"]),
            ]) + " |")
        out.append("")
    out += ["## Skills", ""]
    for r in rows:
        out += [
            f"### {r['name']}",
            "",
            f"`/{r['name']}` · {r['role']} · {r['category']} · {r['status']} · v{r['version']} · owner: {r['owner']}",
            "",
            r["description"],
            "",
            f"- **Brain:** {r['brain']}",
            f"- **Reads:** {_code_list(r['reads'])}",
            f"- **Writes:** {_code_list(r['writes']) if r['writes'] else 'nothing (read-only)'}",
            f"- **Honours preferences:** {_code_list(r['preferences'])}",
            f"- **Requires:** {_code_list(r['requires'])}",
            f"- **Source:** [.agents/skills/{r['folder']}/SKILL.md](.agents/skills/{r['folder']}/SKILL.md)",
            "",
        ]
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate CATALOG.md from skill front matter.")
    ap.add_argument("--check", action="store_true", help="exit 1 if CATALOG.md is out of date")
    ap.add_argument("--stdout", action="store_true", help="print the catalog instead of writing it")
    args = ap.parse_args()
    text = render(load_skills())
    if args.stdout:
        sys.stdout.write(text)
        return 0
    if args.check:
        current = CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
        if current != text:
            print("catalog.py: CATALOG.md is out of date. Run: python3 scripts/catalog.py")
            return 1
        print("catalog.py: CATALOG.md is up to date")
        return 0
    CATALOG.write_text(text, encoding="utf-8")
    print(f"catalog.py: wrote {CATALOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
