"""Parser for a blind reviewer's output (format documented in skills/tailor/references/review.md)."""
import re

KINDS = {"recruiter", "ats"}
VERDICTS = {"pass", "changes"}
MAX_ISSUES = 5
ISSUE = re.compile(r'^- \[(must-fix|nice-to-have)\] "(.+?)" — (.+?) — (suggest|ask): (.+)$')


def parse_review(text: str) -> dict:
    header = re.search(r"^# Review: (\S+)\s*$", text, re.M)
    if not header or header.group(1) not in KINDS:
        raise ValueError(f"review kind must be one of {sorted(KINDS)}")
    verdict = re.search(r"^Verdict: (\S+)\s*$", text, re.M)
    if not verdict or verdict.group(1) not in VERDICTS:
        raise ValueError(f"verdict must be one of {sorted(VERDICTS)}")
    if "## Issues" not in text:
        raise ValueError("missing section: Issues")
    lines = [l.rstrip() for l in text.split("## Issues", 1)[1].splitlines() if l.strip()]
    issues = []
    if lines != ["- none"]:
        for line in lines:
            match = ISSUE.match(line)
            if not match:
                raise ValueError(f"bad issue line: {line!r}")
            severity, quote, problem, kind, action = match.groups()
            issues.append({"severity": severity, "quote": quote, "problem": problem, "kind": kind, "action": action})
    if len(issues) > MAX_ISSUES:
        raise ValueError(f"at most {MAX_ISSUES} issues")
    must_fix = [i for i in issues if i["severity"] == "must-fix"]
    if (verdict.group(1) == "changes") != bool(must_fix):
        raise ValueError("verdict is changes if and only if there is a must-fix issue")
    return {"reviewer": header.group(1), "verdict": verdict.group(1), "issues": issues}


def unverified_quotes(review: dict, cv_text: str) -> list[str]:
    """Quotes that do not appear in the CV text (whitespace-insensitive): those issues are discarded."""
    squash = lambda s: re.sub(r"\s+", " ", s).strip()
    body = squash(cv_text)
    return [i["quote"] for i in review["issues"] if squash(i["quote"]) not in body]
