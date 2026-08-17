#!/usr/bin/env python3
"""Write static magazine pages from collection.json."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = SITE / "data" / "collection.json"
FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Barlow+Condensed:wght@500;600&"
    "family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,600"
    "&display=swap"
)


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def piece_by_id(data: dict, piece_id: str) -> dict:
    for piece in data["pieces"]:
        if piece["id"] == piece_id:
            return piece
    raise KeyError(piece_id)


def issue_by_slug(data: dict, slug: str) -> dict:
    for issue in data["issues"]:
        if issue["slug"] == slug:
            return issue
    raise KeyError(slug)


def img_src(prefix: str, name: str | None) -> str:
    if not name:
        return ""
    return f"{prefix}images/{name}"


def contents_panel(data: dict, prefix: str) -> str:
    years = []
    rooms = []
    for issue in data["issues"]:
        href = f'{prefix}{issue["slug"]}.html'
        if issue["kind"] == "special":
            rooms.append(f'<li><a href="{href}">{esc(issue["title"])}</a></li>')
        else:
            label = issue["year"] or issue["title"]
            years.append(
                f'<li><a href="{prefix}index.html#y-{esc(issue["slug"])}">{esc(label)}</a></li>'
            )
    pieces = "".join(
        f'<li><a href="{prefix}index.html#p-{esc(p["slug"])}">{esc(p["title"])}</a></li>'
        for p in data["pieces"]
    )
    return f"""<div class="contents" id="contents" hidden>
  <div class="contents-bar">
    <p class="kicker">{esc(data["nav"]["index"])}</p>
    <button type="button" class="contents-close" data-contents-close>{esc(data["nav"]["close"])}</button>
  </div>
  <p class="contents-label">{esc(data["nav"]["years"])}</p>
  <ol class="year-grid">{''.join(years)}</ol>
  <p class="contents-label">{esc(data["nav"]["rooms"])}</p>
  <ul class="room-list">{''.join(rooms)}</ul>
  <p class="contents-label">{esc(data["nav"]["pieces"])}</p>
  <ul class="room-list">{pieces}</ul>
  <p class="contents-label"><a href="{prefix}contact.html">{esc(data["nav"]["contact"])}</a></p>
</div>"""


def mast(data: dict, prefix: str, current: str) -> str:
    contact_cur = ' aria-current="page"' if current == "contact" else ""
    return f"""<header class="mast">
  <a class="wordmark" href="{prefix}index.html">{esc(data["name"])}</a>
  <nav class="nav">
    <a href="{prefix}collection.html" data-contents-open>{esc(data["nav"]["index"])}</a>
    <a href="{prefix}contact.html"{contact_cur}>{esc(data["nav"]["contact"])}</a>
  </nav>
</header>
{contents_panel(data, prefix)}"""


def neighbors(data: dict, slug: str) -> tuple[dict | None, dict | None]:
    issues = data["issues"]
    index = next(i for i, issue in enumerate(issues) if issue["slug"] == slug)
    prev_issue = issues[index - 1] if index > 0 else None
    next_issue = issues[index + 1] if index + 1 < len(issues) else None
    return prev_issue, next_issue


def pager(data: dict, issue: dict, prefix: str) -> str:
    prev_issue, next_issue = neighbors(data, issue["slug"])
    prev_html = (
        f'<a class="pager-prev" href="{prefix}{prev_issue["slug"]}.html">'
        f'<span>{esc(prev_issue["year"] or prev_issue["title"])}</span></a>'
        if prev_issue
        else "<span></span>"
    )
    next_html = (
        f'<a class="pager-next" href="{prefix}{next_issue["slug"]}.html">'
        f'<span>{esc(next_issue["year"] or next_issue["title"])}</span></a>'
        if next_issue
        else "<span></span>"
    )
    return f'<nav class="pager">{prev_html}{next_html}</nav>'


def document(title: str, body_class: str, prefix: str, body: str, extra_js: str = "") -> str:
    js = f'<script src="{prefix}site.js" defer></script>'
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}styles.css">
  {js}
</head>
<body{cls}>
{body}
</body>
</html>
"""


