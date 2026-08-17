#!/usr/bin/env python3
"""Build the exhibition site from source/data/inventory.json only.

No inferred object titles. Chapter titles come from source page headings.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = json.loads((ROOT / "source" / "data" / "inventory.json").read_text(encoding="utf-8"))
OUT = ROOT / "exhibition"
FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&"
    "family=Outfit:wght@400;500;600"
    "&display=swap"
)

NAV = [
    ("The collection", "archive.html"),
    ("Timeline", "index.html#timeline"),
    ("Sale", "sale.html"),
    ("Contact", "contact.html"),
]

ERA_CLASS = {
    1930: "era-1930",
    1954: "era-1930",
    1966: "era-1966",
    1970: "era-1970",
    1990: "era-1990",
    2022: "era-2022",
}

ERA_FIELD = {
    1930: "atmosphere/era-1930.jpg",
    1954: "atmosphere/era-1954.jpg",
    1966: "atmosphere/era-1966.jpg",
    1970: "atmosphere/era-1970.jpg",
    1990: "atmosphere/era-1990.jpg",
    2022: "atmosphere/era-2022.jpg",
}

SOURCE_COPY = {
    "site_title": "Top World - Cup - Collection",
    "span": "1930 – 2022",
    "olympics_line": "including Olympic Games 1924 / 1928",
    "sales_note": (
        "Please note, that you can find the information about the items in the "
        "sales documentation (PDF – Sales Document / Verkauf / Sale / Vente / Venta). "
        "If you have any questions, please do not hesitate to contact us."
    ),
    "pdf_by": "by Thomas Käppeli",
    "pdf_highlights": "The highlights of the collection",
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def chapter_heading(page: dict) -> str:
    for text in page.get("bodyCopy") or []:
        if (
            text.startswith("World Cup")
            or text.startswith("Olympic Games")
            or "Olympic Games" in text
            or text.startswith("World Cup")
            or re.match(r"^\d{4}\s+(Olympic Games|World Cup)", text)
        ):
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


def host_name(page: dict) -> str:
    import re

    heading = chapter_heading(page)
    heading = re.sub(r"^\d{4}\s*", "", heading)
    heading = re.sub(r"^(Olympic Games|World Cup)\s*", "", heading, flags=re.I)
    heading = re.sub(r"^\d{4}\s*", "", heading)
    return heading.strip() or chapter_heading(page)


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
    prev_year = None
    for page in tournament_pages():
        year = page.get("year")
        if prev_year == 1938 and year == 1950:
            items.append('<span class="gap" aria-hidden="true"></span>')
        href = prefix + chapter_href(page)
        cur = ' aria-current="page"' if year == current_year else ""
        label = str(year) if year else page["folder"]
        host = host_name(page)
        items.append(
            f'<a href="{href}"{cur}><span class="y">{esc(label)}</span>'
            f'<span class="h">{esc(host)}</span></a>'
        )
        prev_year = year
    return (
        f'<div class="timeline-wrap" id="timeline">'
        f'<p class="timeline-kicker">{esc(SOURCE_COPY["span"])}</p>'
        f'<nav class="timeline" aria-label="Years">{"".join(items)}</nav></div>'
    )


def foot(prefix: str) -> str:
    return (
        f'<footer class="site-foot">{esc(SOURCE_COPY["site_title"])} · '
        f'{esc(SOURCE_COPY["span"])}</footer>'
    )


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


def collage_html(assets: list[dict], heading: str, prefix: str, limit: int = 5) -> str:
    chosen = assets[:limit]
    if not chosen:
        return ""
    cells = []
    for i, asset in enumerate(chosen):
        src = prefix + media_src(asset)
        cells.append(
            f'<a class="p{i}" href="{esc(src)}" data-object data-full="{esc(src)}" '
            f'data-alt="" data-meta="{esc(heading)}">'
            f'<img src="{esc(src)}" alt="" loading="{"eager" if i < 2 else "lazy"}"></a>'
        )
    return f'<div class="spread-stage">{"".join(cells)}</div>'


def spread_html(
    assets: list[dict],
    heading: str,
    year_label: str,
    host: str,
    prefix: str,
    field: str | None,
) -> str:
    field_img = (
        f'<img class="spread-field" src="{prefix}{field}" alt="">' if field else ""
    )
    return f"""<section class="spread">
  {field_img}
  <div class="spread-copy">
    <p class="chapter-kicker">{esc(heading)}</p>
    <p class="chapter-year">{esc(year_label)}</p>
    <p class="chapter-host">{esc(host)}</p>
  </div>
  {collage_html(assets, heading, prefix)}
</section>"""


def write_home() -> None:
    uruguay = next(p for p in tournament_pages() if p.get("year") == 1930)
    u_assets = page_assets(uruguay["file"])
    hero_src = "atmosphere/hero-cup.jpg"
    mosaic = []
    for year in (1930, 1954, 1966, 1970, 1990, 2022, None):
        if year is None:
            pages = collection_pages()
        else:
            pages = [p for p in tournament_pages() if p.get("year") == year]
        for page in pages[:1]:
            assets = page_assets(page["file"])
            if assets:
                mosaic.append((page, assets[0]))
            if len(mosaic) >= 8:
                break
        if len(mosaic) >= 8:
            break
    mosaic_html = "".join(
        f'<a href="{chapter_href(page)}"><img src="{esc(media_src(asset))}" alt=""></a>'
        for page, asset in mosaic
    )
    body = f"""<div class="shell">
{mast("", "index.html")}
<section class="hero">
  <img class="hero-plate" src="{esc(hero_src)}" alt="">
  <div class="hero-copy">
    <p class="eyebrow">{esc(SOURCE_COPY["span"])} · {esc(SOURCE_COPY["olympics_line"])}</p>
    <h1>{esc(SOURCE_COPY["site_title"])}</h1>
    <div class="actions">
      <a class="btn" href="world-cups/1930-uruguay.html">1930 Uruguay</a>
      <a class="btn-ghost" href="archive.html">The collection</a>
    </div>
  </div>
</section>
{timeline("")}
{spread_html(u_assets, chapter_heading(uruguay), "1930", "Uruguay", "", ERA_FIELD[1930])}
<p class="home-block" style="padding-top:0"><a class="btn" href="world-cups/1930-uruguay.html">1930 Uruguay</a></p>
<section class="band-navy home-block">
  <p class="eyebrow">The collection</p>
  <h2>{esc(SOURCE_COPY["site_title"])}</h2>
  <div class="mosaic">{mosaic_html}</div>
  <p style="margin-top:1.4rem"><a class="btn" href="archive.html">The collection</a></p>
</section>
<section class="band-cream home-block">
  <p class="attr">Sales documentation</p>
  <h2>Sale</h2>
  <p style="max-width:36rem">{esc(SOURCE_COPY["sales_note"])}</p>
  <p><a class="btn" href="sale.html">Sale</a></p>
</section>
{foot("")}
</div>
{viewer()}"""
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
    field = ERA_FIELD.get(year)
    host = host_name(page)
    year_label = str(year) if year else heading
    body = f"""<div class="shell">
{mast(rel, href)}
{timeline(rel, year)}
{spread_html(assets, heading, year_label, host, rel, field)}
<article class="chapter">
  {gallery_html(assets[5:], heading, rel) if len(assets) > 5 else ""}
</article>
</div>
{viewer()}
{foot(rel)}"""
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
{viewer()}
{foot("")}"""
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
</div>
{foot("")}"""
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
</div>
{foot("")}"""
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
