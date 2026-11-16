from pathlib import Path

import pytest

from review_format import parse_review, unverified_quotes

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_recruiter_sample():
    review = parse_review(fixture("review.recruiter.sample.md"))
    assert review["reviewer"] == "recruiter" and review["verdict"] == "changes"
    assert [i["severity"] for i in review["issues"]] == ["must-fix", "must-fix", "nice-to-have"]
    assert [i["kind"] for i in review["issues"]] == ["suggest", "ask", "suggest"]


def test_parse_clean_ats_review():
    review = parse_review(fixture("review.ats.clean.md"))
    assert review == {"reviewer": "ats", "verdict": "pass", "issues": []}


def test_pass_with_only_nice_to_haves_is_valid():
    text = fixture("review.recruiter.sample.md").replace("Verdict: changes", "Verdict: pass")
    text = "\n".join(l for l in text.splitlines() if "[must-fix]" not in l)
    assert parse_review(text)["verdict"] == "pass"


def test_verdict_must_match_must_fix_presence():
    with pytest.raises(ValueError, match="if and only if"):
        parse_review(fixture("review.recruiter.sample.md").replace("Verdict: changes", "Verdict: pass"))
    with pytest.raises(ValueError, match="if and only if"):
        parse_review(fixture("review.ats.clean.md").replace("Verdict: pass", "Verdict: changes"))


def test_rejects_unknown_reviewer_and_verdict():
    with pytest.raises(ValueError, match="kind"):
        parse_review(fixture("review.ats.clean.md").replace("ats", "manager"))
    with pytest.raises(ValueError, match="verdict"):
        parse_review(fixture("review.ats.clean.md").replace("pass", "maybe"))


def test_rejects_more_than_five_issues():
    issue = '- [nice-to-have] "Skills" — Padded — suggest: trim\n'
    text = "# Review: recruiter\n\nVerdict: pass\n\n## Issues\n" + issue * 6
    with pytest.raises(ValueError, match="at most 5"):
        parse_review(text)


@pytest.mark.parametrize("line", [
    '- [must-fix] Skills — Padded — suggest: trim',                 # no quote
    '- [critical] "Skills" — Padded — suggest: trim',               # bad severity
    '- [must-fix] "Skills" — Padded — tell: trim',                  # neither suggest nor ask
    '- [must-fix] "Skills" - Padded - suggest: trim',               # hyphens, not em dashes
])
def test_rejects_malformed_issue_lines(line):
    text = f"# Review: recruiter\n\nVerdict: changes\n\n## Issues\n{line}\n"
    with pytest.raises(ValueError, match="bad issue line"):
        parse_review(text)


def test_invented_quote_is_flagged_and_real_quote_is_not():
    review = parse_review(fixture("review.recruiter.sample.md"))
    cv_text = "Managed stakeholders across  merchandising, finance and product\nAnalytics team award for the trading dashboard rebuild"
    assert unverified_quotes(review, cv_text) == ["Skills"]
    assert unverified_quotes(review, cv_text + "\nSkills") == []