def figure(prefix: str, name: str, alt: str) -> str:
    return (
        f'<figure class="figure">'
        f'<img src="{img_src(prefix, name)}" alt="{esc(alt)}">'
        f"</figure>"
    )


def notes_html(notes: list[str]) -> str:
    if not notes:
        return ""
    paras = "".join(f"<p>{esc(n)}</p>" for n in notes)
    return f'<div class="prose">{paras}</div>'


def issue_images(data: dict, issue: dict) -> list[dict]:
    images: list[dict] = []
    seen: set[str] = set()
    if issue.get("leadPieceId"):
        piece = piece_by_id(data, issue["leadPieceId"])
        images.append(
            {
                "src": piece["image"],
                "alt": piece["title"],
                "title": piece["title"],
                "dates": piece.get("dates") or "",
                "notes": piece.get("notes") or [],
                "anchor": f"p-{piece['slug']}",
            }
        )
        seen.add(piece["image"])
    for name in issue.get("sequence") or []:
        if name in seen:
            continue
        images.append(
            {
                "src": name,
                "alt": issue["title"],
                "title": "",
                "dates": "",
                "notes": [],
                "anchor": "",
            }
        )
        seen.add(name)
    if not images and issue.get("thumb"):
        images.append(
            {
                "src": issue["thumb"],
                "alt": issue["title"],
                "title": "",
                "dates": "",
                "notes": [],
                "anchor": "",
            }
        )
    return images


def layout_for(issue: dict, images: list[dict]) -> str:
    if issue["slug"] == "2026":
        return "empty"
    if issue["slug"] == "1930":
        return "hero"
    if issue["slug"] == "1954":
        return "stack"
    if len(images) >= 3:
        return "strip"
    if len(images) == 2:
        return "pair"
    return "solo"


PAPER_BY_ERA = {
    "1930": ("#f4e6d4", "#8a2a24", "#1a0e0c"),
    "1954": ("#f7ebe6", "#c8102e", "#1a1214"),
    "fifa": ("#efe6d4", "#1c3a6b", "#12151c"),
}


def era_attrs(issue: dict) -> str:
    chips = issue.get("chips") or ["#9a2b24", "#14110e", "#f3eee4"]
    era = issue.get("era") or ""
    if era in PAPER_BY_ERA:
        paper, rule, ink = PAPER_BY_ERA[era]
    else:
        paper, rule, ink = "#f3eee4", chips[0], "#14110e"
    key = era or issue["slug"]
    return (
        f'data-era="{esc(key)}" data-paper="{esc(paper)}" '
        f'data-rule="{esc(rule)}" data-ink="{esc(ink)}" '
        f'data-year="{esc(issue.get("year") or "")}"'
    )


def img_tag(item: dict, eager: bool = False, with_id: bool = True) -> str:
    loading = "eager" if eager else "lazy"
    extra_id = (
        f' id="{esc(item["anchor"])}"' if with_id and item.get("anchor") else ""
    )
    return (
        f'<figure class="figure"{extra_id}>'
        f'<img src="images/{esc(item["src"])}" alt="{esc(item["alt"])}" loading="{loading}">'
        f"</figure>"
    )


def beat_word(text: str, year: str = "") -> str:
    return f"""<section class="beat beat-word" data-paper="#f3eee4" data-rule="#9a2b24" data-ink="#14110e" data-year="{esc(year)}">
  <p>{esc(text)}</p>
</section>"""


def beat_object(item: dict, year: str, paper: str, rule: str, ink: str) -> str:
    title = f'<p class="object-title">{esc(item["title"])}</p>' if item.get("title") else ""
    dates = f'<p class="dates">{esc(item["dates"])}</p>' if item.get("dates") else ""
    return f"""<section class="beat beat-solo" id="{esc(item.get("anchor") or "")}" data-paper="{esc(paper)}" data-rule="{esc(rule)}" data-ink="{esc(ink)}" data-year="{esc(year)}">
  <p class="year-mark">{esc(year)}</p>
  {img_tag(item, eager=True, with_id=False)}
  {title}
  {dates}
  {notes_html(item.get("notes") or [])}
</section>"""


