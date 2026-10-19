# Conventions

How notes in the second brain are named, structured and linked. Every skill follows this file.

## 1. Claim types (D12)

Every durable statement (in decisions, product pages, stakeholder notes, meeting "decision candidates") carries a
claim type, a date and a source.

| Type | Meaning | Example |
|------|---------|---------|
| `observation` | Something seen or measured directly. | "Checkout conversion was 2.1% in September." (source: dashboard export) |
| `interpretation` | Someone's reading or opinion of what it means. | "Priya thinks the drop comes from the new shipping form." |
| `hypothesis` | A testable belief we want to check. | "If we prefill the address, conversion rises by ≥0.3 pt." |
| `assumption` | Something we act as if true without checking. | "Sellers update stock at least daily." |
| `decision` | Someone with authority chose a course of action. | "Ship bulk edit behind a flag in v2.4 (decided by Ana, PM)." |

Inline format:

```markdown
- [decision] Ship bulk edit behind a feature flag in v2.4. — 2026-10-20, Ana Souza · source: meetings/2026/2026-10-20-ux-sync.md
- [interpretation] Marco believes sellers won't adopt it without a tutorial. — 2026-10-20 · source: meetings/2026/2026-10-20-ux-sync.md
```

Rules: an opinion stays an `interpretation` even if said confidently. Only mark `decision` when the source shows the
decision being made, and who made it. When unsure, use the weaker type and say so.

## 2. File naming

- **kebab-case**, lowercase, ASCII: `pricing-page.md`, `ana-souza.md`.
- **Dated notes** (meetings, decisions): `YYYY-MM-DD-slug.md`, e.g. `2026-10-20-ux-sync.md`.
- Meetings are filed by year: `meetings/2026/2026-10-20-ux-sync.md`.
- Weekly status: `status/YYYY-Www.md` (ISO week), e.g. `status/2026-W43.md`.
- Release notes: `releases/<version>.html`, e.g. `releases/2.4.0.html` or `releases/sprint-42.html`.
- Story drafts: `backlog/drafts/YYYY-MM-DD-slug.md`.
- Stakeholders: `stakeholders/firstname-lastname.md`.
- Product slug: short kebab-case name set at onboarding, e.g. `listings-optimizer`.

## 3. Brain folder map

```
brain/
├── brain.yaml                 # who you are, your products, Jira/Confluence keys
├── preferences/               # your templates + persona; override templates/
├── inbox/                     # drop transcripts and notes here
│   └── processed/             # raw files moved here after /ingest
├── stakeholders/              # one file per person (shared across products)
└── products/<slug>/
    ├── index.md               # product index: derived page (see §9)
    ├── topics/                # one topic hub per topic: derived pages (see §9)
    ├── product/               # durable product pages (overview, users, metrics)   [approval]
    ├── roadmap/               # roadmap notes                                      [approval]
    ├── decisions/             # one decision record per file                      [approval]
    ├── hypotheses/            # hypotheses being tested                            [approval]
    ├── research/              # interviews, research notes
    ├── meetings/YYYY/         # one note per meeting
    ├── backlog/drafts/        # user story drafts
    ├── releases/              # release notes (HTML)
    ├── status/                # weekly statuses
    └── sweeps/                # /sweep reports, YYYY-Www.md
```

`brain/` is also its own small git repository (see §10).

## 4. Approval rules (D13)

| Where | Rule |
|-------|------|
| `inbox/`, `meetings/`, `backlog/drafts/`, `status/`, `releases/`, `research/`, `sweeps/` | Agent writes freely. |
| `index.md`, `topics/` (derived pages) | Agent writes freely; they are rebuilt from the notes. |
| `stakeholders/` | Agent appends dated lines freely; rewriting or deleting lines needs a yes. |
| `product/`, `roadmap/`, `decisions/`, `hypotheses/`, `brain.yaml`, `preferences/` | Show a diff, apply after a yes. |
| Jira, Confluence | **Always** show exactly what will be written; act only after an explicit yes. |
| Teams, email, chat | Never post. Produce paste-ready text. |

## 5. Sources and citations

Paths in `source:` are relative to the product folder (`brain/products/<slug>/`) when inside it, otherwise relative
to `brain/`. Formats:

```
source: meetings/2026/2026-10-20-ux-sync.md
source: stakeholders/ana-souza.md
jira: ABC-123
confluence: "Listings Optimizer — Product Overview" (<page URL>)
source: pasted by user, 2026-10-21
```

In answers to the user, cite the same way, with the date: "(2026-10-20, meetings/2026/2026-10-20-ux-sync.md)".

## 6. Links

Use **relative markdown links** between brain notes: `[UX sync](../meetings/2026/2026-10-20-ux-sync.md)`.
No absolute paths, no wiki-links (`[[...]]`).

## 7. Front matter per note type

All notes start with YAML front matter. Unknown values: leave empty, never invent. Every type below can also carry
the v2 fields from §8 (`topics`, `people`, `status`, `share`, …); the examples show the usual ones.

**Meeting** (`meetings/YYYY/YYYY-MM-DD-slug.md`, template `templates/meeting-note.md`)

```yaml
---
type: meeting
title: UX sync
date: 2026-10-20
product: listings-optimizer
attendees: [Ana Souza, Marco Lima]
people: [ana-souza, marco-lima]
topics: [bulk-edit, ux]
share: private          # meetings default to private
source_file: inbox/processed/2026-10-20-ux-sync.vtt
tags: [ux]
---
```

**Decision** (`decisions/YYYY-MM-DD-slug.md`, template `templates/decision.md`)

