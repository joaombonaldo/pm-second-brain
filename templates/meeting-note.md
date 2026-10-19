---
type: meeting
title: <Meeting title>
date: <YYYY-MM-DD>
product: <product-slug>
attendees: [<Name>, <Name>]
people: [<firstname-lastname>]       # slugs of people mentioned
topics: [<topic>]                    # 1-4 kebab-case topics; reuse existing ones (see topics/)
share: private                       # meetings are private by default
status: active
source_file: <inbox/processed/file.vtt or "pasted by user, YYYY-MM-DD">
tags: []
---

# <Meeting title> — <YYYY-MM-DD>

## Summary

- <3–5 bullets: what matters for the product>

## Attendees

- <Name> — <role, if known>

## Discussion

### <Topic>

- <Key point. Attribute opinions: "Marco thinks…">

<!-- Anything that must never leave the brain (even in a digest) goes in a private block: -->
<!-- private -->
<!-- /private -->

## Decision candidates

<!-- Claim types: observation | interpretation | hypothesis | assumption | decision. See CONVENTIONS.md. -->
<!-- Use [decision] only if someone clearly decided; name who. -->

- [decision] <What was decided>. — <YYYY-MM-DD>, decided by <Name>
- [interpretation] <Someone's view>. — <YYYY-MM-DD>, <Name>

## Action items

- [ ] <Action> — owner: <Name> — due: <YYYY-MM-DD or "not set">

## Open questions

- <Question raised but not answered> (raised by <Name>)

## Links

- <Relative links to decision records created from this meeting>

## Source

source: <inbox/processed/file.vtt or "pasted by user, YYYY-MM-DD">
