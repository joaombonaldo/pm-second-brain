# .devin/ — Devin CLI configuration

| File | Committed? | What it holds |
|------|------------|---------------|
| `config.json` | Yes | Shared permissions (what the agent may do without asking). No secrets. |
| `mcp_config.json` | Yes | Shared MCP server **placeholders** for Jira, Confluence and GitLab. |
| `mcp_config.local.json` | No (git-ignored) | **Your** real MCP endpoints and tokens. Overrides the shared file. |

## Connecting Jira, Confluence and GitLab

Open question Q1 in `docs/HANDOFF.md`: it is not yet confirmed that Dell's MCP servers work from Devin CLI on a
laptop, or how they authenticate. Until then:

1. Ask the Devin admin for the MCP endpoints Dell uses.
2. Create `.devin/mcp_config.local.json` with the same shape as `mcp_config.json`, real URLs instead of the
   `<DELL_..._MCP_URL>` placeholders, plus whatever auth the server needs. You can also run `devin mcp add`, which
   writes to the local file by default.
3. Never put tokens in `mcp_config.json` — it is shared with the whole team.

The `url` / `transport` fields follow the remote-server example in the
[Devin CLI MCP docs](https://docs.devin.ai/cli/extensibility/mcp/configuration); confirm against Dell's servers.

If MCP doesn't work from the CLI, every skill has a manual fallback (pasted text or a CSV export), and the skills in
`.agents/skills/` also work in the Devin web app, which has Dell's Jira/Confluence/GitLab connections.
