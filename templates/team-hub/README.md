# pm-team-hub

The shared place where our PM team publishes **one short weekly digest per person** and keeps **one card per
product**. The manager and every PM read it to see where the portfolio stands and to spot overlaps, reuse and things
we could build together.

Each PM's real notes stay in their own private second brain (`pm-agents/brain/`). This repo never holds brain files.

## The privacy rule (please read)

A digest is a **summary you write from your brain, not a copy of it**. You always see the exact text and say yes
before anything is pushed. A digest must never contain:

- meeting transcripts or quotes;
- notes about people, or an opinion attributed to a named colleague ("Marco thinks…");
- your interpretations about people;
- anything you marked `share: private`, or wrapped in `<!-- private -->` … `<!-- /private -->`;
- numbers, customer names or dates you did not approve in the preview.

What belongs here: what you worked on, product decisions you can share, what you observed about the product, the
hypotheses you are testing, and what you need from others.

If something private was pushed by mistake, tell the manager; it can be removed from the latest version, but git
history keeps it, so the preview step is what really protects you.

## Folder map

```
pm-team-hub/
├── README.md                               # this file
├── members/<person-slug>.md                # who you are, role, products, focus areas (one per person)
├── products/<product-slug>.md              # product card: mission, focus, building, reusable, needs
├── digests/<YYYY>/<YYYY-Www>/<person-slug>.md   # one weekly digest per person, e.g. digests/2026/2026-W43/ana-souza.md
└── connections/<YYYY-Www>.md               # optional connect-dots reports the manager chooses to share
```

Templates for these files live in the `pm-agents` repo: `templates/team-hub/member.md`, `templates/digest.md` and
`templates/product-card.md`. You do not need to write them by hand; `/publish` does it with you.

## How to join

1. Ask the manager for access to the `pm-team-hub` GitLab repo (read and write).
2. Clone it **next to** your `pm-agents` clone, so both folders sit side by side:

   ```
   cd <the folder that contains pm-agents>
   git clone <pm-team-hub URL>
   ```

3. In `pm-agents`, start Devin and run **/onboard**. When it asks about the team hub, give the path
   (usually `../pm-team-hub`) and your person slug (e.g. `ana-souza`). It is saved in your `brain/brain.yaml`.
4. Your first **/publish** also creates your `members/<person-slug>.md` (you approve it first).

## Weekly rhythm

| When | Who | What |
|------|-----|------|
| Every day | PM | Drop transcripts in `brain/inbox/` → `/ingest` |
| Friday | PM | `/sweep` (tidy the brain) → approve → `/publish` (digest + product card) → approve → push |
| Monday | Manager (or any PM) | `/team-status` for the roll-up, then `/connect-dots` for overlaps and reuse |

## House rules

- One digest per person per week. Re-publishing the same week shows a diff first.
- Never edit someone else's digest. Product cards are edited by their owner (via `/publish`).
- Topics are free kebab-case words, but reuse an existing one when it means the same thing
  (`llm-evaluation`, not a new `llm-evals`). `/publish` checks this for you.
- Connect-dots suggestions are hypotheses for a conversation, not assignments.
