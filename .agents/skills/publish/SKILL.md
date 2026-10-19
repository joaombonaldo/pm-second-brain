---
name: publish
description: Write the PM's weekly digest and product card update from the second brain, run the privacy check, show the exact text, and after an explicit yes commit and push it to the shared team hub (pm-team-hub). Use when the user types /publish, or says "publish my week", "send my digest to the team hub", "update my product card", "share this week with the team". Usually run on Friday after /sweep.
---

# /publish — Reporter

## Purpose

Share a short, reviewed summary of the PM's week with the team, without exposing the private brain. A digest is
written **from** the brain but is **never a copy** of it (privacy rule, `docs/DESIGN-v0.2.md` §5).

## Before you start

1. Read `brain/brain.yaml`. If it does not exist, stop: "Your second brain isn't set up yet. Type **/onboard** first."
2. Read `team_hub.path` and `team_hub.person_slug`. If either is empty, or the folder does not exist, stop and say:
   > Team features are off: no team hub is set up. Clone `pm-team-hub` next to `pm-agents`, then run **/onboard**
   > and give its path (usually `../pm-team-hub`) and your person slug (e.g. `ana-souza`).
3. Load templates: `brain/preferences/digest.md` or `templates/digest.md`; `brain/preferences/product-card.md` or
   `templates/product-card.md`; `templates/team-hub/member.md` (first publish only).

## Inputs

- Week: default = the current ISO week (Monday to today). The user may say "last week" or `2026-W42`.
- Product(s): all products in `brain.yaml` owned by the PM (ask if unsure which ones to publish).
- Optional extra notes from the user ("mention we're hiring a designer").

## Steps

1. **Sync the hub.** Run `git -C <hub> status --porcelain` and `git -C <hub> fetch`. If there are local
   uncommitted changes, stop and explain in one line. If the copy is behind, say "Your hub copy is behind; update it
   with `git pull --rebase`?" and run `git -C <hub> pull --rebase` only after yes.
2. **Check for an existing digest** at `<hub>/digests/<YYYY>/<YYYY-Www>/<person_slug>.md`. If it exists, this is a
   **republish**: you will show a diff against it in step 7 and replace it only after yes. Never write a second
   digest for the same week.
3. **Gather the week's material from the brain.** Prefer the search script:
   `python3 scripts/brain_search.py --root brain --product <slug> --since <monday> --until <sunday> --json --limit 50`
   (superseded notes are excluded by default)
   and, for the product card, `--type decision --limit 5` without the date filter.
   If `scripts/brain_search.py` is missing or fails, list `brain/products/<slug>/{decisions,status,hypotheses,
   product,meetings}/` and keep files whose front matter `date:` (or file-name date) is in the week.
   Read the front matter of every hit and classify `share`: explicit value first; otherwise the defaults from
   `CONVENTIONS.md` §8 (`decision` → team; `meeting`, `stakeholder`, `research`, `sweep` and raw notes → private).
   For other notes with no `share` (product pages, hypotheses, status), use them only as a summary and list them in
   the preview so the PM confirms.
4. **Read the hub vocabulary.** Collect existing `topics`, `building`, `reusable` and `needs` from
   `<hub>/digests/` (last 4 weeks), `<hub>/products/` and `<hub>/members/` — with
   `python3 scripts/brain_search.py --root <hub> --since <4 weeks ago> --json` or by grepping front matter. For every
   topic you plan to use, **reuse an existing hub topic when it means the same thing** (`llm-evaluation`, not
   `llm-evals`). Note each mapping for the preview.
5. **Draft** with the templates:
   - Digest front matter exactly as DESIGN §4.1 (`published` = today). `building`, `reusable`, `needs` come only
     from the PM's own work in the sources or from the user; leave a list empty rather than guess.
   - Digest body ≤ 250 words: Headline · Progress · Decisions (shareable, dated) · Risks / blocked · Asks. Count it.
   - Product card: update `<hub>/products/<product-slug>.md` (or create it): front matter per DESIGN §4.2, Recent
     decisions = last 5 shareable ones, dated. Keep everything the user wrote there that is still true.
   - First publish only: draft `<hub>/members/<person_slug>.md` from the member template.
   - From private notes you may use only the fact that work happened ("ran the bulk-edit design review"), never
     their details.
6. **Run the privacy check** against DESIGN §5 and show it as a checklist, each item ✅ or ⚠️:
   - [ ] No transcript text or quotes.
   - [ ] Nothing from `brain/stakeholders/`; no opinion attributed to a named colleague.
   - [ ] No `interpretation` claims about people.
   - [ ] Nothing from notes or lines marked `share: private` or inside `<!-- private -->` blocks.
   - [ ] Every number, customer name and date is listed below for the PM to approve.
   Then list **what was excluded and why**, by file path and reason only, never quoting the private content
   (e.g. "`meetings/2026/2026-10-20-pricing-sync.md` — share: private"). List the numbers, customer names and dates
   that remain in the text so the PM can approve or remove each.
7. **Preview.** Show the **exact final digest text** (front matter + body), the **product card as a diff** (full
   new file if it is new), the member file if new, and the topic mappings from step 4. On a republish, show the
   diff against the existing digest. Ask: "Publish this? (yes / no / tell me what to change)". Apply edits and show
   the preview again. Anything other than a clear yes means nothing is written.
8. **Write and commit (after yes).** Write the files, then
   `git -C <hub> add <the files you wrote>` and
   `git -C <hub> commit -m "digest: <person_slug> <YYYY-Www>"`.
9. **Push (always ask).** Ask "Push to the team hub now?" and run `git -C <hub> push` only after yes.
   If the push fails (conflict, no access, offline), keep the files and the local commit, explain in one line what
   happened and what to do (e.g. "Someone pushed first: run /publish again to rebase and retry", or "No write
   access: ask the manager"). Never force-push.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, `brain/products/<slug>/**` (front matter first; full text only of
shareable notes), `templates/digest.md`, `templates/product-card.md`, `templates/team-hub/member.md`, and in the hub:
`digests/`, `products/`, `members/`. Never reads `brain/stakeholders/` for content.

## Writes

Only after yes, in the hub: `digests/<YYYY>/<YYYY-Www>/<person_slug>.md`, `products/<product-slug>.md`,
`members/<person_slug>.md` (first publish). One hub commit; push after a second yes. Nothing in `brain/`.

## Rules

- **The privacy rule wins.** When unsure whether something is shareable, leave it out and list it as excluded.
- Never copy text from the brain verbatim; summarise in the PM's own voice.
- Never invent progress, numbers, decisions, needs or reusable assets. A thin week gets a short, honest digest.
- Write only your own digest, product cards you own, and your own member file. Never edit someone else's files.
- Never publish twice for the same week without showing a diff against the existing digest.
- Never write, commit or push without the explicit yes for that step. Never force-push.

## Output

The privacy checklist, the preview, then after publishing the hub paths, then:

```
What changed: <hub files written + commit, pushed or not; or "nothing (not approved)">
What needs you: <approve preview / push, resolve push failure, or "nothing">
What was missing: <e.g. "no decisions this week", "brain_search.py not found, used file listing", or "nothing">
```
