---
type: meeting
title: Bulk edit sync
date: 2026-10-06
product: acme-listings-optimizer
attendees: [Ana Souza, Marco Lima, Priya Nair]
people: [ana-souza, marco-lima, priya-nair]
topics: [bulk-edit, rate-limit, rollout]
share: private
status: active
source_file: inbox/processed/2026-10-06-bulk-edit-sync.vtt
tags: []
---

# Bulk edit sync — 2026-10-06

## Summary

- Agreed scope for bulk title editing in 2.4.
- First release capped at 100 listings per batch.
- Ship behind a feature flag, beta sellers first.

## Discussion

### Batch size

- [observation] Sellers edit between 20 and 80 listings at a time (Priya, from interviews).
- [interpretation] Marco thinks batches of 1,000 would hit the marketplace rate limit (about 50 requests per
  second per partner docs, untested).

## Decision candidates

- [decision] First release caps bulk edit at 100 listings per batch. — 2026-10-06, decided by Ana Souza
- [decision] Ship in 2.4 behind a feature flag, beta sellers first. — 2026-10-06, decided by Ana Souza

## Action items

- [ ] Updated mockups with progress indicator and failure summary — owner: Priya Nair — due: 2026-10-08
- [ ] Rate-limit spike in sandbox — owner: Marco Lima — due: 2026-10-09

## Open questions

- Does bulk edit support undo? (raised by Priya Nair)

## Links

- [Batch cap decision](../../decisions/2026-10-06-batch-cap-100.md)
- [Rollout decision](../../decisions/2026-10-06-beta-sellers-first.md)
- [Marco Lima](../../../../stakeholders/marco-lima.md)

## Source

source: inbox/processed/2026-10-06-bulk-edit-sync.vtt
