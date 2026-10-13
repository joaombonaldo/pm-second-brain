# Your preferences

Files here **override the team defaults** in `templates/` (same file name wins). Skills check this folder first.

| Put this file here | It replaces | Used by |
|--------------------|-------------|---------|
| `persona.md` | `templates/persona.md` | /release-notes, /user-story |
| `release-notes.html` | `templates/release-notes.html` | /release-notes |
| `user-story.md` | `templates/user-story.md` | /user-story |
| `meeting-note.md` | `templates/meeting-note.md` | /ingest |
| `weekly-status.md` | `templates/weekly-status.md` | /weekly-status |
| `decision.md` | `templates/decision.md` | /ingest |

To customise: copy the file from `templates/` into this folder and edit your copy. Keep the `{{placeholders}}` in
HTML templates so the skill knows where to put the content.

## Free-text instructions

Anything you write below is read by every skill. Keep it short.

- <e.g. "Write in British English.">
- <e.g. "In weekly status, always mention hiring.">
