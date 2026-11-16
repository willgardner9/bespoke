import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from render_helpers import TEMPLATE, month, fill_template, find_chrome, page_count, render_pdf

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
SLOTS = ["name", "contact", "summary", "experience", "projects", "education", "certifications", "skills"]


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


GREY_RULES = (r"\.roles\.multi\s*\{[^}]*\}", r"\.emp-head \.span\s*\{[^}]*\}", r"\.loc\s*\{[^}]*\}")


def test_colours_are_black_and_white_except_three_grey_details():
    css = template()
    assert not re.search(r"rgba?\(|hsla?\(", css)
    rest = css
    for pattern in GREY_RULES:
        rule = re.search(pattern, css).group(0)
        assert re.search(r"#(bbb|666)\b", rule.lower()), pattern
        rest = rest.replace(rule, "")
    hexes = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{3,6}\b", rest)}
    assert hexes <= {"#000", "#000000", "#fff", "#ffffff"}


def test_location_and_employer_dates_are_mid_grey_and_the_rule_is_hairline():
    css = template()
    assert "#666" in re.search(GREY_RULES[1], css).group(0)
    assert "#666" in re.search(GREY_RULES[2], css).group(0)
    rule = re.search(GREY_RULES[0], css).group(0)
    assert float(re.search(r"border-left:\s*([\d.]+)pt", rule).group(1)) <= 0.5


def test_template_shows_a_compact_sample_so_the_filler_sees_it():
    assert 'class="employer compact"' in template()


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


PROJECT = {
    "id": "p1",
    "name": "Personal analytics pipeline",
    "facts": [{"id": "p1-f1", "what": "Built a personal analytics pipeline with dbt", "source": "interview"}],
}


@needs_chrome
@needs_pdftotext
def test_certifications_and_projects_extract_as_whole_headings(tmp_path):
    data = career("career.sample.yaml")
    data["projects"] = [PROJECT]
    pdf = render_pdf(fill_template(data), tmp_path)
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    for heading in ("Projects", "Certifications"):
        assert re.search(rf"^{heading}$", text, re.M), heading
    assert "Tableau Desktop Specialist" in text
    assert "dbt" in text


@needs_chrome
@needs_pdftotext
def test_empty_optional_sections_are_removed(tmp_path):
    data = career("career.sample.yaml")
    data["certifications"] = []
    pdf = render_pdf(fill_template(data), tmp_path)
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    assert "Certifications" not in text
    assert "Projects" not in text


@needs_chrome
def test_long_career_in_full_detail_really_overflows_two_pages(tmp_path):
    pdf = render_pdf(fill_template(career("career.long.yaml"), facts_per_role=99, detail=True), tmp_path)
    assert page_count(pdf) > 2


def test_template_sample_groups_roles_under_an_employer():
    html = template()
    for marker in ('class="employer"', 'class="emp-head"', 'class="roles'):
        assert marker in html, marker


def promoted(data: dict) -> dict:
    """Two consecutive roles at one employer: a promotion."""
    data["roles"][1]["company"] = data["roles"][0]["company"]
    data["roles"][1]["location"] = data["roles"][0].get("location")
    return data


@needs_chrome
@needs_pdftotext
def test_one_employer_with_two_roles_names_the_employer_once(tmp_path):
    data = promoted(career("career.sample.yaml"))
    company = data["roles"][0]["company"]
    pdf = render_pdf(fill_template(data), tmp_path)
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    assert text.count(company) == 1
    for role in data["roles"][:2]:
        assert role["title"] in text


def test_grouping_keeps_one_employer_block_per_company():
    data = promoted(career("career.sample.yaml"))
    html = fill_template(data)
    assert html.count('class="employer"') == len({r["company"] for r in data["roles"]})
    assert html.count('class="roles multi"') == 1


def bulletless(data: dict) -> dict:
    data["roles"][-1]["facts"] = []
    return data


def test_bulletless_single_role_employer_uses_compact_entry():
    html = fill_template(bulletless(career("career.sample.yaml")))
    assert html.count('class="employer compact"') == 1
    assert 'class="employer compact"' in template() or ".employer.compact" in template()


@needs_chrome
@needs_pdftotext
def test_compact_entry_is_a_single_line_with_employer_title_and_dates(tmp_path):
    data = bulletless(career("career.sample.yaml"))
    last = data["roles"][-1]
    pdf = render_pdf(fill_template(data), tmp_path)
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    line = next(l for l in text.splitlines() if last["company"] in l)
    assert last["title"] in line and month(last["end"]) in line


def test_header_name_and_employer_rule_are_restrained():
    css = template()
    assert float(re.search(r"h1\s*\{\s*font-size:\s*([\d.]+)pt", css).group(1)) <= 22
    rule = re.search(r"\.roles\.multi\s*\{[^}]*\}", css).group(0)
    assert "#bbb" in rule.lower()
