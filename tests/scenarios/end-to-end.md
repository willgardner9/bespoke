# Scenario: bespoke (end to end)

How to run: a fresh agent follows the `bespoke` orchestrator skill (and the skills it routes to), or for the baseline has no skill. Each case runs in its own temp directory. The agent logs `transcript.md` (`[Agent]` lines; every task-list change as `[tasks] ...`; every helper as `[helper] ...`). Fetching a web page is simulated: a company site fetch returns `fixtures/company-site.sample.md`. The candidate (Zoë) answers questions briefly, knows only what is in `fixtures/career.sample.yaml`, and has never used dbt. Google Chrome (`--no-sandbox` as root) and `pdftotext` are installed.

## Cases

- Case 1: an empty directory. The user says: "Here's a job ad, can you do my application?" and pastes `fixtures/jobad.sample.md`.
- Case 2: a directory holding `career.yaml` (copy of `fixtures/career.sample.yaml`). The user pastes `fixtures/jobad.sample.md` and the company site.
- Case 3: continuing in case 2's directory. The user pastes `fixtures/jobad.second.md` (a different role at the same company).
- Case 4: a directory holding `career.yaml`. The user pastes `fixtures/jobad.weak.md` and the company site; the candidate, when asked, says she does not want to continue.

## Observations (each must hold)

- E1 (case 1): with no `career.yaml`, the agent sends the user to the `measure` skill first and creates no folder, `fitting.md` or CV.
- E2 (case 2): a single task list covers the fitting and tailoring phases; afterwards `northwind-analytics/` holds `job-ad.md`, `fitting.md` (parses with `parse_fitting`), `cv.html` and `cv.pdf`; "dbt" is absent from the CV text.
- E3 (case 3): the new application goes to `northwind-analytics-analytics-lead/`; the first folder is untouched.
- E4 (case 4): `fitting.md` says `weak`, the agent stops and asks, and no `cv.html` or `cv.pdf` is created.

## Baseline (no skill)

Run 2026-11-15, all four cases, no skills.

- E1 FAIL: with no `career.yaml` the agent interviewed the user ad hoc and wrote a CV straight from her answers, saved no career file, and left `cv.html`/`cv.pdf` loose in the working directory.
- E2 FAIL: no company folder, no `job-ad.md`, no `fitting.md`, no task list; `cv.html` and `cv.pdf` dropped in the working directory.
- E3 FAIL: the second ad produced `cv-analytics-lead.html/pdf` beside the first in the same directory, not in its own folder.
- E4 FAIL: it correctly declined to write a CV once she said no, but wrote no `fitting.md` (so no `weak` verdict on file).

## Result with skill

Run 2026-11-15, all four cases, with the skills loaded; helpers were unavailable so the in-sequence fallbacks ran.

- E1 pass: with no `career.yaml` the agent stopped, offered `measure`, and when the candidate declined created no folder, `fitting.md` or CV.
- E2 pass: one top-level task list (check career file, fit analysis, verdict decision, tailor, report) with the `fitting` phases nested under it; `northwind-analytics/` holds `job-ad.md`, `fitting.md` (`parse_fitting` passes, `stretch`, six must-haves), `cv.html`, `cv.pdf` (one page, "Zoë Ñuñez" intact, "dbt" absent).
- E3 pass: the second ad went to `northwind-analytics-analytics-lead/` with its own four files; the first folder's four files had identical checksums before and after.
- E4 pass: `fitting.md` says `weak`; the agent asked, the candidate declined, and no `cv.html` or `cv.pdf` was created.
