# bespoke

Agentic job-application skills for Claude Code. Give it your career history once, then hand it a job ad and get back an honest fit verdict and a tailored, ATS-friendly CV.

## What it does

| Skill | What it does | Writes |
|-------|--------------|--------|
| `measure` | Interviews you about your career, from your CV, LinkedIn export and questions, and builds your career record | `career.yaml` |
| `fitting` | Reads a job ad and the company site, works out what they want, and judges how well you fit | `<company>/fitting.md` |
| `tailor` | Writes a CV for that job from your career record, in a plain format ATS systems read correctly | `<company>/cv.html`, `<company>/cv.pdf` |
| `bespoke` | Runs the whole thing for a new job ad | all of the above |

The CV only ever uses facts from your `career.yaml`. It mirrors the job ad's wording heavily where it is true of you, and never invents or inflates a claim. It is written to plain rules: results first, the tools named, no hedging, each point made once, leadership stated plainly, skills grouped and only those a role evidences. If your record lacks a city, a phone number, how you lead people or what you built something with, it asks rather than guesses.

## Install

In Claude Code:

```
/plugin marketplace add willgardner9/bespoke
/plugin install bespoke@bespoke
```

## First run

1. Make a folder for yourself, for example `~/jobs`, and open Claude Code in it.
2. If you have a LinkedIn profile, export it: Profile, then More, then Save to PDF. Put the PDF and your current CV in the folder.
3. Say: "Use the measure skill to build my career file." Answer the questions; skip any you don't want to answer.
4. For each job: paste the ad (or give a link) and say: "Use bespoke on this job ad". You get a folder named after the company with the fit analysis and `cv.pdf`.

## Your data stays yours

`career.yaml`, job ads and CVs live in your own folder, never in this repo. The repo's `.gitignore` also blocks them if you ever run it inside a clone.

## PDF rendering

`tailor` prints the CV with headless Chrome (a one-line command). If Chrome isn't available it tries the agent's browser tool, and failing that leaves `cv.html` for you to print to PDF yourself.

## Development

Tests are `pytest` (needs PyYAML; the render tests use Chrome and `pdftotext` and skip if they're missing). Skill behaviour is pinned by the written scenarios in `tests/scenarios/`.