def beat_year(data: dict, issue: dict) -> str:
    images = issue_images(data, issue)
    layout = layout_for(issue, images)
    attrs = era_attrs(issue)
    year = issue.get("year") or ""
    mark = f'<p class="year-mark">{esc(year)}</p>' if year else ""
    if layout == "empty":
        return f"""<section class="beat beat-empty" id="y-{esc(issue["slug"])}" {attrs}>
  {mark}
</section>"""

    frames = []
    named = ""
    for i, item in enumerate(images):
        frames.append(img_tag(item, eager=(issue["slug"] in {"1930", "1954"} and i == 0)))
        if item.get("title") and not named:
            dates = f'<p class="dates">{esc(item["dates"])}</p>' if item.get("dates") else ""
            named = (
                f'<div class="object-copy">'
                f'<p class="object-title">{esc(item["title"])}</p>'
                f"{dates}"
                f'{notes_html(item.get("notes") or [])}'
                f"</div>"
            )

    if layout == "hero" and images:
        rest = "".join(frames[1:])
        return f"""<section class="beat beat-hero" id="y-{esc(issue["slug"])}" {attrs}>
  {mark}
  {frames[0]}
  {named}
  <div class="strip">{rest}</div>
</section>"""
    if layout == "pair":
        return f"""<section class="beat beat-pair" id="y-{esc(issue["slug"])}" {attrs}>
  {mark}
  <div class="pair">{''.join(frames)}</div>
</section>"""
    if layout == "stack":
        first = frames[0] if frames else ""
        rest = "".join(frames[1:])
        return f"""<section class="beat beat-stack" id="y-{esc(issue["slug"])}" {attrs}>
  {mark}
  {first}
  {named}
  <div class="stack">{rest}</div>
</section>"""
    if layout == "strip":
        return f"""<section class="beat beat-strip" id="y-{esc(issue["slug"])}" {attrs}>
  {mark}
  {named}
  <div class="strip">{''.join(frames)}</div>
</section>"""
    return f"""<section class="beat beat-solo" id="y-{esc(issue["slug"])}" {attrs}>
  {mark}
  {''.join(frames)}
  {named}
</section>"""


def write_home(data: dict) -> None:
    pin = piece_by_id(data, "fifa-1904")
    pin_item = {
        "src": pin["image"],
        "alt": pin["title"],
        "title": pin["title"],
        "dates": "",
        "notes": [],
        "anchor": "p-fifa-1904",
    }
    beats = [
        beat_object(pin_item, "1904", "#efe6d4", "#0e1624", "#12151c"),
        beat_word(data["copy"]["introduction"][0], "1904"),
        beat_word(data["copy"]["information"][1], "1924"),
    ]
    after = {
        "1930": [
            beat_word(data["copy"]["information"][2], "1930"),
            beat_word(data["copy"]["information"][3], "1930"),
        ],
        "1934": [beat_word(data["copy"]["information"][4], "1934")],
        "2018": [beat_word(data["copy"]["introduction"][1], "2018")],
    }
    for issue in data["issues"]:
        if issue["kind"] == "special":
            continue
        beats.append(beat_year(data, issue))
        beats.extend(after.get(issue["slug"], []))

    beats.extend(
        [
            beat_word(data["copy"]["introduction"][2], "2026"),
            beat_word(data["copy"]["introduction"][3], "2026"),
            beat_word(data["copy"]["information"][0], "2026"),
            beat_word(data["copy"]["viewing"], "2026"),
        ]
    )

    people = []
    for person in data["contacts"]:
        addr = "<br>".join(esc(line) for line in person["address"])
        people.append(
            f'<div class="person"><strong>{esc(person["name"])}</strong><br>{addr}<br>'
            f"{esc(person['phone'])}<br>"
            f'<a href="mailto:{esc(person["email"])}">{esc(person["email"])}</a></div>'
        )
    form = data["form"]
    emails = ", ".join(p["email"] for p in data["contacts"])
    close = f"""<section class="beat beat-close" data-paper="#f3eee4" data-rule="#9a2b24" data-ink="#14110e" data-year="">
  <div class="people">{''.join(people)}</div>
  <form id="enquire" novalidate>
    <label for="name">{esc(form["name"])}</label>
    <input id="name" name="name" autocomplete="name" required>
    <label for="email">{esc(form["email"])}</label>
    <input id="email" name="email" type="email" autocomplete="email" required>
    <label for="piece">{esc(form["piece"])}</label>
    <input id="piece" name="piece">
    <label for="message">{esc(form["message"])}</label>
    <textarea id="message" name="message" required></textarea>
    <button class="btn" type="submit">{esc(form["send"])}</button>
    <p class="form-error" hidden data-required="{esc(form["required"])}"></p>
  </form>
  <div class="form-ok" id="enquire-ok" hidden>
    <p>{esc(form["thanks"])} {esc(emails)}.</p>
  </div>
</section>"""

    body = f"""{mast(data, "", "home")}
<p class="time" id="time" hidden></p>
<main class="walk">
{''.join(beats)}
{close}
</main>
"""
    (SITE / "index.html").write_text(
        document(data["name"], "walk-page", "", body), encoding="utf-8"
    )


