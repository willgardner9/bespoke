# Scenario: measure

How to run: a fresh agent follows the `measure` skill (or, for the baseline, has no skill) while simulating the candidate from the persona below. It works in an empty temp directory, writes `transcript.md` (alternating `[Agent]` and `[Candidate]` turns; every task-list change as `[tasks] ...`; every helper as `[helper] <name> started/finished`, or `[helper] none available, doing in sequence`) and the final `career.yaml`. Then grade each observation.

## Persona (Zoë)

- Input document: `fixtures/cv.sample.txt`. No LinkedIn export (the agent should skip that parser, not invent one).
- Facts available: everything in `fixtures/career.sample.yaml`, but she reveals them only when asked, in her own words, and is vague at first. Asked about strengths she says "I'm a good communicator" until asked for a specific example, then gives the stakeholder prioritisation call story (r3-f3).
- Numbers: gives a number only when asked for one, and only if the fact file has one.
- Not on her CV, revealed only if asked about work outside her job description: she wrote an onboarding guide for new analysts and ran the induction herself, unofficially.
- When offered the exploration round about things that went wrong, she says she would rather skip it.
- She knows nothing beyond these facts and says so rather than inventing.

## Observations (each must hold)

- O1: A task list of the skill's phases is shown at the start and updated as work proceeds.
- O2: Prep helpers are named by purpose (CV parser, employer researcher); no LinkedIn parser is run because there is no export; if helpers are unavailable the agent says so and does the steps in sequence.
- O3: The agent lists the roles it found and asks for confirmation before interviewing.
- O4: Each agent turn in the interview contains one question.
- O5: When the candidate says "I'm a good communicator", the next question asks for a specific example.
- O6: Every exploration round is offered; the skipped round is accepted without pushback.
- O7: The unofficial onboarding guide appears in `career.yaml` as a fact with `source: interview`.
- O8: The final `career.yaml` passes `validate_career`.
- O9: No fact appears that the candidate did not say or the CV did not supply; no salary key.
- O10: The wrap-up names thin areas (roles with no outcomes or numbers) and offers to dig further.

## Part B: re-run

Given the `career.yaml` from part A, the candidate says she has just started a new role, "Lead Analyst at Fenwick Media, from 2026-10", and answers a short interview about it.

- B1: The new role is added with new ids; every earlier role and fact id is unchanged.
- B2: The output still passes `validate_career`.

## Baseline (no skill)

Run 2026-11-15, stub skill only, transcript of 17 agent turns. Result:

- O1 FAIL: no task list.
- O2 FAIL: no helpers, no mention of preparing or of unavailable helpers.
- O3 partial: roles read back, but not a confirmation step before the interview.
- O4 partial: most turns have one question, several are compound ("what was it before, and what did you change?").
- O5 pass, O7 pass (the agent happened to ask about work outside the job description once), O8 pass, O9 pass.
- O6 FAIL: only one exploration-style question; no rounds offered, nothing skippable.
- O10 FAIL: finished with "anything else?", no thin-areas review.
- B1/B2: not run.

## Result with skill

Run 2026-11-15, 47 agent turns for part A, with the skill loaded. Helpers were unavailable in the run, so the in-sequence fallback was exercised.

- O1 to O10: all pass. Task list shown and updated across six phases; CV parser and employer researchers named, no LinkedIn parser; roles confirmed first; one question per turn; "good communicator" answered with a request for an example; all eight rounds offered, round 3 skipped without pushback; onboarding guide stored as `r3-f5` with `source: interview`; file validates; wrap-up listed thin areas and offered to dig further.
- B1, B2: pass. New role added as `r4`; earlier roles and facts byte-for-byte unchanged; file validates.
- Finding fixed in the skill: part B wrote a placeholder outcome ("no outcome yet"). A rule now says to leave a field out rather than write a placeholder.
