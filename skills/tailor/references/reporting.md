# Reporting

How to tell the person what is happening while you work, and what you hand back. The person is often not watching, and the task list already shows progress, so reports are short and look the same every time.

## While you work

- The task list is the progress display. Keep it updated; do not describe it in chat.
- Your first message is one sentence on what you are about to do.
- After that, write nothing between tool calls except:
  1. a **round line** when a check round or a review round finishes (format below);
  2. a question or decision the person has to answer, in one sentence.
- Do not announce what you are about to do, do not say you are waiting for a helper, and do not recap a result the task list or a round line already shows. Detail belongs in the final report.

## Round lines

One line per finished round, in this shape. The parser is `tests/progress_format.py::parse_round_line`.

```text
Check · round 1 of 3 · fact-checker ✗ 3 issues · ATS checker ✗ 1 issue · fixing
Check · round 2 of 3 · fact-checker ✓ · ATS checker ✓
Review · round 1 of 2 · recruiter ✗ 2 must-fix · ATS reviewer ✓ · improving
Review · round 2 of 2 · recruiter ✗ 1 must-fix · ATS reviewer ✓ · stopping
```

- `Check` has at most 3 rounds and names `fact-checker` then `ATS checker`. `Review` has at most 2 rounds and names `recruiter` then `ATS reviewer`.
- `✓` is a pass. `✗` is followed by a count: `issue` or `issues` for a check, `must-fix` for a review (nice-to-haves are not counted).
- The last part is the next move and appears only when something failed: `fixing` (check) or `improving` (review) while rounds remain, `stopping` on the last allowed round.
- The separator is a space, a middle dot and a space.

## The final report

The report is the scorecard below and nothing longer. Open with the `Files` line, and close with at most one sentence offering a next step, such as running `measure` to fill the open items. Do not add a prose summary of the tables. The parser is `tests/progress_format.py::parse_scorecard`.

```markdown
**Files:** `northwind-analytics/cv.pdf` and `cv.html` · 2 pages · led with SQL, Tableau and A/B testing

| Must-have | Fit | On the CV |
|---|---|---|
| Strong SQL for analysis and reporting | met | SQL views behind the weekly trading dashboard (Brightwell Retail) |
| Python for data analysis | met | A/B tests analysed in Python (Brightwell Retail) |
| Building dashboards in Tableau | met | Rebuilt weekly trading dashboard in Tableau (Brightwell Retail) |
| Designing and analysing A/B tests | met | Checkout A/B tests, +3.1% conversion (Brightwell Retail) |
| Experience with dbt for data transformation | gap | not claimed |
| Excellent stakeholder management | met | Weekly prioritisation call across merchandising, finance and product (Brightwell Retail) |

**Keywords:** on the CV: SQL, Python, Tableau, A/B tests, stakeholder management, dashboards, data analysis, reporting · not on the CV: dbt (gap)

| Stage | Rounds | Result |
|---|---|---|
| Checks | 2 of 3 | passed |
| Review | 2 of 2 | passed |

**Changed by the loops:**
- Cut the summary's third sentence, which repeated two bullets
- Moved the trading dashboard award up beside the dashboard bullet

**Open items:**
- Needs a number: the stock-out reduction on the demand forecast (r2-f2)
- Asked for by reviewers, cannot evidence: add dbt to the skills
```

- **Must-haves table.** One row per entry under `Must-haves` in `fitting.md`, in the same order. The first column is the requirement in the ad's words, without any `(shared: …; missing: …)` note. `Fit` is exactly what `fitting.md` says: `met`, `partial` or `gap`. `On the CV` is the line that evidences it: up to eight words naming the bullet, then the employer in brackets. A `gap` row says `not claimed`, and only a `gap` row does. Nice-to-haves are not listed.
- **Keywords line.** Every entry under `Keywords` in `fitting.md` appears exactly once, either after `on the CV:` or after `not on the CV:` with the reason in brackets (`gap` or `not evidenced`). Write `none` when everything is on the CV.
- **Run table.** One row for `Checks` and one for `Review`, with `n of m` rounds and `passed` or what is still failing. If the review was skipped because helpers were unavailable, the row is `| Review | skipped | no helpers available |`.
- **Changed by the loops.** At most five lines, one change each, taken from the check and review rounds. Leave the whole block out if nothing changed.
- **Open items.** Only the lines that apply, one line each, from this list. If none apply, write `**Open items:** none`.
  - `Needs a number:` bullets reworded or dropped for want of a figure, with the fact id.
  - `Skills left off (no fact names them):` skills in `career.yaml` that no fact evidences.
  - `Reframes (ad term -> fact id):` every ad term used for the candidate's own work.
  - `Asked for by reviewers, cannot evidence:` suggestions you could not make because no fact supports them.
  - `Still open after round two:` any review `must-fix` still standing, word for word.
  - `Left out:` anything relevant dropped to keep two pages.
