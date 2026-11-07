# Phase N: Name

## Overview

What the phase delivers and for whom, in 2-4 sentences. What runs before it
and what depends on it. One subtask per run, in the order below. Decisions
below are not reopened inside a subtask.

## What is wrong today

| Area | Where | Problem |
|---|---|---|
| Example | `path/to/module` | What is missing or broken |

## Decisions

| Topic | Decision |
|---|---|
| Source of truth | Where the data lives and who writes it |
| Out of scope | What this phase does not do |

## Order

| # | File | Depends on |
|---|---|---|
| N.1 | [N.1_Subtask_Name.md](N.1_Subtask_Name.md) | none |
| N.2 | N.2_Next_Subtask.md | N.1 |

Which subtasks can run in any order after which.

## Hard rules

- Constraints every subtask must hold (security, compatibility, flags default OFF).
- Migrations: check the current head before adding one.
- UI subtasks go through `.cursor/skills/design-local-review/SKILL.md` before deploy.

## Copy-paste

Implement docs/PROMPTS/PHASE_N_NAME/N.M_<Name>.md
