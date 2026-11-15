"""Validator for career.yaml (schema documented in skills/measure/references/career-schema.md)."""
import re

DATE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
SOURCES = {"cv", "linkedin", "interview"}


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
        for j, fact in enumerate(role.get("facts") or []):
            fwhere = f"{where}.facts[{j}]"
            _require(fact, ["id", "what", "source"], fwhere, errors)
            if fact.get("source") and fact["source"] not in SOURCES:
                errors.append(f"{fwhere}.source: must be one of {sorted(SOURCES)}")
    return errors
