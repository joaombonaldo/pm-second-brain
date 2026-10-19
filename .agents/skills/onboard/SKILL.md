---
name: onboard
description: Set up the PM's second brain (the brain/ folder) for the first time, add another product to an existing brain, or connect the brain to the team hub later. Use when the user types /onboard, says "set me up", "get started", "add a product", "connect me to the team hub", or when any other skill finds that brain/brain.yaml does not exist.
---

# /onboard — Brain Keeper

## Purpose

Create the PM's personal `brain/` folder from `templates/brain/`, ask a few questions, fill in the basics so every
other skill works, and start the brain's private version history (D26). Re-run it to add a product (D14) or to set
up the team hub later. It never overwrites existing files.

## Inputs

- The user's answers to up to 7 questions.
- `templates/brain/` (the skeleton), `templates/stakeholder.md`, `templates/persona.md`,
  `templates/product-index.md`, `templates/team-hub/member.md` (for the hub member card).

## Steps

1. **Check what exists.**
   - No `brain/brain.yaml` → **first setup**. Go to step 2.
   - `brain/brain.yaml` exists → read it and say which products exist. Ask: "Add a product, or set up the team hub?"
     - Add a product: ask questions 3–6 only (plus "Any new stakeholders for this product?"), then steps 4–8.
     - Team hub: ask question 7 only, then steps 4 and 9–10.
2. **Create the skeleton (first setup only).** Copy every file and folder in `templates/brain/` into `brain/`.
   Before copying each file, check whether the target exists; if it does, skip it and note it. Make sure these exist
   afterwards: `brain/preferences/`, `brain/inbox/processed/`, `brain/stakeholders/`, `brain/products/`. Copying
   `templates/brain/products/_example/README.md` as a reference is fine; it is not a real product.
3. **Ask the questions one at a time.** Wait for each answer. One line each, with a short example. Accept "skip".
   1. "What's your name?" (e.g. Ana Souza)
   2. "Are you a PM or the team's manager?" (`pm` or `manager`; default `pm`. It only changes suggestions.)
   3. "What's the product called?" (e.g. Listings Optimizer). Propose a kebab-case slug (`listings-optimizer`) and
      ask the user to confirm or change it.
   4. "Which Jira project key(s) and Confluence space(s) does it use?" (e.g. "Jira LOPT, Confluence LOPT"; "skip" is fine)
   5. "Who are your main stakeholders? Name and role, one per line." (e.g. "Marco Lima — Eng Manager")
   6. "Who do you write release notes for? One sentence." (e.g. "Marketplace sellers who manage 50+ listings")
   7. "Optional — team hub: where is your local clone of `pm-team-hub`? (e.g. `../pm-team-hub`). Say skip if you
      don't have it yet; you can do this later with /onboard." Store the path relative to the pm-agents folder (not
      to `brain/`). If given, propose a person slug from question 1
      (`ana-souza`) and ask to confirm.
4. **Write `brain/brain.yaml`.**
   - First setup: fill the copied file with the answers (keep its comments): `owner.name`, `owner.role`, the product
     entry, `stakeholders`, and `team_hub.path` / `team_hub.person_slug` (leave both `""` if skipped = team features off).
   - Re-run (new product or hub): show the change as a diff and apply after a yes (D13).
   - If the product slug already exists, stop and ask whether they meant a different product.
5. **Create the product folder** `brain/products/<slug>/` with these subfolders (`.gitkeep` in empty ones):
   `product/`, `roadmap/`, `decisions/`, `hypotheses/`, `research/`, `meetings/`, `backlog/drafts/`, `releases/`,
   `status/`, `sweeps/`, `topics/`. Write `brain/products/<slug>/index.md` from `templates/product-index.md` with the
   product name, the overview link and the stakeholders; leave other sections as "Not in the brain yet."
6. **Write `brain/products/<slug>/product/overview.md`** (only if it does not exist): front matter `type: product`,
   `title`, `product`, `share: team`, `updated: <today>`; sections **What it is** (one line if the user said it,
   else "Not in the brain yet."), **Who it's for** (question 6), **Links** (Jira/Confluence or "not set"),
   **Stakeholders** (`- [<Name>](../../../stakeholders/<firstname-lastname>.md) — <role>`).
7. **Write stakeholder files.** For each person from question 5, create `brain/stakeholders/<firstname-lastname>.md`
   from `templates/stakeholder.md` (`share: private`) if it does not exist. If it exists, append the product slug to
   `products:` and a dated line under "Notes" instead of rewriting.
8. **Persona.** If `brain/preferences/persona.md` does not exist, copy `templates/persona.md` there and replace its
   "Who" line with the answer to question 6. If it exists, leave it alone and say so.
9. **Team hub check (only if question 7 was answered).**
   - If the path doesn't exist or has no `members/` folder, say: "I can't find the team hub at `<path>`. Clone it
     there, then run /onboard again." Keep the path in `brain.yaml` anyway.
   - If `<path>/members/<person-slug>.md` does not exist, propose creating it from `templates/team-hub/member.md`
     with name, role, product slug(s) and nothing else (no brain content). Show the full file; write it after a yes.
     Tell the user it reaches the team only when they commit and push the hub (or run `/publish`). Never push here.
10. **Start version history (D26).** First setup: run `git -C brain init`, then
    `git -C brain add -A && git -C brain commit -m "onboard: create brain"`. Re-run: commit with
    `onboard: add product <slug>` or `onboard: connect team hub`. If git is missing or fails, warn once
    ("Your brain isn't versioned: git isn't available") and carry on. Never add a remote.
11. **Finish** with the summary below and suggest the next step: "Drop a Teams transcript in `brain/inbox/` and type
    `/ingest`." For a manager, also mention `/team-status` once the hub is set up.

## Reads

`brain/brain.yaml` (if present), `templates/brain/**`, `templates/stakeholder.md`, `templates/persona.md`,
`templates/product-index.md`, `templates/team-hub/member.md`, `<team_hub.path>/members/` (if configured).

## Writes

`brain/**` skeleton, `brain/brain.yaml`, `brain/preferences/persona.md`, `brain/stakeholders/*.md`,
`brain/products/<slug>/**` including `product/overview.md` and `index.md`; `brain/.git` (version history).
After a yes: `<team_hub.path>/members/<person-slug>.md`.

## Rules

- **Never overwrite** an existing file. If a file exists, skip it, or append, and say so.
- Ask **at most 7 questions**, one at a time. Don't ask for things you can derive. Topics are not asked here:
  they appear as you `/ingest`.
- Team hub questions are always skippable: "you can do this later with /onboard".
- Don't invent stakeholders, keys or descriptions. Leave unknowns empty or write "Not in the brain yet."
- Never copy brain content into the hub. The member card holds only name, role, products and focus areas the user
  states.
- Do not test Jira/Confluence connections here and do not write anything to Jira/Confluence.
- Write only inside `brain/` (and the hub member card after a yes). Never edit `templates/`.

## Output

A short welcome message listing what was created, then:

```
What changed: <files/folders created; files skipped because they existed; brain commit made or "not versioned">
What needs you: <e.g. approve brain.yaml diff or hub member card, or "nothing">
What was missing: <skipped questions, e.g. "no Confluence space", "team hub not set up">
```
