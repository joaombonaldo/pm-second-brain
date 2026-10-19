---
name: sweep
description: Weekly "dreaming" pass that tidies the second brain - merges duplicate notes, marks contradicted decisions as superseded, flags stale notes, promotes repeated observations to product pages, rebuilds topic hubs and the product index, and writes a sweep report. Use when the user types /sweep, says "tidy my brain", "clean up the brain", "weekly upkeep", or on Fridays before /publish.
metadata:
  category: brain
  role: Brain Keeper
  owner: pm-agents core
  version: "0.2.0"
  status: experimental
  brain: required
  reads: "brain/brain.yaml, brain/products/<slug>/, brain/stakeholders/, brain/products/<slug>/sweeps/"
  writes: "brain/products/<slug>/meetings/, brain/products/<slug>/decisions/, brain/products/<slug>/product/, brain/products/<slug>/topics/, brain/products/<slug>/index.md, brain/products/<slug>/sweeps/"
  preferences: ""
  requires: "python3, git"
---

# /sweep — Brain Keeper

## Purpose

Keep the brain trustworthy as it grows (D25). Find problems, propose fixes as **one** diff, apply after a yes, and
leave a report. Never delete anything: superseded and stale notes stay for history.

## Before you start

Read `brain/brain.yaml`. If it does not exist, stop and say: "Your second brain isn't set up yet. Type **/onboard**
first." Pick the product (ask if several; "all" runs one sweep per product). Today's ISO week = `YYYY-Www`.

## Inputs

- Product (or "all"). Optional: "only duplicates", "only contradictions" to run a single step.
- The previous report in `products/<slug>/sweeps/` (to skip items the user already said no to).

## Steps

Collect findings in steps 1–4 **without editing anything**. Use `scripts/brain_search.py` to find candidates, then
read the files before deciding.

1. **Duplicates.** List notes by date and type:
   `python3 scripts/brain_search.py --product <slug> --type meeting --limit 200`. Candidates: same `type` and same
   `date` with similar titles or slugs (e.g. `…-sync.md` and `…-sync-2.md`), or two notes whose summaries cover
   the same meeting. Read both. Proposal: keep the older/fuller one as the main note, copy into it any facts,
   action items or decisions only the other has (with its source), and mark the other `status: superseded`,
   `superseded_by: <main note>`. Re-point links to the main note where it's simple.
2. **Contradictions.** List active decisions per topic:
   `python3 scripts/brain_search.py --product <slug> --type decision --status active --limit 200`, then for each
   topic `--topic <t> --type decision`. Two active decisions conflict when both cannot be true (e.g. "no CSV
   upload" vs "add CSV upload in 2.5"). Also check product pages against newer decisions or observations.
   Proposal: older one `status: superseded` + `superseded_by:`, newer one `supersedes:`, plus a "Replaced by" line
   in the older one. If it's unclear which is right, don't guess: list it under **Needs you** in the report.
3. **Stale notes.** `python3 scripts/brain_search.py --product <slug> --until <today minus 60 days> --limit 200`.
   For each hit, check links: `grep -rl "<file name>" brain/` (anything linking to it) and whether it contains a
   relative link. No links either way → propose `status: stale`. Skip `product/`, `stakeholders/`, decisions and
   notes already `superseded`/`done`.
4. **Repeated observations.** Search the main themes of `[observation]` lines (e.g.
   `python3 scripts/brain_search.py "listings at a time" --product <slug>`). The same observation in **≥ 3 notes**
   (different dates or sources) that isn't in `product/` yet → propose adding one line to the right product page
   (usually `product/users.md` or `product/overview.md`) as `[observation]` with date and all sources.
5. **One diff, one yes.** Show every proposed edit to existing notes as one numbered diff, grouped by step:

   ```
   Duplicates (1)   1. meetings/2026/2026-10-06-bulk-edit-sync-2.md → superseded by …-sync.md (+1 action item moved)
   Contradictions (1) 2. decisions/2026-09-02-no-csv-upload.md → superseded by 2026-10-14-csv-upload-in-2-5.md
   Stale (1)        3. research/2026-07-10-competitor-notes.md → status: stale
   Promote (1)      4. product/users.md += [observation] Sellers edit 20–80 listings at a time (3 sources)
   <unified diff for each>
   Apply? yes (all) / no (none) / numbers, e.g. 1,2,4
   ```

   Apply exactly what the user picked. Nothing changes before the answer.
6. **Rebuild derived pages** (free write, after step 5). For every topic used in any active note, rewrite
   `products/<slug>/topics/<topic>.md` from `templates/topic-hub.md`: state paragraph, active decisions,
   open questions (from meeting notes, unanswered), latest 10 notes, History (superseded decisions). Rewrite
   `products/<slug>/index.md` from `templates/product-index.md`. Every line links to its source note.
7. **Write the report** (free write) to `products/<slug>/sweeps/YYYY-Www.md` with front matter
   `type: sweep`, `product`, `week`, `date`, `share: private`. Sections: **Applied** (with file links), **Declined**
   (so next sweep doesn't re-propose them), **Needs you** (unclear contradictions), **Derived pages rebuilt**,
   **Numbers** (notes scanned, findings per step).
8. **Save (D26).** `git -C brain add -A && git -C brain commit -m "sweep: YYYY-Www"`. If git is missing or fails,
   warn once and carry on.
9. Suggest next: "Ready to share your week? Type `/publish`." (only if `team_hub.path` is set).

## Reads

`brain/brain.yaml`, all notes of the product and `brain/stakeholders/` (via `scripts/brain_search.py` first, then
the files), previous `sweeps/` reports, `templates/topic-hub.md`, `templates/product-index.md`.

## Writes

- After the single yes: status/link fields and merged content in existing notes; added lines in `product/`.
- Freely: `topics/*.md`, `index.md`, `sweeps/YYYY-Www.md`, the brain commit.

## Rules

- **Never delete** a note or a line of original content. Merge = copy into the main note + mark the other superseded.
- One approval for all edits to existing notes; derived pages and the report need none.
- Never mark something superseded on a guess; unclear cases go to **Needs you**.
- Never invent facts while merging or promoting; every promoted line lists all its sources.
- Don't re-propose items listed under **Declined** in the last report unless the notes changed.
- Read-only for Jira, Confluence and the team hub.

## Output

The numbered findings, the user's choice applied, the report path. Then:

```
What changed: <notes updated; topic hubs and index rebuilt; sweeps/YYYY-Www.md; brain commit>
What needs you: <items under "Needs you", or "nothing">
What was missing: <e.g. "no decisions to compare", "git not available">
```
