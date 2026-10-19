---
type: digest
person: <person-slug>                 # e.g. ana-souza (team_hub.person_slug)
role: <pm | manager>
week: <YYYY-Www>                      # ISO week, e.g. 2026-W43
products: [<product-slug>]
topics: [<kebab-case-topic>]          # brain topics active this week; reuse existing hub topics when they mean the same
building:                             # capabilities/components being built — the main matching signal
  - "<capability, e.g. LLM-based title quality scorer>"
reusable:                             # things others could reuse now
  - "<asset, e.g. Prompt templates for product titles>"
needs:                                # what would help: data, people, decisions, tools
  - "<need, e.g. Access to clickstream data for listing CTR>"
published: <YYYY-MM-DD>
---

<!-- Weekly digest: digests/<YYYY>/<YYYY-Www>/<person-slug>.md in pm-team-hub. Written by /publish.
     Body ≤ 250 words. A summary of YOUR work, never a copy of the brain (privacy rule, DESIGN-v0.2 §5):
     no transcripts or quotes, no people notes or attributed opinions, nothing marked share: private,
     no numbers/customer names/dates you did not approve in the preview.
     Leave a list empty ([]) rather than inventing items. -->

# <Full Name> — <YYYY-Www>

**Headline:** <One line: the most important thing this week.>

## Progress

- <What moved, in your words.>

## Decisions

- [decision] <Shareable product decision>. — <YYYY-MM-DD>

## Risks / blocked

- <Risk or blocker, and what would unblock it>

## Asks

- <What you need, and from whom (role or person slug), e.g. "Anyone with a CTR data pipeline — 30 min">
