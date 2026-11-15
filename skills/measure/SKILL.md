---
name: measure
description: Use when someone wants to build or update their career record (career.yaml) from a CV, a LinkedIn export or an interview, so CVs can later be tailored to job ads.
---

# measure: take someone's career measurements

Build `career.yaml` in the current directory: a rich, truthful record of what this person has done, including things that never made it onto their CV. Later skills (`fitting`, `tailor`) use it as their only source of facts, so what you write here sets the ceiling on every CV.

**Principle:** store what the person said or supplied, in plain facts. Never invent, round up or tidy a claim. A gap stays a gap.

Schema: `references/career-schema.md`. Interview technique and the exploration rounds: `references/interview-playbook.md`. Read both before starting.

## Show the process

Start by creating a task list with these phases and keep it updated as you go, so the person can see where they are:

1. Collect documents
2. Prep (helpers)
3. Draft and confirm roles
4. Role-by-role interview
5. Exploration rounds
6. Wrap-up

If `career.yaml` already exists, say so, load it, and tell the person this run will add to it (see Re-running).

## 1. Collect documents

Ask what they have: an existing CV, a LinkedIn profile, anything else (old appraisals, a bio). Accept files or pasted text. Never try to fetch a LinkedIn URL (it blocks automated access): ask for the profile's "Save to PDF" export (Profile, then More, then Save to PDF) or pasted text. No documents at all is fine; go straight to the interview.

## 2. Prep

Run these as parallel helper agents with these names, and tell the person which are running:

- **CV parser**: extracts roles, dates, education, certifications and skills from the CV.
- **LinkedIn parser**: the same, for the LinkedIn export. Skip it if there is no export.
- **Employer researcher**: one per employer; finds what the company does, so your questions can be specific.

If helpers are unavailable, say so and do the same steps one after another yourself.

## 3. Draft and confirm roles

Write a first `career.yaml` from the documents, marking each fact's `source` as `cv` or `linkedin`. Show the person the roles you found (company, title, dates) and ask them to confirm or correct the list before you interview. Fix dates to `YYYY-MM`.

## 4. Role-by-role interview

Newest role first. **One question per message**, in plain conversational language, with a short acknowledgement and no recap of what they just said.

For each role, work through: the problem or goal, what they personally did, how they did it (process, tools, decisions, trade-offs), what changed as a result, and a number if there is one. When they offer an adjective ("good communicator", "strong leader"), ask for a specific example before moving on. Never suggest a number; ask whether one exists.

After each role, have a **fact writer** helper add the new facts to `career.yaml` in the background while you start the next role. If helpers are unavailable, write them yourself after each role.

Facts follow the schema: `id` (`<role id>-f<n>`), `what`, `how`, `outcome`, `metric` only if given, `source: interview`. Keep the person's scope words exactly ("led", "contributed to", "owned", "supported").

## 5. Exploration rounds

This stage is deliberately open, because people forget their best material. Offer each round in `references/interview-playbook.md` one at a time. Every round is optional: if they want to skip one, accept it at once and move on without persuading.

## 6. Wrap-up

Check `career.yaml` against the schema: required keys present, dates `YYYY-MM` or `present`, every fact has a valid `source`, no salary anywhere. Then show the **thin areas** (roles with no outcomes, facts with no numbers, roles with few facts) and offer to dig further now or on a later run. Say where the file is.

## Rules

- Never store salary, anywhere.
- Never write a fact the person did not say or supply in a document.
- Ask for what they have not said instead of guessing it. Leave a field out when they gave nothing for it; never write placeholders such as "no outcome yet".
- Keep ids stable. Never renumber or delete existing facts.

## Re-running

When `career.yaml` exists, skip any phase already done, ask what has changed (a new job, a deeper look at an old one), and add roles or facts with new ids. Existing roles and facts stay exactly as they are unless the person corrects them.
