---
name: delegate-cheap-subagent
description: >-
  Offload trivial, self-contained parts of a larger task to a cheaper subagent
  model to keep the orchestrator's context clean. Use when implementing a
  phase prompt (docs/PROMPTS/PHASE_X/) or any multi-part task that contains
  mechanical, low-judgement chunks: writing tests from a given spec table,
  running tests/lint/typecheck and reporting failures, scaffolding boilerplate
  from an existing pattern, bulk find-and-replace, or gathering command output.
  The orchestrator stays the decision-maker; only execution of a self-contained
  chunk is delegated, and only a clean result comes back.
---

# Delegate Trivial Work to a Cheaper Subagent

## Core idea

You (the orchestrator) keep the judgement, planning, security review, and
integration. You push mechanical, self-contained chunks down to a cheaper
subagent via the `Task` tool. The subagent runs in an isolated context, does the
grunt work (reading files, running commands, retrying), and returns only a clean
summary. Your context never sees the intermediate noise.

## Default model

Delegate with `model: composer-2.5-fast`.

Escalate only if the chunk needs more reasoning than pure mechanics (e.g. a
non-trivial refactor across files following a pattern):

| Need | Slug |
| --- | --- |
| Default - mechanical work | `composer-2.5-fast` |
| Escalation, code-heavy | `claude-sonnet-5-5-high` |

Never delegate to another model without asking.

**Model slugs go stale.** Cursor rotates them, and passing a slug that is no
longer offered fails the `Task` call outright. The authoritative list is the one
in your own `Task` tool description at runtime, not this file. If a slug here is
absent from that list, pick the nearest equivalent from it and update this table
in the same session. Do not silently fall back to the orchestrator model; that
defeats the point of the skill.

**Subagent types also vary.** Use a `shell` type for command runs when the
`Task` tool offers it, otherwise `generalPurpose`. Use `explore` for read-only
codebase search.

## When to delegate (auto)

Delegate a chunk when ALL of these hold:

- It is **self-contained**: everything needed can be written into the subagent
  prompt (spec, file paths, exact commands, acceptance check). The subagent does
  NOT see your conversation or the phase prompt unless you paste it in.
- It is **mechanical / low-judgement**: little architectural or security
  decision-making.
- It is **medium-sized**: worth the startup and context-passing overhead (a
  one-liner usually is not; a noisy multi-step command run still is, because it
  keeps logs out of your context).

Good candidates:

- Write test files from a fully specified test table -> `generalPurpose`.
- Run the test suite / linter / type checker and return only failures -> `shell`.
- Scaffold an endpoint/component by copying an existing sibling pattern -> `generalPurpose`.
- Bulk rename / find-and-replace across many files -> `generalPurpose`.

## Hard triggers - delegate without deliberating

Slow, noisy chores that produce hundreds of lines you do not want in the
orchestrator's context. Fill in the project's real commands in `project.mdc`.

| Chore | Subagent | Background? |
| --- | --- | --- |
| Full test suite of any app or service | `shell` | yes |
| Linter / type checker / formatter check | `shell` | no |
| Production build of any app | `shell` | yes |
| Infra `fmt -check` / `validate` | `shell` | no |
| Writing a test file from a spec table already written down | `generalPurpose` | no |
| Broad codebase exploration ("where is X handled", "audit Y across the repo") | `explore` | no |

Use `run_in_background: true` for anything expected to exceed roughly two
minutes, then keep working. You are notified when it finishes; do not poll it.

## Standard recipe

```
Task(subagent_type="shell", model="composer-2.5-fast", run_in_background=true,
     description="Test and lint run", prompt="""
Repo: <absolute repo path>. From `<app dir>`, run in order:
  1. <lint command>
  2. <test command>
  3. <typecheck command>
Do NOT fix anything and do NOT edit any file.
Return ONLY: per command, pass/fail plus the final summary line verbatim; a
deduplicated list of failing test IDs grouped by file; and one line per
distinct failure cause. No full logs, no tracebacks, no file contents.
""")
```

## When NOT to delegate

Keep in your own context:

- Security-sensitive logic (auth gates, tenant isolation, PII/leak checks,
  signatures, consent).
- Anything needing the full phase/domain context or cross-cutting judgement.
- Trivial one-shot edits you can do faster inline.
- Final review: always sanity-check the subagent's result before integrating.
  You own correctness.

## How to write the subagent prompt

The subagent starts fresh. Give it a complete, standalone brief:

1. **Context block**: paste the relevant spec (exact test table, schema fields,
   target paths). Do not assume it knows the phase.
2. **Exact task**: what to produce, in which file(s).
3. **Constraints**: project conventions (no emojis in code, strict typing,
   follow the pattern in <sibling file>). If `graphify-out/graph.json` exists,
   include the graphify rule from `.cursor/rules/graphify.mdc`.
4. **Acceptance check**: the command it must run to self-verify.
5. **Return contract**: "Return ONLY: (a) files created/modified, (b) final
   pass/fail of the acceptance command, (c) failures verbatim. Do not dump full
   file contents or command logs."

## Parallelism

If several independent chunks exist (e.g. two test files, or tests plus a lint
run), launch multiple `Task` calls in a single message so they run in parallel.
