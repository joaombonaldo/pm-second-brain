# Changelog

All notable changes to pm-agents. Decisions referenced (Dx, Qx) are in [docs/HANDOFF.md](docs/HANDOFF.md).

## v0.1.0 — 2026-10-13

First build (MVP, D8/D9).

**Added**

- `AGENTS.md` router: the four roles (Brain Keeper, Backlog Writer, Release Manager, Reporter), routing table, brain
  rules, approval rules (D13), preference resolution (D6), multi-product handling (D14).
- Six skills in `.agents/skills/` (D5): `onboard`, `ingest`, `ask`, `user-story`, `release-notes` (generic team
  version, D10), `weekly-status`.
- `README.md` 15-minute quick start, incl. how to download a Teams transcript (D11) and back up `brain/`.
- `CONVENTIONS.md`: claim types (D12), file naming, front matter per note type, links, citations, brain folder map.
- `templates/`: meeting note, decision, stakeholder, user story, weekly status, persona, release-notes HTML, and the
  `templates/brain/` skeleton copied by `/onboard`.
- `.devin/config.json` with conservative permissions and Jira/Confluence/GitLab MCP placeholders (D17, Q1 open).
- `.gitignore` keeping the personal `brain/` and local config out of the repo (D4).
- `evals/`: 10 manual scenarios and fictional fixtures (Acme Listings Optimizer).
- `scripts/validate.py`: checks skill front matter, required templates, relative links and `.gitignore`.

**Known gaps**

- Jira/Confluence MCP from Devin CLI unverified (Q1); skills fall back to pasted text/CSV.
- Generic user-story format until Dell's is supplied (Q7).
- João's personal release-notes skill not merged yet (D10).
