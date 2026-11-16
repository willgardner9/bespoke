import copy
from pathlib import Path

import pytest
import yaml

from schema import validate_career

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def load(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))


def test_sample_is_valid():
    assert validate_career(load("career.sample.yaml")) == []


def test_long_career_is_valid():
    assert validate_career(load("career.long.yaml")) == []


def test_missing_role_company_flagged():
    data = load("career.sample.yaml")
    del data["roles"][0]["company"]
    errors = validate_career(data)
    assert any("company" in e for e in errors)


def test_bad_date_flagged():
    data = load("career.sample.yaml")
    data["roles"][0]["start"] = "March 2021"
    errors = validate_career(data)
    assert any("start" in e and "YYYY-MM" in e for e in errors)


def test_present_is_allowed_as_end_date():
    data = load("career.sample.yaml")
    data["roles"][0]["end"] = "present"
    assert validate_career(data) == []


def test_unknown_source_flagged():
    data = load("career.sample.yaml")
    data["roles"][0]["facts"][0]["source"] = "rumour"
    errors = validate_career(data)
    assert any("source" in e for e in errors)


def test_salary_rejected_anywhere():
    data = load("career.sample.yaml")
    nested = copy.deepcopy(data)
    nested["roles"][0]["facts"][0]["salary"] = "£50k"
    assert any("salary" in e for e in validate_career(nested))
    top = copy.deepcopy(data)
    top["preferences"]["salary"] = "£60k"
    assert any("salary" in e for e in validate_career(top))


def test_project_is_valid():
    data = load("career.sample.yaml")
    data["projects"] = [
        {"id": "p1", "name": "Personal pipeline", "facts": [{"id": "p1-f1", "what": "Used dbt on a side project", "source": "interview"}]}
    ]
    assert validate_career(data) == []


def test_project_fact_source_checked():
    data = load("career.sample.yaml")
    data["projects"] = [
        {"id": "p1", "name": "Personal pipeline", "facts": [{"id": "p1-f1", "what": "Used dbt", "source": "rumour"}]}
    ]
    assert any("projects[0]" in e and "source" in e for e in validate_career(data))


def test_project_missing_name_flagged():
    data = load("career.sample.yaml")
    data["projects"] = [{"id": "p1", "facts": []}]
    assert any("projects[0]" in e and "name" in e for e in validate_career(data))


def test_vague_career_fixture_is_valid():
    assert validate_career(load("career.vague.yaml")) == []


def test_tech_management_and_hands_on_are_accepted():
    data = load("career.sample.yaml")
    data["roles"][0]["management"] = "Technical lead of a squad of 15, no line reports"
    data["roles"][0]["hands_on"] = "Still writes production Python"
    data["roles"][0]["facts"][0]["tech"] = ["Tableau", "SQL"]
    assert validate_career(data) == []


def test_tech_must_be_a_list_of_strings():
    data = load("career.sample.yaml")
    data["roles"][0]["facts"][0]["tech"] = "Tableau"
    assert any("tech" in e for e in validate_career(data))
    data["roles"][0]["facts"][0]["tech"] = []
    assert any("tech" in e for e in validate_career(data))


def test_management_must_be_text():
    data = load("career.sample.yaml")
    data["roles"][0]["management"] = ["line manager"]
    assert any("management" in e for e in validate_career(data))


@pytest.mark.parametrize("metric", ["several thousand", "a few thousand pounds", "many users", "a lot of requests"])
def test_vague_metric_rejected(metric):
    data = load("career.sample.yaml")
    data["roles"][0]["facts"][0]["metric"] = metric
    assert any("metric" in e for e in validate_career(data))


@pytest.mark.parametrize("metric", ["at least 2,000 a day", "up to 100,000 a day", "+3.1% conversion", "over 40 services"])
def test_figure_or_bound_metric_accepted(metric):
    data = load("career.sample.yaml")
    data["roles"][0]["facts"][0]["metric"] = metric
    assert validate_career(data) == []


def test_project_fact_tech_and_metric_checked():
    data = load("career.sample.yaml")
    data["projects"] = [
        {"id": "p1", "name": "Pipeline", "facts": [{"id": "p1-f1", "what": "Built it", "source": "interview", "tech": "dbt", "metric": "several"}]}
    ]
    errors = validate_career(data)
    assert any("projects[0]" in e and "tech" in e for e in errors)
    assert any("projects[0]" in e and "metric" in e for e in errors)
