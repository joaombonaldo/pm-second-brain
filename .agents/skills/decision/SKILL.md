---
name: decision
description: Log a product decision straight from the chat in one step, check whether it replaces an older decision, and offer to mark the old one as superseded. Use when the user types /decision, or says "log a decision", "we decided…", "record that we chose…", "Ana decided today that…", "note this decision".
metadata:
  category: brain
  role: Brain Keeper
  owner: pm-agents core
  version: "0.2.0"
  status: experimental
  brain: required
  reads: "brain/brain.yaml, brain/preferences/, brain/products/<slug>/decisions/, brain/products/<slug>/topics/, brain/products/<slug>/index.md"
  writes: "brain/products/<slug>/decisions/, brain/products/<slug>/topics/, brain/products/<slug>/index.md"
  preferences: "decision.md"
  requires: "python3, git"
---

# /decision — Brain Keeper

## Purpose

Capture a decision while it is fresh, as a proper decision record with claim type, who decided, date and source,
without making the PM fill in a form. Keep history honest: an older conflicting decision is marked `superseded`,
never deleted (D29).

## Before you start

Read `brain/brain.yaml`. If it does not exist, stop and say: "Your second brain isn't set up yet. Type **/onboard**
first." Load the template: `brain/preferences/decision.md` if it exists, else `templates/decision.md`.

## Inputs

- The decision as the user says it, in chat.
- Optional: a pointer to a meeting note or document it came from.

## Steps

1. **Extract the four essentials** from what the user said: **what** was decided, **why**, **who decided**,
   **date** (today if they say "today"). Also note the product (ask only if `brain.yaml` has several and it's
   unclear) and a source (meeting note path, doc, or "stated by user in chat, <today>").
2. **Ask only for what's missing**, all in one short message, e.g. "Who made the call, and roughly why?". Never
   guess who decided. If the user says "nobody decided yet", log it as `status: proposed`.
3. **Look for related and conflicting decisions:**

   ```bash
   python3 scripts/brain_search.py "<2-4 key words>" --type decision --product <slug>
   python3 scripts/brain_search.py --topic <topic> --type decision --product <slug>
   ```

   Read the top hits. A decision **conflicts** if it is still active (`accepted`/`proposed`) and cannot be true at
   the same time as the new one (e.g. "cap at 100" vs "cap at 250"; "open after two weeks" vs "after one week").
   A decision that only adds detail does not conflict; link it under Context instead.
4. **Pick topics** (1–4) from existing ones in `products/<slug>/topics/`; create a new topic only if none fits.
5. **Draft the record** `brain/products/<slug>/decisions/YYYY-MM-DD-<slug>.md` from the template:
   `status: accepted` (or `proposed`), `decided_by`, `source`, `topics`, `people` (slugs), `share: team` (use
   `private` if the user says it's confidential), `valid_from`. Body: **Decision** line with `[decision]` claim,
   **Context** (the why, with sources), **Consequences**, **History** (if superseding).
6. **Draft the supersede change** if step 3 found a conflict: on the old file set `status: superseded` and
   `superseded_by: <new file name>`, and add one line under its Context: "Replaced by [<new title>](<new file>) on
   <date>." On the new file set `supersedes: <old file name>`.
7. **Show everything in one message**: the full new file, then the diff of the old file (if any), and ask:
   "Save this decision? (yes / no)". If there is a conflict also ask: "It replaces <old title> from <date>. Mark that
   one as superseded? (yes / no)". Apply only what the user approves.
8. **Update derived pages** (free write): the touched topic hubs (active decisions; old one moved to History) and
   `products/<slug>/index.md` (latest decisions).
9. **Save (D26).** `git -C brain add -A && git -C brain commit -m "decision: <short title>"`. If git is missing or
   fails, warn once and carry on.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, `templates/decision.md`, `brain/products/<slug>/decisions/`, `topics/`,
`index.md`, the source note if given. Search with `scripts/brain_search.py`.

## Writes

- After a yes: the new `decisions/*.md`; status/link changes on the superseded decision.
- Freely: `topics/*.md`, `index.md`, the brain commit.

## Rules

- `[decision]` only if someone with authority actually decided. If not, `status: proposed` and say so.
- Never invent who decided, the date or the reason. Missing "why" may stay "Not stated" if the user skips it.
- Never delete or rewrite the old decision's content; only change `status`, `superseded_by` and add the
  "Replaced by" line.
- If unsure whether two decisions conflict, ask the user instead of superseding.
- Never write to Jira or Confluence. If the decision needs stories, suggest `/user-story`.

## Output

The saved file path and the decision line; the superseded file (if any). Then:

```
What changed: <new decision file; old decision marked superseded; topic hubs/index updated; brain commit>
What needs you: <approval if still pending, or "nothing">
What was missing: <e.g. "reason not stated", "git not available">
```
