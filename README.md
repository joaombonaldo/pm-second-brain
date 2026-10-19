# pm-agents

A team of AI agents that helps you run your product, with a **second brain** (your product memory) at its center.
You clone this folder, open it with Devin CLI, and talk to it. Your notes stay on your laptop.

**The team**

- **Brain Keeper** remembers meetings, decisions and people, and answers questions from that memory.
- **Backlog Writer** turns ideas and decisions into user stories.
- **Release Manager** writes release notes for your users.
- **Reporter** drafts your weekly status and publishes a short weekly digest to the team hub.
- **Connector** looks across the team's digests for overlaps, reuse and things you could build together.

## Quick start (about 15 minutes)

### 1. Prerequisites

- **Devin CLI** installed and signed in. Check by typing `devin --version` in a terminal.
  Install guide: https://docs.devin.ai/cli
- **git** installed (`git --version`).
- **Optional: Jira / Confluence access through Devin (MCP).** The Jira-based parts (creating stories, pulling sprint
  stories) need it. Whether this works from Devin CLI on a Dell laptop is still being confirmed (Q1 in
  [docs/HANDOFF.md](docs/HANDOFF.md)). Everything also works without it: you paste text or a CSV export instead.

### 2. Clone and start

```bash
git clone <pm-agents GitLab URL>
cd pm-agents
devin
```

### 3. Set up your brain

In Devin, type:

```
/onboard
```

It asks you up to 7 short questions (your name, PM or manager, your product, Jira key and Confluence space, main
stakeholders, who you write release notes for, and optionally where your team hub is) and creates your personal
`brain/` folder. `brain/` is never pushed to the shared repo; it keeps its own private version history.

Have a second product? Run `/onboard` again later to add it.

### 4. Feed it your first meeting

Download a Teams transcript:

1. In Teams, open the meeting's **chat**.
2. Click the **Recap** tab.
3. Open **Transcript**.
4. Click **Download** and choose **.vtt** (best) or **.docx**.
5. Save the file into the `brain/inbox/` folder of your pm-agents clone.

Then type:

```
/ingest
```

You get a meeting note with summary, decisions, action items and open questions. Anything that would change your
product pages or decision log is shown to you first and only saved after you say yes.

No transcript? Paste your meeting notes straight into the chat after `/ingest`.

### 5. Ask your brain

```
/ask what did we decide about the pricing page?
```

Answers come with the file and date they came from. If the brain doesn't know, it says so.

## Command cheat sheet

| Command | What it does | Who |
|---------|--------------|-----|
| `/onboard` | Create your brain, add another product, or connect the team hub | Brain Keeper |
| `/ingest` | Turn every file in `brain/inbox/` into meeting notes; one approval at the end | Brain Keeper |
| `/ask <question>` | Answer from your brain (and the team hub for team questions), with sources | Brain Keeper |
| `/decision <what>` | Log a decision from chat; offers to mark an older conflicting one as replaced | Brain Keeper |
| `/sweep` | Weekly tidy-up: duplicates, contradictions, stale notes, topic pages | Brain Keeper |
| `/user-story <idea>` | Draft user stories; create Jira issues only after you confirm | Backlog Writer |
| `/release-notes <version>` | Draft release notes as an HTML page | Release Manager |
| `/weekly-status` | Draft this week's status plus a short paste-ready version | Reporter |
| `/publish` | Write your weekly digest + product card; you approve the exact text before it reaches the hub | Reporter |
| `/team-status` | One-screen roll-up of everyone's digests, risks, asks, who hasn't published | Reporter / Connector |
| `/connect-dots` | Find overlaps, reuse and joint opportunities across the team, with evidence | Connector |

You can also just ask in plain words ("write release notes for sprint 42") and the right skill is picked.

## Skills marketplace

Every skill the team can use is listed in [CATALOG.md](CATALOG.md), grouped by category, with its status
(`stable` or `experimental`), owner and what it needs. Every skill reads your `brain/brain.yaml` and
`brain/preferences/`, so it works on your product unchanged. Ask "what can you do?" in Devin for a quick tour.

Built a useful workflow? Turn it into a skill for everyone: [CONTRIBUTING.md](CONTRIBUTING.md) explains how
(template, one eval scenario, `python3 scripts/validate.py`, merge request).

## Weekly rhythm

- **Every day:** drop transcripts in `brain/inbox/` → `/ingest`.
- **Friday:** `/sweep` → approve → `/publish` → approve.
- **Monday (manager):** `/team-status`, then `/connect-dots`.

## Team hub setup

The team hub is a small shared GitLab repo, `pm-team-hub`, where each person publishes **one short digest a week**
and keeps **one card per product**. It never holds brain files: your notes stay private.

1. **One person creates it** (usually the manager): make an empty GitLab repo `pm-team-hub`, copy everything from
   `templates/team-hub/` in this repo into it, commit and push. Give every PM read and write access.
2. **Everyone clones it next to `pm-agents`**, so the two folders sit side by side:

   ```bash
   cd <the folder that contains pm-agents>
   git clone <pm-team-hub GitLab URL>
   ```

3. **Connect it:** in `pm-agents`, run `/onboard` and choose "set up the team hub". Give the path (usually
   `../pm-team-hub`) and your person slug (e.g. `ana-souza`).

No hub yet? Everything else works; team commands just tell you they're off.

**What gets shared.** Only what you approve in `/publish`: a summary of your work, shareable decisions, asks.
Never transcripts, people notes, colleagues' opinions or anything marked `share: private`. You see the exact text
first, and pushing asks again.

## For managers

Same repo, same install. During `/onboard`, answer **manager** when asked for your role. You get your own private
brain (your work, 1:1 notes, team goals), and on Mondays:

- `/team-status`: everyone's headline, cross-team risks, open asks with who could help, who hasn't published.
- `/connect-dots`: overlaps (two people building the same thing), reuse (one person's asset matches another's
  need), combinations and dependencies, each with the digest it comes from and a confidence level.

Both read only the hub, never anyone's brain. Publishing your own digest (e.g. team priorities) is optional.

## Updating

```bash
cd pm-agents
git pull
```

Your `brain/` folder is not touched by updates.

## Backing up your brain (optional)

`brain/` lives only on your laptop. `/onboard` makes it its own small git repo, and every command that changes it
saves a commit, so you can undo (`git -C brain log --oneline`). To back it up, add a private remote by hand:

```bash
cd brain
git remote add origin <your private personal GitLab project URL>
git push -u origin HEAD
```

Keep that project **private**. Check your team's data rules first (Q3 in [docs/HANDOFF.md](docs/HANDOFF.md)).

## Make it yours

Put your own templates and persona in `brain/preferences/` and they replace the team defaults in `templates/`.
See `brain/preferences/README.md` after onboarding.

## Read more

- [docs/HANDOFF.md](docs/HANDOFF.md): why things are the way they are, decisions and open questions.
- [docs/DESIGN-v0.2.md](docs/DESIGN-v0.2.md): the team layer and memory upgrades in detail.
- [AGENTS.md](AGENTS.md): the rules every agent follows.
- [CATALOG.md](CATALOG.md) and [CONTRIBUTING.md](CONTRIBUTING.md): browse and add skills;
  [docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md): the brain contract every skill follows.
- [CONVENTIONS.md](CONVENTIONS.md): how notes in the brain are named and structured.
- [evals/README.md](evals/README.md): how to test the skills.

## Presentation

An 8-slide overview for managers and colleagues (with speaker notes): [docs/presentation/pm-second-brain-overview.pptx](docs/presentation/pm-second-brain-overview.pptx).
