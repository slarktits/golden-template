---
name: phase-task-completion
description: >-
  Standard closing report after finishing a phase subtask (any
  docs/PROMPTS/PHASE_X/ task). Use immediately after a subtask's code and
  tests are done. Produces, in order: a short Russian summary of what was done,
  callouts of important new functions/components/variables, an optional
  step-by-step apply section (build / migrations / deploy), a PROGRESS.md
  update check, and a minimal English copy-paste prompt for the next step to run
  in a fresh agent. Use when the user says a task is finished, asks to wrap up a
  subtask, or asks "what's next" after implementing a phase task.
---

# Phase Task Completion Report

Emit this report at the end of every phase subtask, in the order below. The
report is chat output, never a file.

## Output order

```
1. Summary (RU)
2. Important entities (RU)      <- only if any were created
3. Apply steps (step-by-step)   <- only if something must be run/applied
4. PROGRESS.md check
5. Next-step prompt (EN)        <- minimal, copy-paste ready
```

Blocks 4 and 5 are emitted only AFTER the apply steps (block 3) are fully
green. If there is nothing to apply, emit 1, 2, 4, 5 in a single message.

## 1. Summary (Russian)

3-7 bullet points, plain Russian, describing what was actually implemented in
this subtask. Focus on behaviour and outcome, not a file-by-file diff dump.

```
## Итог (3.2)
- Добавил PATCH `/api/v1/profile/contact` с проверкой роли admin.
- Все три публичных ответа отдают новые поля через общий билдер.
- Тесты на валидаторы и на отсутствие утечки email - зелёные.
```

## 2. Important entities (Russian, conditional)

If the subtask introduced functions, components, classes, or variables worth
remembering (public API, shared helpers, new config keys, new env vars, new DB
columns), list them. Skip this block entirely if nothing notable was added.

```
## На что обратить внимание
- `build_public_profile(entity)` - общий билдер публичного профиля, переиспользуется во всех ответах.
- Новая переменная окружения `PROFILE_CACHE_TTL`.
```

## 3. Apply steps (conditional, step-by-step)

If the subtask requires anything to be run or applied (new build, migration,
deploy/rollout, infrastructure apply, secret sync, smoke test), do NOT dump a
script. Follow `.cursor/skills/manual-execution-stepwise/SKILL.md`:

- Optionally post a short numbered plan of the upcoming steps first.
- Then emit ONE step, state the expected output, and STOP.
- Wait for the user's output; react to it; only then emit the next step.
- On failure: fix and re-issue the SAME step, don't advance.
- Verification is its own step after any state-changing command.

Only after the last apply step is confirmed green do you proceed to blocks 4
and 5. If the subtask is pure code with no apply actions, say so in one line and
skip to block 4.

## 4. PROGRESS.md check

Re-verify `docs/PROGRESS.md` reflects this subtask (project AI Rule 4). If it
is missing or stale, update it now, then state one line confirming it's done.

```
## PROGRESS.md
Обновлён: отметил 3.2 как выполненный, добавил заметку про общий билдер.
```

If it was already updated during implementation, just confirm: `PROGRESS.md уже
актуален для 3.2.`

## 5. Next-step prompt (English, minimal, copy-paste)

Give a minimal English prompt the user can paste into a fresh agent to start the
next subtask: the next subtask file path plus a one-line instruction. No
summaries, no context dump; the fresh agent reads the prompt file itself.

Wrap it in a fenced block so it's easy to copy:

```
Implement docs/PROMPTS/PHASE_3_PROFILE/3.3_Public_Endpoint.md.
Follow existing code patterns and the project rules. Write tests and run them.
```

Determine the next subtask from the phase README "Order" table (or the numeric
sequence of files). If the next step is ambiguous, ask the user which subtask is
next instead of guessing.

## Full example (no apply actions)

```
## Итог (3.1)
- Реализовал сервис генерации ICS без персональных данных.
- Добавил endpoint `GET /api/v1/events/{token}/calendar.ics` (rate-limit 5/min, Cache-Control: no-store).
- Тесты на отсутствие PII и на rate-limit - зелёные.

## На что обратить внимание
- `CalendarService.build_ics(...)` - единая точка генерации ICS.

Применять нечего - чистый код, миграций и деплоя не требует.

## PROGRESS.md
Обновлён: 3.1 отмечен выполненным.

## Следующий шаг
Скопируй в новый агент:
    Implement docs/PROMPTS/PHASE_3_PROFILE/3.2_Contact_Settings.md.
    Follow existing code patterns and the project rules. Write tests and run them.
```
