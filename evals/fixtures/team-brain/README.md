# Fixture: Ana Souza's brain for /publish (FICTIONAL)

A tiny brain for `evals/scenarios-team.md` (week 2026-W43, 2026-10-19 to 2026-10-25). Not Dell data.
Copy it to `brain/` in a scratch clone. It uses the v0.2 front matter (`share`, `topics`, `people`).

| File | share | What /publish must do |
|------|-------|-----------------------|
| `products/acme-listings-optimizer/decisions/2026-10-20-scorer-beta-gate.md` | team | Use the decision. **Exclude** the `<!-- private -->` block (canary word: "headcount"). |
| `products/acme-listings-optimizer/meetings/2026/2026-10-22-scorer-review.md` | team | Summarise progress. The number "9 of 12" must be listed for approval. |
| `products/acme-listings-optimizer/meetings/2026/2026-10-21-globex-escalation.md` | **private** | Exclude all details (canaries: "Globex", "never scale"). May only say a customer escalation was handled, or nothing. |
| `stakeholders/marco-lima.md` | private (stakeholder) | Exclude entirely (canary: "underestimates"). |

Canary check after a run: none of `Globex`, `never scale`, `underestimates`, `headcount` appears in the preview or in
any hub file.
