# Bespoke: agentic job-application skills (design)

Date: 2026-11-15
Status: draft, awaiting approval

## Intent and why

Will wants an agentic workflow for job applications that he and his wife
can both use. Each of them should be able to turn "here's a job ad" into a
tailored, ATS-friendly CV, with an honest view of whether the job is worth
applying for, without hand-editing CVs per application.

It ships as a Claude plugin called **bespoke**, hosted in a GitHub repo.
Will's wife installs the skills from that repo; each person works in their
own directory. The skills carry the whole workflow: there is no app and no
server.

## Goals

- Build a rich, structured, truthful record of a person's career, including
  things that never made it onto their CV (`career.yaml`).
- Read a job ad and the company's website and work out what the employer
  actually wants.
- Judge honestly whether the candidate fits, and stop early if not.
- Write a CV tailored to that job from `career.yaml` only, in a plain,
  ATS-safe format, and output it as a PDF.
- Make the process visible and interactive: the user can see which phases
  and which helper agents are running and what each is doing.
- Work for any profession, not just software engineering.

## Non-goals

- No web app, SaaS, accounts or hosted service.
- No auto-submitting applications, no job searching or job-board scraping.
- No cover letters in v1 (a natural later skill).
- No multiple visual CV templates; one template, deliberately plain.
- No Word output in v1.

## Anti-goals (failure even if it technically works)

- A CV containing any claim, number, tool, title or date not traceable to
  `career.yaml`.
- Under-mirroring the ad. Keyword-heavy is fine and encouraged: the CV
  should echo the ad's exact terms and phrasing wherever it is true of the
  candidate. The only line is truth, never inventing or inflating a claim
  to hit a keyword.
- An interview that feels like filling in a form, so people give up before
  the career file is rich enough to be useful.
- Flattering the candidate in the fit verdict. A weak fit must say so.
- A setup that needs a developer to install or run (it must work for a
  non-technical user).

## Constraints

- Skills are markdown instructions, so judgement-heavy work lives there; the
  only fixed artefact is the HTML CV template, shipped inside the `tailor`
  skill.
- Users' data (`career.yaml`, job ads, CVs) lives in their own directory,
  never in the skills repo. The repo must contain no personal data.
- LinkedIn cannot be fetched automatically. Intake takes the profile's
  "Save to PDF" export, or pasted text.
- Dependencies must stay minimal. The PDF is made by headless Chrome, with
  fallbacks (see Approaches).
- UK conventions by default: UK spelling, no photo, no date of birth, two
  pages maximum.
- Target environment: Claude Code plugins installed from a GitHub repo
  (shell, subagents, task list and web fetch available). Helper agents are
  an enhancement, not a requirement: where a skill says "parallel helper
  agents", it must also work by doing the same steps one after another in
  the main thread if subagents are unavailable. The same applies to the
  mid-interview background writer (fall back to writing after each role).

## Approaches considered

How `tailor` produces the PDF (the only real build trade-off):

1. **HTML to PDF via headless Chrome, driven by the skill (picked).** The
   skill carries the HTML template. Rendering tries, in order: headless
   Chrome one-liner; the agent's own browser tool to open and export;
   finally saving `cv.html` and asking the user to print to PDF. Real
   selectable text, no install beyond a browser, template identical for
   everyone. Weakness: depends on a browser being available; mitigated by
   the fallbacks.
2. **Python with WeasyPrint.** Nicer typographic control, but needs pip
   plus system libraries (Pango), which is painful on a Mac. Rejected for
   install friction.
3. **Markdown to DOCX to PDF via pandoc.** Gives a Word file as a bonus,
   but two tools to install and a less polished PDF. Rejected for v1.

Will picked option 1, with the point that the agent's browser can do the
rendering, so no script is required.

Skill structure (my call, not discussed): three standalone skills that hand
off through files, plus a thin orchestrating skill, so each stage can be
re-run alone (for example re-tailoring without redoing the fit analysis).

## The design

### Directory layout (per person)

```
<their dir>/
├── career.yaml          built by measure, extended over time
├── <company>/
│   ├── job-ad.md        the advert as supplied
│   ├── fitting.md       what they want, plus the fit verdict
│   ├── cv.html
│   └── cv.pdf
```

The user said the output is `<company>/cv.pdf`. If a company folder exists
with a different job-ad, use `<company>-<role>` as the folder (my call).

### Plugin and skills

Plugin `bespoke`, with:

- **`measure`**: intake interview, builds `career.yaml`
- **`fitting`**: reads the job ad and company site, judges fit
- **`tailor`**: writes and renders the CV
- **`bespoke`** (orchestrator): runs fitting then tailor for a new job ad,
  and sends the user to measure first if `career.yaml` is missing.

### measure

Input: any of an existing CV, a LinkedIn "Save to PDF" export, pasted text.
Output: `career.yaml`.

Flow:

