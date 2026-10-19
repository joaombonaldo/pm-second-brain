---
name: ask
description: Answer questions about the PM's product, people, decisions, meetings and plans using only what is in the second brain, with citations; for team questions, also search the team hub. Use when the user types /ask, or asks "what did we decide about…", "who owns…", "when did…", "what do we know about…", "what did we believe in August…", "remind me…", "what is the team doing on…". Read-only.
metadata:
  category: brain
  role: Brain Keeper
  owner: pm-agents core
  version: "0.2.0"
  status: stable
  brain: required
  reads: "brain/, <team_hub.path>/digests/, <team_hub.path>/products/, jira, confluence"
  writes: ""
  preferences: ""
  requires: "python3, team-hub, jira-mcp, confluence-mcp"
---

# /ask — Brain Keeper

## Purpose

Answer from the brain (and, for team questions, the team hub), with sources, and be honest about gaps. Show the
current truth first; explain history when it helps. This skill is **read-only**.

## Before you start

Read `brain/brain.yaml`. If it does not exist, stop and say: "Your second brain isn't set up yet. Type **/onboard**
first."

## Inputs

- The user's question.
- Optional: "also check Jira/Confluence" — only then use the Jira/Confluence MCP tools, read-only.
- Optional: "include old decisions" / "what did we believe in <month>" → include superseded notes.

## Steps

1. **Pick the scope.** Named product → `--product <slug>`; otherwise all of `brain/`. Team question ("what is the
   team doing…", "does anyone else…", `--team`) → also the hub (step 4).
2. **Search with the script first** (D28). Run 2–3 searches with different key words and filters, e.g.:

   ```bash
   python3 scripts/brain_search.py "batch limit bulk edit" --product acme-listings-optimizer
   python3 scripts/brain_search.py "batch cap" --type decision
   python3 scripts/brain_search.py --person marco-lima --since 2026-10-01
   python3 scripts/brain_search.py --topic bulk-edit --limit 20
   python3 scripts/brain_search.py "rollout" --type decision --status all      # include superseded
   python3 scripts/brain_search.py "rollout" --until 2026-08-31 --status all   # "what did we believe in August?"
   ```

   Superseded notes are hidden by default. Use `--status all` only when the user asks about the past, about
   history, or when a current decision has `supersedes:`. If the script fails, say so in one line and fall back to
   grep. Before saying "not in the brain", also try synonyms and `grep -ri`.
3. **Read the hits.** Open the top files and read the relevant sections; never answer from the result line alone.
   Prefer, in order: `decisions/`, `product/`, `roadmap/`, `topics/` and `index.md` (for orientation; check the
   linked notes for facts), then `meetings/` (newest first), `status/`, `stakeholders/`, `backlog/drafts/`.
4. **Team questions: search the hub too** (only if `team_hub.path` in `brain.yaml` is set and exists):

   ```bash
   python3 scripts/brain_search.py "title scorer" --root ../pm-team-hub
   python3 scripts/brain_search.py --root ../pm-team-hub --type digest --since 2026-10-12
   python3 scripts/brain_search.py --root ../pm-team-hub --type product-card --topic llm-evaluation
   ```

   If `team_hub.path` is empty, say: "Team hub isn't set up. Run /onboard to connect it." and answer from the brain.
5. **History and conflicts.** If a hit has `superseded_by:`, read the newer note and give that as the answer. If the
   current decision has `supersedes:`, follow the chain back and explain briefly: "Until 2026-10-06 the plan was X
   (decisions/…); it changed to Y because …". If two active sources disagree, show both with dates and say which is
   newer (suggest `/sweep` to resolve it).
6. **Optional live check.** Only if the user asked: query Jira/Confluence read-only and cite `jira: KEY-123` or the
   page title. If the MCP tool is missing, say so in one line.
7. **Answer.**
   - Lead with the direct answer in 1–3 sentences (the current, non-superseded truth).
   - Then supporting bullets, each with its citation: `(2026-10-06, products/<slug>/decisions/2026-10-06-batch-cap-100.md)`.
   - Label claim types when it matters: "decided", "Marco's view (interpretation)", "hypothesis, not yet tested".
   - Team answers: a separate **From the team hub** section citing hub files (`hub: digests/2026/2026-W43/ana-souza.md`).
     Keep brain citations under **From your brain**. Never put private brain content (meetings, stakeholders,
     `share: private`, private blocks) into a sentence framed as "what the team is doing".
8. **When the brain doesn't know**, say exactly: **"That's not in the brain."** Then suggest what would fill the gap,
   e.g. "If this came up in last Tuesday's sync, drop that transcript in `brain/inbox/` and run `/ingest`."

## Reads

Everything under `brain/` (via `scripts/brain_search.py` first). The hub at `team_hub.path` for team questions.
Optionally Jira/Confluence via MCP (read-only, only on request).

## Writes

Nothing. Do not create, edit or move any file. Do not write to Jira, Confluence or the hub.

## Rules

- Answer only from sources you actually read in this session. No background knowledge, no guessing.
- Never present a superseded decision as current. Mention it only as history, labelled with its date.
- Never upgrade a claim: an interpretation stays an interpretation, a proposal is not a decision.
- Never invent numbers, dates, names or Jira keys.
- Hub content is what colleagues chose to share; cite it as theirs, separately from the brain.
- If the user asks you to save something, suggest `/ingest` or `/decision`.

## Output

The answer with citations, then:

```
What changed: nothing (read-only)
What needs you: <follow-up question, or "nothing">
What was missing: <gaps found, and what to ingest to fill them, or "nothing">
```
