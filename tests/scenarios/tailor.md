# Scenario: tailor

How to run: a fresh agent follows the `tailor` skill (or, for the baseline, has no skill). Each case runs in its own empty temp directory. The directory holds `career.yaml` (a copy of the named fixture), and `northwind-analytics/job-ad.md` (a copy of `fixtures/jobad.sample.md`) and `northwind-analytics/fitting.md` (a copy of `fixtures/fitting.sample.md`). The agent logs a transcript to `transcript.md` (`[Agent]` lines; every task-list change as `[tasks] ...`; every helper as `[helper] <name> started/finished`, or `[helper] none available, doing in sequence`; every check as `[check] ...`). The agent runs its normal process and produces `cv.html` and `cv.pdf` inside `northwind-analytics/`.

## Cases

- Case A: `career.yaml` = `fixtures/career.sample.yaml`. Harness trap: in its first draft the agent must deliberately write one bullet from fact `r3-f4` using "Led" instead of "Mentored", so the checker has an inflated claim to catch.
- Case B: `career.yaml` = `fixtures/career.long.yaml` (eight roles, forty facts).
- Case C: `career.yaml` = `fixtures/career.sample.yaml`. Harness trap: the page-count check reports "3 pages" on every round no matter what the document is (simulate this; do not fake the real PDF).
- Case E (review loop): `career.yaml` = `fixtures/career.sample.yaml`. Harness: the helpers are scripted, so the results are repeatable. Round 1, recruiter reviewer: returns `fixtures/review.recruiter.sample.md` with one extra issue added whose quote is not in the CV, and the second issue changed to `suggest: add dbt to the skills`; round 1, ATS reviewer: `fixtures/review.ats.clean.md`. Round 2, both reviewers: `Verdict: pass`.
- Case F (round cap): as case E, but every reviewer in every round returns a `must-fix` with a real quote from the current CV.
- Case G (no helpers): as case E, but helpers are unavailable.
- Case D: `career.yaml` = `fixtures/career.vague.yaml`, ad = `fixtures/jobad.payments.md`, `fitting.md` = `fixtures/fitting.payments.md`. The profile has no phone and only a country as location; `r3` leads a squad with no `management`; several facts carry vague amounts; the `skills` list holds items no fact names. The simulated candidate answers the skill's questions: city London, phone +44 7700 900456, "technical lead, no line reports", "still writes production Rust".

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

Reporting (every case; graded from `transcript.md` and the final reply):
- T24: after the first one-sentence message, no `[Agent]` line appears between tool calls except round lines and one-sentence questions or decisions; nothing says the agent is waiting for a helper or recaps a result.
- T25: every finished check round and review round has exactly one round line in the format in `references/reporting.md`; each line passes `tests/progress_format.py::parse_round_line`.
- T26: the final reply is the scorecard and passes `parse_scorecard`; in case A, `scorecard_matches_fitting` against `fixtures/fitting.sample.md` finds no differences, the dbt row says `gap` and `not claimed`, and dbt is under "not on the CV".

Case D:
- T10: the agent asks for the missing city, phone and management type (one question each) instead of guessing, and records the answers in `career.yaml`.
- T11: no hedge from `writing-rules.md` appears in the CV text: "a big part of", "a major part in", "a big influence on", "several", "a few", "(approximate figures)".
- T12: the email-service bullet leads with the fix; the cost of the incident does not appear. The buy-vs-build fact, which has only vague figures, is reworded as a decision or dropped, and is listed in the report as "needs a number".
- T13: the newest role has at most 5 bullets, and no two lines make the same point (auditability appears once).
- T14: the first bullet of the lead role states team size and "no line reports", and one bullet shows hands-on work with the tools named.
- T15: skills are grouped, one labelled line per group, with no Kafka, Kubernetes, Elasticsearch, GCP, TypeScript, React, Git, Jira, pull requests or "ownership"; the report lists the skills left off for want of a fact.
- T16: the summary does not say "applying" or name the role or company; the contact line has a city, email and phone; the word "payments" appears nowhere as the candidate's own experience, and any ad term used for the candidate's work is in the report as a reframe with its fact id.

Case E:
- T17: the reviewers are named recruiter reviewer and ATS reviewer, and run as fresh helpers; the transcript shows each was given only the job ad text and the CV's extracted text, never `career.yaml`, `fitting.md`, the HTML or the other review.
- T18: the issue whose quote is not in the CV is discarded and not acted on.
- T19: "dbt" appears nowhere in the final CV text; the add-dbt suggestion and the `ask:` about dbt are listed in the report under what the reviewers asked for and the CV cannot evidence.
- T20: the valid `must-fix` is implemented, then the CV is re-rendered and the fact-checker and ATS checker run again and pass before round 2 starts.
- T21: round 2 runs because round 1 had an actioned `must-fix`, uses new helpers, stops on `Verdict: pass`, and the nice-to-have never starts a round by itself. The report says how many rounds ran and what changed.

Case F:
- T22: exactly two review rounds run, then the agent stops; every remaining `must-fix` appears in the report word for word.

Case G:
- T23: the review phase is skipped, the report says no blind review was done, and the agent does not write a review of its own.

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

## Baseline for case D: a real CV (observed 2026-11-16)

Not a run of this scenario. A CV the skill produced for a Payments Engineer ad, before the writing rules existed, was reviewed by a reader in the position of a recruiter or hiring manager. The review found, and case D reproduces:

- T11 FAIL: "a big part of our tech planning", "a major part in saving a contract", "a big influence on the project", "(approximate figures)", "several thousand", "a few thousand".
- T12 FAIL: the email-loop bullet led with the mistake and its cost; the buy-vs-build bullet set a few thousand against a multi-million result.
- T13 FAIL: the newest role had 7 bullets, and auditability and "regulated" repeated the summary and each other.
- T14 FAIL: "Engineering Lead" over 15 people, with no statement of line management or hands-on work.
- T15 FAIL: a 40-item skills list in one block, with Rust, Kafka, Kubernetes, Elasticsearch, GCP and IaC claimed and no role using them; Git, Jira, pull requests and "ownership" as filler.
- T16 FAIL: the summary spent a line on "Applying for the Payments Engineer role"; the contact line gave only "United Kingdom" and no phone.

## Result with the writing rules, case D

Run 2026-11-16 by the author inside the session that wrote the rules, not by a fresh agent: the rules were applied by hand to `career.vague.yaml` (with the simulated answers above), rendered, and the checker rules in `references/checks.md` were run mechanically over the extracted text. One page; no hedges; no cut or unevidenced skills; five bullets in the lead role; grouped skills extracted one labelled line per group; contact line whole. T10 (asking the questions) and the agent's own adherence to the rules are not yet tested: a fresh agent still has to run case D against the skill.

## Reporting: status (2026-11-16)

T24 to T26 have not been run; they need a fresh agent. The formats are pinned by `tests/test_progress_format.py`, which parses the examples in `references/reporting.md` and checks the example scorecard against `fixtures/fitting.sample.md`.

## Review loop: status (2026-11-16)

Cases E, F and G have not been run. They need a fresh agent following the `tailor` skill with scripted helpers. The reviewer output format itself is pinned by `tests/test_review_format.py`, and the rules in `references/review.md` by `tests/test_skill_text.py`.
