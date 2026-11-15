# Checks

Run both. Each returns pass or fail with specifics. Each is given the `career.yaml`, `fitting.md`, the rendered `cv.pdf` and its extracted text.

## Fact-checker

Rule: **strict on facts and scope, loose on wording.**

For every bullet, summary sentence and skill on the CV, find the fact id(s) in `career.yaml` it comes from and list the trace (`bullet -> fact id`). Fail on any of:

- an employer, title, date, number, tool, qualification or certification not in `career.yaml`;
- a stronger scope than the fact states (for example "led" where the fact says "mentored" or "contributed to", "owned" where it says "supported");
- a claim with no fact behind it, or one stitched from several facts into something none of them says;
- any term from a `gap` requirement in `fitting.md` appearing as if the candidate has it.

Rewording, reordering and using the ad's vocabulary for something that is true are allowed.

## ATS checker

Read the extracted PDF text and check:

- the reading order is correct: name, contact line, summary, then experience newest first, education, skills;
- the headings are the standard words Summary, Experience, Education, Skills (plus Projects and Certifications when present), extracted whole;
- accents and en dashes in names and dates survived (for example "Zoë Ñuñez", "Mar 2021 – Present");
- there are no tables, columns, icons, images or text boxes in the HTML;
- the PDF is at most two pages;
- the `<style>` block in `cv.html` is identical to the template's, and no element inside a slot carries a `style=` attribute;
- keyword coverage: list every `Keywords` entry that is true of the candidate (backed by a `met` or `partial` requirement) but missing from the CV text, and fail if there are any.
