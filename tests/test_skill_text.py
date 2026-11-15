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
