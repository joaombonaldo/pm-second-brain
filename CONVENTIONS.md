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
    ├── product/               # durable product pages (overview, users, metrics)   [approval]
    ├── roadmap/               # roadmap notes                                      [approval]
    ├── decisions/             # one decision record per file                      [approval]
    ├── hypotheses/            # hypotheses being tested                            [approval]
    ├── research/              # interviews, research notes
    ├── meetings/YYYY/         # one note per meeting
    ├── backlog/drafts/        # user story drafts
    ├── releases/              # release notes (HTML)
    ├── status/                # weekly statuses
    └── sweeps/                # weekly upkeep reports (once /sweep exists)
```

## 4. Approval rules (D13)

| Where | Rule |
|-------|------|
| `inbox/`, `meetings/`, `backlog/drafts/`, `status/`, `releases/`, `research/` | Agent writes freely. |
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

All notes start with YAML front matter. Unknown values: leave empty, never invent.

**Meeting** (`meetings/YYYY/YYYY-MM-DD-slug.md`, template `templates/meeting-note.md`)

```yaml
---
type: meeting
title: UX sync
date: 2026-10-20
product: listings-optimizer
attendees: [Ana Souza, Marco Lima]
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
supersedes:             # path to older decision, if any
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
