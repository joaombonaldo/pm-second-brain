# pm-agents

A team of AI agents that helps you run your product, with a **second brain** (your product memory) at its center.
You clone this folder, open it with Devin CLI, and talk to it. Your notes stay on your laptop.

**The team**

- **Brain Keeper** remembers meetings, decisions and people, and answers questions from that memory.
- **Backlog Writer** turns ideas and decisions into user stories.
- **Release Manager** writes release notes for your users.
- **Reporter** drafts your weekly status.

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

It asks you up to 6 short questions (your name, your product, Jira key, Confluence space, main stakeholders, who you
write release notes for) and creates your personal `brain/` folder. `brain/` is never pushed to the shared repo.

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
| `/onboard` | Create your brain, or add another product | Brain Keeper |
| `/ingest` | Turn transcripts and notes in `brain/inbox/` into meeting notes | Brain Keeper |
| `/ask <question>` | Answer from your brain, with sources | Brain Keeper |
| `/user-story <idea>` | Draft user stories; create Jira issues only after you confirm | Backlog Writer |
| `/release-notes <version>` | Draft release notes as an HTML page | Release Manager |
| `/weekly-status` | Draft this week's status plus a short paste-ready version | Reporter |

You can also just ask in plain words ("write release notes for sprint 42") and the right skill is picked.

## Updating

```bash
cd pm-agents
git pull
```

Your `brain/` folder is not touched by updates.

## Backing up your brain (optional)

`brain/` lives only on your laptop. To back it up, make it its own private git repo:

```bash
cd brain
git init
git add .
git commit -m "Brain backup"
git remote add origin <your private personal GitLab project URL>
git push -u origin main
```

Keep that project **private**. Check your team's data rules first (Q3 in [docs/HANDOFF.md](docs/HANDOFF.md)).

## Make it yours

Put your own templates and persona in `brain/preferences/` and they replace the team defaults in `templates/`.
See `brain/preferences/README.md` after onboarding.

## Read more

- [docs/HANDOFF.md](docs/HANDOFF.md): why things are the way they are, decisions and open questions.
- [AGENTS.md](AGENTS.md): the rules every agent follows.
- [CONVENTIONS.md](CONVENTIONS.md): how notes in the brain are named and structured.
- [evals/README.md](evals/README.md): how to test the skills.
