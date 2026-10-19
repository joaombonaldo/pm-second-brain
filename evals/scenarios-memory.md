# Eval scenarios — memory (v0.2)

Fictional product: **Acme Listings Optimizer** (slug `acme-listings-optimizer`). Run in a scratch clone, never on
your real brain. See [README.md](README.md) for scoring. The fixture brain is in `fixtures/memory/brain/`; two
extra transcripts are in `fixtures/memory/inbox/`.

**Setup for every scenario (fresh copy each time, unless the scenario says otherwise):**

```bash
rm -rf brain && cp -r evals/fixtures/memory/brain brain
git -C brain init -q && git -C brain add -A && git -C brain commit -qm "fixture"
```

What the fixture contains (so you can check results):

| File (under `products/acme-listings-optimizer/`) | Why it's there |
|---|---|
| `meetings/2026/2026-10-06-bulk-edit-sync.md` + `…-sync-2.md` | Same meeting ingested twice; `-2` has one extra action item (Ana — write stories, due 2026-10-12) |
| `decisions/2026-09-02-no-csv-upload.md` vs `2026-10-14-csv-upload-in-2-5.md` | Two **active** decisions that contradict |
| `decisions/2026-09-01-flag-internal-only.md` → `2026-10-06-beta-sellers-first.md` | Already superseded pair (history) |
| `decisions/2026-10-06-batch-cap-100.md` | Active decision that a new one will replace |
| `research/2026-07-10-competitor-notes.md` | Older than 60 days, no links in or out → stale |
| "Sellers edit 20–80 listings at a time" | Observation in 3 notes (sync, sprint 25 planning, seller interviews), not in `product/users.md` |
| `topics/bulk-edit.md`, `index.md` | Out of date on purpose |

## M1. Sweep merges a duplicate meeting note

- **Skill:** `/sweep`
- **Input:** `/sweep`, then answer `yes` only to the duplicate item.
- **Expected behaviour:** Finds the two 2026-10-06 bulk-edit-sync notes, proposes one merge, applies it after yes.
- **Pass criteria:**
  - The duplicate pair is proposed as **one** numbered item, inside a single combined diff with the other findings.
  - After yes: the main note contains Ana's "write bulk title edit stories" action item (due 2026-10-12), with its
    source; `…-sync-2.md` still exists with `status: superseded` and `superseded_by:` pointing to the main note.
  - No file deleted (`git -C brain status` shows no `D` entries).
  - Items answered "no" are unchanged and listed under **Declined** in `sweeps/2026-W43.md`.

## M2. Sweep: contradiction → superseded, behind a yes

- **Skill:** `/sweep`
- **Input:** `/sweep`. First answer `no`; check nothing changed. Run `/sweep` again and answer `yes`.
- **Expected behaviour:** Detects the CSV-upload contradiction and the stale note; edits nothing until yes.
- **Pass criteria:**
  - Proposes `2026-09-02-no-csv-upload.md` → `status: superseded`, `superseded_by: 2026-10-14-csv-upload-in-2-5.md`,
    and `supersedes:` on the newer one. Does **not** propose superseding the newer one.
  - Proposes `competitor-notes.md` → `status: stale`. Does not flag `flag-internal-only.md` (it has links).
  - After `no`: `git -C brain diff HEAD --stat` shows changes only in derived pages/report (`topics/`, `index.md`,
    `sweeps/`), never in `decisions/` or `research/`.
  - After `yes`: both decision files exist; the old one has a "Replaced by" line; its original text is intact.

## M3. /decision supersedes an older decision

- **Skill:** `/decision`
- **Input:** `/decision We'll open bulk edit to all sellers after one week without errors instead of two. Ana decided today after the beta data.`
- **Expected behaviour:** Has what/why/who/date, so asks nothing (or only to confirm). Finds the conflict with
  `2026-10-06-beta-sellers-first.md` and offers to supersede it.
- **Pass criteria:**
  - Shows the full new file `decisions/2026-10-19-<slug>.md` (`decided_by: Ana Souza`, `status: accepted`,
    `supersedes: 2026-10-06-beta-sellers-first.md`, `share: team`, topics reuse `bulk-edit`/`rollout`) and the
    diff of the old file, then waits.
  - Nothing written before yes. After yes: old file has `status: superseded` + `superseded_by:`; not deleted.
  - `topics/rollout.md` (or `bulk-edit.md`) lists the new decision as active and the old one under History.
  - Asking "who decided?" is not needed; if the input omits who, it asks — it never guesses.

## M4. Batch ingest with one consolidated approval

