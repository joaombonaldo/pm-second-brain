# pm-agents — Handoff & Decisions Log

> Purpose of this file: everything decided so far about this project, why, and what's next — so the work can be
> continued by any person or agent (Claude Code, Devin, another chat) without the original conversation.
>
> Owner: João Miguel Bonaldo Meier (Product Manager 2, Dell Technologies)
> Started: 2026-10-13 · Last updated: 2026-10-19 (v0.2: team layer + memory upgrades — spec in `docs/DESIGN-v0.2.md`)
> Living plan (with diagrams): https://claude.ai/code/artifact/7ab8e89c-86b6-4ce0-ba26-644b5a7c49b7

---

## 1. Goal

Build a **"team of AI agents" that helps a Product Manager run their product**, with a **second brain** (product memory)
at its center. It runs on **Devin** (Dell's approved agent), lives in **one GitLab repo**, and a PM uses it by
**cloning the repo and running it locally**.

Rollout ambition:

1. Pilot on João's own product.
2. Share with João's 5 PM peers.
3. Grow into the shared agents repo for João's whole team (~25 people, mixed roles), where the second brain is one of
   several agents/skill packs.

## 2. Requirements as stated by João

- **Easy to use.** PMs "just clone it locally and use it on their behalf". No heavy setup.
- **Feed it meeting transcripts.** Dell uses Microsoft Teams; unclear how a local agent could connect to Teams.
- **Integrations available at Dell:** Devin has Jira, Confluence and GitLab MCP connections.
- **Bring existing work in.** João already has a **release-notes skill** that knows how he likes release notes, the
  persona he writes for, his HTML template, and can read the sprint's user stories. Skills like this, plus a
  **user-story writer** and others, should live in the same repo.
- **"Literally create a team of AI agents to help me run my product."**
- Ask questions before committing work; document all decisions (this file).

## 3. Decisions

Status: ✅ decided · 🔁 superseded · ⏳ pending validation.

| # | Decision | Why | Status |
|---|----------|-----|--------|
| D1 | The brain is **plain markdown in git**, not Devin Knowledge, not a vector DB. | Portable, diffable, grep-able, survives a tool change; every agent reads markdown. Prior art (PM second brain from the pm-skills author, COG, agamarora/second-brain) converges on this. | ✅ |
| D2 | **Runtime = Devin CLI on the PM's laptop.** | João wants "clone and use locally". Devin CLI reads `AGENTS.md`, skills, subagents and MCP config from the repo, so cloning is the install. | ✅ |
| D3 | ~~Two repos: `pm-brain-core` (skills, indexed by Devin web org-wide) + one `brain-<product>` content repo per PM.~~ | Designed for the Devin web app, where org-indexed skills would collide if copied into many repos. Dropped once the runtime became local CLI. | 🔁 by D4 |
| D4 | **One repo, `pm-agents`.** Shared skills/agents/templates are committed; each PM's knowledge lives in a **git-ignored `brain/` folder** inside the clone. | Simplest possible onboarding (one clone), updates via `git pull`, personal data never reaches the shared repo. A PM may make `brain/` its own git repo and push it to a private personal GitLab project as backup. | ✅ |
| D5 | Skills live in **`.agents/skills/<name>/SKILL.md`** (open Agent Skills standard). | Read by Devin CLI *and* the Devin web app, and by other agents (Claude Code, Cursor, etc.). Chosen by João on 2026-10-13. | ✅ |
| D6 | **Shared procedure, personal style.** A skill holds the team-default steps; each PM's persona, tone and templates live in `brain/preferences/` and override `templates/`. | This is how João's personal release-notes skill becomes reusable for 25 people without losing his style. | ✅ |
| D7 | **Four agent roles**, routed by `AGENTS.md`: Brain Keeper, Backlog Writer, Release Manager, Reporter. | Matches a PM's week: remember → write backlog → ship → report. One entry point; the router picks the role. | 🔁 v0.2 adds a fifth role, **Connector** (`/team-status`, `/connect-dots`); `/publish` joins Reporter (D18–D23) |
| D8 | **MVP = skills only; no custom subagents yet.** Subagent profiles (`.devin/agents/<name>/AGENT.md`) come later, only where isolation pays (e.g. digesting a 1-hour transcript, a read-only Reporter). | Custom subagents are experimental in Devin CLI and cost extra credits. Chosen by João: "MVP only". | ✅ |
| D9 | **MVP skills (6):** `onboard`, `ingest`, `ask`, `user-story`, `release-notes`, `weekly-status`. Next: `decision`, `sweep` (pilot week 2), then `refine`, `sprint-summary`, `exec-update`, `meeting-prep`, `prd`, `roadmap-review`, `publish`. | Smallest set that covers capture, recall, backlog, shipping and reporting. A new skill is added after the same manual request has been typed three times. | 🔁 v0.2 built `decision`, `sweep`, `publish`, `team-status`, `connect-dots` (11 skills); remaining later: `refine`, `sprint-summary`, `exec-update`, `meeting-prep`, `prd`, `roadmap-review` |
| D10 | **release-notes ships as a generic team version.** João merges his real skill + HTML template later (his template goes to `brain/preferences/release-notes.html`). | João chose "build a generic version" on 2026-10-13. | ✅ |
| D11 | **Transcripts: manual drop first.** Teams Recap → download `.vtt`/`.docx` → save to `brain/inbox/` → `/ingest`. Optional: point `brain/inbox/` at a OneDrive-synced folder. Automation (Power Automate + Microsoft Graph, or an IT-approved Microsoft 365 MCP server) is a Phase 5 item with Dell IT. | Teams has no setting to auto-save transcripts to OneDrive; the Power Automate transcript trigger is reported unreliable and transcripts can be organizer-only; Graph/MCP needs Entra app registration + admin consent. Agents never post to Teams — they produce text to paste. | ✅ |
| D12 | **Claim types** on every durable statement: `observation`, `interpretation`, `hypothesis`, `assumption`, `decision` + date + source. | A stakeholder's opinion must not become a "fact" by accident. Borrowed from the open-source PM second brain. | ✅ |
| D13 | **Human approval for durable writes.** Agents write freely to `brain/inbox/` and drafts; changes to `product/`, `roadmap/`, `decisions/` are shown as a diff and applied after a yes. **Any Jira/Confluence write is always confirmed first.** | Trust: a hallucinated decision or Jira change is worse than none. | ✅ |
| D14 | **Multiple products per PM:** `brain/products/<slug>/…`; `stakeholders/`, `preferences/`, `inbox/` are shared across products. `/onboard` can be re-run to add a product. | João's original ask mentioned "a product (or products)". | ✅ |
| D15 | **No scheduler on a laptop:** weekly upkeep is a command the PM runs (Friday `/sweep`, once it exists). | Devin CLI has no built-in schedule; Devin web Automations could do it later if wanted. | ✅ |
| D16 | Delivery of the first build: **zip with git history**; João pushes it to Dell GitLab himself. | The build environment cannot reach Dell's GitLab. Chosen by João on 2026-10-13. | ✅ |
| D17 | MCP servers (Jira, Confluence, GitLab) are **placeholders** in `.devin/mcp_config.json`; real endpoints/auth go in `.devin/mcp_config.local.json` (git-ignored) or env vars. `.devin/config.json` holds only permissions. | Exact Dell endpoints and whether they work from the CLI are unknown (see Q1). No secrets in the shared repo. Devin CLI v3000.3+ reads MCP servers from the dedicated `mcp_config*.json` files (https://docs.devin.ai/cli/extensibility/mcp/configuration). | ⏳ |
| D18 | **Roles: `pm` and `manager`, same repo and install.** `owner.role` in `brain.yaml` only changes defaults; no skill is hard-blocked. The manager has his own private brain too. | João (2026-10-19): each PM has a brain; the manager has access to a summary of all of them *and* his own brain. One codebase is easier to maintain. | ✅ |
| D19 | **Team hub = separate GitLab repo `pm-team-hub`** holding only members, product cards, weekly digests and optional connect-dots reports. | Keeps private brains private; gives the manager one place to read; works with plain git. | ✅ |
| D20 | **Hub audience: all PMs + manager.** | Chosen by João; PMs spotting overlaps themselves is a feature. | ✅ |
| D21 | **Digest + product card schemas** with `topics`, `building`, `reusable`, `needs` as the matching signals (see `docs/DESIGN-v0.2.md` §4). | `/connect-dots` needs structured fields to find overlap/reuse/combination reliably. | ✅ |
| D22 | **Privacy rule:** a digest is a summary written from the brain, never a copy: no transcripts/quotes, no people notes or attributed opinions, nothing marked `share: private`. | João: "my manager won't be able to see everything… and I don't want him to", but needs a consultable summary. | ✅ |
| D23 | **Publishing is weekly and PM-approved** (`/publish`, Friday after `/sweep`); exact text previewed; push always asks. | Chosen by João. | ✅ |
| D24 | **Front matter v2:** `topics`, `people`, `status`, `supersedes`/`superseded_by`, `valid_from`, `share`. | Enables grouping, versioning of beliefs, privacy filtering and metadata search. | ✅ |
| D25 | **`/sweep` is the "dreaming" pass:** merge duplicates, mark contradicted notes superseded, flag stale, promote repeated observations, rebuild topic hubs/index; one diff, approved; never deletes. | João asked for dreaming; mirrors agent-memory consolidation, with a human gate for product decisions. | ✅ |
| D26 | **Versioned brain:** `/onboard` runs `git init` in `brain/`; every writing skill ends with a brain commit. | Undo any agent change; answer "what did we believe in August?". | ✅ |
| D27 | **Topic hubs + product index** as derived pages, updated by `/ingest`, rebuilt by `/sweep`. | Grouping across meetings; faster, cheaper `/ask`. | ✅ |
| D28 | **`scripts/brain_search.py`** (stdlib): front-matter filters + keyword ranking; single retrieval entry point for all skills, works on the hub too. | "RAG with metadata" without infra; token-efficient. | ✅ |
| D29 | **Batch `/ingest` with one consolidated approval; new `/decision`** with supersede check. | Fast backfill on day one; decisions logged without a meeting. | ✅ |
| D30 | **Vector search still deferred**, pluggable behind `brain_search.py`. Revisit on eval misses from wording, ~1,000 notes, and Dell guidance on embeddings. | Small brains don't need it; embeddings raise a data-handling question at Dell. | ✅ |

## 4. Open questions

- **Q1 (blocking for Jira-based skills):** Do the Jira, Confluence and GitLab MCP connections work in **Devin CLI on a
  Dell laptop**, or only in the Devin web app? How do people authenticate (SSO, personal token, env var)?
  Fallback: run Jira-heavy skills in the Devin web app (skills in `.agents/skills/` work there too).
- **Q2:** Does Dell already have an approved Microsoft 365 / Teams MCP server or Graph app that could read transcripts?
- **Q3:** Data rules — what product data may live on laptops and in private GitLab projects?
- **Q4:** Which other roles among the ~25 people need their own skill packs (engineering, design, analysts), and who
  co-maintains them?
- **Q5:** Should `brain/` be backed up to a private GitLab project by default?
- ~~**Q6:** Would João's manager value a read-only portfolio view rolling up all PMs' weekly statuses?~~ Answered
  2026-10-19: yes — João wants it, plus cross-PM "connect the dots" (D18–D23).
- **Q8 (team layer):** Who creates and owns the `pm-team-hub` GitLab repo, and does the manager agree to the
  weekly-digest rhythm? Can all PMs get write access to it?
- **Q9:** Are weekly digests themselves subject to Dell data rules (same as Q3), e.g. may they mention customer names?
- **Q7:** Dell's preferred user-story format (fields, acceptance-criteria style, labels) — the MVP uses a generic
  "As a / I want / so that" + Given/When/Then template until João supplies Dell's.

## 5. Research summary (2026-10-13)

**Devin features relevant here**

- `AGENTS.md` — open standard; Devin reads it before working. https://docs.devin.ai/onboard-devin/agents-md
- Skills — `SKILL.md` in `.agents/skills/<name>/` (also `.devin/`, `.claude/`, `.cursor/`…); invoked automatically or
  via `/name` (CLI) / `@skills:name` (web). Devin web indexes skills across all org-connected repos and runs one at a
  time. https://docs.devin.ai/product-guides/skills · https://docs.devin.ai/cli/extensibility/skills/overview
- Devin CLI extensibility — rules, skills, plugins, custom subagents, MCP servers, hooks; project config in
  `.devin/config.json`, MCP servers in `.devin/mcp_config.json`, personal overrides in the `*.local.json` twins
  (git-ignored); also reads `.claude/`,
  `.cursor/` config. https://docs.devin.ai/cli/extensibility · https://docs.devin.ai/cli/extensibility/configuration
- Custom subagents (experimental) — `.devin/agents/<name>/AGENT.md`, own prompt, tools, model, permissions.
  https://docs.devin.ai/cli/subagents
- Devin web: Knowledge (org-level notes with triggers), Playbooks + `!macros`, Scheduled sessions / Automations,
  native Jira/GitLab/Slack/Teams, MCP Marketplace (Confluence, Notion…), API.
  https://docs.devin.ai/integrations

**Prior art**

- Open-source PM second brain (sibling of pm-skills): `knowledge/ hypotheses/ decisions/ interviews/ sweeps/`, claim
  tagging, 17-scenario eval harness.
- COG second brain — markdown + git + skills, PM role pack, framework separated from user content.
  https://github.com/huytieu/COG-second-brain
- agamarora/second-brain — template repo + setup wizard. https://github.com/agamarora/second-brain

**Teams transcripts**

- Not auto-saved as standalone files; downloadable from the meeting Recap; automation via Power Automate + Graph is
  possible but fragile. https://techcommunity.microsoft.com/discussions/microsoftteams/auto-saving-transcription-files-in-a-folder/4499413/replies/4547647

## 6. Rollout plan

| Phase | Dates | Exit criteria |
|-------|-------|---------------|
| 0 · Confirm platform | Oct 14–16, 2026 | Q1 and Q3 answered; GitLab project `pm-agents` created |
| 1 · Build core | Oct 19–30 | MVP skills working on João's real material; evals written |
| 2 · Pilot on João's product | Nov 2–27 | Daily use; add `decision` + `sweep` in week 2; issues logged in GitLab |
| Gate | Nov 27 | ≥3 days/week use for 3 of 4 weeks · weekly status < half of today's time · ≥8/10 evals correct with citations · 0 inbox items older than 7 days at sweep · "would miss it" = yes. Fail → extend 2 weeks. |
| 3 · Harden | Nov 30–Dec 4 | README quick start, 10-min walkthrough, sanitized example brain |
| 4 · Share with PMs | Wave 1 Dec 7–18 (2 PMs) · Wave 2 Jan 11–22, 2027 (3 PMs) | Each PM onboarded in a 30-min pairing; monthly agents sync set |
| 5 · Open to the team | Feb 1–26, 2027 | Role packs (pm / engineering / design), plugins as install path tested, `CONTRIBUTING.md`, transcript automation decided with IT |

## 7. Repo map

v0.1 map superseded. Current structure: `docs/DESIGN-v0.2.md` §3 (team hub) and §9 (skills), `CONVENTIONS.md`
(brain folders), `AGENTS.md` (roles and routing). Quick view:

```
pm-agents/
├── AGENTS.md  README.md  CONVENTIONS.md  CHANGELOG.md
├── .agents/skills/   onboard ingest ask decision sweep · user-story · release-notes · weekly-status publish · team-status connect-dots
├── .devin/           config.json (permissions) · mcp_config.json (MCP placeholders) · README.md
├── templates/        notes, digest, product card, topic hub, product index, release-notes.html, brain/ skeleton, team-hub/ bootstrap
├── scripts/          validate.py · brain_search.py
├── evals/            scenarios.md · scenarios-memory.md · scenarios-team.md · fixtures/
└── docs/             HANDOFF.md (this file) · DESIGN-v0.2.md
```

## 8. How to continue in another environment

1. Clone `pm-agents` (or unzip the delivered archive) and read, in order: this file → `AGENTS.md` →
   `CONVENTIONS.md` → the skill you want to change.
2. Run `python3 scripts/validate.py` before every commit.
3. When you change a decision, update the table in §3 (mark the old row 🔁 and add a new one) and add a line to
   `CHANGELOG.md`.
4. Prompt to paste into any coding agent to pick up the work:

   > You are continuing development of `pm-agents`, a repo of AI-agent skills for Product Managers at Dell, run with
   > Devin CLI. Read `docs/HANDOFF.md` fully first; it holds every decision and open question. Respect decisions
   > marked ✅ unless I tell you otherwise. Ask me before committing. Next task: <describe it>.

5. Immediate next steps after the first build:
   - Answer Q1 (MCP from the CLI) and fill `.devin/mcp_config.local.json` (see `.devin/README.md`).
   - Merge João's real release-notes skill: move his steps into `.agents/skills/release-notes/SKILL.md` where they are
     team-generic, and his HTML template + persona into his `brain/preferences/`.
   - Replace the generic story template with Dell's format (Q7).
   - Run `/onboard` on João's product and ingest 4–6 weeks of transcripts.
