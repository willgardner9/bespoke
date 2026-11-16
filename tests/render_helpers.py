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


def remove_section(html: str, name: str) -> str:
    pattern = re.compile(rf'<section data-section="{name}">.*?</section>\s*', re.S)
    assert pattern.search(html), f"section {name} missing"
    return pattern.sub("", html, count=1)


def _bullet(fact: dict, detail: bool) -> str:
    text = fact["what"]
    if detail:
        text = ". ".join(filter(None, [fact["what"], fact.get("how"), fact.get("outcome")]))
    return f"<li>{text}</li>"


def fill_template(career: dict, facts_per_role: int = 2, detail: bool = False) -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    profile = career["profile"]
    html = set_slot(html, "name", profile["name"])
    html = set_slot(html, "contact", " | ".join(filter(None, [profile.get("location"), profile.get("email"), profile.get("phone")])))
    html = set_slot(html, "summary", "Experienced analyst.")
    employers: list[list[dict]] = []
    for role in career["roles"]:
        if employers and employers[-1][0]["company"] == role["company"]:
            employers[-1].append(role)
        else:
            employers.append([role])
    roles = []
    for group in employers:
        multi = len(group) > 1
        span = f'{month(group[-1]["start"])} – {month(group[0]["end"])}'
        loc = group[0].get("location")
        if not multi and not group[0]["facts"][:facts_per_role]:
            role = group[0]
            where = f', {loc}' if loc else ""
            roles.append(
                '<div class="employer compact"><div class="emp-head">'
                f'<span>{role["company"]}, <span class="plain">{role["title"]}{where}</span></span>'
                f'<span class="span">{span}</span></div></div>'
            )
            continue
        block = f'<div class="employer"><div class="emp-head"><span>{group[0]["company"]}</span><span class="span">{span}</span></div>'
        if loc:
            block += f'<div class="loc">{loc}</div>'
        block += f'<div class="roles {"multi" if multi else "single"}">'
        for role in group:
            bullets = "".join(_bullet(f, detail) for f in role["facts"][:facts_per_role])
            dates = f'<span class="dates">{month(role["start"])} – {month(role["end"])}</span>' if multi else ""
            block += (f'<div class="role"><div class="role-head"><span>{role["title"]}</span>{dates}</div>'
                      f'<ul>{bullets}</ul></div>')
        roles.append(block + "</div></div>")
    html = set_slot(html, "experience", "".join(roles))
    edu = "".join(
        f'<div class="item"><span><b>{e["qualification"]}</b>, {e["institution"]}</span>'
        f'<span>{month(e["start"])} – {month(e["end"])}</span></div>'
        for e in career.get("education", [])
    )
    html = set_slot(html, "education", edu)
    projects = "".join(
        f'<div class="role"><div class="role-head"><span>{p["name"]}</span></div>'
        f'<ul>{"".join(_bullet(f, detail) for f in p["facts"])}</ul></div>'
        for p in career.get("projects", [])
    )
    if projects:
        html = set_slot(html, "projects", projects)
    else:
        html = remove_section(html, "projects")
    certs = "".join(
        f'<p>{c["name"]}{" (" + str(c["year"]) + ")" if c.get("year") else ""}</p>'
        for c in career.get("certifications", [])
    )
    if certs:
        html = set_slot(html, "certifications", certs)
    else:
        html = remove_section(html, "certifications")
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
