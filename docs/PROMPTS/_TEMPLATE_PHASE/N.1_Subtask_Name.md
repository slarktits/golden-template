# N.1 Subtask Name

## Goal

One or two sentences: the observable outcome when this subtask is done.

## What to Implement

### Component or module (`path/to/module`)
- Responsibility 1
- Responsibility 2

### Endpoints / hooks / commands

| Name | Input | Returns |
|------|-------|---------|
| `GET /api/v1/resource` | query params | paginated list |

### Data / config

| Column or key | Rule |
|---|---|
| `example_field` | type, nullable, default, validation |

## Files to Create
- `path/to/new_file`

## Files to Modify
- `path/to/existing_file` - what changes

## Dependencies
- Packages or services, with versions if they matter

## Tests
- Behaviour 1 is covered (input -> expected result)
- Error case returns the documented error shape
- Security / leak check if data crosses a trust boundary

## Notes
- What to avoid, risks, references to other subtasks (e.g. "N.2 adds enforcement")

## Done when

Tests pass, lint and typecheck clean, `docs/PROGRESS.md` updated, related docs match the behaviour.