- **Skill:** `/ingest`
- **Setup:** fresh fixture, then `cp evals/fixtures/memory/inbox/*.txt brain/inbox/`.
- **Input:** `/ingest`, then answer `1` (only the first proposal).
- **Expected behaviour:** Writes both meeting notes first, then shows **one** numbered approval message.
- **Pass criteria:**
  - Two meeting notes written (2026-10-16 rate limit review, 2026-10-17 design review) before any question, with
    `people`, `topics`, `share: private`.
  - Exactly **one** approval message listing both decisions: (1) raise batch cap to 250 from 2.5 (Ana), marked as
    superseding `2026-10-06-batch-cap-100.md`; (2) failure summary downloadable as CSV (Ana). Accepts `yes/no/1,3`.
  - Priya's "filter by error type" is an `interpretation`, not a decision. The 60 req/s is an observation from
    Marco's spike, attributed. "Tell beta sellers before 2.5?" is an open question.
  - After `1`: only the cap-250 decision file exists; batch-cap-100 is `superseded`; no CSV-summary decision file.
  - Both `.txt` files are in `brain/inbox/processed/`; `index.md` and touched topic hubs updated.
  - `git -C brain log --oneline -1` shows one `ingest: 2 meetings …` commit.

## M5. Ask hides superseded and explains history

- **Skill:** `/ask`
- **Input:** `/ask who gets bulk edit first?` then `/ask what was the plan before that?`
- **Expected behaviour:** Runs `scripts/brain_search.py` first; answers from the current decision; follows the
  `supersedes` link for history.
- **Pass criteria:**
  - First answer: beta sellers first, behind a flag, open to all after two weeks without errors; cites
    `decisions/2026-10-06-beta-sellers-first.md` (2026-10-06). Does not present "internal accounts only" as current.
  - Second answer: internal accounts only (2026-09-01), replaced on 2026-10-06; cites both files.
  - No files changed.

## M6. brain_search filters and self-test

- **Skill:** none (script). Run from the repo root.
- **Input:**

  ```bash
  python3 scripts/brain_search.py --selftest
  python3 scripts/brain_search.py "rollout" --type decision --root evals/fixtures/memory/brain
  python3 scripts/brain_search.py "rollout" --type decision --status all --root evals/fixtures/memory/brain
  python3 scripts/brain_search.py --person marco-lima --since 2026-10-10 --root evals/fixtures/memory/brain
  python3 scripts/brain_search.py --share private --root evals/fixtures/memory/brain --limit 50 --json
  ```

- **Pass criteria:**
  - Self-test prints `selftest: OK` and exits 0.
  - Query 2 lists `2026-10-06-beta-sellers-first.md` and not `2026-09-01-flag-internal-only.md`; query 3 lists both.
  - Query 4 returns only notes dated on/after 2026-10-10 that mention Marco (sprint 25 planning, his stakeholder file).
  - Query 5 is valid JSON with no `decision` entries. Each text line has the shape `path | date | type | title | line`.

## M7. Brain versioning

- **Skill:** `/onboard`, then `/decision`
- **Setup:** no `brain/` folder (`rm -rf brain`).
- **Input:** `/onboard` with the values from `fixtures/brain.yaml` (skip the team hub), then
  `/decision We keep bulk edit titles-only for 2.4. Ana decided today because price edits need finance review.`
- **Pass criteria:**
  - `brain/.git` exists; `git -C brain log --oneline` shows `onboard: create brain`, then `decision: …`.
  - `git status` in the pm-agents repo does not show `brain/` (still ignored).
  - With git hidden from PATH, the skills warn once ("not versioned") and still finish; no crash, no retries.
  - No remote is added (`git -C brain remote` is empty).

## M8. Sweep promotes a repeated observation and rebuilds derived pages

- **Skill:** `/sweep`
- **Input:** `/sweep`, answer `yes`.
- **Pass criteria:**
  - Proposes adding `[observation] Sellers edit 20–80 listings at a time` to `product/users.md`, citing all three
    source notes with dates. Nothing promoted from fewer than 3 notes.
  - `topics/bulk-edit.md` is rebuilt: no longer says "internal accounts only" as the state; active decisions are the
    non-superseded ones; the old rollout decision appears under History; every line links to a note that exists.
  - `index.md` lists the latest active decisions (newest first) and links the topic hubs.
  - Report `sweeps/2026-W43.md` exists with Applied / Declined / Needs you / Derived pages rebuilt / Numbers.
  - One `sweep: 2026-W43` commit in `brain/`.
