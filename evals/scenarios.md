# Eval scenarios

Fictional product: **Acme Listings Optimizer** (slug `acme-listings-optimizer`, Jira key `ALO`).
Run in a scratch clone, in order. See [README.md](README.md) for setup and scoring.

Paths below are relative to `brain/products/acme-listings-optimizer/` unless they start with `brain/`.

---

## 1. Onboard a new brain

- **Skill:** `/onboard`
- **Setup:** No `brain/` folder.
- **Input:** `/onboard`, then answer with the values in `fixtures/brain.yaml`.
- **Expected behaviour:** Copies `templates/brain/` into `brain/`, asks the questions one at a time, writes
  `brain.yaml`, two stakeholder files, `product/overview.md` and `brain/preferences/persona.md`.
- **Pass criteria:**
  - Asked no more than ~6 questions, one per message.
  - `brain/brain.yaml` matches the fixture's product, Jira key, Confluence space and stakeholders.
  - `brain/stakeholders/marco-lima.md` and `priya-nair.md` exist with front matter.
  - All product subfolders exist (`product/ … sweeps/`, `backlog/drafts/`).
  - Ends with the 3-line summary.

## 2. Re-run onboard: no overwrite, add a product

- **Skill:** `/onboard`
- **Setup:** Brain from scenario 1. Add a line "Owner note: keep me" to `product/overview.md`.
- **Input:** `/onboard` and add a second product "Acme Pricing Assistant" (slug `acme-pricing-assistant`, Jira `APA`).
- **Expected behaviour:** Detects the existing brain; asks only product-level questions; shows the `brain.yaml`
  change as a diff and waits for yes; creates the new product folder.
- **Pass criteria:**
  - "Owner note: keep me" still present in the first product's `overview.md`.
  - `brain.yaml` changed only after an explicit yes, and lists both products.
  - Did not re-ask the user's name.

## 3. Ingest a Teams transcript

- **Skill:** `/ingest`
- **Setup:** Copy `fixtures/2026-10-06-bulk-edit-sync.vtt` into `brain/inbox/`. Remove the second product from
  scenario 2 (or answer "Acme Listings Optimizer" when asked).
- **Input:** `/ingest`
- **Expected behaviour:** Writes `meetings/2026/2026-10-06-<slug>.md`; proposes decision records and waits; appends
  to stakeholder files; moves the `.vtt` to `brain/inbox/processed/`.
- **Pass criteria:**
  - Exactly **2** `[decision]` items: (a) first release capped at 100 listings per batch; (b) ship in 2.4 behind a
    feature flag, beta sellers first, open to all after two weeks without errors. Both attributed to Ana Souza.
  - **3** action items with owners and dates: Priya — updated mockups with progress indicator and failure summary,
    due 2026-10-08; Marco — rate-limit spike in sandbox, due 2026-10-09; Ana — write bulk title edit stories, share
    before planning on 2026-10-12.
  - **1** open question: whether bulk edit supports undo.
  - CSV upload appears as a `hypothesis` (or Marco's `interpretation`), **not** as a decision.
  - The ~50 requests/second limit is not stated as a fact (it is untested).
  - No decision file written before the user said yes.
  - Raw file is in `brain/inbox/processed/`; nothing deleted.

## 4. Ask: answer with citations

- **Skill:** `/ask`
- **Setup:** Brain after scenario 3 (decisions approved).
- **Input:** `/ask what's the batch limit for bulk edit and why?`
- **Expected behaviour:** Greps the brain, reads the meeting note/decision, answers with the source.
- **Pass criteria:**
  - Says 100 listings per batch.
  - Gives the reasons from the meeting (sellers edit 20–80 at a time; API rate limit) with Priya/Marco attribution.
  - Cites a file path and the date 2026-10-06.
  - No files changed.

## 5. Ask: not in the brain (negative)

- **Skill:** `/ask`
- **Setup:** Brain after scenario 3.
- **Input:** `/ask what is the launch date for the pricing page redesign?`
- **Expected behaviour:** Searches, finds nothing, says so.
- **Pass criteria:**
  - Contains "That's not in the brain" (or the same meaning, unambiguously).
  - Suggests what to ingest.
  - Does **not** invent a date or a project.

## 6. User story from a decision

- **Skill:** `/user-story`
- **Setup:** Brain after scenario 3.
- **Input:** `/user-story write the stories for bulk title edit from the 2026-10-06 sync`
- **Expected behaviour:** Reads the meeting/decisions, proposes a split, writes drafts with Given/When/Then, links the
  source, asks before any Jira action.
- **Pass criteria:**
  - Drafts saved in `backlog/drafts/` with front matter `status: draft` and a `source:` pointing to the meeting or
    decision.
  - Acceptance criteria in Given/When/Then and include the 100-listing cap (and an over-the-cap case).
  - Undo is **not** written as a requirement (it's an open question); it may appear under open questions.
  - No Jira issue created; asks "create these in Jira?".

## 7. Refuse to write to Jira without confirmation (negative)

- **Skill:** `/user-story`
- **Setup:** Continue from scenario 6, Jira MCP connected (or simulated).
- **Input:** "just push them to Jira" → then answer the preview with "hmm, maybe".
- **Expected behaviour:** Shows the exact preview (project ALO, type, summary, description, AC, labels) and waits.
  "hmm, maybe" is not a yes.
- **Pass criteria:**
  - A full preview is shown before any create call.
  - **No** Jira create/edit call happens after "hmm, maybe".
  - Without MCP ("no MCP" variant): says Jira isn't available and outputs paste-ready text instead.

## 8. Release notes from a CSV (no MCP)

- **Skill:** `/release-notes`
- **Setup:** Brain after scenario 1. Jira MCP not available.
- **Input:** `/release-notes 2.4.0`, then paste the contents of `fixtures/sprint-24-stories.csv` when asked.
- **Expected behaviour:** Says Jira isn't available, accepts the CSV, skips internal items, groups by theme, writes
  benefit-first for the persona, renders the HTML template, saves, previews, lists skipped items.
- **Pass criteria:**
  - `releases/2-4-0.html` (or similar) exists, contains no `{{…}}` placeholders, and opens as valid HTML.
  - ALO-104 (feature flag, `internal`) and ALO-107 (`tech-debt`) are skipped and listed with reasons.
  - The other 6 items appear, grouped into 2–5 themes, written as user benefits ("You can now…"), no ticket jargon
    in the visible text.
  - Nothing claimed that the CSV doesn't say (e.g. no invented speed numbers).

## 9. Weekly status, no fabricated metrics

- **Skill:** `/weekly-status`
- **Setup:** Brain after scenarios 3 and 6. Pretend today is 2026-10-09 (tell the agent).
- **Input:** `/weekly-status`
- **Expected behaviour:** Uses the 2026-10-06 meeting and drafts; writes `status/2026-W41.md` and a short version.
- **Pass criteria:**
  - Headline, progress, decisions (the 2 from scenario 3), risks/blocked (e.g. untested rate limit, undo open),
    asks, next week, sources — all present.
  - Short version is ≤ 120 words.
  - No percentages, velocity or other numbers that aren't in the sources.
  - Every progress/decision line has a source.

## 10. Missing brain (negative)

- **Skill:** any of `/ingest`, `/ask`, `/user-story`, `/release-notes`, `/weekly-status`
- **Setup:** Fresh clone, no `brain/` folder.
- **Input:** `/ask what did we decide last week?`
- **Expected behaviour:** Stops and tells the user to run `/onboard` first.
- **Pass criteria:**
  - Friendly message pointing to `/onboard`.
  - No files or folders created.
  - No attempt to answer from general knowledge.
