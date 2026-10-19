#!/usr/bin/env python3
"""Validate the pm-agents repo. Standard library only.

Checks:
  1. Every .agents/skills/*/SKILL.md has YAML front matter with `name` equal to its folder name
     and a non-empty `description` of at most 1024 characters.
  2. Required templates exist.
  3. Relative markdown links in repo .md files resolve (http(s)/mailto links, anchor-only links,
     links inside code, and files under templates/brain/ and templates/team-hub/ are ignored: their
     links are relative to the future brain/ or pm-team-hub/ they get copied into).
  4. .gitignore ignores the top-level brain folder with `/brain/`.
  5. Marketplace metadata (docs/SKILL-STANDARD.md): `name` and `description` are the first two keys; name is
     kebab-case and unique; descriptions are not copies of each other; every `metadata` field is present with an
     allowed value; unquoted values contain no ': ' (strict YAML parsers reject them); non-core skills have an eval
     file in evals/skills/. Warns (does not fail) when two descriptions share many trigger phrases.
  6. CATALOG.md is up to date (`scripts/catalog.py --check`).

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
    "docs/DESIGN-v0.2.md",
    "scripts/brain_search.py",
    "scripts/catalog.py",
    "CATALOG.md",
    "CONTRIBUTING.md",
    "docs/SKILL-STANDARD.md",
    "templates/skill/SKILL.md",
    "templates/skill/eval.md",
    "evals/skills/README.md",
    "templates/meeting-note.md",
    "templates/decision.md",
    "templates/stakeholder.md",
    "templates/user-story.md",
    "templates/weekly-status.md",
    "templates/release-notes.html",
    "templates/persona.md",
    "templates/topic-hub.md",
    "templates/product-index.md",
    "templates/digest.md",
    "templates/product-card.md",
    "templates/team-hub/README.md",
    "templates/team-hub/member.md",
    "templates/brain/brain.yaml",
    "templates/brain/preferences/README.md",
    "templates/brain/inbox/.gitkeep",
    "templates/brain/inbox/processed/.gitkeep",
    "templates/brain/stakeholders/.gitkeep",
    "templates/brain/products/_example/README.md",
]

EXPECTED_SKILLS = [
    "onboard", "ingest", "ask", "decision", "sweep",   # Brain Keeper
    "user-story",                                      # Backlog Writer
    "release-notes",                                   # Release Manager
    "weekly-status", "publish",                        # Reporter
    "team-status", "connect-dots",                     # Connector (team-status shared with Reporter)
]
HTML_PLACEHOLDERS = ["{{product_name}}", "{{version}}", "{{date}}", "{{intro}}", "{{sections}}"]

SKIP_DIRS = {".git", "brain", "node_modules", "__pycache__"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


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


# ---------------------------------------------------------------- marketplace metadata (v0.3)

sys.path.insert(0, str(ROOT / "scripts"))
import catalog  # noqa: E402  (stdlib-only sibling script)

ALLOWED = {
    "category": set(catalog.CATEGORIES),
    "role": {"Brain Keeper", "Backlog Writer", "Release Manager", "Reporter", "Connector", "other"},
    "status": {"experimental", "stable", "deprecated"},
    "brain": {"required", "optional", "none"},
}
ALLOWED_REQUIRES = {"jira-mcp", "confluence-mcp", "gitlab-mcp", "team-hub", "python3", "git"}
META_FIELDS = ["category", "role", "owner", "version", "status", "brain", "reads", "writes", "preferences", "requires"]
CORE_OWNER = "pm-agents core"
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
QUOTED_RE = re.compile(r'"([^"]{3,})"')
STOP = set("""a an and or the to of for in on at by with from into as is are be it its this that these those
your you my me we our their them any all each one two use when user types says say says, if only also
via not no do does what who how which about""".split())


def _trigger_phrases(desc: str) -> set[str]:
    return {re.sub(r"[…\s.]+$", "", p.lower()).strip() for p in QUOTED_RE.findall(desc)}


def _content_bigrams(desc: str) -> set[tuple[str, str]]:
    words = [w for w in re.findall(r"[a-z0-9-]+", desc.lower()) if w not in STOP and not w.startswith("/")]
    return set(zip(words, words[1:]))


def check_marketplace() -> None:
    skills = catalog.load_skills()
    names: dict[str, str] = {}
    descs: dict[str, str] = {}
    for s in skills:
        fm, where = s["fm"], rel(s["path"])
        if fm is None:
            continue  # already reported by check_skills
        if fm["keys"][:2] != ["name", "description"]:
            err(f"{where}: `name` and `description` must be the first two front matter keys")
        name = fm["fields"].get("name", "")
        if name and (not KEBAB_RE.match(name) or len(name) > 64):
            err(f"{where}: name '{name}' must be kebab-case (a-z, 0-9, single hyphens), max 64 chars")
        if name in names:
            err(f"{where}: name '{name}' is already used by {names[name]}")
        names[name] = where
        desc = fm["fields"].get("description", "")
        for other, other_desc in descs.items():
            if desc and desc.strip().lower() == other_desc.strip().lower():
                err(f"{where}: description is a copy of skill '{other}'")
        descs[name] = desc
        for key, raw_value in fm["raw_values"]:
            v = raw_value.strip()
            if v and v[0] not in "\"'>|" and ": " in re.sub(r"\s+#.*$", "", v):
                err(f"{where}: `{key}` has ': ' in an unquoted value; strict YAML parsers (Devin) reject it. "
                    f"Quote the value or rephrase.")
        if "metadata" not in fm["keys"]:
            err(f"{where}: missing `metadata:` block with marketplace fields (docs/SKILL-STANDARD.md)")
            continue
        m = fm["metadata"]
        for field in META_FIELDS:
            if field not in m:
                err(f"{where}: metadata.{field} is missing")
        for field, allowed in ALLOWED.items():
            if field in m and m[field] not in allowed:
                err(f"{where}: metadata.{field} '{m[field]}' not allowed (use one of: {', '.join(sorted(allowed))})")
        if "owner" in m and not m["owner"]:
            err(f"{where}: metadata.owner is empty (a person or team)")
        if "version" in m and not SEMVER_RE.match(m["version"]):
            err(f"{where}: metadata.version '{m['version']}' must be semver, e.g. \"0.1.0\"")
        for req in catalog.split_list(m.get("requires", "")):
            if req not in ALLOWED_REQUIRES:
                err(f"{where}: metadata.requires '{req}' not allowed (use: {', '.join(sorted(ALLOWED_REQUIRES))})")
        if m.get("owner") != CORE_OWNER and name not in EXPECTED_SKILLS:
            if not (ROOT / "evals" / "skills" / f"{name}.md").is_file():
                err(f"{where}: new skill needs at least one eval scenario in evals/skills/{name}.md (CONTRIBUTING.md)")
    # "Devin picks the wrong skill" risk: overlapping trigger phrases or wording
    items = sorted(descs.items())
    for i, (a, da) in enumerate(items):
        for b, db in items[i + 1:]:
            shared = _trigger_phrases(da) & _trigger_phrases(db)
            ba, bb = _content_bigrams(da), _content_bigrams(db)
            jac = len(ba & bb) / len(ba | bb) if ba and bb else 0.0
            if len(shared) >= 2 or jac >= 0.25:
                detail = f"shared trigger phrases: {sorted(shared)}" if shared else f"wording overlap {jac:.0%}"
                warn(f"skills '{a}' and '{b}' may trigger on the same requests ({detail}); make the descriptions "
                     f"more distinct")
            elif len(shared) == 1:
                warn(f"skills '{a}' and '{b}' share the trigger phrase \"{next(iter(shared))}\"")


def check_catalog() -> None:
    expected = catalog.render(catalog.load_skills())
    current = catalog.CATALOG.read_text(encoding="utf-8") if catalog.CATALOG.is_file() else ""
    if current != expected:
        err("CATALOG.md is out of date. Run: python3 scripts/catalog.py")


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
        if parts[:2] in {("templates", "brain"), ("templates", "team-hub")}:
            continue  # links are relative to the brain/ or pm-team-hub/ these get copied into
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
    check_marketplace()
    check_catalog()
    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        print(f"validate.py: {len(errors)} problem(s) found\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    skills = len(list((ROOT / ".agents" / "skills").glob("*/SKILL.md")))
    print(f"validate.py: OK ({skills} skills, {len(REQUIRED_FILES)} required files, links, .gitignore, marketplace metadata and CATALOG.md checked; {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
