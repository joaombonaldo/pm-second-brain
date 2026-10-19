# Fixture: pm-team-hub (FICTIONAL)

A fictional team hub used by `evals/scenarios-team.md`. Not Dell data. People, products and numbers are invented.

- Team: Ana Souza (`acme-listings-optimizer`), Bruno Reis (`acme-pricing-assistant`), Carla Dias
  (`acme-search-insights`); manager Diego Martins (no digests, as allowed for managers).
- Weeks: 2026-W41 (all three PMs published) and 2026-W42 (Carla did **not** publish).

## Seeded signals (answer key for /connect-dots and /team-status)

| Lens | Who | Evidence (front matter) | Expected confidence |
|------|-----|-------------------------|---------------------|
| **Overlap** | Ana + Carla | Ana `building`: "LLM-based title quality scorer" (W41, W42, card) · Carla `building`: "LLM-based listing quality scorer for search relevance" (W41, card); shared topic `llm-evaluation` | high or medium (Carla's side is from W41) |
| **Reuse** | Ana → Bruno | Ana `reusable`: "Prompt library for product titles and descriptions" · Bruno `needs`: "Tested prompt templates for seller-facing copy (price-change explanations)" | high |
| Reuse (secondary) | Ana → Carla | Ana `reusable` (W42): "Title quality rubric…" · Carla `needs`: "Rubric for judging listing quality consistently" | high or medium |
| Reuse (secondary) | Carla → Bruno | Carla `reusable`: "Weekly search query volume by category" · Bruno `needs` (W42): "Signal of upcoming demand per category…" | medium |
| **Combine** | Carla + Bruno | Carla `building`: "Search demand trends by category" + Bruno `building`: "Price elasticity model per category" → demand-aware price suggestions | low or medium, framed as a hypothesis |
| Distractor | Bruno | `building`: "Price feed data quality audit", topic `data-quality` — shares the word "quality" only; must **not** be reported as an overlap with the scorers | — |

Cross-team risks for `/team-status`: Ana (no labelled examples) and Carla (unstable rubric) are two sides of the same
calibration problem; Bruno's beta date is at risk until he has prompt templates.
