---
name: onboard
description: Set up the PM's second brain (the brain/ folder) for the first time, or add another product to an existing brain. Use when the user types /onboard, says "set me up", "get started", "add a product", or when any other skill finds that brain/brain.yaml does not exist.
---

# /onboard — Brain Keeper

## Purpose

Create the PM's personal `brain/` folder from `templates/brain/`, ask a few questions, and fill in the basics so
every other skill works. Re-run it to add another product (D14). It never overwrites existing files.

## Inputs

- The user's answers to up to 6 questions.
- `templates/brain/` (the skeleton), `templates/stakeholder.md`, `templates/persona.md`.

## Steps

1. **Check what exists.**
   - If `brain/brain.yaml` does **not** exist → this is a **first setup**. Go to step 2.
   - If it exists → this is **add a product**. Read `brain/brain.yaml`, tell the user which products already exist,
     and skip to step 3 asking only questions 2–4 and 6 (product, Jira, Confluence, persona) plus
     "Any new stakeholders for this product?".
2. **Create the skeleton (first setup only).** Copy every file and folder in `templates/brain/` into `brain/`.
   Before copying each file, check whether the target already exists; if it does, skip it and note it.
   Make sure these folders exist afterwards: `brain/preferences/`, `brain/inbox/processed/`, `brain/stakeholders/`,
   `brain/products/`. Do not copy `templates/brain/products/_example/` as a real product; copying its README to
   `brain/products/_example/README.md` as a reference is fine.
3. **Ask the questions one at a time.** Wait for each answer before the next. Keep each question to one line with a
   short example. Accept "skip" for any of them.
   1. "What's your name?" (e.g. Ana Souza)
   2. "What's the product called?" (e.g. Listings Optimizer). Propose a slug in kebab-case (e.g.
      `listings-optimizer`) and ask the user to confirm or change it.
   3. "Which Jira project key(s) does it use?" (e.g. LOPT; several allowed; "skip" is fine)
   4. "Which Confluence space(s)?" (e.g. LOPT or a space URL; "skip" is fine)
   5. "Who are your main stakeholders? Name and role, one per line." (e.g. "Marco Lima — Eng Manager")
   6. "Who do you write release notes for? One sentence." (e.g. "Marketplace sellers who manage 50+ listings")
4. **Write `brain/brain.yaml`.**
   - First setup: fill the copied `brain/brain.yaml` with the answers (keep its comments).
   - Add a product: append a new entry under `products:` and show the change as a diff; apply after a yes (D13).
   - If the product slug already exists, stop and ask whether they meant a different product.
5. **Create the product folder** `brain/products/<slug>/` with these subfolders (add a `.gitkeep` in empty ones):
   `product/`, `roadmap/`, `decisions/`, `hypotheses/`, `research/`, `meetings/`, `backlog/drafts/`, `releases/`,
   `status/`, `sweeps/`.
6. **Write `brain/products/<slug>/product/overview.md`** (only if it does not exist):

   ```markdown
   ---
   type: product
   title: <Product name>
   product: <slug>
   updated: <today>
   ---
   # <Product name>

   ## What it is
   <one line if the user said it; otherwise "Not in the brain yet.">

   ## Who it's for
   <persona sentence from question 6>

   ## Links
   - Jira: <keys or "not set">
   - Confluence: <spaces or "not set">

   ## Stakeholders
   - [<Name>](../../../stakeholders/<firstname-lastname>.md) — <role>
   ```
7. **Write stakeholder files.** For each person from question 5, create `brain/stakeholders/<firstname-lastname>.md`
   from `templates/stakeholder.md` if it does not exist. If it exists, append the product slug to `products:` and
   a dated line under "Notes" instead of rewriting.
8. **Persona.** If `brain/preferences/persona.md` does not exist, copy `templates/persona.md` there and replace its
   "Who" line with the answer to question 6. If it exists, leave it alone and mention that it already exists.
9. **Finish** with the summary below and suggest the next step: "Drop a Teams transcript in `brain/inbox/` and type
   `/ingest`."

## Reads

`brain/brain.yaml` (if present), `templates/brain/**`, `templates/stakeholder.md`, `templates/persona.md`.

## Writes

`brain/**` skeleton, `brain/brain.yaml`, `brain/preferences/persona.md`, `brain/stakeholders/*.md`,
`brain/products/<slug>/**` including `product/overview.md`.

## Rules

- **Never overwrite** an existing file. If a file exists, skip it, or append, and say so.
- Ask **at most ~6 questions**, one at a time. Don't ask for things you can derive.
- Don't invent stakeholders, keys or descriptions. Leave unknowns empty or write "Not in the brain yet."
- Do not test Jira/Confluence connections here and do not write anything to Jira/Confluence.
- Write only inside `brain/`. Never edit `templates/`.

## Output

A short welcome message listing what was created, then:

```
What changed: <files/folders created; files skipped because they existed>
What needs you: <e.g. approve brain.yaml diff, or "nothing">
What was missing: <skipped questions, e.g. "no Confluence space">
```
