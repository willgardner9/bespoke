"""Parsers for tailor's progress lines and final scorecard (formats in skills/tailor/references/reporting.md)."""
import re

ROUNDS = {
    "Check": {"max": 3, "names": ("fact-checker", "ATS checker"), "unit": "issue", "action": "fixing"},
    "Review": {"max": 2, "names": ("recruiter", "ATS reviewer"), "unit": "must-fix", "action": "improving"},
}
ROUND_LINE = re.compile(r"^(Check|Review) · round (\d+) of (\d+) · (.+)$")
RESULT = re.compile(r"^(?P<name>.+?) (?P<mark>✓|✗)(?: (?P<n>\d+) (?P<unit>issues?|must-fix))?$")
FITS = {"met", "partial", "gap"}
MAX_CV_WORDS = 12


def parse_round_line(line: str) -> dict:
    match = ROUND_LINE.match(line)
    if not match:
        raise ValueError(f"bad round line: {line!r}")
    kind, rnd, of, rest = match.group(1), int(match.group(2)), int(match.group(3)), match.group(4)
    spec = ROUNDS[kind]
    if of != spec["max"]:
        raise ValueError(f"{kind} has {spec['max']} rounds, not {of}")
    if not 1 <= rnd <= of:
        raise ValueError(f"round {rnd} is outside 1 to {of}")
    parts = rest.split(" · ")
    action = parts.pop() if parts and parts[-1] in {"fixing", "improving", "stopping"} else None
    if len(parts) != len(spec["names"]):
        raise ValueError(f"{kind} reports {list(spec['names'])}")
    results = []
    for part, expected in zip(parts, spec["names"]):
        res = RESULT.match(part)
        if not res or res["name"] != expected:
            raise ValueError(f"bad result {part!r}, expected {expected!r}")
        failed = res["mark"] == "✗"
        if failed:
            n = int(res["n"] or 0)
            unit = spec["unit"] if spec["unit"] == "must-fix" else ("issue" if n == 1 else "issues")
            if n < 1 or res["unit"] != unit:
                raise ValueError(f"bad count in {part!r}, expected a count and {unit!r}")
        elif res["n"]:
            raise ValueError(f"a pass carries no count: {part!r}")
        results.append({"name": expected, "passed": not failed, "count": int(res["n"]) if failed else 0})
    any_failed = any(not r["passed"] for r in results)
    if any_failed:
        wanted = "stopping" if rnd == of else spec["action"]
        if action != wanted:
            raise ValueError(f"a failed round {rnd} of {of} ends with {wanted!r}")
    elif action:
        raise ValueError("a round that passed has no next move")
    return {"kind": kind, "round": rnd, "of": of, "results": results, "action": action}


def _table(text: str, header: str) -> list[list[str]]:
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == header)
    except StopIteration:
        raise ValueError(f"missing table: {header}")
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def parse_scorecard(text: str) -> dict:
    must_haves = []
    for requirement, fit, on_cv in _table(text, "| Must-have | Fit | On the CV |"):
        if fit not in FITS:
            raise ValueError(f"fit must be one of {sorted(FITS)}: {fit!r}")
        if (fit == "gap") != (on_cv == "not claimed"):
            raise ValueError(f"only a gap row says 'not claimed': {requirement!r}")
        if len(on_cv.split()) > MAX_CV_WORDS:
            raise ValueError(f"'On the CV' is over {MAX_CV_WORDS} words: {requirement!r}")
        must_haves.append({"requirement": requirement, "fit": fit, "on_cv": on_cv})
    keywords = re.search(r"^\*\*Keywords:\*\* on the CV: (.*?) · not on the CV: (.*)$", text, re.M)
    if not keywords:
        raise ValueError("missing Keywords line")
    split = lambda s: [] if s.strip() == "none" else [k.strip() for k in s.split(",") if k.strip()]
    on = split(keywords.group(1))
    off = [re.sub(r"\s*\((gap|not evidenced)\)$", "", k) for k in split(keywords.group(2))]
    run = []
    for stage, rounds, result in _table(text, "| Stage | Rounds | Result |"):
        if stage not in {"Checks", "Review"}:
            raise ValueError(f"unknown stage {stage!r}")
        if not (re.fullmatch(r"\d of \d", rounds) or rounds == "skipped") or (rounds == "skipped" and stage != "Review"):
            raise ValueError(f"bad rounds for {stage}: {rounds!r}")
        run.append({"stage": stage, "rounds": rounds, "result": result})
    if not re.search(r"^\*\*Files:\*\* ", text, re.M):
        raise ValueError("missing Files line")
    if not re.search(r"^\*\*Open items:\*\*", text, re.M):
        raise ValueError("missing Open items")
    return {"must_haves": must_haves, "keywords_on": on, "keywords_off": off, "run": run}


def scorecard_matches_fitting(card: dict, fitting: dict) -> list[str]:
    """Differences between a scorecard and the parsed fitting.md it reports on; empty means they agree."""
    problems = []
    strip_note = lambda r: re.sub(r"\s*\(shared:.*\)$", "", r)
    expected = [(strip_note(m["requirement"]), m["status"]) for m in fitting["must_haves"]]
    actual = [(m["requirement"], m["fit"]) for m in card["must_haves"]]
    if actual != expected:
        problems.append(f"must-have rows differ: {actual} vs {expected}")
    if sorted(card["keywords_on"] + card["keywords_off"]) != sorted(fitting["keywords"]):
        problems.append("keywords on and off the CV are not exactly fitting.md's Keywords")
    return problems
