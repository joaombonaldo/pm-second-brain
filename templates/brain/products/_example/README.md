# Product folder — what goes where

`/onboard` creates one folder per product at `brain/products/<slug>/`. This `_example` folder is only a reference;
it is not a real product.

| Folder | What goes in it | Who writes | Approval |
|--------|-----------------|------------|----------|
| `index.md` | Product index: current focus, latest decisions, topics, key people. Start here. | /ingest, /decision, /sweep | No (derived page) |
| `topics/` | One hub per topic: state, active decisions, open questions, latest notes | /ingest, /decision, /sweep | No (derived page) |
| `product/` | Durable product pages: `overview.md`, users, metrics, glossary | /onboard, /ingest (proposed) | Yes — diff first |
| `roadmap/` | Roadmap notes, themes, timing | You, /ingest (proposed) | Yes — diff first |
| `decisions/` | One decision record per file, `YYYY-MM-DD-slug.md` | /ingest, /decision (proposed) | Yes — diff first |
| `hypotheses/` | Hypotheses being tested and their results | You, /ingest (proposed) | Yes — diff first |
| `research/` | Interview notes, research summaries | You, /ingest | No |
| `meetings/YYYY/` | One note per meeting, `YYYY-MM-DD-slug.md` | /ingest | No |
| `backlog/drafts/` | User story drafts | /user-story | No (Jira writes always confirmed) |
| `releases/` | Release notes pages, `<version>.html` | /release-notes | No |
| `status/` | Weekly statuses, `YYYY-Www.md` | /weekly-status | No |
| `sweeps/` | Weekly upkeep reports, `YYYY-Www.md` | /sweep | No (edits to other notes: yes first) |

Shared across all products (one level up, in `brain/`): `stakeholders/`, `preferences/`, `inbox/`.

Derived pages (`index.md`, `topics/`) only summarise and link; the facts live in the notes they link to.
Old decisions are never deleted: they get `status: superseded` and a link to what replaced them.

Naming, front matter and claim types: see `CONVENTIONS.md` at the root of pm-agents.
