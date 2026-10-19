#!/usr/bin/env python3
"""brain_search.py — find notes in a pm-agents brain (or the team hub). Python 3 standard library only.

Filters markdown files by their YAML front matter, then ranks them by keyword relevance
(simple BM25 over title x2 + body; lowercase, accents stripped). Superseded notes are hidden
unless you pass --status all (or --status superseded).

Usage:
  python3 scripts/brain_search.py "batch limit bulk edit"
  python3 scripts/brain_search.py "rollout" --type decision --product acme-listings-optimizer
  python3 scripts/brain_search.py --topic bulk-edit --since 2026-10-01 --limit 20
  python3 scripts/brain_search.py "rate limit" --person marco-lima --status all
  python3 scripts/brain_search.py "title scorer" --root ../pm-team-hub --type digest --json
  python3 scripts/brain_search.py --selftest

Output (one line per hit, best first; no query = newest first):
  path | date | type | title | best-matching line

Filters (all optional, combined with AND):
  --type T        front matter `type` (meeting, decision, stakeholder, digest, ...)
  --topic T       in `topics` (or `tags`)
  --person P      slug or name; matches `people`, `person`, `attendees`, `decided_by`, `owner`, `name`
  --status S      default: everything except superseded.  Or one of: active | superseded | stale |
                  done | accepted | proposed | all.  `active` matches active, accepted, proposed and
                  notes with no status.
  --since D       date >= D (YYYY-MM-DD).  Date = `date`, else `published`, else `updated`, else file mtime.
  --until D       date <= D
  --product P     path contains products/<P>/ (or products/<P>.md), or front matter `product`/`products`
  --share S       team | private | team,private (comma list).  Missing `share` defaults to team for decision, digest, product-card,
                  member and connections notes; private for everything else.
  --root DIR      folder to search (default: brain)
  --limit N       max results (default 10)
  --json          JSON list instead of text lines
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__"}
TEAM_DEFAULT_TYPES = {"decision", "digest", "product-card", "member", "connections"}
ACTIVE_STATUSES = {"", "active", "accepted", "proposed"}
STOPWORDS = set(
    "a an and are as at be by do does did for from has have how in is it of on or that the this to was "
    "were what when where which who why will with we our you your about".split()
)


# ------------------------------------------------------------------ text helpers

def fold(text: str) -> str:
    """Lowercase and strip accents: 'Precificação' -> 'precificacao'."""
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", fold(text)) if t not in STOPWORDS]


def slug(text: str) -> str:
    return "-".join(re.findall(r"[a-z0-9]+", fold(str(text))))


# ------------------------------------------------------------------ front matter

def _scalar(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    # drop trailing "  # comment" on unquoted values
    return re.split(r"\s+#", raw, maxsplit=1)[0].strip()


def _inline_list(raw: str) -> list[str]:
    inner = raw.strip()[1:-1]
    return [_scalar(x) for x in inner.split(",") if _scalar(x)]


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Tolerant parser: top-level scalars, inline lists [a, b] and block lists (- a).
    Anything else (nested maps, multi-line strings) is skipped. Returns (meta, body)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text
    meta: dict = {}
    key = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$", line.rstrip())
        if m and not line[0].isspace():
            key, raw = m.group(1), (m.group(2) or "")
            raw_clean = _scalar(raw) if not raw.strip().startswith("[") else raw.strip()
            if raw_clean.startswith("[") and raw_clean.endswith("]"):
                meta[key] = _inline_list(raw_clean)
            else:
                meta[key] = raw_clean
            continue
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and key is not None:
            value = _scalar(item.group(1))
            if isinstance(meta.get(key), list):
                meta[key].append(value)
            elif meta.get(key, "") == "":
                meta[key] = [value]
            continue
        # indented "sub: value" (nested map) or anything else: ignore
    return meta, "\n".join(lines[end + 1:])


def as_list(value) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    return [str(value)]


# ------------------------------------------------------------------ notes

class Note:
    def __init__(self, path: Path, root: Path):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        self.meta, self.body = parse_front_matter(text)
        self.type = str(self.meta.get("type", "") or "")
        self.title = self._title()
        self.date = self._date()
        self.title_tokens = tokens(self.title)
        topic_text = " ".join(as_list(self.meta.get("topics")) + as_list(self.meta.get("tags")))
        self.body_tokens = tokens(self.body) + tokens(topic_text.replace("-", " "))

    def _title(self) -> str:
        for k in ("title", "name"):
            if self.meta.get(k) and isinstance(self.meta[k], str):
                return self.meta[k]
        for line in self.body.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return self.path.stem

    def _date(self) -> str:
        for k in ("date", "published", "updated"):
            v = self.meta.get(k)
            if isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}", v):
                return v[:10]
        return _dt.date.fromtimestamp(self.path.stat().st_mtime).isoformat()

    @property
    def status(self) -> str:
        return str(self.meta.get("status", "") or "").strip().lower()

    @property
    def share(self) -> str:
        explicit = str(self.meta.get("share", "") or "").strip().lower()
        if explicit:
            return explicit
        return "team" if self.type in TEAM_DEFAULT_TYPES else "private"

    def people(self) -> set[str]:
        out = set()
        for k in ("people", "person", "attendees", "decided_by", "owner", "name"):
            out.update(slug(v) for v in as_list(self.meta.get(k)))
        return out

    def topics(self) -> set[str]:
        return {slug(v) for v in as_list(self.meta.get("topics")) + as_list(self.meta.get("tags"))}

    def products(self) -> set[str]:
        out = {slug(v) for v in as_list(self.meta.get("product")) + as_list(self.meta.get("products"))}
        parts = self.rel.split("/")
        for i, part in enumerate(parts[:-1]):
            if part == "products":
                nxt = parts[i + 1]
                out.add(nxt[:-3] if nxt.endswith(".md") else nxt)
        return out

    def best_line(self, query: list[str]) -> str:
        best, best_score = "", 0
        for line in self.body.splitlines():
            s = line.strip()
            if not s or s.startswith("<!--"):
                continue
            toks = set(tokens(s))
            score = sum(1 for q in set(query) if q in toks) - (0.5 if s.startswith("#") else 0)
            if score > best_score:
                best, best_score = s, score
        if not best:  # fall back to first content line
            best = next((l.strip() for l in self.body.splitlines()
                         if l.strip() and not l.startswith("#") and not l.strip().startswith("<!--")), "")
        best = best.replace("|", "/")
        return best[:157] + "..." if len(best) > 160 else best


def load_notes(root: Path) -> list[Note]:
    notes = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                try:
                    notes.append(Note(Path(dirpath) / f, root))
                except (OSError, ValueError):
                    continue  # unreadable file: skip, never crash
    return notes


# ------------------------------------------------------------------ filter + rank

def keep(note: Note, a) -> bool:
    if a.type and note.type != a.type:
        return False
    if a.topic and slug(a.topic) not in note.topics():
        return False
    if a.person and slug(a.person) not in note.people():
        return False
    status = (a.status or "default").lower()
    if status == "default":
        if note.status == "superseded":
            return False
    elif status == "active":
        if note.status not in ACTIVE_STATUSES:
            return False
    elif status != "all" and note.status != status:
        return False
    if a.since and note.date < a.since:
        return False
    if a.until and note.date > a.until:
        return False
    if a.product and slug(a.product) not in note.products():
        return False
    if a.share and note.share not in {s.strip().lower() for s in a.share.split(",") if s.strip()}:
        return False
    return True


def rank(notes: list[Note], query: list[str], k1: float = 1.2, b: float = 0.75) -> list[tuple[float, Note]]:
    if not query:
        return [(0.0, n) for n in sorted(notes, key=lambda n: (n.date, n.rel), reverse=True)]
    docs = []
    for n in notes:
        tf: dict[str, float] = {}
        for t in n.body_tokens:
            tf[t] = tf.get(t, 0) + 1
        for t in n.title_tokens:  # title counts double
            tf[t] = tf.get(t, 0) + 2
        length = len(n.body_tokens) + 2 * len(n.title_tokens)
        docs.append((n, tf, length))
    N = len(docs) or 1
    avg = sum(d[2] for d in docs) / N or 1
    df = {q: sum(1 for _, tf, _ in docs if q in tf) for q in set(query)}
    scored = []
    for n, tf, length in docs:
        score = 0.0
        for q in set(query):
            f = tf.get(q, 0)
            if not f:
                continue
            idf = math.log(1 + (N - df[q] + 0.5) / (df[q] + 0.5))
            score += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * length / avg))
        if score > 0:
            scored.append((score, n))
    scored.sort(key=lambda x: (-x[0], x[1].rel))
    return scored


def search(a) -> list[dict]:
    root = Path(a.root)
    if not root.is_dir():
        raise SystemExit(f"brain_search: folder not found: {root}")
    notes = [n for n in load_notes(root) if keep(n, a)]
    query = tokens(" ".join(a.query))
    results = []
    for score, n in rank(notes, query)[: a.limit]:
        results.append({
            "path": n.rel, "date": n.date, "type": n.type or "-", "title": n.title,
            "status": n.status or "-", "share": n.share, "score": round(score, 3),
            "best_line": n.best_line(query),
            "superseded_by": str(n.meta.get("superseded_by", "") or ""),
        })
    return results


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Search a pm-agents brain by front matter + keywords.",
                                epilog="See the docstring at the top of this file for examples.")
    p.add_argument("query", nargs="*", help="keywords (optional)")
    p.add_argument("--root", default="brain")
    p.add_argument("--type")
    p.add_argument("--topic")
    p.add_argument("--person")
    p.add_argument("--status", default="default")
    p.add_argument("--since")
    p.add_argument("--until")
    p.add_argument("--product")
    p.add_argument("--share")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--json", action="store_true")
    p.add_argument("--selftest", action="store_true", help="run built-in tests and exit")
    return p


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    if a.selftest:
        return selftest()
    results = search(a)
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif not results:
        print("No matching notes.")
    else:
        for r in results:
            print(f"{r['path']} | {r['date']} | {r['type']} | {r['title']} | {r['best_line']}")
    return 0


# ------------------------------------------------------------------ self-test

SYNTHETIC = {
    "products/acme-listings-optimizer/research/2026-10-10-precificacao.md":
        "---\ntype: research\ntitle: Precificação dinâmica\ndate: 2026-10-10\ntopics: [pricing]\n---\n"
        "Notas sobre precificação com sellers.\n",
    "products/acme-listings-optimizer/research/2026-10-11-title-weight.md":
        "---\ntype: research\ntitle: Zeppelin study\ndate: 2026-10-11\n---\nShort note.\n",
    "products/acme-listings-optimizer/research/2026-10-11-body-mention.md":
        "---\ntype: research\ntitle: Misc research\ndate: 2026-10-11\n---\n"
        "A long note about many things: sellers, listings, titles, images, prices, feeds, exports, "
        "imports, errors, retries, dashboards, and once a zeppelin.\n",
    "products/other-product/decisions/2026-10-12-other.md":
        "---\ntype: decision\ntitle: Other product batch decision\ndate: 2026-10-12\nstatus: accepted\n---\n"
        "Batch cap for the other product.\n",
    "products/acme-listings-optimizer/research/broken.md":
        "---\ntype: research\ntitle: [unclosed\ntopics: [a, b\n: weird\n  nested: map\n---\nStill searchable kiwi.\n",
    "products/acme-listings-optimizer/research/no-front-matter.md":
        "# Plain note\n\nNo front matter, mentions mango.\n",
}


def selftest() -> int:
    repo = Path(__file__).resolve().parent.parent
    fixture = repo / "evals" / "fixtures" / "memory" / "brain"
    failures: list[str] = []

    def check(name: str, cond: bool, detail: str = "") -> None:
        print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  -> {detail}"))
        if not cond:
            failures.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "brain"
        if fixture.is_dir():
            shutil.copytree(fixture, root)
        else:
            print(f"WARN fixture brain not found at {fixture}; using synthetic notes only")
            root.mkdir()
        for rel, text in SYNTHETIC.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        nodate = root / "products/acme-listings-optimizer/research/no-front-matter.md"
        ts = _dt.datetime(2026, 3, 1, 12, 0).timestamp()
        os.utime(nodate, (ts, ts))

        def run(*args: str) -> list[dict]:
            a = build_parser().parse_args(["--root", str(root), *args])
            return search(a)

        def paths(res):
            return [r["path"] for r in res]

        # front matter parser
        meta, _ = parse_front_matter("---\na: 1  # c\nb: [x, 'y z']\nc:\n  - one\n  - two\nd:\n  e: f\n---\nbody")
        check("parser: scalars, inline + block lists, nested ignored",
              meta.get("a") == "1" and meta.get("b") == ["x", "y z"] and meta.get("c") == ["one", "two"],
              str(meta))

        has_fixture = fixture.is_dir()
        if has_fixture:
            res = run("rollout", "sellers", "--type", "decision")
            check("default hides superseded", all(r["status"] != "superseded" for r in res), str(paths(res)))
            check("current rollout decision found",
                  any(p.endswith("2026-10-06-beta-sellers-first.md") for p in paths(res)), str(paths(res)))
            res_all = run("rollout", "--type", "decision", "--status", "all")
            check("--status all includes superseded",
                  any(p.endswith("2026-09-01-flag-internal-only.md") for p in paths(res_all)), str(paths(res_all)))
            res_sup = run("--status", "superseded")
            check("--status superseded only superseded",
                  bool(res_sup) and all(r["status"] == "superseded" for r in res_sup), str(res_sup))
            sup = [r for r in res_sup if r["path"].endswith("2026-09-01-flag-internal-only.md")]
            check("superseded_by exposed", bool(sup) and sup[0]["superseded_by"] != "", str(sup))
            res = run("--type", "decision", "--limit", "50")
            check("--type decision", bool(res) and all(r["type"] == "decision" for r in res), str(res))
            res = run("--topic", "bulk-edit", "--limit", "50")
            check("--topic bulk-edit", len(res) >= 3, str(paths(res)))
            res = run("--person", "marco-lima", "--limit", "50")
            check("--person slug matches attendees name",
                  any("meetings/" in p for p in paths(res)), str(paths(res)))
            res = run("--person", "Marco Lima", "--type", "stakeholder")
            check("--person by display name", len(res) == 1, str(paths(res)))
            res = run("--share", "private", "--limit", "50")
            check("--share private excludes decisions (default team)",
                  bool(res) and all(r["type"] != "decision" for r in res), str(paths(res)))
            res = run("--share", "team,private", "--limit", "200")
            check("--share comma list", len(res) == len(run("--limit", "200")), str(len(res)))
            res = run("--share", "team", "--type", "decision", "--limit", "50")
            check("--share team includes decisions", len(res) >= 2, str(paths(res)))
            res = run("batch", "cap")
            check("ranking: batch cap decision near top",
                  bool(res) and any("batch-cap" in p for p in paths(res)[:3]), str(paths(res)))

        res = run("--since", "2026-10-10", "--until", "2026-10-11", "--limit", "50")
        check("--since/--until window",
              bool(res) and all("2026-10-10" <= r["date"] <= "2026-10-11" for r in res), str(res))
        res = run("--product", "other-product", "--limit", "50")
        check("--product by path", paths(res) == ["products/other-product/decisions/2026-10-12-other.md"],
              str(paths(res)))
        res = run("--product", "acme-listings-optimizer", "--limit", "100")
        check("--product excludes other product",
              bool(res) and all("other-product" not in p for p in paths(res)), str(paths(res)))
        res = run("--product", "other-product", "--share", "team")
        check("share default: decision without share = team", len(res) == 1, str(paths(res)))
        res = run("precificacao", "--share", "private")
        check("share default: research without share = private", len(res) == 1, str(paths(res)))
        res = run("precificacao")
        check("accents stripped", bool(res) and res[0]["path"].endswith("precificacao.md"), str(paths(res)))
        res = run("zeppelin")
        check("title weight beats single body mention",
              len(res) >= 2 and res[0]["path"].endswith("title-weight.md"), str(paths(res)))
        res = run("kiwi")
        check("malformed front matter tolerated", len(res) == 1, str(paths(res)))
        res = run("mango", "--until", "2026-03-31")
        check("mtime used when no date", len(res) == 1 and res[0]["date"] == "2026-03-01", str(res))
        res = run("--limit", "2")
        check("--limit", len(res) == 2, str(paths(res)))
        out = os.popen(f'"{sys.executable}" "{__file__}" zeppelin --json --root "{root}"').read()
        try:
            data = json.loads(out)
            ok = isinstance(data, list) and data and {"path", "date", "type", "title", "best_line"} <= set(data[0])
        except ValueError:
            ok = False
        check("--json output", bool(ok), out[:200])

    print(f"\nselftest: {'OK' if not failures else str(len(failures)) + ' failure(s)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
