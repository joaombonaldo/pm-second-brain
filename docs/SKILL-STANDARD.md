# Skill standard (v0.3) — the brain contract and marketplace metadata

Every skill in `.agents/skills/` follows this file, so it works on **any** PM's product unchanged and the team can
browse and trust it. Browse skills in [CATALOG.md](../CATALOG.md); add one with [CONTRIBUTING.md](../CONTRIBUTING.md);
start from [templates/skill/SKILL.md](../templates/skill/SKILL.md).

## 1. The brain contract

A skill never assumes a product, a person or a file layout beyond what is listed here. It uses only these entry
points.

### 1.1 Entry points a skill may use

| Entry point | What it gives | How to use it |
|-------------|---------------|---------------|
| `brain/brain.yaml` | `owner.name`, `owner.role` (`pm` · `manager`), `products[]` (`name`, `slug`, `jira_keys`, `confluence_spaces`, `release_notes_persona`), `stakeholders[]`, `team_hub.path`, `team_hub.person_slug`, `defaults.timezone`, `defaults.week_starts_on` | Read it first. Pick the product from `products[]`: one → use it; several → ask. Never hard-code a slug, key or name. |
| `brain/preferences/<file>` > `templates/<file>` | The PM's personal template, persona or style, else the team default | Resolve every template and persona in this order. Also honour free-text lines in `brain/preferences/README.md`. List the files you honour in `metadata.preferences`. |
| `brain/products/<slug>/…` and `brain/stakeholders/` | Notes, laid out as in [CONVENTIONS.md](../CONVENTIONS.md) §3 | Read and write only the folders you declare in `metadata.reads` / `metadata.writes`. |
| `python3 scripts/brain_search.py` | Front matter filters + keyword ranking (`--type --topic --person --product --since --until --status --share --root --json`) | First retrieval step; then read the files it finds. If it fails, say so in one line and fall back to `grep`. |
| `team_hub.path` | Local clone of `pm-team-hub` (relative to the pm-agents folder) | Empty or missing = team features off: say so and point to `/onboard`. Never copy brain content to the hub except through `/publish`. |
| Jira / Confluence / GitLab MCP | Live data | Optional. If a tool is missing or fails, say so in one line and use the manual fallback (pasted text, CSV). Never fake a result. |

### 1.2 Rules every skill follows

These restate the brain rules in [AGENTS.md](../AGENTS.md); a skill may be stricter, never looser.

1. **Cite sources** for every product fact: brain path + date, `jira: KEY-123`, or a Confluence page title.
2. **Use claim types** (`observation`, `interpretation`, `hypothesis`, `assumption`, `decision`) for durable
   statements. Never upgrade a claim. Never invent names, dates, numbers or metrics: say "That's not in the brain."
3. **Approval before durable writes** (`product/`, `roadmap/`, `decisions/`, `hypotheses/`, `brain.yaml`,
   `preferences/`): show the diff, apply after a yes. Never delete or overwrite a brain file without a yes.
4. **Never write to Jira or Confluence without an explicit yes** to the exact preview. Never post to Teams, email or
   chat.
5. **Brain commit after writes:** `git -C brain add -A && git -C brain commit -m "<skill>: <short what>"`. Warn once
   if git fails; never push the brain.
6. **End with the 3-line summary** (`What changed` / `What needs you` / `What was missing`).
7. **No brain?** If `brain/brain.yaml` is missing, still say something useful: what the skill does, and
   "Type **/onboard** to set up your brain (about 5 minutes)." Only skills marked `brain: none` skip this.
8. **Personal style lives in preferences**, not in the skill. A skill never contains one person's tone, template or
   Dell data.

## 2. Marketplace metadata

`name` and `description` stay the **first two keys** (Devin CLI reads them to list and pick skills). Marketplace
fields go **inside `metadata:`**, the map the [Agent Skills spec](https://agentskills.io/specification) reserves for
client-specific properties. Values are strings (spec: string → string); lists are comma-separated strings.

```yaml
---
name: weekly-status                     # kebab-case, = folder name, unique, ≤ 64 chars
description: Draft the PM's weekly status ... Use when the user types /weekly-status, or says "...".   # ≤ 1024 chars
metadata:
  category: reporting                   # brain | backlog | release | reporting | team | comms | research | other
  role: Reporter                        # Brain Keeper | Backlog Writer | Release Manager | Reporter | Connector | other
  owner: pm-agents core                 # person or team who maintains it
  version: "0.2.0"                      # semver, quoted
  status: stable                        # experimental | stable | deprecated
  brain: required                       # required | optional | none
  reads: "brain/brain.yaml, brain/products/<slug>/meetings/"
  writes: "brain/products/<slug>/status/"          # "" = read-only
  preferences: "README.md, weekly-status.md"       # files in brain/preferences/ it honours; "" = none
  requires: "jira-mcp, git"             # jira-mcp | confluence-mcp | gitlab-mcp | team-hub | python3 | git; "" = none
---
```

Notes:

- **`requires`** lists what the skill uses. MCP entries are always optional at run time (the skill falls back to
  pasted text); `team-hub` is required only by skills that stop without it (see the skill's "Before you start").
- **`brain`**: `required` = stops and points to `/onboard` when the brain is missing; `optional` = works without it
  (e.g. `/onboard` creates it); `none` = never touches `brain/`.
- **Unknown keys.** The spec defines `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`;
  Devin CLI adds its own top-level keys (`argument-hint`, `model`, `subagent`, `agent`, `permissions`, `triggers`).
  We put our fields under `metadata` so they cannot collide with those. Neither source says that unknown keys are
  ignored. **To verify (Q1-style) on a Dell laptop:** after adding metadata, `/` completion in Devin CLI still lists
  every skill with its description, and a skill still triggers from plain words.
- `scripts/validate.py` checks these fields; `scripts/catalog.py` turns them into [CATALOG.md](../CATALOG.md).

## 3. Skill body skeleton

Sections, in order: **Purpose** · **Inputs** · **Before you start** (load `brain.yaml` + preferences; brain check;
team hub check if needed) · **Steps** · **Reads** · **Writes** · **Rules** · **Output** (ending with the 3-line
summary). Keep a skill under ~150 lines. The template: [templates/skill/SKILL.md](../templates/skill/SKILL.md).

## 4. Status and versions

- New skills start **experimental**. Promotion to **stable**: its eval file passes, and ≥ 3 successful real uses by
  ≥ 2 PMs are noted in the merge request.
- **deprecated**: kept for one minor release with a pointer to the replacement in its description, then removed.
- Semver: **patch** = wording or bug fix, same behaviour; **minor** = new step, input or output, backward
  compatible; **major** = changed trigger, removed behaviour, or new writes/approvals.
