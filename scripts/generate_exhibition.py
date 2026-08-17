#!/usr/bin/env python3
"""Build the exhibition site from source/data/inventory.json only.

No inferred object titles. Chapter titles come from source page headings.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = json.loads((ROOT / "source" / "data" / "inventory.json").read_text(encoding="utf-8"))
OUT = ROOT / "exhibition"
FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,500&"
    "family=IBM+Plex+Sans:wght@400;500;600&"
    "family=Source+Serif+4:opsz,wght@8..60,400;8..60,500"
    "&display=swap"
)

NAV = [
    ("Collection", "archive.html"),
    ("Sale", "sale.html"),
    ("Contact", "contact.html"),
]

ERA_CLASS = {
    1930: "era-1930",
    1966: "era-1966",
    1970: "era-1970",
    1990: "era-1990",
    2022: "era-2022",
}

SOURCE_COPY = {
    "site_title": "Top World - Cup - Collection",
    "sales_note": (
        "Please note, that you can find the information about the items in the "
        "sales documentation (PDF – Sales Document / Verkauf / Sale / Vente / Venta). "
        "If you have any questions, please do not hesitate to contact us."
    ),
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def chapter_heading(page: dict) -> str:
    for text in page.get("bodyCopy") or []:
        if text.startswith("World Cup") or text.startswith("Olympic Games"):
            return text
        if text.startswith("Aotographs") or text.startswith("Autographs"):
            return text
        if "FIFA" in text and "official" in text.lower():
            return text
        if text.lower().startswith("information board"):
            return text
        if text.lower().startswith("sports"):
            return text
        if text == "Divers":
            return text
    if page.get("headings"):
        return page["headings"][0]["text"]
    return page.get("title") or page["file"]


def page_assets(page_name: str) -> list[dict]:
    return [
        a
        for a in INV["assets"]
        if a.get("sourcePage") == page_name
        and a.get("localPath")
        and not a.get("navChrome")
        and not a.get("error")
    ]


def media_src(asset: dict) -> str:
    # source/assets/1930-uruguay/file.jpg -> media/1930-uruguay/file.jpg
    rel = Path(asset["localPath"])
    parts = rel.parts
    if "assets" in parts:
        i = parts.index("assets")
        return "media/" + "/".join(parts[i + 1 :])
    return asset["localPath"]


def tournament_pages() -> list[dict]:
    return [
        p
        for p in INV["pages"]
        if p.get("kind") in {"olympic", "world-cup"} and not p.get("error")
    ]


def collection_pages() -> list[dict]:
    return [
        p
        for p in INV["pages"]
        if p.get("kind") == "collection" and not p.get("error")
    ]


def chapter_href(page: dict) -> str:
    folder = page["folder"]
    if page["kind"] in {"olympic", "world-cup"}:
        return f"world-cups/{folder}.html"
    return f"collections/{folder}.html"


def prefix_for(href: str) -> str:
    return "../" if "/" in href else ""


def document(title: str, body: str, prefix: str, era: str = "", current: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(SOURCE_COPY['site_title'])}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/exhibition.css">
  <script src="{prefix}js/exhibition.js" defer></script>
</head>
<body class="{esc(era)}">
{body}
</body>
</html>
"""


def mast(prefix: str, current: str) -> str:
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if current == href else ""
        links.append(f'<a href="{prefix}{href}"{cur}>{esc(label)}</a>')
    return f"""<header class="mast">
  <a class="wordmark" href="{prefix}index.html">{esc(SOURCE_COPY["site_title"])}</a>
  <nav class="nav">{''.join(links)}</nav>
</header>"""


def timeline(prefix: str, current_year: int | None = None) -> str:
    items = []
    years = tournament_pages()
    prev_year = None
    for page in years:
        year = page.get("year")
        if prev_year == 1938 and year == 1950:
            items.append('<span class="gap" aria-hidden="true"></span>')
        href = prefix + chapter_href(page)
        cur = ' aria-current="page"' if year == current_year else ""
        label = str(year) if year else page["folder"]
        items.append(f'<a href="{href}"{cur}>{esc(label)}</a>')
        prev_year = year
    return f'<div class="timeline-wrap"><nav class="timeline" aria-label="Years">{"".join(items)}</nav></div>'


def viewer() -> str:
    return """<div class="viewer" id="viewer" hidden role="dialog" aria-modal="true">
  <div class="viewer-bar">
    <span id="viewer-meta"></span>
    <button type="button" data-close>Close</button>
  </div>
  <img id="viewer-image" alt="">
  <div class="viewer-foot">
    <button type="button" data-prev>Previous</button>
    <button type="button" data-next>Next</button>
  </div>
</div>"""


def gallery_html(assets: list[dict], heading: str, prefix: str) -> str:
    if not assets:
        return "<p class=\"note\"></p>"
    cells = []
    for i, asset in enumerate(assets):
        src = prefix + media_src(asset)
        cls = "hero-item" if i == 0 else ("span-2" if i in {3, 8} else "")
        cells.append(
            f'<a class="{cls}" href="{esc(src)}" data-object data-full="{esc(src)}" '
            f'data-alt="" data-meta="{esc(heading)}">'
            f'<img src="{esc(src)}" alt="" width="{asset.get("width") or ""}" '
            f'height="{asset.get("height") or ""}" loading="{"eager" if i == 0 else "lazy"}">'
            f"</a>"
        )
    return f'<div class="gallery">{"".join(cells)}</div>'


