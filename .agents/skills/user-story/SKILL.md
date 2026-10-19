---
name: user-story
description: Turn an idea, decision, meeting note or request into well-formed user stories with Given/When/Then acceptance criteria, saved as drafts in the brain, and optionally created in Jira after explicit confirmation. Use when the user types /user-story, or says "write a story for…", "turn this into tickets", "create Jira issues for…", "break this down into stories".
---

# /user-story — Backlog Writer

## Purpose

Write user stories a team can pick up: small, testable, linked to where the idea came from. Drafts live in the
brain; Jira is touched only after the user confirms exactly what will be created.

## Before you start

1. Read `brain/brain.yaml` and `brain/preferences/README.md`. If `brain/brain.yaml` does not exist, stop and say:
   "Your second brain isn't set up yet. Type **/onboard** first."
2. Load the story template: `brain/preferences/user-story.md` if it exists, else `templates/user-story.md`.
   (The team default is generic "As a / I want / so that" + Given/When/Then until Dell's format is known — Q7.)
3. Load the persona(s): `brain/preferences/persona.md` if it exists, else `templates/persona.md`.

## Inputs

- An idea in the chat, or a pointer to a brain file (decision, meeting note, research note), or a Jira key to refine.
- Optional: Jira project key (default: first key in `brain.yaml` for the product), epic, labels.

## Steps

1. **Find the source.** If the user points to a brain file, read it. If they describe an idea, grep the brain for
   related decisions, meetings and existing drafts (avoid duplicates; if a similar draft exists, show it and ask
   whether to update it instead).
2. **Clarify only what blocks you.** Ask at most 2 short questions (e.g. "Who is the user here: seller or admin?").
   Otherwise state your assumptions in the draft.
3. **Split.** One story = one user-visible outcome deliverable in a sprint. If the idea is bigger, propose a list of
   story titles first and ask which to write.
4. **Write each story** with the template:
   - Title: short, starts with a verb ("Bulk edit listing titles").
   - Story: "As a <persona>, I want <capability>, so that <benefit>."
   - Acceptance criteria: 3–6 items in **Given / When / Then**, each testable, including at least one edge or
     error case.
   - Notes: assumptions (tagged `[assumption]`), out of scope, dependencies, open questions.
   - Source: link to the brain file(s) it came from (`source: decisions/2026-10-20-bulk-edit-flag.md`).
5. **INVEST check.** For each story, check Independent, Negotiable, Valuable, Estimable, Small, Testable. Fix what you
   can; list any remaining concerns under the story as "INVEST: <issue>".
6. **Save drafts** to `brain/products/<slug>/backlog/drafts/YYYY-MM-DD-<title-slug>.md` (one file per story, with
   front matter from `CONVENTIONS.md`, `status: draft`). Never overwrite; add `-2` if the name exists.
7. **Show the drafts** in the chat and ask: "Want me to create these in Jira?"
8. **Jira — only after explicit confirmation.**
   - If the Jira MCP tool is available: show a preview listing exactly what will be created for each issue:
     project key, issue type, summary, description (full text), acceptance criteria, labels, epic link. Ask:
     "Create these N issues in <KEY>? (yes / no)". Create only on a clear "yes". Anything else = do not create.
   - After creating: write the returned keys into each draft (`jira: ABC-123`, `status: created-in-jira`) and report
     them. If a creation fails, report the error; do not retry silently.
   - Updating an existing issue follows the same rule: show the before/after, wait for "yes".
   - If the Jira MCP tool is missing or fails: say so in one line and output each story as copy-paste-ready text
     (Summary / Description / Acceptance criteria blocks) so the user can paste it into Jira.
9. **Save (D26).** `git -C brain add -A && git -C brain commit -m "user-story: <N> drafts (<short topic>)"`. If git
   is missing or fails, warn once and carry on.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, templates, related files in `brain/products/<slug>/` (decisions, meetings,
research, product, backlog/drafts).

## Writes

- Freely: `brain/products/<slug>/backlog/drafts/*.md`.
- Jira issues: **only** after the user confirms the exact preview.

## Rules

- Never create, edit, transition or comment on a Jira issue without an explicit "yes" to the exact preview.
- Never invent requirements the source doesn't support; tag guesses as `[assumption]` and list them.
- No estimates, priorities or sprint assignments unless the user gives them.
- Keep the user's and stakeholders' wording for domain terms.

## Output

The stories (or the Jira keys created), then:

```
What changed: <draft files written; Jira issues created with keys, or "no Jira changes">
What needs you: <confirm Jira creation; answer open questions; review assumptions>
What was missing: <e.g. "Jira MCP not available — paste-ready text provided", "no persona for admins">
```
