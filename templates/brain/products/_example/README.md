# Product folder — what goes where

`/onboard` creates one folder per product at `brain/products/<slug>/`. This `_example` folder is only a reference;
it is not a real product.

| Folder | What goes in it | Who writes | Approval |
|--------|-----------------|------------|----------|
| `product/` | Durable product pages: `overview.md`, users, metrics, glossary | /onboard, /ingest (proposed) | Yes — diff first |
| `roadmap/` | Roadmap notes, themes, timing | You, /ingest (proposed) | Yes — diff first |
| `decisions/` | One decision record per file, `YYYY-MM-DD-slug.md` | /ingest (proposed) | Yes — diff first |
| `hypotheses/` | Hypotheses being tested and their results | You, /ingest (proposed) | Yes — diff first |
| `research/` | Interview notes, research summaries | You, /ingest | No |
| `meetings/YYYY/` | One note per meeting, `YYYY-MM-DD-slug.md` | /ingest | No |
| `backlog/drafts/` | User story drafts | /user-story | No (Jira writes always confirmed) |
| `releases/` | Release notes pages, `<version>.html` | /release-notes | No |
| `status/` | Weekly statuses, `YYYY-Www.md` | /weekly-status | No |
| `sweeps/` | Weekly upkeep reports | /sweep (not built yet) | No |

Shared across all products (one level up, in `brain/`): `stakeholders/`, `preferences/`, `inbox/`.

Naming, front matter and claim types: see `CONVENTIONS.md` at the root of pm-agents.
