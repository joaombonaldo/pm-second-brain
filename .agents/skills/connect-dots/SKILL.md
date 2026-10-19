---
name: connect-dots
description: Look across the team hub's recent digests and product cards to find where PMs could work together - overlaps (two people building the same thing), reuse (one person's reusable asset matches another's need), combinations (two pieces that together enable something new) and dependencies or risks between teams - each with evidence, confidence and a next step. Use when the user types /connect-dots, or says "connect the dots", "find overlaps", "who could reuse what", "what could we build together", "are two people doing the same thing". Primary user is the manager; any PM can run it. Reads only the hub.
---

# /connect-dots — Connector

## Purpose

Turn the team's published digests into a short, ranked list of concrete collaboration opportunities, each backed by
the files it comes from. Suggestions start conversations; they are not assignments. Reads **only the hub**.

## Before you start

1. Read `brain/brain.yaml`. If it does not exist, stop: "Your second brain isn't set up yet. Type **/onboard** first."
2. Read `team_hub.path`. If it is empty or the folder does not exist, stop and say:
   > Team features are off: no team hub is set up. Clone `pm-team-hub` next to `pm-agents`, then run **/onboard**
   > and give its path (usually `../pm-team-hub`).

## Inputs

- Look-back: default **4 weeks** ending with the latest digest week; the user may ask for another span
  ("last 8 weeks").
- Optional focus: a person, product or topic ("anything that touches pricing?").

## Steps

1. **Freshen the hub copy.** `git -C <hub> fetch`; if behind, ask before `git -C <hub> pull --rebase`. If offline,
   say so in one line and use the local copy.
2. **Load the evidence.** Prefer
   `python3 scripts/brain_search.py --root <hub> --type digest --since <start of look-back> --json --limit 100`
   and `--type product-card`. If the script is missing or fails, list `<hub>/digests/<YYYY>/<YYYY-Www>/*.md` for
   the look-back weeks and `<hub>/products/*.md`. For each person and product, collect front matter `topics`,
   `building`, `reusable`, `needs` (newest week wins when they changed) plus the Risks / Asks sections.
3. **Apply the four lenses.** Only compare **different people**.
   - **Overlap**: the same or clearly similar `building` item, or ≥ 2 shared `topics` together with related work.
   - **Reuse**: a `reusable` item of A that matches a `needs` item (or an Ask) of B.
   - **Combine**: two complementary `building` items (X from A + Y from B) that together enable Z, which neither
     has alone. Always write it as a hypothesis: "If X and Y were connected, …".
   - **Dependency / risk**: B's need, risk or plan is blocked by, or depends on, A's work or decision.
4. **Test every candidate** before keeping it:
   - Can you point to the exact lines on **both** sides? If not, drop it.
   - Is the match about meaning, not just a shared word? (`quality` in "title quality scorer" vs "data quality
     audit" is not an overlap by itself.)
   - Is it based on something written, not on something missing? **Never infer from absence** ("C never mentions
     pricing, so…").
5. **Score and rank.** Confidence: **high** (explicit match on both sides, current within 2 weeks), **medium**
   (strong but partial, or one side older), **low** (plausible, thin evidence, or any Combine). Always give the
   reason. Rank by value to the team (time saved, risk avoided, new capability) × confidence. Keep **at most 7**.
6. **Write the report.** For each suggestion:
   - **Lens · title** (e.g. "Overlap · Two LLM quality scorers")
   - **Who**: people and products.
   - **What**: 1–2 sentences.
   - **Evidence**: file paths plus the specific front matter field or line, quoted briefly, e.g.
     `digests/2026/2026-W42/ana-souza.md` → building: "LLM-based title quality scorer".
   - **Confidence**: high / medium / low — reason.
   - **Next step**: one concrete action, e.g. "30-min sync between Ana and Carla to compare scoring rubrics".
   If nothing passes step 4, say clearly: **"Nothing meaningful found in the last N weeks."** Then list what would
   help (e.g. "3 of 4 digests have empty `building` lists"). Never pad the list.
7. **Offer to save.** Ask where, if anywhere:
   - **My brain** → `brain/products/<slug>/research/connect-dots-<YYYY-Www>.md` (ask which product if several),
     then `git -C brain add -A && git -C brain commit -m "connect-dots: <YYYY-Www>"`.
   - **Team hub** → `<hub>/connections/<YYYY-Www>.md`: show the exact file, write it after yes,
     `git -C <hub> add` + `commit -m "connections: <YYYY-Www>"`, then ask again before `git -C <hub> push`. If the
     push fails, keep the file and commit and explain in one line. Never force-push.

## Reads

`brain/brain.yaml` (only `team_hub`), and in the hub: `digests/`, `products/`, `members/`, earlier
`connections/` (to avoid repeating last week's suggestions without saying so). Nothing from any private brain.

## Writes

Nothing by default. After yes: one file in the user's brain (+ brain commit) and/or `<hub>/connections/<YYYY-Www>.md`
(+ hub commit; push after a second yes).

## Rules

- **Never invent overlaps.** Every suggestion cites real lines on both sides; no citation, no suggestion.
- **Never infer from absence**, and never guess what someone is doing beyond what they published.
- A Combine is always a hypothesis with low or medium confidence, never presented as a plan.
- Suggestions are framed as "could", addressed to both people equally; no ranking of people, no blame.
- If a suggestion repeats one from an earlier `connections/` report, say "repeated from <week>".
- Max 7 suggestions. Fewer, stronger ones beat many weak ones.

## Output

The ranked suggestions (or "Nothing meaningful found"), then:

```
What changed: <nothing, or saved file(s) + commit(s), pushed or not>
What needs you: <e.g. "schedule the 2 suggested syncs", "approve hub save", or "nothing">
What was missing: <e.g. "Carla has no digest in the last 2 weeks", "brain_search.py not found", or "nothing">
```
