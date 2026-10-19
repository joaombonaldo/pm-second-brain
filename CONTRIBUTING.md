# Contributing a skill

Thanks for making pm-agents better for the whole team. A skill is one folder with a `SKILL.md` that tells the agent
how to do one PM job. Browse what exists in [CATALOG.md](CATALOG.md) first: improving a skill often beats adding one.

You don't need to be an engineer. If you can write a clear checklist, you can write a skill.

## Propose a new skill (about 30 minutes)

1. **Check it's new.** Read [CATALOG.md](CATALOG.md). If an existing skill is close, propose a change to it instead
   (or a preference file, see "Personal style" below).
2. **Copy the template.**

   ```bash
   cp -r templates/skill .agents/skills/<your-skill-name>
   mv .agents/skills/<your-skill-name>/eval.md evals/skills/<your-skill-name>.md
   ```

3. **Fill the front matter.** `name` (= folder name), a `description` that says what it does and when to use it
   with the user's likely words in quotes, and the `metadata` fields. Field rules:
   [docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md) §2.
4. **Write the body** in the template's sections. Follow the **brain contract**
   ([docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md) §1): read `brain/brain.yaml`, resolve
   `brain/preferences/<file>` before `templates/<file>`, cite sources, ask before durable writes, commit the brain,
   end with the 3-line summary.
5. **Add at least one eval scenario** in `evals/skills/<your-skill-name>.md` with fictional data
   ([evals/skills/README.md](evals/skills/README.md)). Run it once in a scratch clone and record the result.
6. **Run the checks** and fix what they report:

   ```bash
   python3 scripts/validate.py
   python3 scripts/catalog.py          # regenerates CATALOG.md; commit it with your skill
   ```

7. **Open a merge request** on GitLab with: what the skill does, who asked for it, the eval result, and one real
   example run (with personal or Dell data removed). Add a line to [CHANGELOG.md](CHANGELOG.md).

## Review checklist

Reviewers (any `pm-agents core` maintainer plus one PM who would use it) check:

- [ ] **Clear trigger.** The description says what and when, with quoted phrases, and doesn't collide with an
      existing skill's phrases (`validate.py` warns about overlaps — read the warning, don't ignore it).
- [ ] **Brain contract.** Uses only the entry points in the standard; works on any product; says something useful and
      points to `/onboard` when the brain is missing (unless `brain: none`).
- [ ] **Honest output.** Cites sources, uses claim types, says "That's not in the brain." instead of guessing.
- [ ] **Safe writes.** Durable brain writes are shown first; Jira/Confluence writes need an explicit yes to the exact
      preview; nothing is posted to Teams, email or chat.
- [ ] **No secrets, no Dell data.** No tokens, URLs to internal systems, customer names or real numbers in the skill
      or its eval. Fixtures are fictional.
- [ ] **Preferences, not personal style.** Tone, templates and personas come from `brain/preferences/`, never
      hard-coded for one person.
- [ ] **Metadata is true.** `reads`, `writes`, `requires` and `preferences` match the body.
- [ ] **Starts `experimental`**, with `version: "0.1.0"`.
- [ ] `validate.py` passes and `CATALOG.md` is regenerated.

## Promotion to stable

A skill moves from `experimental` to `stable` when its eval file passes and it has **≥ 3 successful real uses by
≥ 2 PMs**, noted in the merge request that flips the status. Core skills follow the same rule.

## Naming

- kebab-case, lowercase, ASCII, ≤ 64 characters, unique, equal to the folder name.
- Prefer **verb-noun** (`draft-prd`, `prep-meeting`) or a well-known PM noun (`weekly-status`).
- No personal names or product names: a skill must work for everyone.

## Versioning

`metadata.version` follows semver. Bump it in the same merge request as the change:

- **Patch** (`0.1.0 → 0.1.1`): wording, typo or bug fix; same behaviour.
- **Minor** (`0.1.1 → 0.2.0`): new optional input, step or output; existing use still works.
- **Major** (`0.2.0 → 1.0.0`): changed trigger, removed behaviour, or new writes or approvals.

## Deprecation

Set `status: deprecated`, start the description with "Deprecated: use /<other> instead.", and keep the skill for one
minor release of pm-agents. Then remove the folder and regenerate the catalog. Never delete a skill people use
without pointing them somewhere.

## Ownership

Every skill has an `owner` (a person or a team). The owner answers questions, reviews changes and keeps the eval
passing. Core skills are owned by `pm-agents core`. Leaving the team? Hand the skill to someone and update `owner`.

## Personal style

Want release notes in your own tone, or a different story format? Don't fork the skill: put your template or persona
in `brain/preferences/` (see `templates/brain/preferences/README.md`). Skills list the preference files they honour
in `metadata.preferences`.
