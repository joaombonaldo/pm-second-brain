---
name: team-status
description: Roll up the team's weekly digests from the shared team hub (pm-team-hub) into one short portfolio view - each person's headline and products, cross-team risks, open asks grouped by who could help, and who hasn't published. Use when the user types /team-status, or says "team status", "portfolio roll-up", "how is the team doing this week", "what did everyone publish", "who hasn't published". Primary user is the manager; any PM can run it. Reads only the hub.
metadata:
  category: team
  role: Reporter
  owner: pm-agents core
  version: "0.2.0"
  status: experimental
  brain: required
  reads: "brain/brain.yaml, <team_hub.path>/digests/, <team_hub.path>/members/, <team_hub.path>/products/"
  writes: "brain/products/<slug>/status/ (after yes)"
  preferences: ""
  requires: "python3, team-hub, git"
---

# /team-status — Reporter (shared with Connector)

## Purpose

Give the manager (or any PM) a sourced, one-screen picture of the team's week, built only from what people chose to
publish. It reads **only the hub**: it never sees, and never asks for, anyone's private brain.

## Before you start

1. Read `brain/brain.yaml`. If it does not exist, stop: "Your second brain isn't set up yet. Type **/onboard** first."
2. Read `team_hub.path`. If it is empty or the folder does not exist, stop and say:
   > Team features are off: no team hub is set up. Clone `pm-team-hub` next to `pm-agents`, then run **/onboard**
   > and give its path (usually `../pm-team-hub`).

## Inputs

- Week: default = the **latest week** that has a folder in `<hub>/digests/<YYYY>/`. The user may ask for another
  (`2026-W42`, "last week").
- Optional focus: a product, a person or a topic ("only search-related work").

## Steps

1. **Freshen the hub copy.** Run `git -C <hub> fetch`. If the copy is behind, ask "Update your hub copy first?" and
   run `git -C <hub> pull --rebase` only after yes. If fetch fails (offline, no access), say so in one line and
   continue with the local copy, noting its last commit date (`git -C <hub> log -1 --format=%cs`).
2. **Load the week's digests.** The week folder is the source of truth: list
   `<hub>/digests/<YYYY>/<YYYY-Www>/*.md` (a digest may be published a day after its week ends). Use
   `python3 scripts/brain_search.py --root <hub> --type digest --topic <t> --json` for a focus filter. Read every
   digest in full (they are short).
3. **Load context.** Read `<hub>/members/*.md` (who should publish) and the product cards of the products named in
   the digests. Read the previous week's digests only to spot risks and asks that are **still open**.
4. **Find who hasn't published.** Members (`members/*.md`, role `pm`; managers only if they published before) with
   no digest this week. If `members/` is empty, use people who published in any of the last 4 weeks. List them
   neutrally ("no digest for 2026-W42"), with the week of their last digest if any.
5. **Draft the roll-up:**
   - **Per person**: `<Name> (<products>) — <their headline, shortened if needed>` · source path.
   - **Cross-team risks**: risks that appear in ≥ 2 digests, or one person's risk that touches another person's
     product, plus risks still open from last week (marked "still open"). Each with source paths.
   - **Open asks, grouped by who could help**: for each ask/need, name the person whose `reusable`, `building`,
     `topics` or member "Ask me about" plausibly matches, and cite both files. Asks with no match go under
     "No obvious helper yet".
   - **Not published**: from step 4.
   - **Sources**: every digest and card path used.
6. **Check length**: ≤ 400 words, excluding the Sources list. Count them. Cut detail, never sources.
7. **Offer to save.** Ask: "Save this to your brain?" After yes, write
   `brain/products/<slug>/status/team-<YYYY-Www>.md` (ask which product if several; if the file exists, show a diff
   first), then `git -C brain add -A && git -C brain commit -m "team-status: <YYYY-Www>"` (warn once and carry on if
   git fails). Suggest `/connect-dots` as the next step.

## Reads

`brain/brain.yaml` (only `team_hub`), and in the hub: `digests/`, `members/`, `products/`. Nothing else: no one's
private brain, not even the user's own notes.

## Writes

Nothing by default. After yes: `brain/products/<slug>/status/team-<YYYY-Www>.md` and one brain commit. Never writes
to the hub.

## Rules

- **Only what was published.** Every statement points to a digest or product card path. If the hub doesn't say it,
  it's not in the roll-up. Never guess what someone who didn't publish is working on.
- Not publishing is a fact, not a judgement: no blame wording, no guesses about why.
- Keep people's words' meaning: shorten headlines, never upgrade them (a risk stays a risk, an ask stays an ask).
- A helper match is a suggestion ("could help"), never an assignment.
- If the requested week has no digests, say so and name the latest week that has some.

## Output

The roll-up (≤ 400 words + sources), then:

```
What changed: <nothing, or status/team-YYYY-Www.md saved + brain commit>
What needs you: <e.g. "nudge Carla Dias (no digest)", "follow up on 2 cross-team risks", or "nothing">
What was missing: <e.g. "hub copy not updated (offline)", "no members/ files, used last 4 weeks", or "nothing">
```
