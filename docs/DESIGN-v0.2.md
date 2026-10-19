# pm-agents v0.2 — Design spec: team layer + memory upgrades

> Status: approved by João on 2026-10-19. This file is the contract every builder (human or agent) works against.
> Decisions referenced as D18–D30 are also logged in `docs/HANDOFF.md` §3.

## 1. What v0.2 adds

1. **Team layer.** Each PM keeps a private brain. Once a week each PM publishes a short, reviewed **digest** to a
   shared **team hub**. The manager (and every PM) can read all digests, get a portfolio roll-up, and ask an agent to
   **connect the dots**: overlaps, reuse opportunities, things two PMs could build together.
2. **Memory upgrades.** A "dreaming" `/sweep`, versioned brains, topic grouping, metadata-filtered search, batch
   ingest and quick decision logging.

What does **not** change: plain markdown is the source of truth (D1); one shared `pm-agents` repo (D4); skills in
`.agents/skills/` (D5); human approval for durable writes (D13); no vector DB (D1, revisited in §8).

## 2. Roles (D18)

Same repo, same install, for everyone. `brain/brain.yaml` gets `owner.role: pm | manager`.

| | PM | Manager |
|---|---|---|
| Own private brain | yes | yes (his own work, 1:1 notes, team goals) |
| Publishes a weekly digest | yes | optional (e.g. team priorities) |
| Reads the hub | yes | yes |
| `/team-status` (portfolio roll-up) | yes | yes — primary user |
| `/connect-dots` | yes | yes — primary user |

No skill is hard-blocked by role; `role` only changes defaults (e.g. a manager's `/weekly-status` suggests
`/team-status`). Easier to maintain, and PMs finding overlaps themselves is a feature.

## 3. Team hub (D19, D20)

A **separate GitLab repo**, `pm-team-hub`, cloned by every member next to their `pm-agents` clone. Readable and
writable by all PMs + the manager (D20: audience = all PMs + manager). It contains **only digests and cards** —
never brain files.

```
pm-team-hub/
├── README.md                     # what this is, the privacy rule, how to join
├── members/<person-slug>.md      # who, role, products, focus areas (one per person)
├── products/<product-slug>.md    # product card: mission, current focus, what we're building, reusable assets, needs
├── digests/<YYYY>/<YYYY-Www>/<person-slug>.md   # one weekly digest per person; <YYYY> = ISO-week year
└── connections/<YYYY-Www>.md     # optional: connect-dots reports the manager chooses to share
```

`brain/brain.yaml` gets:

```yaml
team_hub:
  path: ../pm-team-hub        # local clone of the hub; empty = team features off
  person_slug: joao-meier     # your folder/file name in the hub
```

A bootstrap template lives in `templates/team-hub/` (README + empty folders + example member/product files with a
fictional person). Whoever creates the hub copies it into a new GitLab repo.

## 4. Digest and product card (D21)

### 4.1 Weekly digest — `digests/<YYYY>/<YYYY-Www>/<person-slug>.md`

```yaml
---
type: digest
person: joao-meier
role: pm
week: 2026-W43
products: [cab]
topics: [bulk-edit, llm-evaluation, feed-quality]     # kebab-case, the PM's brain topics that were active
building:                                            # capabilities/components being built — the main matching signal
  - "LLM-based title quality scorer"
reusable:                                            # things others could reuse now
  - "Prompt templates for product titles (WhatsApp BR)"
needs:                                               # what would help: data, people, decisions, tools
  - "Access to clickstream data for listing CTR"
published: 2026-10-23
---
```

Body sections, ≤ 250 words total: **Headline** (1 line) · **Progress** · **Decisions** (shareable ones only, with
date) · **Risks / blocked** · **Asks**.

### 4.2 Product card — `products/<product-slug>.md`

Front matter: `type: product-card`, `product`, `owner` (person slug), `topics`, `building`, `reusable`, `needs`,
`updated`. Body: **Mission** (2 lines) · **Current focus** · **What we're building** · **Reusable assets** ·
**Needs** · **Recent decisions** (last 5, dated). Updated by `/publish`, full-file diff shown before writing.

### 4.3 Matching vocabulary

`topics`, `building`, `reusable` and `needs` are what `/connect-dots` matches on. Topics are free kebab-case, but
`/publish` first reads all existing topics in the hub and **reuses an existing topic when it means the same thing**
(e.g. prefer an existing `llm-evaluation` over a new `llm-evals`). This keeps the team vocabulary converging without a
fixed taxonomy.

## 5. Privacy rule for publishing (D22) — the most important rule in v0.2

A digest is written **from** the brain but is **not a copy** of it. `/publish` must never include:

- raw transcript text or quotes;
- anything from `brain/stakeholders/` (people notes) or any opinion attributed to a named colleague;
- `interpretation` claims about people;
- any note or line marked `share: private` (front matter field, see §6) or inside a `<!-- private -->` …
  `<!-- /private -->` block;
- numbers, customer names or dates the PM hasn't approved in the preview.

Allowed: summaries of the PM's own work, `decision` claims about the product (unless `share: private`), product
`observation`s, `hypothesis` being tested, asks. The PM sees the **exact final text** of the digest and product
card diff and must say yes; nothing is pushed otherwise (D23).

