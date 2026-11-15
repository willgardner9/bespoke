# career.yaml schema

`career.yaml` lives in the person's own directory, never in this repo. It stores **raw facts, not CV prose**: plain statements of what happened, so `tailor` can reword them per job without losing the truth. The validator is `tests/schema.py::validate_career`.

## Top level

| Key | Type | Notes |
|-----|------|-------|
| `profile` | mapping | `name` (required), `email`, `phone`, `location`, `links[]` |
| `roles` | list | Non-empty. Newest first. See below |
| `education` | list | `institution`, `qualification`, `start`, `end` (`YYYY-MM`) |
| `certifications` | list | `name`, `year` |
| `skills` | list | Plain strings, written as the person would say them |
| `achievements` | list | Plain strings |
| `preferences` | mapping | `target_roles[]`, `avoid[]`, `locations[]` |

## Role

`id` (e.g. `r3`), `company`, `title`, `start`, `end`, `location`, `context`, `facts[]`.

- `start` and `end` are `YYYY-MM`; `end` may also be `present`.
- `context` is one or two plain sentences on the team or business, so scope is clear.

## Fact

| Key | Required | Notes |
|-----|----------|-------|
| `id` | yes | `<role id>-f<n>`, stable once written; `fitting.md` cites these |
| `what` | yes | What was done, in plain words |
| `how` | no | How: process, tools, decisions, trade-offs |
| `outcome` | no | What changed as a result |
| `metric` | no | A number, only if the person gave one |
| `source` | yes | `cv`, `linkedin` or `interview` |

## Rules

- Never store salary, anywhere. The validator rejects any `salary` key.
- Never write a fact the person did not say or supply in a document. Gaps stay gaps.
- Keep scope words as the person used them ("led", "contributed to", "owned", "supported"); `tailor` is checked against them.
- Re-running `measure` adds roles and facts; it never deletes existing ones.
