# Evals — /your-skill-name

Copy to `evals/skills/<your-skill-name>.md`. Use only fictional data (the Acme fixtures in `evals/fixtures/` are a
good start). At least one scenario before review; add one each time the skill misbehaves in real use.

| Date | Version | Result | Notes |
|------|---------|--------|-------|
| YYYY-MM-DD | 0.1.0 | PASS / FAIL | <who ran it, what failed> |

---

## 1. <Happy path, in a few words>

- **Setup:** <e.g. brain from `evals/fixtures/memory/brain/` copied to `brain/`; Jira MCP off.>
- **Input:** `/your-skill-name <what the user types>`
- **Expected behaviour:** <what the skill should do, step by step, in 2–4 lines.>
- **Pass criteria:**
  - <Observable result, e.g. "writes `status/2026-W43.md` with 3 cited sources".>
  - Every fact cites a brain file or Jira key; nothing invented.
  - Ends with the 3-line summary.

## 2. No brain (negative)

- **Setup:** no `brain/` folder.
- **Input:** `/your-skill-name`
- **Pass criteria:** says what the skill does and points to `/onboard`; writes nothing.
