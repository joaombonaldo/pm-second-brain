---
type: digest
person: carla-dias
role: pm
week: 2026-W41
products: [acme-search-insights]
topics: [search-relevance, llm-evaluation, demand-trends]
building:
  - "LLM-based listing quality scorer for search relevance"
  - "Search demand trends by category"
reusable:
  - "Weekly search query volume by category"
needs:
  - "Rubric for judging listing quality consistently"
published: 2026-10-09
---

# Carla Dias — 2026-W41

**Headline:** Kicked off an LLM judge that scores listing quality to explain search ranking to sellers.

## Progress

- First version of the listing quality scorer rates title and attributes against search relevance.
- Demand trends view by category is in design.

## Decisions

- [decision] Insights show trends by category only, never per competitor seller. — 2026-10-08

## Risks / blocked

- Scorer results vary between runs; we need a stable rubric.

## Asks

- Anyone who has defined a listing or title quality rubric.