def write_home() -> None:
    pages = tournament_pages()
    uruguay = next(p for p in pages if p.get("year") == 1930)
    hero_assets = page_assets(uruguay["file"])
    hero_assets = sorted(
        hero_assets,
        key=lambda a: (a.get("width") or 0) * (a.get("height") or 0),
        reverse=True,
    )
    hero = hero_assets[0]
    hero_src = media_src(hero)
    body = f"""<div class="shell">
{mast("", "index.html")}
{timeline("")}
<section class="hero">
  <figure class="hero-figure">
    <img src="{esc(hero_src)}" alt="" width="{hero.get("width") or ""}" height="{hero.get("height") or ""}">
  </figure>
  <div class="hero-copy">
    <h1>{esc(SOURCE_COPY["site_title"])}</h1>
    <p class="lede">{esc(SOURCE_COPY["sales_note"])}</p>
    <div class="actions">
      <a class="action" href="world-cups/1930-uruguay.html">1930 Uruguay</a>
      <a class="action" href="archive.html">Collection</a>
      <a class="action" href="sale.html">Sale</a>
    </div>
  </div>
</section>
</div>"""
    (OUT / "index.html").write_text(
        document(SOURCE_COPY["site_title"], body, "", current="index.html"),
        encoding="utf-8",
    )


def write_chapter(page: dict) -> None:
    heading = chapter_heading(page)
    assets = page_assets(page["file"])
    year = page.get("year")
    era = ERA_CLASS.get(year, "")
    href = chapter_href(page)
    dest = OUT / href
    dest.parent.mkdir(parents=True, exist_ok=True)
    rel = prefix_for(href)
    year_label = str(year) if year else heading
    host = heading if year else page.get("kind") or ""
    for cut in (
        f"World Cup {year} " if year else "World Cup ",
        f"Olympic Games {year} " if year else "Olympic Games ",
        "World Cup ",
        "Olympic Games ",
    ):
        if host.startswith(cut):
            host = host[len(cut) :]
            break
    body = f"""<div class="shell">
{mast(rel, href)}
{timeline(rel, year)}
<article class="chapter">
  <header class="chapter-head">
    <p class="chapter-year">{esc(year_label)}</p>
    <p class="chapter-host">{esc(host)}</p>
  </header>
  {gallery_html(assets, heading, rel)}
</article>
</div>
{viewer()}"""
    dest.write_text(
        document(f"{heading} · {SOURCE_COPY['site_title']}", body, rel, era=era),
        encoding="utf-8",
    )


def write_archive() -> None:
    folders = []
    cards = []
    seen = set()
    for page in tournament_pages() + collection_pages():
        folder = page["folder"]
        if folder not in seen:
            folders.append((folder, chapter_heading(page)))
            seen.add(folder)
        heading = chapter_heading(page)
        for asset in page_assets(page["file"]):
            src = media_src(asset)
            cards.append(
                f'<a href="{esc(src)}" data-archive-item data-folder="{esc(folder)}" '
                f'data-object data-full="{esc(src)}" data-alt="" data-meta="{esc(heading)}">'
                f'<img src="{esc(src)}" alt="" loading="lazy"></a>'
            )
    buttons = ['<button type="button" data-folder="all" aria-pressed="true">All</button>']
    for folder, label in folders:
        buttons.append(
            f'<button type="button" data-folder="{esc(folder)}">{esc(label)}</button>'
        )
    body = f"""<div class="shell">
{mast("", "archive.html")}
{timeline("")}
<div class="page"><h1>Collection</h1></div>
<div class="filter" id="archive-filter">{''.join(buttons)}</div>
<div class="archive-grid">{''.join(cards)}</div>
</div>
{viewer()}"""
    (OUT / "archive.html").write_text(
        document(f"Collection · {SOURCE_COPY['site_title']}", body, ""),
        encoding="utf-8",
    )


def write_sale() -> None:
    docs = []
    for doc in INV.get("documents") or []:
        name = Path(doc["localPath"]).name
        docs.append(
            f'<li><a href="documents/{esc(name)}">{esc(name)}</a></li>'
        )
    body = f"""<div class="shell">
{mast("", "sale.html")}
<article class="page">
  <h1>Sale</h1>
  <p>{esc(SOURCE_COPY["sales_note"])}</p>
  <ul class="docs">{''.join(docs)}</ul>
</article>
</div>"""
    (OUT / "sale.html").write_text(
        document(f"Sale · {SOURCE_COPY['site_title']}", body, ""),
        encoding="utf-8",
    )


def write_contact() -> None:
    contact = next(p for p in INV["pages"] if p["file"] == "contact.html")
    paras = "".join(f"<p>{esc(line)}</p>" for line in contact.get("bodyCopy") or [])
    body = f"""<div class="shell">
{mast("", "contact.html")}
<article class="page">
  <h1>Contact</h1>
  {paras}
</article>
</div>"""
    (OUT / "contact.html").write_text(
        document(f"Contact · {SOURCE_COPY['site_title']}", body, ""),
        encoding="utf-8",
    )


def write_sitemap() -> None:
    urls = ["index.html", "archive.html", "sale.html", "contact.html"]
    for page in tournament_pages() + collection_pages():
        urls.append(chapter_href(page))
    (OUT / "sitemap.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")


def main() -> None:
    (OUT / "world-cups").mkdir(parents=True, exist_ok=True)
    (OUT / "collections").mkdir(parents=True, exist_ok=True)
    media = OUT / "media"
    docs = OUT / "documents"
    if not media.exists():
        media.symlink_to((ROOT / "source" / "assets").resolve())
    if not docs.exists() and (ROOT / "source" / "documents").exists():
        docs.symlink_to((ROOT / "source" / "documents").resolve())
    write_home()
    write_archive()
    write_sale()
    write_contact()
    for page in tournament_pages() + collection_pages():
        write_chapter(page)
    write_sitemap()
    print(f"wrote exhibition → {OUT}")


if __name__ == "__main__":
    main()
