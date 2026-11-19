# Golden Template

Stack-agnostic starting point for new projects worked on with coding agents
in Cursor or in Orca (Cursor, Claude, Antigravity, OpenCode). It carries the
development process (phases, subtask specs, progress tracking, completion
reports), agent rules and skills, ponytail and graphify. No language,
framework or product is assumed.

## Contents

| Path | Purpose |
|---|---|
| `AGENTS.md` | Agent operating model. Cursor, OpenCode and Antigravity load it directly. `CLAUDE.md` imports it for Claude Code |
| `.cursor/rules/*.mdc` | Source of truth for rules (project, ponytail, graphify, phase rules) |
| `.agents/rules/`, `.claude/rules/` | Generated from `.cursor/rules/` by `make agents-sync`. Do not edit |
| `.agents/skills/` | All skills: phase process, ponytail, graphify. `.claude/skills` is a symlink here |
| `.cursor/mcp.json`, `.mcp.json`, `.opencode/opencode.jsonc`, `.agents/mcp_config.json` | Context7 and browse MCP for Cursor, Claude, OpenCode, Antigravity |
| `docs/` | DEVELOPMENT_PLAN, PROGRESS, ARCHITECTURE, CONFIGURATION, PROMPTS |
| `docs/PROMPTS/_TEMPLATE_PHASE/` | Format reference for a phase README and a subtask |

## Start a new project

1. Create the repo from this template (GitHub "Use this template", or clone and reset the remote).
2. Fill the TODO sections in `.cursor/rules/project.mdc`, then `make agents-sync`.
3. Plan the first phase: ask the agent to use the `phase-planning` skill.
4. Run subtasks one per agent context: `Implement subtask based on @docs/PROMPTS/PHASE_1_<NAME>/1.1_<Name>.md`.
5. Once code exists, build the graph: `/graphify .` in the agent, or `graphify update .` (code only, no LLM).

## Prerequisites (per machine)

| Tool | Install | Why |
|---|---|---|
| graphify CLI | `uv tool install graphifyy` | `graphify query/path/explain/update` used by the rule and skill |
| `browse` on `PATH` | same machine setup as other Orca repos | Shared browser MCP for Claude, OpenCode, Antigravity and Cursor |
| `CONTEXT7_API_KEY` | environment of the agent process | Context7 header in every MCP config. The key is not committed |

Each agent reads its own MCP file (see the contents table). A user-level
`~/.cursor/mcp.json` is optional and not required for this repo.

## Ponytail

The rule `.cursor/rules/ponytail.mdc` (and its generated copies) keeps ponytail
(full level) on for every agent that opens the repo. If you also installed
ponytail's Cursor hooks globally, they stay silent while this rule exists, and
`/ponytail lite|ultra|off` answers with a notice. To switch levels per chat,
delete the rule and rely on the hooks (`node <ponytail>/scripts/cursor-hooks.js install`).

Skills: `/ponytail`, `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, `/ponytail-help`.

## Updating vendored tools

| Tool | Command |
|---|---|
| graphify rule and skill | `graphify cursor install` (rewrites `.cursor/rules/graphify.mdc`), then `make agents-sync`. The skill stays in `.agents/skills/graphify/` (`graphify install --platform agents --project` if you need to refresh it) |
| ponytail rule and skills | copy `.cursor/rules/ponytail.mdc` into `.cursor/rules/` and `skills/ponytail*/SKILL.md` into `.agents/skills/`, then `make agents-sync` |
| rule drift | `make agents-check` |
