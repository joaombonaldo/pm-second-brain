---
type: digest
person: ana-souza
role: pm
week: 2026-W42
products: [acme-listings-optimizer]
topics: [llm-evaluation, prompt-design, bulk-edit]
building:
  - "LLM-based title quality scorer"
  - "Bulk title edit for up to 100 listings"
reusable:
  - "Prompt library for product titles and descriptions"
  - "Title quality rubric (clarity, attributes, marketplace rules)"
needs:
  - "A labelled set of good and bad listing titles to calibrate the scorer"
published: 2026-10-16
---

# Ana Souza — 2026-W42

**Headline:** Title quality scorer runs end to end on a test set; calibration data is still missing.

## Progress

- Scorer now returns a score and a one-line reason for each generated title.
- Bulk title edit is in development behind a feature flag.
- Rubric written up so others can reuse it.

## Decisions

- [decision] Bulk edit ships in 2.4 behind a feature flag, beta sellers first. — 2026-10-13

## Risks / blocked

- Without labelled examples we can't tell sellers how reliable the score is.

## Asks

- Still looking for labelled listing-quality examples.
