---
name: phase-planning
description: >-
  Create or extend a development phase: phase folder in docs/PROMPTS/, phase
  README with decisions and order, numbered subtask specs, a phase rule in
  .cursor/rules/, and entries in DEVELOPMENT_PLAN.md, PROGRESS.md and the
  PROMPTS index. Use when the user asks to plan a feature, add a phase, split
  work into subtasks, write phase prompts, or turn a review into fix subtasks.
---

# Phase Planning

Work is organized as phases. A phase is a folder of subtask specs. Each
subtask is one agent run. Specs describe what to build; code is written when
the subtask is executed (`.cursor/rules/subtask-docs.mdc`).

## Before writing

1. Read `docs/DEVELOPMENT_PLAN.md` and `docs/PROMPTS/README.md` for the next free phase number and dependencies.
2. Explore the code the phase touches (graphify first if the graph exists). Note what exists today and what is wrong.
3. Settle open decisions with the user (AskQuestion). Decisions are fixed in the README and not reopened inside a subtask.
4. Ask before creating or overwriting prompts unless explicitly told to.

## Files to create

| Path | Content |
|---|---|
| `docs/PROMPTS/PHASE_N_<SLUG>/README.md` | Phase plan, from `docs/PROMPTS/_TEMPLATE_PHASE/README.md` |
| `docs/PROMPTS/PHASE_N_<SLUG>/N.1_<Name>.md` ... | One file per subtask, from `_TEMPLATE_PHASE/N.1_Subtask_Name.md` |
| `.cursor/rules/phase-N-<slug>.mdc` | Short phase rule, format below |

`<SLUG>` is UPPER_SNAKE in the folder name, kebab-case in the rule name.
Subtask files are `N.M_Title_Words.md`, numbered in execution order.

## Files to update

| Path | Change |
|---|---|
| `docs/PROMPTS/README.md` | Row in the phase table, line in Quick Reference, dependency graph if needed |
| `docs/DEVELOPMENT_PLAN.md` | One line in Overview with status `Planned`, plus a short section |
| `docs/PROGRESS.md` | Phase heading with unchecked subtasks |
| `.cursor/rules/project.mdc` | Phase number in Pending Phases, one-line summary of hard rules if any |

## Phase README sections

1. Overview: goal in 2-4 sentences, what runs before and after.
2. What is wrong today (or Context): table of current state and problems.
3. Decisions: table Topic / Decision.
4. Order: table # / File / Depends on; which subtasks can run in parallel.
5. Hard rules: constraints that hold for every subtask.
6. Copy-paste: the one-line prompt to run a subtask.

## Subtask spec sections

Goal; What to implement (tables for endpoints, columns, keys, files);
Files to create / modify; Dependencies; Tests (behaviours, not code);
Notes and constraints; Done when (commands that must pass, docs to update).

Size: one agent run. If a subtask needs more than one context, split it.
Security-relevant phases end with a security/test subtask that acts as a merge gate.

## Phase rule format

```
---
description: Phase N <name>, <one-line scope>
globs: docs/PROMPTS/PHASE_N_<SLUG>/**,<code paths the phase touches>
alwaysApply: false
---
```

Body: `READ docs/PROMPTS/PHASE_N_<SLUG>/README.md first.` plus 3-6 lines with the
invariants an agent must not break. No duplicated README content.

When the phase completes: move it from Pending to Completed in `project.mdc`
with key facts and date, mark it Complete in `DEVELOPMENT_PLAN.md`, and delete
or shrink the phase rule if its invariants are now covered elsewhere.
