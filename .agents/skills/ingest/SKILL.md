---
name: ingest
description: Process meeting transcripts and notes into the second brain. Use when the user types /ingest, drops files into brain/inbox/ (.vtt, .docx, .txt, .md), pastes meeting notes or a transcript, or says "process my meeting", "file this transcript", "add these notes to the brain".
---

# /ingest — Brain Keeper

## Purpose

Turn raw meeting material into a clean meeting note in the brain, keep stakeholder files current, and propose
(never silently apply) changes to decisions and durable product pages.

## Before you start

1. Read `brain/brain.yaml` and `brain/preferences/README.md`. If `brain/brain.yaml` does not exist, stop and say:
   "Your second brain isn't set up yet. Type **/onboard** first."
2. Load the meeting template: `brain/preferences/meeting-note.md` if it exists, else `templates/meeting-note.md`.

## Inputs

- Files in `brain/inbox/` (not in `brain/inbox/processed/`): `.vtt`, `.docx`, `.txt`, `.md`.
- Or text pasted in the chat.

## Steps

1. **List the inbox.** Show the files found (oldest first). If there are none and nothing was pasted, say
   "Your inbox is empty. Save a Teams transcript (.vtt or .docx) into `brain/inbox/` or paste your notes here."
   and stop. If there are several, process them one by one; finish each fully before the next.
2. **Read the content.**
   - `.vtt`: drop the `WEBVTT` header, cue numbers/IDs, timestamp lines (`00:01:02.000 --> 00:01:05.000`) and
     styling tags. Read the speaker from `<v Name>` tags or a `Name:` prefix. Merge consecutive cues from the same
     speaker into one turn. Keep the time of the first cue of each turn if you need to reference a moment.
   - `.docx`: extract the text with whatever tool is available (e.g. `python3` with `python-docx`, `pandoc`,
     `textutil` on macOS). Ask before running any shell command that is not read-only. If nothing works, ask the
     user to open the file and paste the text.
   - `.txt` / `.md` / pasted text: use as is.
3. **Detect the product.** If `brain.yaml` has one product, use it. If several, match on product names, Jira keys and
   stakeholders mentioned. If still unclear, ask: "Which product is this meeting about: A or B?"
4. **Work out date and title.** Date: from the file name, the transcript metadata, or the content; if none, ask.
   Title: short, from the meeting's purpose (e.g. "UX sync", "Sprint 42 planning"). Slug = kebab-case title.
5. **Write the meeting note** to `brain/products/<slug>/meetings/YYYY/YYYY-MM-DD-<title-slug>.md` using the template.
   If that file exists, add `-2`, `-3` to the slug; never overwrite. Fill:
   - **Summary**: 3–5 bullets, what matters for the product.
   - **Attendees**: speakers found, plus anyone named as present.
   - **Discussion**: key points by topic, short bullets. Attribute opinions to people.
   - **Decision candidates**: each with a claim type (see `CONVENTIONS.md`). Only use `[decision]` when someone
     clearly decided ("let's go with…", "agreed", "we'll do X") and say who. Otherwise use `interpretation`,
     `hypothesis` or `assumption`.
   - **Action items**: `- [ ] <action> — owner: <name> — due: <date or "not set">`. Never invent an owner or a date.
   - **Open questions**: things raised but not answered.
   - **Source**: path of the raw file as it will be after step 9 (`inbox/processed/<file>`), or "pasted by user, <date>".
6. **Update stakeholders.** For each attendee with a file in `brain/stakeholders/`, append one dated line under
   "Notes", e.g. `- 2026-10-20 — Owns the bulk-edit API change (action item). source: products/<slug>/meetings/2026/2026-10-20-ux-sync.md`.
   Append only; never rewrite existing lines. For a person with no file who seems important (owns an action item
   or made a decision), propose creating one from `templates/stakeholder.md` and create it after a yes.
7. **Propose durable changes (D13).** For each `[decision]`, draft a decision record in
   `brain/products/<slug>/decisions/YYYY-MM-DD-<slug>.md` from `templates/decision.md` (or preferences). If the meeting
   changes something in `product/`, `roadmap/` or `hypotheses/`, draft the edit. Show every proposal as a diff (or
   the full new file) in one message and ask: "Apply these? (yes / no / pick)". Apply only what the user approves.
8. **Link.** In the meeting note, link to any decision files created, using relative links.
9. **Move the raw file** to `brain/inbox/processed/` (keep the original name; if a file with that name exists,
   prefix the date). For pasted text, nothing to move.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, `brain/inbox/*`, `brain/stakeholders/*`,
`brain/products/<slug>/product/*`, `decisions/*` (to avoid duplicating an existing decision), templates.

## Writes

- Freely: `brain/products/<slug>/meetings/YYYY/*.md`, appended lines in `brain/stakeholders/*.md`, moving files
  into `brain/inbox/processed/`.
- After a yes: new stakeholder files, `decisions/*.md`, edits in `product/`, `roadmap/`, `hypotheses/`.

## Rules

- Never invent attendees, owners, due dates, numbers or decisions. If unsure, leave it out or mark it as an open
  question.
- Keep people's opinions as `interpretation`, attributed by name.
- Do not quote long stretches of the transcript; summarise. Short quotes are fine when wording matters.
- Never write to Jira or Confluence from this skill. If action items look like stories, suggest `/user-story`.
- Never delete the raw file; move it to `processed/`.

## Output

Show: the path of the meeting note, the summary bullets, decisions and action items (so the user can check them),
and the list of pending proposals. End with:

```
What changed: <meeting note path; stakeholder files appended; files moved>
What needs you: <proposals waiting for yes; unclear product/date; owners missing>
What was missing: <e.g. ".docx could not be read", "no due dates in transcript">
```