## 6. Front matter v2 (D24)

Every brain note keeps its v1 fields (see `CONVENTIONS.md`) and adds, where relevant:

| Field | Values | Used by |
|---|---|---|
| `topics` | list of kebab-case topics | topic hubs, `/ask`, `/publish` |
| `people` | list of person slugs mentioned | `/ask` filters |
| `status` | `active` (default) · `superseded` · `stale` · `done` (decisions may also use `proposed` / `accepted`) | `/sweep`, `/ask` (superseded hidden unless asked) |
| `supersedes` / `superseded_by` | relative path | decision history |
| `valid_from` | date the fact became true | "what did we believe in August?" |
| `share` | `team` (default for decisions and hub files) · `private` (default for everything else: meetings, stakeholders, research, sweeps, raw notes) | `/publish` |

## 7. Memory upgrades (D25–D29)

- **D25 · `/sweep` = dreaming pass.** Run weekly (Friday, before `/publish`) or on demand. Steps: merge duplicate
  notes; detect contradictions (newer decision vs older one, conflicting facts) and propose marking the older one
  `status: superseded` + `superseded_by`; flag notes older than 60 days with no links as `stale`; promote
  observations seen in ≥ 3 notes into the product pages; rebuild topic hubs and the product index; write a report to
  `products/<slug>/sweeps/YYYY-Www.md`. **All edits to existing notes are shown as one diff and applied after yes**;
  the report itself is written freely. Never deletes; superseded/stale notes stay for history.
- **D26 · Versioned brain.** `/onboard` runs `git init` inside `brain/` (a separate repo; still ignored by the shared
  repo). Every skill that writes to the brain ends with one commit inside `brain/`:
  `git -C brain add -A && git -C brain commit -m "<skill>: <short what>"`. If git is missing or fails, warn once and
  carry on. A PM may add a private remote for backup (README explains; not automatic).
- **D27 · Topic grouping.** Topic hubs at `products/<slug>/topics/<topic>.md` (template `templates/topic-hub.md`):
  one-paragraph state, active decisions, open questions, latest notes (links). Product index at
  `products/<slug>/index.md` (template `templates/product-index.md`): current focus, roadmap link, latest 10 decisions,
  topics list, key people. `/ingest` updates the index and touched topic hubs (free write: they are derived pages);
  `/sweep` rebuilds them fully.
- **D28 · Metadata search.** `scripts/brain_search.py` (python3 stdlib only) — filters markdown files by front matter
  (`--type --topic --person --status --since --until --product --share`) then ranks by keyword relevance (simple
  BM25-style scoring over title + body), prints top N as `path | date | type | title | best-matching line`. Works on any
  root (`--root brain` default, `--root ../pm-team-hub` for the hub). `/ask`, `/sweep`, `/publish`,
  `/team-status` and `/connect-dots` call it first instead of reading whole folders — fewer tokens, better recall.
  Superseded notes excluded unless `--status all`. Must have a `--json` output option and a small self-test
  (`python3 scripts/brain_search.py --selftest`) using `evals/fixtures/`.
- **D29 · Batch ingest + `/decision`.** `/ingest` processes every inbox file, writes all meeting notes (free writes),
  then shows **one** consolidated approval message with every proposed decision/durable change, numbered, accepting
  `yes` / `no` / `1,3`. `/decision` logs a decision in one step from chat (asks only for what's missing: what, why,
  who decided, date), checks for an older conflicting decision and offers to supersede it.

## 8. Vector search (D30)

Still deferred. `brain_search.py` is the single retrieval entry point, so a semantic/hybrid backend can be added
behind it later without touching skills. Revisit when evals show `/ask` misses caused by wording, or a brain passes
~1,000 notes, and only after Dell confirms where embeddings may be computed.

## 9. New and changed skills

| Skill | Status | Owner role | What |
|---|---|---|---|
| `onboard` | changed | all | + `owner.role`, `team_hub` setup (optional), `git init` in brain/, topics question optional |
| `ingest` | changed | all | batch mode, topics/people/share front matter, index + topic hub updates, brain commit |
| `ask` | changed | all | uses `brain_search.py`; hides superseded; `--team`/team questions search the hub too |
| `decision` | **new** | Brain Keeper | quick decision log with supersede check |
| `sweep` | **new** | Brain Keeper | dreaming pass (D25) |
| `publish` | **new** | Reporter | weekly digest + product card → hub, preview + yes, then `git pull --rebase`, commit, push (push asks) |
| `team-status` | **new** | Reporter (manager) | roll-up of the latest week's digests: per person headline, cross-team risks, open asks, who hasn't published |
| `connect-dots` | **new** | Connector (manager) | finds overlaps (same `building`/topics), reuse (`reusable` ↔ `needs`), combinations (X + Y → Z), dependencies; every suggestion cites the digest/product-card files it's based on and states confidence; output to chat, optionally saved to the manager's brain or `hub/connections/` after yes |

`AGENTS.md` adds a fifth role, **Connector** (`/connect-dots`, and `/team-status` shared with Reporter).

## 10. Weekly rhythm (what a PM actually does)

Daily: drop transcripts → `/ingest`. Friday: `/sweep` → approve → `/publish` → approve. Manager, Monday:
`/team-status`, then `/connect-dots`.