```yaml
---
type: decision
title: Ship bulk edit behind a feature flag
date: 2026-10-20
product: listings-optimizer
status: accepted        # proposed | accepted | superseded
decided_by: Ana Souza
source: meetings/2026/2026-10-20-ux-sync.md
topics: [bulk-edit]
people: [ana-souza]
share: team             # decisions default to team
supersedes:             # older decision this one replaces, e.g. 2026-09-01-internal-only.md
superseded_by:          # set on the OLD decision when a newer one replaces it
valid_from: 2026-10-20
---
```

**Stakeholder** (`stakeholders/firstname-lastname.md`, template `templates/stakeholder.md`)

```yaml
---
type: stakeholder
name: Ana Souza
role: Engineering Manager
team: Catalog Platform
products: [listings-optimizer]
people: [ana-souza]
share: private          # stakeholder notes are always private
updated: 2026-10-20
---
```

**Status** (`status/YYYY-Www.md`, template `templates/weekly-status.md`)

```yaml
---
type: status
week: 2026-W43
period: 2026-10-19 to 2026-10-25
product: listings-optimizer
sources: [meetings/2026/2026-10-20-ux-sync.md]
---
```

**Story draft** (`backlog/drafts/YYYY-MM-DD-slug.md`, template `templates/user-story.md`)

```yaml
---
type: story-draft
title: Bulk edit listing titles
date: 2026-10-21
product: listings-optimizer
status: draft           # draft | approved | created-in-jira
jira:                   # issue key once created, e.g. ABC-123
source: decisions/2026-10-20-bulk-edit-flag.md
---
```

## 8. Front matter v2 (D24)

v2 adds these fields to any note, where relevant. v1 notes without them stay valid: missing fields use the defaults.

| Field | Values | Default when missing | Used by |
|-------|--------|----------------------|---------|
| `topics` | list of kebab-case topics, e.g. `[bulk-edit, llm-evaluation]` | none | topic hubs, `/ask`, `/publish` |
| `people` | list of person slugs (`firstname-lastname`) mentioned | none | `/ask` filters |
| `status` | `active` · `superseded` · `stale` · `done` | `active` | `/sweep`, `/ask` |
| `supersedes` / `superseded_by` | path relative to the note's folder | empty | decision history |
| `valid_from` | `YYYY-MM-DD`, the date the fact became true | the note's `date` | "what did we believe in August?" |
| `share` | `team` · `private` | `team` for decisions; `private` for meetings, stakeholders, research and raw notes | `/publish` |

Rules:

- **Topics are reused, not invented.** Before adding a topic, look at the existing ones (`ls brain/products/<slug>/topics/`)
  and reuse one that means the same thing (`llm-evaluation`, not a new `llm-evals`). One to four topics per note.
- **Decisions keep their own status words.** A decision's `status` is `proposed`, `accepted` or `superseded`;
  `accepted` and `proposed` count as active. Other notes use `active`, `superseded`, `stale` or `done`.
- **Superseding never deletes.** The old note gets `status: superseded` and `superseded_by: <new note>`; the new note
  gets `supersedes: <old note>`. Both stay in the brain so history can be explained.
- **`stale`** means "older than 60 days and nothing links to it or from it". It is a flag for review, not a verdict.
- `people` uses slugs so search works; `attendees` and `decided_by` keep display names.

## 9. Derived pages: topic hubs and product index (D27)

Derived pages are summaries **built from** other notes. Agents may rewrite them freely (no approval) because they
hold no original facts: every line links to the note it came from. Never put a fact only in a derived page.

**Topic hub** — `products/<slug>/topics/<topic>.md`, template `templates/topic-hub.md`, `type: topic-hub`.
One per topic that appears in at least one note. Sections: **State** (one paragraph), **Active decisions**,
**Open questions**, **Latest notes** (newest first, max 10, relative links). Superseded decisions are listed under
**History**, not under active decisions.

**Product index** — `products/<slug>/index.md`, template `templates/product-index.md`, `type: product-index`.
Sections: **Current focus**, **Roadmap** (link), **Latest decisions** (10 newest active ones), **Topics** (links to
hubs), **Key people** (links to stakeholder files).

`/ingest` and `/decision` update the index and the hubs they touch; `/sweep` rebuilds all of them from scratch.

## 10. Brain versioning (D26)

`brain/` is a separate git repository, created by `/onboard` (`git init` inside `brain/`). It is still ignored by the
shared pm-agents repo (`/brain/` in `.gitignore`), so nothing personal reaches GitLab.

Every skill that writes to the brain ends with **one** commit:

```bash
git -C brain add -A && git -C brain commit -m "<skill>: <short what>"
```

Examples: `ingest: 2 meetings (2026-10-16, 2026-10-17)`, `decision: raise batch cap to 250`,
`sweep: 2026-W43`. If git is missing or the commit fails, warn once in the summary ("Brain not versioned: git not
available") and carry on. Nothing to commit is not an error. Never push automatically; a PM may add a private remote
for backup by hand. To see history: `git -C brain log --oneline`.

## 11. Private content (D22)

Two ways to keep something out of anything shared (digests, product cards, `/connect-dots` reports):

- **Whole note:** `share: private` in the front matter (the default for meetings, stakeholders and research).
- **Part of a note:** wrap it in a private block. Everything between the markers is never published, even when the
  note itself is `share: team`.

```markdown
<!-- private -->
Marco is unhappy with the API team's timelines; talk to him 1:1 first.
<!-- /private -->
```

Markers go on their own lines. Blocks don't nest. If a closing marker is missing, treat the rest of the note as
private. Anything from `stakeholders/`, raw transcript quotes and `interpretation` claims about people are never
published, with or without markers.
