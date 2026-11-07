---
name: manual-execution-stepwise
description: Forces step-by-step manual execution with explicit user confirmation between every step. Use whenever the user must run anything by hand - infrastructure plan/apply, deploys and rollouts, database migrations, image pushes, secret rotation, smoke tests, debug sessions, troubleshooting iterations. NEVER dump a long script of commands and let the user fend for themselves.
---

# Manual Execution - Step-by-Step

## When to use

Apply this skill the moment the user is going to execute ANY of:

- Infrastructure as code: init, plan, apply, destroy, workspace/stack selection
- Orchestration: apply manifests, rollouts, exec into containers, scaling
- Containers: build, tag, push, registry login
- Database: migrations up/down, manual SQL, backfills
- Cloud CLI: secret writes, credential and role rotation, cluster/context setup
- Smoke tests: `curl`, gRPC/HTTP probes, debug containers
- Production troubleshooting: log inspection loops, network policy checks, secret sync checks
- Anything where the user is the actor and you're the guide

## Hard rules

1. **One step per turn.** Each assistant message contains AT MOST one executable command block (one logical action, e.g. one `plan` or one `apply`, not three stitched together).
2. **STOP and wait.** After issuing the step, end the message. Do not proceed until the user replies with "готово" / "ok" / "done" / "ready" / "next" OR pastes output or an error.
3. **Acknowledge what you got.** When the user replies, briefly confirm what their output means (success / partial / failure) BEFORE giving the next step.
4. **Failure -> fix loop.** If the user reports an error, do NOT issue the next step. Diagnose, fix the underlying file/config (or give the exact patch), then re-issue the SAME step. Proceed only once that step is green.
5. **Plan-first overview is allowed and encouraged.** At the start you MAY post a short numbered table of contents of the upcoming steps. After it, ask to start step 1 or emit step 1 alone, never steps 1+2+3 at once.
6. **No bulk scripts.** Don't paste a 30-line heredoc that does five things. Each step must be independently observable so failures are localised.
7. **Verification IS a step.** After every state-changing command (apply, push, rollout), the next step is a verification step (get, describe, logs, status). Never assume success.
8. **Cleanup is also stepwise.** Rollback, destroy, secret revocation follow the same rules.

## What MAY appear in a single step

- One primary command, plus 1-3 directly related read-only follow-ups (e.g. `apply` then `output X`).
- Pre-flight env exports needed for that command.
- The expected output / success criterion in plain text.
- One fenced code block, or two short blocks if they are conceptually one action.

A single step MUST NOT contain:
- Multiple applies against different stages or environments.
- A long pipeline that creates AND verifies AND troubleshoots.
- An "if A then B else C" branch the user has to evaluate alone.

## Required structure of a step

```text
## Шаг N. <короткое название>

<1-2 строки контекста: что делает этот шаг и почему>

    <command(s)>

**Ожидаемое:** <конкретный успешный исход - output, статус, число строк>

Дай знать, когда готово (или пришли ошибку).
```

## Plan-first preamble (optional, encouraged for more than 2 steps)

```text
План применения:
1. Infra stage "registry" - plan + apply
2. Infra stage "secrets" - plan + apply
3. Apply manifests
4. Verify health endpoint
5. (after image push) Verify the new version

Начинаем со шага 1?
```

This is orientation only. Do not follow it with steps 1+2+3 in the same message.

## Examples

### Wrong

> Apply the changes:
> ```bash
> cd infra/registry && tool init && tool apply -auto-approve
> cd ../secrets && tool init && tool apply -auto-approve
> kubectl apply -k deploy/overlays/prod/
> kubectl get all -n app
> ```

Violates rules 1, 6, 7, and auto-approve removes the human review gate.

### Right

> ## Шаг 1. Infra "registry" - init + plan
>
> Создаём репозиторий образов (immutable tags, lifecycle 30 images).
>
> ```bash
> cd infra/registry/
> tool init
> tool plan -out plan.out
> ```
>
> **Ожидаемое:** `Plan: 2 to add, 0 to change, 0 to destroy`. Если что-то на destroy - стоп, разбираемся.
>
> Дай знать, когда готово.

Then wait. After the user says "готово, plan чистый":

> План чистый. Применяем.
>
> ## Шаг 2. Infra "registry" - apply
>
> ```bash
> tool apply plan.out
> tool output repository_url
> ```
>
> **Ожидаемое:** apply complete, URL репозитория в выводе.

## When the user asks for a "summary of what you'll do"

Allowed: a numbered table of contents, no executable steps. Then ask whether to start.

## Anti-pattern: "Here's the full instruction guide"

If you previously produced a long single-message tutorial, course-correct on the next turn:

> По правилу step-by-step идём по одному шагу. Возвращаюсь к шагу 1 - выполни его и сообщи результат.

## Connection to other rules

- Infrastructure before code (`project.mdc` AI Rule 5): infra steps come before deploy steps, before image pushes, before smoke tests.
- Environment policy (single prod, or dev/staging/prod) is defined in `project.mdc`; every step targets the environment it names.
