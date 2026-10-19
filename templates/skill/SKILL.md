---
# Copy this folder to .agents/skills/<your-skill-name>/ and fill it in. Rules: docs/SKILL-STANDARD.md.
# Keep `name` and `description` as the first two keys: Devin CLI reads them to list and pick skills.
name: your-skill-name
# What it does + when to use it, with the user's likely words in quotes. ≤ 1024 chars. Must not reuse
# another skill's trigger phrases (validate.py warns). Unquoted text must not contain ": ".
description: <Verb> <what> from <source> for <who>. Use when the user types /your-skill-name, or says "<phrase 1>", "<phrase 2>".
# Marketplace fields live under `metadata` (Agent Skills spec: string values; lists are comma-separated strings).
metadata:
  category: other            # brain | backlog | release | reporting | team | comms | research | other
  role: other                # Brain Keeper | Backlog Writer | Release Manager | Reporter | Connector | other
  owner: "<your name or team>"
  version: "0.1.0"           # semver; bump per docs/SKILL-STANDARD.md §4
  status: experimental       # new skills start experimental
  brain: required            # required | optional | none
  reads: "brain/brain.yaml, brain/preferences/, brain/products/<slug>/<folder>/"
  writes: "brain/products/<slug>/<folder>/"     # "" if read-only
  preferences: "README.md"   # files in brain/preferences/ you honour, e.g. "README.md, persona.md"; "" = none
  requires: ""               # any of: jira-mcp, confluence-mcp, gitlab-mcp, team-hub, python3, git
---

# /your-skill-name — <Role>

## Purpose

<One or two sentences: the outcome for the PM, and what this skill never does.>

## Inputs

- <What the user gives, e.g. a sprint name, a pasted list, a brain file.>
- <Optional inputs and their defaults.>

## Before you start

1. Read `brain/brain.yaml` and `brain/preferences/README.md`. If `brain/brain.yaml` does not exist, say what this
   skill does in one line, then: "Your second brain isn't set up yet. Type **/onboard** first (about 5 minutes)."
2. Pick the product from `products[]`: one → use it; several → ask.
3. Load templates and persona: `brain/preferences/<file>` if it exists, else `templates/<file>`.
4. <Only if you use the team hub:> read `team_hub.path`; if empty or missing, say team features are off and point to
   `/onboard`.

## Steps

1. **Find sources.** `python3 scripts/brain_search.py "<key words>" --product <slug>`; read the files it finds. If
   the script fails, say so in one line and use `grep`.
2. **<Do the work.>** Cite every fact (brain path + date, `jira: KEY-123`). Tag durable statements with claim types.
   If something is not in the brain, say "That's not in the brain." and suggest what to ingest.
3. **Show before durable writes.** Changes to `product/`, `roadmap/`, `decisions/`, `hypotheses/`, `brain.yaml` or
   `preferences/`: show the diff, apply after a yes.
4. **Jira/Confluence (if any).** Show exactly what will be written; act only after an explicit yes. If the MCP tool
   is missing, give paste-ready text instead.
5. **Save.** `git -C brain add -A && git -C brain commit -m "your-skill-name: <short what>"`. If git fails, warn once.

## Reads

<Same list as `metadata.reads`, in words.>

## Writes

<Same list as `metadata.writes`; say which writes need a yes.>

## Rules

- Never invent names, dates, numbers or metrics.
- Never write to Jira or Confluence without an explicit yes; never post to Teams, email or chat.
- Personal style comes from `brain/preferences/`, never from this file.

## Output

<What the user sees.> Then:

```
What changed: <files written or updated, or "nothing">
What needs you: <approvals, questions, things to paste/send, or "nothing">
What was missing: <gaps in the brain or tools, or "nothing">
```
