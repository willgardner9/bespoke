import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from render_helpers import TEMPLATE, fill_template, find_chrome, page_count, render_pdf

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
SLOTS = ["name", "contact", "summary", "experience", "education", "skills"]


def template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def career(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("slot", SLOTS)
def test_slots_present(slot):
    html = template()
    assert f'data-slot="{slot}"' in html
    assert f"<!--slot:{slot}-->" in html and f"<!--/slot:{slot}-->" in html


@pytest.mark.parametrize("tag", ["<table", "<img", "<svg", "<canvas"])
def test_no_forbidden_markup(tag):
    assert tag not in template().lower()


@pytest.mark.parametrize("prop", ["column-count", "columns:", "float:"])
def test_no_forbidden_layout_css(prop):
    assert prop not in template().lower()


def test_font_is_arial_or_helvetica():
    families = re.findall(r"font-family:\s*([^;]+);", template())
    assert families and all(f.strip().lower().startswith(("arial", "helvetica")) for f in families)


def test_colours_are_black_and_white_only():
    css = template()
    assert not re.search(r"rgba?\(|hsla?\(", css)
    hexes = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{3,6}\b", css)}
    assert hexes <= {"#000", "#000000", "#fff", "#ffffff"}


def test_a4_page_rules():
    assert re.search(r"@page\s*\{[^}]*size:\s*A4[^}]*margin:", template(), re.S)


def test_type_never_below_10pt():
    sizes = [float(s) for s in re.findall(r"font-size:\s*([\d.]+)pt", template())]
    assert sizes and min(sizes) >= 10


needs_chrome = pytest.mark.skipif(find_chrome() is None, reason="Chrome not installed")
needs_pdftotext = pytest.mark.skipif(shutil.which("pdftotext") is None, reason="pdftotext not installed")


@needs_chrome
def test_long_career_renders_within_two_pages(tmp_path):
    pdf = render_pdf(fill_template(career("career.long.yaml")), tmp_path)
    assert 1 <= page_count(pdf) <= 2


@needs_chrome
@needs_pdftotext
def test_extracted_text_keeps_accents_and_en_dash(tmp_path):
    pdf = render_pdf(fill_template(career("career.sample.yaml")), tmp_path)
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    assert "Zoë Ñuñez" in text
    assert "Mar 2021 – Present" in text


@needs_chrome
@needs_pdftotext
def test_extracted_headings_are_whole_standard_words(tmp_path):
    pdf = render_pdf(fill_template(career("career.sample.yaml")), tmp_path)
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    for heading in ("Summary", "Experience", "Education", "Skills"):
        assert re.search(rf"^{heading}$", text, re.M), f"heading {heading!r} not extracted as a whole word"


def test_no_letter_spacing_or_case_transform():
    css = template()
    assert "letter-spacing" not in css
    assert "text-transform" not in css
