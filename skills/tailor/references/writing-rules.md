# Writing rules

How the content is written. Every rule can be checked by reading the finished CV, and `checks.md` checks them. Facts still come only from `career.yaml`: these rules change how a true fact is put, never what is claimed.

## Bullets

- **One point, one place.** No two lines on the CV (summary sentences and bullets together) make the same point. The summary sets the frame; a bullet that only restates it is cut, and one that adds the how or the number stays.
- **Shape of a bullet:** verb, what was built or done with the tools used, then the result with its number. The strongest result in a role comes first.
- **Name the stack.** A bullet about technical work names the languages, datastores, brokers, platforms or tools from the fact's `tech` (or `how`). For other fields, name the tools, systems or methods. A bullet with no tool, method or system named and no number is rewritten from its fact or dropped.
- **Lead with the result or the fix.** When a fact starts from an incident or a mistake, the bullet opens with what was built or changed and what it made safe or faster. The incident goes in only if it explains the fix in a few words, and its cost never leads.
- **Figures must carry weight.** Use a number from the fact's `metric`. Leave out a figure that is small beside the other numbers in the same role (a cost of a few thousand next to a multi-million result); state the decision and its reason instead.
- **Budget.** The newest role has at most 5 bullets, the next role at most 4, any other role at most 3, and older or less relevant roles one or two lines. Cut by relevance to the ad; a bullet that needs trimming to fit is dropped, not shrunk.

## No hedging

Say what was done, with a verb and a number. Scope goes in the verb ("led", "delivered", "contributed to", "owned"), as `career.yaml` has it, and never in a size word.

Never write:

- a size word standing in for a contribution: "a big part of", "a major part in", "a key part of", "a big influence on", "a significant role in";
- a vague amount standing in for a number: "several", "a few", "a couple of", "many", "numerous", "dozens of", "a lot of", as in "several thousand";
- a bracketed caveat: "(approximate figures)", "(estimated)", "(roughly)".

Allowed: a figure, or a bound with one marker and no brackets: "up to 100,000 a day", "over 40 services", "about 30%" (only when the fact's `metric` says it is an estimate).

When a fact only has a vague amount or a size word, do not guess a figure. Restate the fact as what the person did (its `what` and `how`), or drop the bullet, and list it in the report under "needs a number" so the person can run `measure` and give one.

## Leading people

- Keep the title exactly as `career.yaml` has it. Clarify the shape of the role in the first bullet instead.
- For a role with `management`, the first bullet says it plainly: team size and make-up, and whether the person line-manages or leads technically. Use `management`'s own words ("technical lead, no line reports" and "line manager of four" are different claims).
- When the ad is for a hands-on role (it asks for building, coding or designing, or the title is an individual contributor title), include a bullet that shows what the person still does themselves, from `hands_on` or from facts written in the first person, with the tools named.
- If a role's facts use words like "lead" or "managed" and the role has no `management`, or the ad is hands-on and the role has no `hands_on` and no hands-on fact, do not guess. Ask one question for each gap (see Missing details in `SKILL.md`).

## Summary

- Two or three sentences. Never "applying for", never the job title or company being applied to; the summary is about the candidate.
- Sentence one is who the person is and the domain they work in, in the ad's vocabulary where true. The rest names the kinds of problem they solve. Numbers live in the bullets.
- No years of experience unless a figure is derivable from the dates in `career.yaml`.

## Using the ad's vocabulary for the candidate's own work

The ad's domain can differ from the candidate's. A payments ad and a candidate from sanctions screening is the common case. The honest move is to describe the same engineering with the ad's terms for the property, never to claim the domain.

- A term may be mirrored only if a cited fact shows what the term means. For a `partial` requirement, the words after `shared:` in `fitting.md` are available; the words after `missing:` are never used, and never is a keyword from a `gap`.
- The domain itself (payments, money movement, a named scheme, a named tool) is only used when a fact is in that domain. Put the candidate's real domain next to the property: "reliable, traceable processing in financial crime and sanctions systems" says what is true and reads right to a payments reader.
- Where the ad's term is stronger than the fact, keep the fact's term. A fact that shows idempotent handling supports "idempotent processing, so no item is processed twice", not "exactly-once guarantees", unless the fact says so.
- List every reframe (ad term, fact id) in the report so the person can reject one.

## Skills

- Grouped, one labelled line per group, three to five groups, with labels that fit the candidate's stack (for example Languages, Data and messaging, Cloud and infrastructure, Observability). Most relevant group first.
- About 24 items at most. Each is a specific technology, method or named standard.
- **Evidence.** An item goes on the CV only if a fact names it in `tech`, `how` or `what`, and it should also appear in a bullet. Being in the `skills` list in `career.yaml` is not evidence. An item without a fact is left off and listed in the report ("listed in `career.yaml`, no evidence").
- **Cut:** tools and practices everyone in the field has (version control, ticketing, pull requests, code review, agile ceremonies), and traits ("ownership", "teamwork", "communication"). Spoken languages stay only when the ad asks for one.
- Use the ad's wording for an item where it is true.

## Contact line

`City, UK | email | phone | profile links`, from `profile`. The location is a city, never a country alone; the phone number is required. If `profile` lacks either, ask for it (see Missing details in `SKILL.md`).
