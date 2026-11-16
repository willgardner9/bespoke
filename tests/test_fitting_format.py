from pathlib import Path

import pytest
import yaml

from fitting_format import parse_fitting

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def sample_text() -> str:
    return (FIXTURES / "fitting.sample.md").read_text(encoding="utf-8")


def test_parse_sample():
    parsed = parse_fitting(sample_text())
    assert parsed["verdict"] == "stretch"
    assert len(parsed["must_haves"]) == 6
    gaps = [m for m in parsed["must_haves"] if m["status"] == "gap"]
    assert [g["requirement"].split()[0] for g in gaps] == ["Experience"]
    assert gaps[0]["evidence"] == []
    assert "SQL" in parsed["keywords"]
    assert parsed["questions"]


def test_rejects_bad_verdict():
    bad = sample_text().replace("Verdict: stretch", "Verdict: maybe")
    with pytest.raises(ValueError, match="verdict"):
        parse_fitting(bad)


def test_gap_has_no_evidence_ids_and_met_has_some():
    parsed = parse_fitting(sample_text())
    for item in parsed["must_haves"] + parsed["nice_to_haves"]:
        if item["status"] == "gap":
            assert item["evidence"] == []
        else:
            assert item["evidence"], item["requirement"]


def test_evidence_ids_exist_in_career_sample():
    career = yaml.safe_load((FIXTURES / "career.sample.yaml").read_text(encoding="utf-8"))
    known = {f["id"] for r in career["roles"] for f in r["facts"]}
    parsed = parse_fitting(sample_text())
    cited = {e for m in parsed["must_haves"] + parsed["nice_to_haves"] for e in m["evidence"]}
    assert cited <= known


def test_partial_line_with_shared_and_missing_parses():
    parsed = parse_fitting((FIXTURES / "fitting.payments.md").read_text(encoding="utf-8"))
    partial = [m for m in parsed["must_haves"] if m["status"] == "partial"]
    assert partial
    domain = next(m for m in partial if "money movement" in m["requirement"])
    assert "shared:" in domain["requirement"] and "missing:" in domain["requirement"]
    assert domain["evidence"] == ["r3-f3", "r2-f1"]


def test_payments_fitting_cites_only_ids_in_vague_career():
    career = yaml.safe_load((FIXTURES / "career.vague.yaml").read_text(encoding="utf-8"))
    known = {f["id"] for r in career["roles"] for f in r["facts"]}
    parsed = parse_fitting((FIXTURES / "fitting.payments.md").read_text(encoding="utf-8"))
    cited = {e for m in parsed["must_haves"] + parsed["nice_to_haves"] for e in m["evidence"]}
    assert cited <= known
