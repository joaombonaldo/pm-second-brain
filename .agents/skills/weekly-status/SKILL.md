---
name: weekly-status
description: Draft the PM's weekly status report from the last 7 days of meetings, decisions and notes in the second brain (plus Jira progress if available), with a short paste-ready version for Teams or email. Use when the user types /weekly-status, or says "weekly status", "update for my manager", "what happened this week", "status report".
---

# /weekly-status — Reporter

## Purpose

Give stakeholders an honest, sourced picture of the week in a few minutes of the PM's time.

## Before you start

1. Read `brain/brain.yaml` and `brain/preferences/README.md`. If `brain/brain.yaml` does not exist, stop and say:
   "Your second brain isn't set up yet. Type **/onboard** first."
2. Load the template: `brain/preferences/weekly-status.md` if it exists, else `templates/weekly-status.md`.

## Inputs

- Product (ask if several in `brain.yaml`; or "all" for one status per product).
- Period: default = the last 7 days ending today. The user may give another week.
- Optional: anything the user wants to add ("mention the hiring freeze").

## Steps

1. **Collect sources from the period.** In `brain/products/<slug>/`: `meetings/` notes dated in the period,
   `decisions/` dated in the period, `backlog/drafts/` and `releases/` changed in the period, the previous
   `status/` file (for continuity: open risks, last week's "next week"). Use front matter `date:` first, file
   name date second.
2. **Jira progress (optional).** If the Jira MCP tool is available, read-only: issues moved to done in the period and
   currently blocked issues for the product's key(s). If not available, say so in one line and skip it.
3. **Draft the status** with the template:
   - **Headline**: one sentence, the most important thing this week.
   - **Progress**: what moved, with sources.
   - **Decisions**: decisions made this week (claim type `decision` only), with who and source.
   - **Risks / blocked**: open risks, blockers, slipped action items from meeting notes. Say who owns each.
   - **Asks**: what the PM needs from readers (decisions, help, unblocking). Only asks supported by the sources or
     given by the user.
   - **Next week**: planned items from action items and meetings.
   - **Sources**: list of brain files and Jira keys used.
4. **Compare with last week's status** if it exists: carry forward unresolved risks (marked "still open") and note
   items from last week's "next week" that didn't happen.
5. **Write the short version**: ≤ 120 words, plain text, ready to paste into Teams or email. Headline first, then 3–5
   bullets, then asks. Count the words.
6. **Save** to `brain/products/<slug>/status/YYYY-Www.md` (ISO week of the period's end). If it exists, show a diff
   and ask before replacing it. Put the short version at the end of the file under "Short version".
7. **Show** both versions in the chat.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, `templates/weekly-status.md`, `brain/products/<slug>/{meetings,decisions,
backlog,releases,status}/`, `brain/stakeholders/*` (names and roles only). Jira via MCP (read-only).

## Writes

`brain/products/<slug>/status/YYYY-Www.md`. Nothing in Jira, Confluence, Teams or email.

## Rules

- **Never fabricate metrics**, percentages, dates or progress. Use a number only if it appears in a source; cite it.
- If the week has little in the brain, say so in the status ("Light week in the brain: only 1 meeting ingested")
  rather than padding it, and suggest ingesting missing meetings.
- Interpretations stay attributed ("Marco thinks…"); don't present them as facts.
- Never send or post the status. The user pastes it.

## Output

Full status and short version, file path, then:

```
What changed: <status/YYYY-Www.md written>
What needs you: <review; confirm asks; paste the short version>
What was missing: <e.g. "no meetings ingested Wed–Fri", "Jira MCP not available">
```
