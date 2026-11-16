"""Validator for career.yaml (schema documented in skills/measure/references/career-schema.md)."""
import re

DATE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
SOURCES = {"cv", "linkedin", "interview"}
VAGUE_AMOUNT = re.compile(r"\b(several|a few|a couple|many|numerous|dozens?|a lot)\b", re.I)


def _find_salary(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else str(key)
            if str(key).lower() == "salary":
                yield here
            yield from _find_salary(value, here)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _find_salary(value, f"{path}[{i}]")


def _require(obj, keys, where, errors):
    for key in keys:
        if obj.get(key) in (None, "", []):
            errors.append(f"{where}: missing {key}")


def _check_fact(fact: dict, where: str, errors: list[str]) -> None:
    _require(fact, ["id", "what", "source"], where, errors)
    if fact.get("source") and fact["source"] not in SOURCES:
        errors.append(f"{where}.source: must be one of {sorted(SOURCES)}")
    tech = fact.get("tech")
    if tech is not None and not (isinstance(tech, list) and tech and all(isinstance(t, str) and t.strip() for t in tech)):
        errors.append(f"{where}.tech: must be a non-empty list of strings")
    metric = fact.get("metric")
    if metric is not None and VAGUE_AMOUNT.search(str(metric)):
        errors.append(f"{where}.metric: a vague amount is not a metric, give a figure or a bound")


def validate_career(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["career data must be a mapping"]
    for path in _find_salary(data):
        errors.append(f"{path}: salary is never stored")
    profile = data.get("profile")
    if not isinstance(profile, dict) or not profile.get("name"):
        errors.append("profile: missing name")
    roles = data.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append("roles: must be a non-empty list")
        return errors
    for i, role in enumerate(roles):
        where = f"roles[{i}]"
        _require(role, ["id", "company", "title", "start", "end"], where, errors)
        if role.get("start") and not DATE.match(str(role["start"])):
            errors.append(f"{where}.start: must be YYYY-MM")
        end = role.get("end")
        if end and end != "present" and not DATE.match(str(end)):
            errors.append(f"{where}.end: must be YYYY-MM or present")
        for key in ("management", "hands_on"):
            if role.get(key) is not None and not (isinstance(role[key], str) and role[key].strip()):
                errors.append(f"{where}.{key}: must be a plain sentence")
        for j, fact in enumerate(role.get("facts") or []):
            _check_fact(fact, f"{where}.facts[{j}]", errors)
    for i, project in enumerate(data.get("projects") or []):
        where = f"projects[{i}]"
        _require(project, ["id", "name"], where, errors)
        for j, fact in enumerate(project.get("facts") or []):
            _check_fact(fact, f"{where}.facts[{j}]", errors)
    return errors
