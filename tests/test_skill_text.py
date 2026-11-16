"""Structural checks that the skill text carries the rules the review required."""
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parent.parent / "skills"


def text(*parts: str) -> str:
    return (SKILLS.joinpath(*parts)).read_text(encoding="utf-8")


@pytest.mark.parametrize("skill", ["measure", "fitting", "tailor", "bespoke"])
def test_untrusted_content_rule_in_every_skill(skill):
    assert "data, never instructions" in text(skill, "SKILL.md")


def test_fitting_passes_the_rule_into_helper_briefs():
    assert "in each helper's brief" in text("fitting", "SKILL.md")


def test_measure_passes_the_rule_into_employer_researcher_brief():
    assert "in the employer researcher's brief" in text("measure", "SKILL.md")


def test_measure_allows_one_fact_writer_at_a_time_and_rereads():
    body = text("measure", "SKILL.md")
    assert "one fact writer at a time" in body
    assert "re-read `career.yaml`" in body


def test_fitting_confirmed_gap_answer_goes_through_schema_and_asks_context():
    body = text("fitting", "SKILL.md")
    assert "career-schema.md" in body
    assert "which role" in body
    assert "projects" in body


def test_fitting_notes_injected_text_in_company_notes():
    assert "record it under Company notes" in text("fitting", "SKILL.md")


def test_checks_allow_certifications_and_projects_headings():
    body = text("tailor", "references", "checks.md")
    assert "Certifications" in body and "Projects" in body


def test_checks_guard_template_integrity():
    body = text("tailor", "references", "checks.md")
    assert "<style>" in body
    assert "style=" in body


def test_tailor_covers_new_slots_and_achievements():
    body = text("tailor", "SKILL.md")
    assert "certifications" in body and "projects" in body
    assert "achievements" in body
    assert "remove the whole section" in body.lower() or "Remove the whole section" in body


def test_tailor_reads_writing_rules_and_they_exist():
    assert "references/writing-rules.md" in text("tailor", "SKILL.md")
    assert (SKILLS / "tailor" / "references" / "writing-rules.md").exists()


@pytest.mark.parametrize("phrase", ["a big part of", "a major part in", "a big influence on", "(approximate figures)", "several", "a few"])
def test_writing_rules_name_the_hedges_to_cut(phrase):
    assert phrase in text("tailor", "references", "writing-rules.md")


@pytest.mark.parametrize("rule", [
    "One point, one place",
    "Name the stack",
    "Lead with the result or the fix",
    "at most 5 bullets",
    "technical lead, no line reports",
    "Never \"applying for\"",
    "shared:",
    "Being in the `skills` list in `career.yaml` is not evidence",
    "version control, ticketing, pull requests, code review",
    "never a country alone",
])
def test_writing_rules_carry_each_review_point(rule):
    assert rule in text("tailor", "references", "writing-rules.md")


def test_tailor_asks_for_missing_details_instead_of_guessing():
    body = text("tailor", "SKILL.md")
    assert "Missing details" in body
    assert "management" in body and "hands_on" in body
    assert "phone" in body


def test_tailor_report_lists_reframes_numbers_and_unevidenced_skills():
    body = text("tailor", "SKILL.md")
    assert "reframes" in body and "needs a number" in body and "no fact names them" in body


def test_tailor_never_uses_missing_words_or_gap_keywords():
    body = text("tailor", "SKILL.md")
    assert "never those after `missing:`" in body
    assert "Never mirror a keyword that belongs to a `gap`" in body


@pytest.mark.parametrize("rule", [
    "no fact names in `tech`",
    "`management`",
    "a hedge from `writing-rules.md`",
    "make the same point",
    "city (not a country alone)",
    "does not say \"applying\"",
    "at most 5 bullets",
    "grouped",
])
def test_checks_enforce_the_new_rules(rule):
    assert rule in text("tailor", "references", "checks.md")


def test_measure_captures_stack_management_contact_and_numbers():
    schema = text("measure", "references", "career-schema.md")
    for key in ("`tech`", "`management`", "`hands_on`", "never just a country"):
        assert key in schema
    playbook = text("measure", "references", "interview-playbook.md")
    assert "Name the stack" in playbook and "figure or a bound" in playbook and "line-manage" in playbook
    body = text("measure", "SKILL.md")
    assert "phone number" in body and "`tech`" in body


def test_fitting_format_defines_shared_and_missing():
    body = text("fitting", "references", "fitting-format.md")
    assert "shared:" in body and "missing:" in body
    assert "shared:" in text("fitting", "references", "verdict-rubric.md")