def write_collection(data: dict) -> None:
    years = []
    rooms = []
    for issue in data["issues"]:
        href = f'{issue["slug"]}.html'
        if issue["kind"] == "special":
            rooms.append(f'<li><a href="{href}">{esc(issue["title"])}</a></li>')
        else:
            years.append(
                f'<li><a href="index.html#y-{esc(issue["slug"])}">{esc(issue["year"])}</a></li>'
            )
    pieces = "".join(
        f'<li><a href="index.html#p-{esc(p["slug"])}">{esc(p["title"])}</a></li>'
        for p in data["pieces"]
    )
    body = f"""{mast(data, "", "collection")}
<main class="wrap">
  <p class="kicker">{esc(data["name"])}</p>
  <h1>{esc(data["nav"]["index"])}</h1>
  <p class="contents-label">{esc(data["nav"]["years"])}</p>
  <ol class="year-grid">{''.join(years)}</ol>
  <p class="contents-label">{esc(data["nav"]["rooms"])}</p>
  <ul class="room-list">{''.join(rooms)}</ul>
  <p class="contents-label">{esc(data["nav"]["pieces"])}</p>
  <ul class="room-list">{pieces}</ul>
</main>
"""
    (SITE / "collection.html").write_text(
        document(f"{data['nav']['collection']} · {data['name']}", "", "", body),
        encoding="utf-8",
    )


def write_issue(data: dict, issue: dict) -> None:
    lead = ""
    if issue.get("leadPieceId"):
        piece = piece_by_id(data, issue["leadPieceId"])
        dates = f'<p class="dates">{esc(piece["dates"])}</p>' if piece.get("dates") else ""
        lead = f"""
  <p class="kicker">{esc(issue["title"])}</p>
  <div class="ornament" aria-hidden="true"></div>
  <h1><a href="piece/{esc(piece["slug"])}.html">{esc(piece["title"])}</a></h1>
  {dates}
  {notes_html(piece.get("notes") or [])}
  {figure("", piece["image"], piece["title"])}
"""
    else:
        lead = f"""
  <p class="kicker">{esc(data["nav"]["collection"])}</p>
  <h1>{esc(issue["title"])}</h1>
"""
        if issue.get("thumb") and not issue.get("sequence"):
            lead += figure("", issue["thumb"], issue["title"])

    frames = []
    for name in issue.get("sequence") or []:
        frames.append(figure("", name, issue["title"]))
    seq = f'<div class="sequence">{"".join(frames)}</div>' if frames else ""

    era = f"era-{issue['era']}" if issue.get("era") else ""
    body = f"""{mast(data, "", "collection")}
<main class="wrap">
{lead}
{seq}
  {pager(data, issue, "")}
</main>
"""
    (SITE / f"{issue['slug']}.html").write_text(
        document(f"{issue['title']} · {data['name']}", era, "", body),
        encoding="utf-8",
    )


