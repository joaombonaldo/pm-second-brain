---
name: release-notes
description: Draft user-facing release notes for a sprint or version as an HTML page, written benefit-first for the PM's persona, from the done stories in Jira or a pasted list/CSV. Use when the user types /release-notes, or says "release notes for sprint/version…", "what shipped in…", "write the changelog for users".
metadata:
  category: release
  role: Release Manager
  owner: pm-agents core
  version: "0.2.0"
  status: stable
  brain: required
  reads: "brain/brain.yaml, brain/preferences/, brain/products/<slug>/product/, jira"
  writes: "brain/products/<slug>/releases/"
  preferences: "README.md, persona.md, release-notes.html"
  requires: "jira-mcp, git"
---

# /release-notes — Release Manager

> **Team default. João will merge his personal version (D10).** Personal style (persona, tone, HTML template) belongs
> in `brain/preferences/`, not in this file.

## Purpose

Explain what shipped in a way the target user cares about, and save it as a ready-to-share HTML page.

## Before you start

1. Read `brain/brain.yaml` and `brain/preferences/README.md`. If `brain/brain.yaml` does not exist, stop and say:
   "Your second brain isn't set up yet. Type **/onboard** first."
2. Load the persona: `brain/preferences/persona.md` if it exists, else the `release_notes_persona` in `brain.yaml`
   for this product, else `templates/persona.md`.
3. Load the HTML template: `brain/preferences/release-notes.html` if it exists, else `templates/release-notes.html`.

## Inputs

- Sprint name or version (ask if not given: "Which sprint or version?").
- The done stories: from Jira via MCP, or a pasted list, or a CSV export (columns like key, summary, type, labels,
  status, description).

## Steps

1. **Pick the product** (ask if several in `brain.yaml`) and the sprint/version.
2. **Get the stories.**
   - Jira MCP available: query read-only for issues in that sprint/fix version with a done status in the product's
     project key(s). Show the count and the JQL (or filter) you used.
   - Not available or it fails: say so in one line and ask the user to paste the list or the CSV (Jira → Filters →
     export CSV). Parse what they give; don't require exact column names.
3. **Classify each item** as *user-facing* or *internal*. Internal = tech debt, refactoring, CI/build, test-only,
   spikes, dependency upgrades, or labelled `internal` / `tech-debt` / `no-release-notes`. **Skip internal items**
   unless the user asked to include them. Bugs are user-facing only if the user could notice the fix.
4. **Group by theme** (2–5 themes, named for the user, e.g. "Faster bulk editing", "Fixes"). Put the most valuable
   theme first.
5. **Write each item benefit-first** for the persona: what they can now do or what got better, then (briefly) how.
   One or two sentences. Plain words; no internal codenames or ticket jargon. Don't promise anything the story
   doesn't say. Keep the Jira key out of the visible text; put it in a `data-jira="KEY-123"` attribute on the `<li>` (as the
   template example shows) so it stays traceable.
6. **Write an intro**: 1–2 sentences, the headline of this release for the persona.
7. **Render the HTML.** Copy the template and replace the placeholders: `{{product_name}}`, `{{version}}`,
   `{{date}}` (today unless the user gives a release date), `{{intro}}`, `{{sections}}`. `{{sections}}` is one
   `<section>` per theme with an `<h2>` and a `<ul>` of `<li>` items, following the markup example in the template.
   Escape `<`, `>` and `&` in text. Delete the instructions comment at the top of the template. Leave no `{{…}}`
   placeholder in the output.
8. **Save** to `brain/products/<slug>/releases/<version>.html` (version in kebab-case, e.g. `2-4-0.html` or
   `sprint-42.html`). If the file exists, ask before overwriting; otherwise save as `<version>-v2.html`.
9. **Show** a markdown preview of the content (intro + themes + items), then the list of **skipped items** with the
   reason for each, so the user can pull any back in.
10. **Save (D26).** `git -C brain add -A && git -C brain commit -m "release-notes: <version>"`. If git is missing or
    fails, warn once and carry on.

## Reads

`brain/brain.yaml`, `brain/preferences/*`, `templates/persona.md`, `templates/release-notes.html`, optionally
`brain/products/<slug>/product/*` for product vocabulary. Jira via MCP (read-only).

## Writes

`brain/products/<slug>/releases/<version>.html`. Nothing in Jira or Confluence.

## Rules

- Never write to Jira or Confluence. Publishing the page anywhere is the user's job (or a future `/publish`).
- Never invent features, numbers or dates. If a story's benefit is unclear, write it neutrally and flag it.
- Never post to Teams or email; the user shares the file.
- Personal template and persona in `brain/preferences/` always win over the team defaults.

## Output

Markdown preview, skipped items list, file path, then:

```
What changed: <releases/<version>.html written>
What needs you: <review flagged items; confirm skipped items; share the file>
What was missing: <e.g. "Jira MCP not available — used pasted CSV", "3 stories had no description">
```
