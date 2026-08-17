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


def mast(data: dict, prefix: str, current: str) -> str:
    def nav_item(key: str, href: str) -> str:
        cur = ' aria-current="page"' if current == key else ""
        return f'<a href="{href}"{cur}>{esc(data["nav"][key])}</a>'

    return f"""<header class="mast">
  <a class="wordmark" href="{prefix}index.html">{esc(data["name"])}</a>
  <nav class="nav">
    {nav_item("collection", prefix + "collection.html")}
    {nav_item("contact", prefix + "contact.html")}
  </nav>
</header>"""


def document(title: str, body_class: str, prefix: str, body: str, extra_js: str = "") -> str:
    js = f'<script src="{prefix}site.js" defer></script>' if extra_js else ""
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


def write_home(data: dict) -> None:
    cover = piece_by_id(data, data["coverPieceId"])
    issue = issue_by_slug(data, cover["issue"])
    supporting = [piece_by_id(data, pid) for pid in data["supportingPieceIds"]]
    also = "".join(
        f'<li><a href="piece/{esc(p["slug"])}.html">{esc(p["title"])}</a></li>'
        for p in supporting
    )
    dates = f'<p class="dates">{esc(cover["dates"])}</p>' if cover.get("dates") else ""
    body = f"""{mast(data, "", "home")}
<main class="wrap">
  <p class="kicker">{esc(issue["title"])}</p>
  <div class="ornament" aria-hidden="true"></div>
  <h1>{esc(cover["title"])}</h1>
  {dates}
  {notes_html(cover.get("notes") or [])}
  {figure("", cover["image"], cover["title"])}
  <section class="also">
    <p class="kicker">{esc(data["alsoInThisIssue"])}</p>
    <ul class="also-list">{also}</ul>
  </section>
  <a class="to-collection" href="collection.html">{esc(data["nav"]["collection"])}</a>
</main>
"""
    (SITE / "index.html").write_text(
        document(data["name"], f"era-{issue['era']}", "", body), encoding="utf-8"
    )


def write_collection(data: dict) -> None:
    rows = []
    for issue in data["issues"]:
        chips = "".join(f'<i style="background:{c}"></i>' for c in issue["chips"])
        year_label = issue["year"] if issue["year"] else ""
        if issue.get("thumb"):
            thumb = f'<img class="thumb" src="images/{esc(issue["thumb"])}" alt="">'
        else:
            thumb = '<span class="thumb empty" aria-hidden="true"></span>'
        rows.append(
            f'<li><a href="{esc(issue["slug"])}.html">'
            f'<span class="year">{esc(year_label)}</span>'
            f'<span class="title">{esc(issue["title"])}</span>'
            f'<span class="chips" aria-hidden="true">{chips}</span>'
            f"{thumb}</a></li>"
        )
    # The grid is year | title | chips+thumb. Spec wanted chip + image.
    # Rebuild rows with chips beside thumb via CSS? Keep simple: year, title+chips, thumb.
    body = f"""{mast(data, "", "collection")}
<main class="wrap">
  <p class="kicker">{esc(data["name"])}</p>
  <h1>{esc(data["nav"]["collection"])}</h1>
  <ol class="index">{''.join(rows)}</ol>
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
  <a class="to-collection" href="collection.html">{esc(data["nav"]["collection"])}</a>
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
  <a class="to-collection" href="collection.html">{esc(data["nav"]["collection"])}</a>
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