def write_piece(data: dict, piece: dict) -> None:
    issue = issue_by_slug(data, piece["issue"])
    dates = f'<p class="dates">{esc(piece["dates"])}</p>' if piece.get("dates") else ""
    era = f"era-{issue['era']}" if issue.get("era") else ""
    body = f"""{mast(data, "../", "collection")}
<main class="wrap">
  <p class="kicker"><a href="../{esc(issue["slug"])}.html">{esc(issue["title"])}</a></p>
  <div class="ornament" aria-hidden="true"></div>
  <h1>{esc(piece["title"])}</h1>
  {dates}
  {notes_html(piece.get("notes") or [])}
  {figure("../", piece["image"], piece["title"])}
  <p class="endnote"><a href="../contact.html">{esc(data["contactLine"])}</a></p>
  {pager(data, issue, "../")}
</main>
"""
    dest = SITE / "piece" / f"{piece['slug']}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        document(f"{piece['title']} · {data['name']}", era, "../", body),
        encoding="utf-8",
    )


def write_contact(data: dict) -> None:
    intro = "".join(f"<p>{esc(p)}</p>" for p in data["copy"]["introduction"])
    info = "".join(f"<p>{esc(p)}</p>" for p in data["copy"]["information"])
    people = []
    for person in data["contacts"]:
        addr = "<br>".join(esc(line) for line in person["address"])
        people.append(
            f'<div class="person">'
            f"<strong>{esc(person['name'])}</strong><br>{addr}<br>"
            f"{esc(person['phone'])}<br>"
            f'<a href="mailto:{esc(person["email"])}">{esc(person["email"])}</a>'
            f"</div>"
        )
    f = data["form"]
    emails = ", ".join(p["email"] for p in data["contacts"])
    body = f"""{mast(data, "", "contact")}
<main class="wrap">
  <p class="kicker">{esc(data["copy"]["highlightsKicker"])}</p>
  <p class="dates">{esc(data["copy"]["byline"])}</p>
  <div class="prose">{intro}</div>
  <h2>{esc(data["copy"]["informationHeading"])}</h2>
  <div class="prose">{info}</div>
  <p>{esc(data["copy"]["viewing"])}</p>
  <div class="people">{''.join(people)}</div>
  <form id="enquire" novalidate>
    <label for="name">{esc(f["name"])}</label>
    <input id="name" name="name" autocomplete="name" required>
    <label for="email">{esc(f["email"])}</label>
    <input id="email" name="email" type="email" autocomplete="email" required>
    <label for="piece">{esc(f["piece"])}</label>
    <input id="piece" name="piece">
    <label for="message">{esc(f["message"])}</label>
    <textarea id="message" name="message" required></textarea>
    <button class="btn" type="submit">{esc(f["send"])}</button>
    <p class="form-error" hidden data-required="{esc(f["required"])}"></p>
  </form>
  <div class="form-ok" id="enquire-ok" hidden>
    <p>{esc(f["thanks"])} {esc(emails)}.</p>
  </div>
</main>
"""
    (SITE / "contact.html").write_text(
        document(f"{data['nav']['contact']} · {data['name']}", "", "", body, extra_js="1"),
        encoding="utf-8",
    )


def write_404(data: dict) -> None:
    body = f"""{mast(data, "", "home")}
<main class="wrap">
  <p class="kicker">{esc(data["name"])}</p>
  <h1>{esc(data["notFound"])}</h1>
</main>
"""
    (SITE / "404.html").write_text(
        document(data["name"], "", "", body), encoding="utf-8"
    )


def main() -> None:
    data = load()
    SITE.mkdir(parents=True, exist_ok=True)
    write_home(data)
    write_collection(data)
    write_contact(data)
    write_404(data)
    for issue in data["issues"]:
        write_issue(data, issue)
    for piece in data["pieces"]:
        write_piece(data, piece)
    print(f"wrote pages in {SITE}")


if __name__ == "__main__":
    main()
