---
trigger: always_on
description: "Reminder to offload trivial self-contained chunks to a cheaper subagent"
---

<!-- Generated from .cursor/rules/delegate-cheap-subagent.mdc by scripts/sync_agent_config.py. Edit the source, then run `make agents-sync`. -->

# Delegate Trivial Work

When a task (esp. a phase prompt) contains mechanical, self-contained chunks
(writing tests from a given spec, running test/lint/typecheck, scaffolding
from an existing pattern, bulk edits), delegate them to a cheaper subagent
instead of doing them inline.

Cursor agent: `Task`, default model `composer-2.5-fast` (the slug must be in
that tool's model list). Claude, OpenCode, Antigravity: that agent's own
subagent or task tool and the cheapest model it lists. Do not call `Task` and
do not pass Cursor model slugs.

Always delegate, without deliberating first:

- the full test suite of any app or service - background
- linters, type checkers, formatters in check mode
- production builds of any app - background
- infrastructure validation (`fmt -check`, `validate`, `plan` read-only)
- broad codebase exploration - `explore`

Always demand a return contract ("return ONLY failures, no logs") and tell the
subagent not to edit files when you only want a report.

Keep judgement, security-sensitive logic, and final review yourself. Full
workflow, model table, and copy-paste recipes:
`.agents/skills/delegate-cheap-subagent/SKILL.md`.
