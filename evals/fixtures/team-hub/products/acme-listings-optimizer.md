---
type: product-card
product: acme-listings-optimizer
owner: ana-souza
topics: [llm-evaluation, prompt-design, bulk-edit]
building:
  - "LLM-based title quality scorer"
  - "Bulk title edit for up to 100 listings"
reusable:
  - "Prompt library for product titles and descriptions"
  - "Title quality rubric (clarity, attributes, marketplace rules)"
needs:
  - "A labelled set of good and bad listing titles to calibrate the scorer"
updated: 2026-10-16
---

# Acme Listings Optimizer

## Mission

Help marketplace sellers with large catalogs keep every listing accurate and attractive,
with AI-written titles they can trust and edit in bulk.

## Current focus

Bulk title edit for the 2.4 release and a quality score for generated titles.

## What we're building

- LLM-based title quality scorer
- Bulk title edit for up to 100 listings

## Reusable assets

- Prompt library for product titles and descriptions (ask Ana Souza)
- Title quality rubric (ask Ana Souza)

## Needs

- A labelled set of good and bad listing titles to calibrate the scorer (data)

## Recent decisions

- [decision] Bulk edit ships in 2.4 behind a feature flag, beta sellers first. — 2026-10-13
- [decision] First bulk edit release is capped at 100 listings per batch. — 2026-10-06
