"""Parser for <company>/fitting.md (format documented in skills/fitting/references/fitting-format.md)."""
import re

VERDICTS = {"strong", "stretch", "weak"}
ITEM = re.compile(r"^- \[(met|partial|gap)\] (.+?) — evidence: (.+)$")


def _sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None and line.strip():
            sections[current].append(line.rstrip())
    return sections


def _items(lines: list[str]) -> list[dict]:
    items = []
    for line in lines:
        match = ITEM.match(line)
        if not match:
            raise ValueError(f"bad requirement line: {line!r}")
        status, requirement, evidence = match.groups()
        ids = [] if evidence.strip() == "none" else [e.strip() for e in evidence.split(",")]
        items.append({"status": status, "requirement": requirement, "evidence": ids})
    return items


def parse_fitting(text: str) -> dict:
    verdict = re.search(r"^Verdict: (\S+)\s*$", text, re.M)
    if not verdict or verdict.group(1) not in VERDICTS:
        raise ValueError(f"verdict must be one of {sorted(VERDICTS)}")
    sections = _sections(text)
    for name in ("Must-haves", "Nice-to-haves", "Keywords", "Company notes", "Questions for candidate"):
        if name not in sections:
            raise ValueError(f"missing section: {name}")
    return {
        "verdict": verdict.group(1),
        "must_haves": _items(sections["Must-haves"]),
        "nice_to_haves": _items(sections["Nice-to-haves"]),
        "keywords": [k.strip() for k in " ".join(sections["Keywords"]).split(",") if k.strip()],
        "questions": [q[2:].strip() for q in sections["Questions for candidate"] if q.startswith("- ")],
    }
