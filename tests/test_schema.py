import copy
from pathlib import Path

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
