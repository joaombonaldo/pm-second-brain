# Changelog

All notable changes to pm-agents. Decisions referenced (Dx, Qx) are in [docs/HANDOFF.md](docs/HANDOFF.md).

## v0.2.0 — 2026-10-19

Team layer + memory upgrades. Spec: [docs/DESIGN-v0.2.md](docs/DESIGN-v0.2.md) (D18–D30).

**Added**

- **Team layer.** Separate `pm-team-hub` repo (D19, D20) bootstrapped from `templates/team-hub/` (README with the
  privacy rule, `member.md`, empty folders). Weekly digest and product card schemas with `topics`, `building`,
  `reusable`, `needs` (D21): `templates/digest.md`, `templates/product-card.md`.
- New skills: `/publish` (digest + product card, privacy check, exact preview, separate yes to commit and push; D22,
  D23), `/team-status` (portfolio roll-up), `/connect-dots` (overlaps, reuse, combinations, dependencies with
  evidence and confidence), `/decision` (quick decision log with supersede check; D29), `/sweep` ("dreaming" pass;
  D25).
- Fifth role **Connector**; roles of people `pm` / `manager` in `brain.yaml` (D18), defaults only.
- `scripts/brain_search.py`: stdlib front-matter filters + keyword ranking, `--json`, `--selftest`; the first
  retrieval step for `/ask`, `/ingest`, `/decision`, `/sweep`, `/publish`, `/team-status`, `/connect-dots` (D28).
- Front matter v2 (`topics`, `people`, `status`, `supersedes`/`superseded_by`, `valid_from`, `share`) and private
  blocks in `CONVENTIONS.md` (D24); topic hubs and product index as derived pages (D27): `templates/topic-hub.md`,
  `templates/product-index.md`.
- Evals: `evals/scenarios-memory.md`, `evals/scenarios-team.md` with fixtures (`memory/`, `team-hub/`,
  `team-hub-unrelated/`, `team-brain/`).

**Changed**

- `/onboard`: asks PM or manager, optional team hub path + person slug, creates `index.md`, `topics/`, `sweeps/`, and
  runs `git init` in `brain/` (D26).
- `/ingest`: batch mode with one consolidated approval (D29), v2 front matter, topic hub/index updates, supersede
  proposals.
- `/ask`: searches with `brain_search.py`, hides superseded notes unless asked, team questions also search the hub.
- Every skill that writes to the brain ends with a brain commit (D26).
- `AGENTS.md`: five roles, new routes, team hub rules, weekly rhythm. `README.md`: team hub setup, "For managers",
  weekly rhythm, 11-command cheat sheet. `scripts/validate.py`: new required files and skills.

**Known gaps**

- Vector search still deferred (D30). Hub ownership and access (Q8) and data rules for digests (Q9) open.

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
- `.devin/config.json` with conservative permissions; Jira/Confluence/GitLab MCP placeholders in
  `.devin/mcp_config.json`, explained in `.devin/README.md` (D17, Q1 open).
- `.gitignore` keeping the personal `brain/` and local config out of the repo (D4).
- `evals/`: 10 manual scenarios and fictional fixtures (Acme Listings Optimizer).
- `scripts/validate.py`: checks skill front matter, required templates, relative links and `.gitignore`.

**Known gaps**

- Jira/Confluence MCP from Devin CLI unverified (Q1); skills fall back to pasted text/CSV.
- Generic user-story format until Dell's is supplied (Q7).
- João's personal release-notes skill not merged yet (D10).
