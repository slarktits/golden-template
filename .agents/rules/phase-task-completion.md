---
trigger: always_on
description: "Standard closing report after finishing any phase subtask"
---

<!-- Generated from .cursor/rules/phase-task-completion.mdc by scripts/sync_agent_config.py. Edit the source, then run `make agents-sync`. -->

# Phase Task Completion

After finishing any phase subtask (docs/PROMPTS/PHASE_X/), emit the closing
report in this order: (1) short Russian summary of what was done, (2) callouts
of important new functions/components/variables, (3) step-by-step apply
instructions if anything must be run/built/migrated, (4) a PROGRESS.md update
check, (5) a minimal English copy-paste prompt for the next step.

The report is chat output, never a file. Full workflow:
`.agents/skills/phase-task-completion/SKILL.md`.
