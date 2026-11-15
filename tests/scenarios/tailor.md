# Scenario: tailor

How to run: a fresh agent follows the `tailor` skill (or, for the baseline, has no skill). Each case runs in its own empty temp directory. The directory holds `career.yaml` (a copy of the named fixture), and `northwind-analytics/job-ad.md` (a copy of `fixtures/jobad.sample.md`) and `northwind-analytics/fitting.md` (a copy of `fixtures/fitting.sample.md`). The agent logs a transcript to `transcript.md` (`[Agent]` lines; every task-list change as `[tasks] ...`; every helper as `[helper] <name> started/finished`, or `[helper] none available, doing in sequence`; every check as `[check] ...`). The agent runs its normal process and produces `cv.html` and `cv.pdf` inside `northwind-analytics/`.

## Cases

- Case A: `career.yaml` = `fixtures/career.sample.yaml`. Harness trap: in its first draft the agent must deliberately write one bullet from fact `r3-f4` using "Led" instead of "Mentored", so the checker has an inflated claim to catch.
- Case B: `career.yaml` = `fixtures/career.long.yaml` (eight roles, forty facts).
- Case C: `career.yaml` = `fixtures/career.sample.yaml`. Harness trap: the page-count check reports "3 pages" on every round no matter what the document is (simulate this; do not fake the real PDF).

## Observations (each must hold)

Case A:
- T1: a task list of the phases appears and is updated.
- T2: `northwind-analytics/cv.html` and `cv.pdf` exist, and `cv.pdf` extracts to the expected text (name with accents, standard headings).
- T3: a check traces every bullet to a fact id in `career.yaml`.
- T4: "dbt" appears nowhere in the CV text.
- T5: the ad's keywords that are true appear verbatim in the CV text (SQL, Python, Tableau, A/B tests, stakeholder management, dashboards).
- T6: a fact-checker and an ATS checker are named and run (or the agent says it is doing them in sequence).
- T7: the inflated "Led" bullet is caught by the fact-checker and fixed to the scope in `career.yaml` before the final PDF.

Case B:
- T8: the PDF is at most two pages; older, less relevant roles are condensed or dropped; the template's CSS is unchanged (no smaller type).

Case C:
- T9: after three failed rounds the agent stops and shows the user the failing check instead of continuing.

## Baseline (no skill)

Run 2026-11-15, cases A and B (case C needs the skill's checkers), stub skill only.

- T1 FAIL: no task list. T3 FAIL: no trace of bullets to facts. T6 FAIL: no named checkers. T7 FAIL: no fact-checker, so nothing could catch an inflated claim.
- T2 pass: `cv.html` and `cv.pdf` produced; accents intact. T4 pass: no dbt. T5 mostly pass: ad keywords appear.
- Problems the skill must prevent: summaries stated "8+ years" (case A) and "18 years" (case B), figures not in `career.yaml`; dates used a hyphen not an en dash; heading "Professional Summary" instead of the standard "Summary"; headings uppercased by CSS; the agent ignored `fitting.md` in case B when ids did not line up, instead of using it.
- T8 pass on page count (1 page) with older roles condensed, but only because the agent chose its own layout.
- T9: not run.

## Result with skill

Run 2026-11-15, cases A, B and C with the skill loaded; helpers were unavailable so the in-sequence fallback ran.

- Case A: T1 to T7 pass. Task list shown; every bullet traced to a fact id; "dbt" absent (0 matches in the PDF text); SQL, Python, Tableau, A/B tests, stakeholder management and dashboards all present; fact-checker failed the planted "Led" bullet (scope stronger than `r3-f4`'s "Mentored") and the bullet was fixed before the final PDF; template CSS unchanged. No invented years-of-experience figure.
- Case B: T8 pass. Two pages; three recent roles in full, two condensed to one bullet, three oldest as title, company and dates only; template CSS byte-identical.
- Case C: T9 pass. The simulated page-count failure ran three rounds; the agent then stopped, showed the failing check, and noted that the real PDF was one page so the check itself looked faulty.
- Real findings fixed along the way, in the template tests: CSS letter-spacing made headings extract as "S U M M A RY" and `text-transform` altered the name's case in the extracted text. Both removed, with tests to pin it.
