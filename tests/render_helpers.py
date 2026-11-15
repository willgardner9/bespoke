"""Test-only helpers: fill the CV template from career data and render it with headless Chrome."""
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "skills" / "tailor" / "assets" / "cv-template.html"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def month(value: str) -> str:
    if value == "present":
        return "Present"
    year, mon = str(value).split("-")
    return f"{MONTHS[int(mon) - 1]} {year}"


def set_slot(html: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--slot:{name}-->)(.*?)(<!--/slot:{name}-->)", re.S)
    assert pattern.search(html), f"slot {name} missing"
    return pattern.sub(lambda m: m.group(1) + content + m.group(3), html, count=1)


def fill_template(career: dict, facts_per_role: int = 2) -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    profile = career["profile"]
    html = set_slot(html, "name", profile["name"])
    html = set_slot(html, "contact", " | ".join(filter(None, [profile.get("location"), profile.get("email"), profile.get("phone")])))
    html = set_slot(html, "summary", "Experienced analyst.")
    roles = []
    for role in career["roles"]:
        bullets = "".join(f"<li>{f['what']}</li>" for f in role["facts"][:facts_per_role])
        roles.append(
            '<div class="role"><div class="role-head">'
            f'<span class="role-title">{role["title"]}</span>'
            f'<span class="dates">{month(role["start"])} – {month(role["end"])}</span></div>'
            f'<div class="company">{role["company"]}</div><ul>{bullets}</ul></div>'
        )
    html = set_slot(html, "experience", "".join(roles))
    edu = "".join(
        f'<div class="role"><div class="role-head"><span class="role-title">{e["qualification"]}</span>'
        f'<span class="dates">{month(e["start"])} – {month(e["end"])}</span></div>'
        f'<div class="company">{e["institution"]}</div></div>'
        for e in career.get("education", [])
    )
    html = set_slot(html, "education", edu)
    html = set_slot(html, "skills", ", ".join(career.get("skills", [])))
    return html


def find_chrome() -> str | None:
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def render_pdf(html: str, workdir: Path) -> Path:
    chrome = find_chrome()
    assert chrome, "no Chrome available"
    src = workdir / "cv.html"
    out = workdir / "cv.pdf"
    src.write_text(html, encoding="utf-8")
    subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={out}", src.as_uri()],
        check=True, capture_output=True, timeout=90,
    )
    return out


def page_count(pdf: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf.read_bytes()))
