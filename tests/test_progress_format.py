import re
from pathlib import Path

import pytest

from fitting_format import parse_fitting
from progress_format import parse_round_line, parse_scorecard, scorecard_matches_fitting

ROOT = Path(__file__).resolve().parent.parent
REPORTING = (ROOT / "skills" / "tailor" / "references" / "reporting.md").read_text(encoding="utf-8")


def block(lang: str) -> str:
    match = re.search(rf"```{lang}\n(.*?)```", REPORTING, re.S)
    assert match, f"no ```{lang} block in reporting.md"
    return match.group(1)


def fitting_sample() -> dict:
    return parse_fitting((ROOT / "fixtures" / "fitting.sample.md").read_text(encoding="utf-8"))


# ---- round lines ----

@pytest.mark.parametrize("line", [l for l in block("text").splitlines() if l.strip()])
def test_every_round_line_example_in_the_doc_parses(line):
    assert parse_round_line(line)["kind"] in {"Check", "Review"}


def test_round_line_examples_cover_fail_pass_and_stopping():
    parsed = [parse_round_line(l) for l in block("text").splitlines() if l.strip()]
    assert {p["action"] for p in parsed} == {"fixing", "improving", "stopping", None}


def test_round_line_fields():
    parsed = parse_round_line("Check · round 1 of 3 · fact-checker ✗ 3 issues · ATS checker ✗ 1 issue · fixing")
    assert parsed["results"] == [
        {"name": "fact-checker", "passed": False, "count": 3},
        {"name": "ATS checker", "passed": False, "count": 1},
    ]


@pytest.mark.parametrize("line", [
    "Check round 1 of 3 fact-checker ✓ ATS checker ✓",                                          # wrong separators
    "Check · round 1 of 4 · fact-checker ✓ · ATS checker ✓",                                     # check has 3 rounds
    "Review · round 3 of 2 · recruiter ✓ · ATS reviewer ✓",                                      # round out of range
    "Check · round 1 of 3 · ATS checker ✓ · fact-checker ✓",                                     # names out of order
    "Check · round 1 of 3 · fact-checker ✗ · ATS checker ✓ · fixing",                            # failure with no count
    "Check · round 1 of 3 · fact-checker ✗ 1 issues · ATS checker ✓ · fixing",                   # 1 issues
    "Check · round 1 of 3 · fact-checker ✓ 2 issues · ATS checker ✓",                            # a pass with a count
    "Check · round 1 of 3 · fact-checker ✗ 2 issues · ATS checker ✓",                            # failed, no next move
    "Check · round 3 of 3 · fact-checker ✗ 2 issues · ATS checker ✓ · fixing",                   # last round must stop
    "Review · round 1 of 2 · recruiter ✗ 2 issues · ATS reviewer ✓ · improving",                 # review counts must-fix
    "Review · round 1 of 2 · recruiter ✓ · ATS reviewer ✓ · improving",                          # passed, yet a next move
])
def test_bad_round_lines_rejected(line):
    with pytest.raises(ValueError):
        parse_round_line(line)


# ---- scorecard ----

def test_doc_example_scorecard_parses():
    card = parse_scorecard(block("markdown"))
    assert len(card["must_haves"]) == 6
    assert [r["stage"] for r in card["run"]] == ["Checks", "Review"]


def test_doc_example_scorecard_agrees_with_the_sample_fitting():
    assert scorecard_matches_fitting(parse_scorecard(block("markdown")), fitting_sample()) == []


def test_gap_rows_say_not_claimed_and_dbt_is_not_on_the_cv():
    card = parse_scorecard(block("markdown"))
    gaps = [m for m in card["must_haves"] if m["fit"] == "gap"]
    assert [g["on_cv"] for g in gaps] == ["not claimed"]
    assert "dbt" in card["keywords_off"] and "dbt" not in card["keywords_on"]


def test_mismatch_with_fitting_is_reported():
    card = parse_scorecard(block("markdown"))
    card["must_haves"][4]["fit"] = "met"
    card["keywords_on"].remove("SQL")
    problems = scorecard_matches_fitting(card, fitting_sample())
    assert len(problems) == 2


def test_partial_note_is_not_part_of_the_requirement_column():
    fitting = {"must_haves": [{"status": "partial", "requirement": "Payments (shared: correctness; missing: payments)", "evidence": ["r1"]}], "keywords": []}
    card = {"must_haves": [{"requirement": "Payments", "fit": "partial", "on_cv": "x (A)"}], "keywords_on": [], "keywords_off": []}
    assert scorecard_matches_fitting(card, fitting) == []


@pytest.mark.parametrize("old,new,match", [
    ("| gap | not claimed |", "| gap | SQL views (Brightwell Retail) |", "not claimed"),
    ("| met | SQL views behind the weekly trading dashboard (Brightwell Retail) |", "| met | not claimed |", "not claimed"),
    ("| Experience with dbt for data transformation | gap |", "| Experience with dbt for data transformation | maybe |", "fit must be"),
    ("| Checks | 2 of 3 |", "| Checks | skipped |", "bad rounds"),
    ("| Review | 2 of 2 |", "| Tests | 2 of 2 |", "unknown stage"),
])
def test_bad_scorecards_rejected(old, new, match):
    text = block("markdown")
    assert old in text
    with pytest.raises(ValueError, match=match):
        parse_scorecard(text.replace(old, new))


def test_skipped_review_row_is_valid():
    text = block("markdown").replace("| Review | 2 of 2 | passed |", "| Review | skipped | no helpers available |")
    assert parse_scorecard(text)["run"][1] == {"stage": "Review", "rounds": "skipped", "result": "no helpers available"}


def test_on_the_cv_cell_is_kept_short():
    text = block("markdown").replace("SQL views behind the weekly trading dashboard", "SQL " * 14)
    with pytest.raises(ValueError, match="over 12 words"):
        parse_scorecard(text)


@pytest.mark.parametrize("label", ["**Files:**", "**Open items:**"])
def test_files_and_open_items_are_required(label):
    text = block("markdown")
    assert label in text
    with pytest.raises(ValueError):
        parse_scorecard(text.replace(label, "**Other:**"))
