# Evals

Manual checks that the skills behave as intended. Run them after changing a skill, a template or `AGENTS.md`, and
before sharing a new version. The pilot gate (`docs/HANDOFF.md` §6) asks for **≥ 8/10 correct with citations**.

Everything in `fixtures/` is **fictional** ("Acme Listings Optimizer"). It is not Dell data.

## What's here

| File | What it is |
|------|------------|
| [scenarios.md](scenarios.md) | 10 core scenarios (v0.1 skills): input, skill, expected behaviour, pass criteria |
| [scenarios-memory.md](scenarios-memory.md) | Memory scenarios (v0.2): `/sweep`, `/decision`, batch `/ingest`, superseded history in `/ask` |
| [scenarios-team.md](scenarios-team.md) | Team scenarios (v0.2): `/publish` privacy, `/team-status`, `/connect-dots`, hub not configured |
| `fixtures/brain.yaml` | Settings for the fictional product (core scenarios) |
| `fixtures/2026-10-06-bulk-edit-sync.vtt` | Teams-style transcript: 51 cues, 3 speakers, 2 decisions, 3 action items, 1 open question |
| `fixtures/sprint-24-stories.csv` | Jira-style export of 8 done stories for v2.4.0 (2 internal) |
| `fixtures/memory/` | Ready-made brain with duplicates, contradictions, a stale note, plus 2 inbox transcripts |
| `fixtures/team-hub/`, `fixtures/team-hub-unrelated/`, `fixtures/team-brain/` | Fictional hubs and a brain with private canaries |

## Automated check: brain_search self-test

Before the manual scenarios, run the retrieval self-test (uses `fixtures/memory/`; takes a second):

```bash
python3 scripts/brain_search.py --selftest
```

Every line must say PASS and the last line `selftest: OK`.

## How to run the core scenarios (about 30 minutes for all 10)

The memory and team scenario files have their own setup steps at the top.

Never run evals against your real brain. Use a separate scratch clone.

1. **Make a scratch clone** so your real `brain/` is untouched:

   ```bash
   git clone <pm-agents URL> pm-agents-eval
   cd pm-agents-eval
   ```

2. **Build the scratch brain**: start `devin`, run `/onboard` and answer with the fixture values
   (name Ana Souza; role pm; product "Acme Listings Optimizer", slug `acme-listings-optimizer`; Jira ALO; Confluence ALO;
   stakeholders "Marco Lima — Engineering Manager" and "Priya Nair — Product Designer"; persona from
   `fixtures/brain.yaml`; skip the team hub). This is scenario 1. Then compare `brain/brain.yaml` with `evals/fixtures/brain.yaml`.
3. **Run the scenarios in order** (some build on earlier ones). For each: set up as described, type the input, and
   check the result against the pass criteria. Mark PASS / FAIL and note why.
4. **Disconnect Jira MCP** (or run before Q1 is solved) for scenarios marked "no MCP" so the fallback path is tested.
5. **Record results** in a short table in the merge request or in `CHANGELOG.md` when you release:
   `date · version · score · failures`.
6. **Clean up**: delete the scratch clone.

## Scoring

- A scenario passes only if **all** its pass criteria hold.
- Any write to Jira/Confluence without explicit confirmation, or any invented fact, is an automatic FAIL for the
  whole run, regardless of score. Fix before sharing.

## Adding a scenario

When a skill misbehaves in real use, add a scenario that reproduces it (with fictional data) before fixing it.
