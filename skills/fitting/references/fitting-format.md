# fitting.md format

Written to `<company>/fitting.md`. The parser is `tests/fitting_format.py::parse_fitting`, so keep to this exactly.

```
# Fit: <company> – <role>

Verdict: strong|stretch|weak

## Must-haves
- [met|partial|gap] <requirement, in the ad's words> — evidence: <fact id, fact id|none>

## Nice-to-haves
- [met|partial|gap] <requirement> — evidence: <fact id|none>

## Keywords
<the ad's exact terms, comma-separated, on one line>

## Company notes
<what they do, size, values and tone, anything useful for tone of the CV>

## Questions for candidate
- <a question still worth asking, one per line>
```

## Rules

- The separator before `evidence:` is an em dash with a space either side.
- `met` and `partial` must cite at least one fact id that exists in `career.yaml`. `gap` always says `none`.
- Use the ad's own wording for each requirement, so `tailor` can mirror it.
- `Keywords` holds exact terms from the ad (tools, methods, role words), not paraphrases.
- `Keywords` may include the ad's terms for requirements that are a `gap`. `tailor` mirrors a keyword only when a `met` or `partial` requirement backs it, never one from a `gap`.
- If there are no open questions, write `- none`.
