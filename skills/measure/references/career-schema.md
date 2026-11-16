# career.yaml schema

`career.yaml` lives in the person's own directory, never in this repo. It stores **raw facts, not CV prose**: plain statements of what happened, so `tailor` can reword them per job without losing the truth. The validator is `tests/schema.py::validate_career`.

## Top level

| Key | Type | Notes |
|-----|------|-------|
| `profile` | mapping | `name` (required), `email`, `phone`, `location` (a city, for example `London`, never just a country), `links[]` |
| `roles` | list | Non-empty. Newest first. See below |
| `projects` | list | Work that belongs to no role (side projects, unpaid or personal work). `id` (`p1`), `name`, `facts[]` with ids `p<n>-f<n>` and the same fact fields |
| `education` | list | `institution`, `qualification`, `start`, `end` (`YYYY-MM`) |
| `certifications` | list | `name`, `year` |
| `skills` | list | Plain strings, written as the person would say them |
| `achievements` | list | Plain strings |
| `preferences` | mapping | `target_roles[]`, `avoid[]`, `locations[]` |

## Role

`id` (e.g. `r3`), `company`, `title`, `start`, `end`, `location`, `context`, `management`, `hands_on`, `facts[]`.

- `start` and `end` are `YYYY-MM`; `end` may also be `present`.
- `context` is one or two plain sentences on the team or business, so scope is clear.
- `management` (ask for any role that leads people or a team): one plain sentence saying whether the person line-manages (and how many people) or leads technically with no line reports, and the size and make-up of the team. For example: `Technical lead of a squad of 15, no line reports` or `Line manager of 4 engineers inside a squad of 15`.
- `hands_on` (ask for any role with `management`): one plain sentence on the work the person still does themselves, in their words, with the tools. For example: `Still writes production Rust and TypeScript, about half of their time`. Leave it out if they do none.

## Fact

| Key | Required | Notes |
|-----|----------|-------|
| `id` | yes | `<role id>-f<n>`, stable once written; `fitting.md` cites these |
| `what` | yes | What was done, in plain words |
| `how` | no | How: process, decisions, trade-offs |
| `tech` | no | List of the specific languages, datastores, brokers, platforms, tools or methods used on this piece of work, as the person names them. Only what they said they used here, never what they use elsewhere |
| `outcome` | no | What changed as a result |
| `metric` | no | A number, only if the person gave one. A figure, or a bound (`at least 100,000 a day`, `up to 100,000 a day`). Never a vague amount such as "several thousand" |
| `source` | yes | `cv`, `linkedin` or `interview` |

## Rules

- Never store salary, anywhere. The validator rejects any `salary` key.
- Never write a fact the person did not say or supply in a document. Gaps stay gaps.
- Keep scope words as the person used them ("led", "contributed to", "owned", "supported"); `tailor` is checked against them.
- A vague amount ("a few thousand", "a big saving") is not a metric. Ask for a figure or a bound; if the person has neither, leave `metric` out and keep the plain wording in `outcome`.
- `skills` is the person's own list. A skill only reaches a CV when a fact evidences it, so give every skill a fact that names it in `tech`.
- Re-running `measure` adds roles and facts; it never deletes existing ones.
