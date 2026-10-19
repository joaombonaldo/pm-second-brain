---
type: digest
person: ana-souza
role: pm
week: 2026-W41
products: [acme-listings-optimizer]
topics: [llm-evaluation, prompt-design, bulk-edit]
building:
  - "LLM-based title quality scorer"
  - "Bulk title edit for up to 100 listings"
reusable:
  - "Prompt library for product titles and descriptions"
needs:
  - "A labelled set of good and bad listing titles to calibrate the scorer"
published: 2026-10-09
---

# Ana Souza — 2026-W41

**Headline:** Started an LLM-based scorer that rates generated titles before sellers publish them.

## Progress

- Defined the scoring rubric for titles: clarity, key attributes present, marketplace rules.
- Bulk title edit stories are ready for sprint planning.
- Cleaned up our prompt library for titles and descriptions so other teams can use it.

## Decisions

- [decision] First bulk edit release is capped at 100 listings per batch. — 2026-10-06

## Risks / blocked

- No labelled examples yet to check whether the scorer agrees with human judgement.

## Asks

- Anyone with labelled listing-quality examples: 30 minutes to compare notes.
