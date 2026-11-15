import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["measure", "fitting", "tailor", "bespoke"]


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, f"{path} has no YAML frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def test_plugin_manifest():
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "bespoke"


def test_marketplace_lists_plugin():
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert "bespoke" in [p["name"] for p in market["plugins"]]


@pytest.mark.parametrize("skill", SKILLS)
def test_skill_frontmatter(skill):
    fields = _frontmatter(ROOT / "skills" / skill / "SKILL.md")
    assert fields.get("name") == skill
    assert fields.get("description")


def test_gitignore_blocks_personal_data():
    lines = (ROOT / ".gitignore").read_text().splitlines()
    assert "career.yaml" in lines
    assert "*/cv.pdf" in lines


def test_no_personal_data_in_repo():
    skip = {".git", ".superpowers"}
    found = [
        p
        for p in ROOT.rglob("career.yaml")
        if not skip.intersection(p.relative_to(ROOT).parts)
    ]
    assert found == []
