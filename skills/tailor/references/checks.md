# Checks

Run both. Each returns pass or fail with specifics. Each is given the `career.yaml`, `fitting.md`, the rendered `cv.pdf` and its extracted text.

## Fact-checker

Rule: **strict on facts and scope, loose on wording.**

For every bullet, summary sentence and skill on the CV, find the fact id(s) in `career.yaml` it comes from and list the trace (`bullet -> fact id`). Fail on any of:

- an employer, title, date, number, tool, qualification or certification not in `career.yaml`;
- a stronger scope than the fact states (for example "led" where the fact says "mentored" or "contributed to", "owned" where it says "supported");
- a claim with no fact behind it, or one stitched from several facts into something none of them says;
- any term from a `gap` requirement in `fitting.md` appearing as if the candidate has it, or any word after `missing:` in a `partial` line;
- a skill or tool on the CV that no fact names in `tech`, `how` or `what` (appearing only in the `skills` list of `career.yaml` is not evidence);
- a leadership claim that differs from the role's `management` (for example "managed" or "line-managed" where `management` says no line reports), or a hands-on claim with no `hands_on` or first-person fact behind it;
- a hedge from `writing-rules.md`: a size word standing in for a contribution ("a big part of", "a major part in", "a big influence on"), a vague amount standing in for a number ("several", "a few", "a couple of", "many"), or a bracketed caveat such as "(approximate figures)";
- two lines, in the summary or bullets, that make the same point;
- a reframe that uses the ad's term where it is stronger than what the fact shows. List every reframe as `ad term -> fact id`.

Rewording, reordering and using the ad's vocabulary for something that is true are allowed.

## ATS checker

Read the extracted PDF text and check:

- the reading order is correct: name, contact line, summary, then experience newest first, education, skills;
- each employer appears once, with all its roles beneath it and the employer span matching the earliest start and latest end of those roles;
- any employer with one role and no bullets is the one-line compact entry, not a full employer block;
- the headings are the standard words Summary, Experience, Education, Skills (plus Projects and Certifications when present), extracted whole;
- accents and en dashes in names and dates survived (for example "Zoë Ñuñez", "Mar 2021 – Present");
- there are no tables, multi-column layouts, icons, images or text boxes in the HTML;
- the PDF is at most two pages;
- the `<style>` block in `cv.html` is identical to the template's, and no element inside a slot carries a `style=` attribute;
- keyword coverage: list every `Keywords` entry that is true of the candidate (backed by a `met` or `partial` requirement) but missing from the CV text, and fail if there are any;
- the contact line holds a city (not a country alone), an email and a phone number;
- the summary does not say "applying", and does not name the job title or company applied for;
- the newest role has at most 5 bullets, the next at most 4, any other at most 3;
- the Skills section is grouped (one labelled line per group, three to five groups), has about 24 items or fewer, and none of the cut items from `writing-rules.md` (version control, ticketing, pull requests, code review, agile ceremonies, trait words);
- each bullet about technical work names a tool, language, platform or method, or carries a number.
