---
name: ingest
description: Process meeting transcripts and notes into the second brain, all inbox files in one batch with a single approval at the end. Use when the user types /ingest, drops files into brain/inbox/ (.vtt, .docx, .txt, .md), pastes meeting notes or a transcript, or says "process my meeting", "file this transcript", "add these notes to the brain".
---

# /ingest — Brain Keeper

## Purpose

Turn every raw meeting file in the inbox into a clean meeting note, keep stakeholder files, the product index and
topic hubs current, and propose (never silently apply) decisions and durable changes, all in **one** approval
message (D29). End with one commit in the brain's history (D26).

## Before you start

1. Read `brain/brain.yaml` and `brain/preferences/README.md`. If `brain/brain.yaml` does not exist, stop and say:
   "Your second brain isn't set up yet. Type **/onboard** first."
2. Load the meeting template: `brain/preferences/meeting-note.md` if it exists, else `templates/meeting-note.md`.
3. List existing topics per product: `ls brain/products/<slug>/topics/` (reuse these names, see `CONVENTIONS.md` §8).

## Inputs

- Every file in `brain/inbox/` (not in `brain/inbox/processed/`): `.vtt`, `.docx`, `.txt`, `.md`.
- Or text pasted in the chat (treated as one file).

## Steps

1. **List the inbox.** Show the files found, oldest first. If there are none and nothing was pasted, say
   "Your inbox is empty. Save a Teams transcript (.vtt or .docx) into `brain/inbox/` or paste your notes here."
   and stop. Process **all** files in this run; do not stop to ask between files unless the product or date of a
   file is truly unknown (then ask once, listing every unclear file together).
2. **Read each file.**
   - `.vtt`: drop the `WEBVTT` header, cue numbers, timestamp lines and styling tags. Speaker from `<v Name>` or a
     `Name:` prefix. Merge consecutive cues from the same speaker.
   - `.docx`: extract text with an available tool (`python3` + `python-docx`, `pandoc`, `textutil`). Ask before
     running any shell command that is not read-only. If nothing works, ask the user to paste the text.
   - `.txt` / `.md` / pasted: use as is.
3. **Product, date, title.** One product in `brain.yaml` → use it; several → match names, Jira keys, people.
   Date from file name, metadata or content. Title from the meeting's purpose; slug = kebab-case title.
4. **Write each meeting note** (free write) to `brain/products/<slug>/meetings/YYYY/YYYY-MM-DD-<title-slug>.md`.
   If the file exists, add `-2`, `-3`; never overwrite. Before writing, run
   `python3 scripts/brain_search.py --type meeting --since <date> --until <date> --product <slug>`; if a note for the
   same meeting already exists, say so in the approval message (it may be a duplicate for `/sweep`). Fill:
   - Front matter v2: `people` (slugs of speakers and people named), `topics` (1–4, reuse existing),
     `share: private`, `status: active`.
   - **Summary** (3–5 bullets), **Attendees**, **Discussion** (opinions attributed by name).
   - **Decision candidates** with claim types. `[decision]` only when someone clearly decided ("let's go with…",
     "agreed", "decided") and say who. Otherwise `interpretation`, `hypothesis` or `assumption`.
   - **Action items**: `- [ ] <action> — owner: <name> — due: <date or "not set">`. Never invent owner or date.
   - **Open questions**, **Source** (`inbox/processed/<file>` or "pasted by user, <date>").
   - Things said in confidence about people go inside `<!-- private -->` … `<!-- /private -->`.
5. **Append to stakeholders** (free write). For each attendee with a file in `brain/stakeholders/`, append one dated
   line under "Notes" with the source path. Append only.
6. **Collect proposals** across all files (do not ask yet). For each:
   - `[decision]` → a draft decision record from `templates/decision.md` (`share: team`, `topics`, `people`,
     `valid_from`). Check for conflicts:
     `python3 scripts/brain_search.py "<key words>" --type decision --product <slug> --status active`.
     If an active decision says something incompatible, the proposal also sets the old one to
     `status: superseded` + `superseded_by:` and the new one's `supersedes:`.
   - New stakeholder file for an important person with no file (owns an action item or made a decision).
   - Edits to `product/`, `roadmap/`, `hypotheses/` the meetings justify.
7. **One approval message.** Show every proposal numbered, each with its diff or full new file and its source note:

   ```
   1. New decision: Raise batch cap to 250 (2026-10-16, Ana Souza) — from meetings/2026/2026-10-16-rate-limit-review.md
      Supersedes decisions/2026-10-06-batch-cap-100.md (sets status: superseded)
      <diff>
   2. New stakeholder file: stakeholders/joana-reis.md
      <full file>
   Apply? yes (all) / no (none) / numbers, e.g. 1,3
   ```

   Apply exactly what the user picked. Anything unclear = ask again; never guess.
8. **Link.** In each meeting note, add relative links to the decision files created.
9. **Update derived pages** (free write, `CONVENTIONS.md` §9). For every topic touched, update
   `products/<slug>/topics/<topic>.md` (create from `templates/topic-hub.md` if missing): latest notes, active
   decisions, open questions, history for anything superseded. Update `products/<slug>/index.md` (create from
   `templates/product-index.md` if missing): latest decisions, topics list, key people.
10. **Move the raw files** to `brain/inbox/processed/` (keep names; if taken, prefix the date). Never delete.
11. **Save (D26).** `git -C brain add -A && git -C brain commit -m "ingest: <N> meetings (<dates>)"`. If git is
    missing or fails, warn once and carry on.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, `brain/inbox/*`, `brain/stakeholders/*`, `brain/products/<slug>/`
(`product/`, `decisions/`, `topics/`, `index.md`), templates. Search with `scripts/brain_search.py`.

## Writes

- Freely: `meetings/YYYY/*.md`, appended lines in `stakeholders/*.md`, `topics/*.md`, `index.md`, moves into
  `inbox/processed/`, the brain commit.
- After the single approval: new stakeholder files, `decisions/*.md`, status changes on old decisions, edits in
  `product/`, `roadmap/`, `hypotheses/`.

## Rules

- Never invent attendees, owners, due dates, numbers or decisions. If unsure, leave it out or make it an open question.
- Keep opinions as `interpretation`, attributed by name. Untested numbers are not `observation`s.
- Summarise; no long transcript quotes.
- **One** approval message per run, after all notes are written. Never write a decision before the yes.
- Superseding never deletes: the old decision stays, marked `superseded`.
- Never write to Jira or Confluence. If action items look like stories, suggest `/user-story`.

## Output

Per file: meeting note path, summary bullets, decisions, action items. Then the numbered approval message. After the
answer, end with:

```
What changed: <meeting notes; stakeholder lines; decisions applied; topic hubs/index updated; files moved; brain commit>
What needs you: <proposals not yet answered; unclear product/date; owners missing>
What was missing: <e.g. ".docx could not be read", "no due dates in transcript", "git not available">
```
