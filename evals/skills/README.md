# Per-skill evals

One file per skill: `evals/skills/<skill-name>.md`, made from [templates/skill/eval.md](../../templates/skill/eval.md).
Each file holds that skill's scenarios (fictional data only) and a short results table, so the owner and reviewers
can see at a glance whether the skill still works.

- **New skills** need at least one scenario here before review; `scripts/validate.py` fails without it for any skill
  not owned by `pm-agents core`.
- **Promotion to stable** needs this file to pass (see [CONTRIBUTING.md](../../CONTRIBUTING.md)).
- **Run them** the same way as the core scenarios: a scratch clone, never your real brain
  ([evals/README.md](../README.md)).

## Core skills

The 11 core skills are covered by the existing scenario files; they don't have a file here yet.

| Skill | Scenarios |
|-------|-----------|
| `/onboard` | [scenarios.md](../scenarios.md) 1, 2, 10 |
| `/ingest` | [scenarios.md](../scenarios.md) 3; [scenarios-memory.md](../scenarios-memory.md) M4 |
| `/ask` | [scenarios.md](../scenarios.md) 4, 5; [scenarios-memory.md](../scenarios-memory.md) M5 |
| `/decision` | [scenarios-memory.md](../scenarios-memory.md) M3 |
| `/sweep` | [scenarios-memory.md](../scenarios-memory.md) M1, M2, M8 |
| `/user-story` | [scenarios.md](../scenarios.md) 6, 7 |
| `/release-notes` | [scenarios.md](../scenarios.md) 8 |
| `/weekly-status` | [scenarios.md](../scenarios.md) 9 |
| `/publish` | [scenarios-team.md](../scenarios-team.md) 1, 5–8 |
| `/team-status` | [scenarios-team.md](../scenarios-team.md) 1, 2 |
| `/connect-dots` | [scenarios-team.md](../scenarios-team.md) 3, 4 |

When a core skill changes, add its scenarios here as `evals/skills/<name>.md` rather than growing the shared files.