1. **Prep (parallel helper agents):** parse the CV; parse the LinkedIn
   export; research each employer so questions can be specific.
2. **Draft `career.yaml`** from the documents and show the user the roles
   it found, to confirm the list.
3. **Role-by-role interview.** One question at a time, in plain
   conversational language. For each role: the problem or goal, what the
   person did personally, how they did it (process, tools, decisions and
   trade-offs), what changed as a result, and a number if there is one.
   Ask for a specific example before accepting adjectives ("good
   communicator"). After each role, a background helper agent writes the
   answers into `career.yaml` while the interview moves on.
4. **Exploration rounds** (a deliberately open stage, because people forget
   their best material). Each round is optional and skippable:
   - proudest and hardest moments
   - work done outside the job description, unofficial responsibilities
   - things that went wrong and what changed afterwards
   - how they work: process, tools, how they decide
   - people: leading, mentoring, influencing, difficult stakeholders
   - recognition: praise, promotions, awards, things colleagues come to
     them for
   - transferable skills across fields, especially for people changing
     direction
   - what they want next and what they want to avoid
5. **Wrap up:** show thin areas (roles with no outcomes or numbers) and
   offer to dig further now or later. Re-running measure adds a new job or
   deepens an old one without redoing everything.

Storage: raw facts, not CV prose. Each role has projects and facts; each
fact records what, how, outcome, metric if any, and where it came from
(cv, linkedin, interview). Plus skills, education, certifications,
achievements, and a preferences block (target roles, deal-breakers,
location). Salary is not stored.

### fitting

Input: job ad (pasted, file, or URL) and company website, plus
`career.yaml`.

Flow:

1. **Parallel helper agents:** ad analyst (must-haves, nice-to-haves,
   keywords and exact phrasing, seniority, red flags); company researcher
   (what they do, values, tone, recent news); both write to `fitting.md`.
2. **Match:** compare each requirement against `career.yaml` and record
   evidence or "gap".
3. **Verdict:** strong, stretch or weak, with named gaps and the strongest
   matching evidence. On a weak verdict, stop and ask whether to continue.
4. If a likely-true requirement has no evidence in `career.yaml`, ask the
   user a targeted question (and add the answer to `career.yaml` via the
   measure conventions).

### tailor

Input: `career.yaml`, `fitting.md`.

Flow:

1. Select and order the facts that best answer the requirements; mirror
   the ad's exact vocabulary and keywords as heavily as the truth allows
   (job title terms, tools, methods, phrasing from the must-haves), in the
   summary, bullets and skills list; keep to two pages.
2. Fill the HTML template: name and contact line, short summary, work
   experience (title, company, dates right-aligned, bullets), education,
   skills as a plain comma-separated list. Single column, black on white,
   Arial or Helvetica, standard section headings, no icons, tables,
   columns or graphics; dates formatted like "Mar 2021 – Present".
3. Render to `cv.pdf` (fallback chain above); keep `cv.html`.
4. **Parallel check agents:** a fact-checker that traces every bullet back
   to `career.yaml` and fails on anything untraceable; an ATS checker that
   extracts the PDF text and checks reading order, headings, keyword
   coverage and page count. Fix and re-render, at most three rounds; if
   either check still fails, stop and show the user what is failing.
   Fact-checker rule: strict on facts, loose on phrasing. Every employer,
   title, date, number, tool, qualification and the scope of each claim
   (led vs contributed to, owned vs supported) must match `career.yaml`;
   rewording and reordering are allowed, inflating scope or adding detail
   is a fail.
5. Report what was emphasised, what was left out, and any gaps the user
   may want to address.

### Visibility (applies to every skill)

Each skill opens by creating a task list showing its phases, updating it as
it goes. Helper agents are given clear purpose-based names (for example
"ad analyst", "fact-checker") so the user sees what is running in
parallel. Interactive points (confirming roles, answering interview
questions, verdict on a weak fit) are visible as their own steps.

## Left to the builder

- Exact `career.yaml` schema and field names.
- Exact interview wording and question banks per exploration round.
- The HTML/CSS template details within the constraints above.
- How the Chrome path is found on macOS, Windows and Linux.
- Repo layout, plugin manifest, README for the installer.
- Test approach (sample career files and sample job ads).

## Calls I made (not agreed with Will)

- Skill structure: three standalone skills plus an orchestrator.
- Folder naming when one company has several roles.
- Exploration round topics and the optional/skippable rule.
- Salary excluded from `career.yaml`.
- Two-page cap, UK spelling and no photo or date of birth.
- Background helper agent for writing facts mid-interview.
- Target is Claude Code plugins; helper agents degrade to in-line steps.
- Fact-checker is strict on facts and scope, loose on wording; fix loop is
  capped at three rounds.
- Keyword mirroring is aggressive (per Will); the ATS checker reports any
  must-have keyword that is true of the candidate but missing from the CV.
