# Golden Template

Stack-agnostic starting point for new projects worked on with Cursor agents.
It carries the development process (phases, subtask specs, progress tracking,
completion reports), agent rules and skills, ponytail and graphify. No
language, framework or product is assumed.

## Contents

| Path | Purpose |
|---|---|
| `AGENTS.md` | Agent operating model: directive / orchestration / execution, self-annealing |
| `.cursor/rules/project.mdc` | Project rules, fill the TODO sections per project |
| `.cursor/rules/phase-task-completion.mdc` | Closing report after every subtask |
| `.cursor/rules/delegate-cheap-subagent.mdc` | Offload mechanical work to a cheaper subagent |
| `.cursor/rules/subtask-docs.mdc` | Phase docs are specs, not code |
| `.cursor/rules/ponytail.mdc` | Ponytail ruleset, always on |
| `.cursor/rules/graphify.mdc` | Query the graphify knowledge graph before raw search |
| `.cursor/skills/` | phase-planning, phase-task-completion, manual-execution-stepwise, delegate-cheap-subagent, design-local-review, browser-testing, ponytail skills |
| `.agents/skills/graphify/` | `/graphify` skill to build and query the graph |
| `docs/` | DEVELOPMENT_PLAN, PROGRESS, ARCHITECTURE, CONFIGURATION, PROMPTS |
| `docs/PROMPTS/_TEMPLATE_PHASE/` | Format reference for a phase README and a subtask |

## Start a new project

1. Create the repo from this template (GitHub "Use this template", or clone and reset the remote).
2. Fill the TODO sections in `.cursor/rules/project.mdc`.
3. Plan the first phase: ask the agent to use the `phase-planning` skill.
4. Run subtasks one per agent context: `Implement subtask based on @docs/PROMPTS/PHASE_1_<NAME>/1.1_<Name>.md`.
5. Once code exists, build the graph: `/graphify .` in the agent, or `graphify update .` (code only, no LLM).

## Prerequisites (per machine)

| Tool | Install | Why |
|---|---|---|
| graphify CLI | `uv tool install graphifyy` | `graphify query/path/explain/update` used by the rule and skill |
| Context7 MCP | Cursor Settings -> MCP, user level | Library docs lookup (AI Rule 1) |

Context7 is configured once per user in `~/.cursor/mcp.json`, not in the repo,
so no API key is committed:

```json
{ "mcpServers": { "context7": { "url": "https://mcp.context7.com/mcp", "headers": { "CONTEXT7_API_KEY": "<key>" } } } }
```

## Ponytail

The rule `.cursor/rules/ponytail.mdc` keeps ponytail (full level) on for
everyone who opens the repo, including cloud agents. If you also installed
ponytail's Cursor hooks globally, they stay silent while this rule exists, and
`/ponytail lite|ultra|off` answers with a notice. To switch levels per chat,
delete the rule and rely on the hooks (`node <ponytail>/scripts/cursor-hooks.js install`).

Skills: `/ponytail`, `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, `/ponytail-help`.

## Updating vendored tools

| Tool | Command |
|---|---|
| graphify rule and skill | `graphify cursor install && graphify install --platform agents --project` |
| ponytail rule and skills | copy `.cursor/rules/ponytail.mdc` and `skills/ponytail*/SKILL.md` from the ponytail repo into `.cursor/rules/` and `.cursor/skills/` |
