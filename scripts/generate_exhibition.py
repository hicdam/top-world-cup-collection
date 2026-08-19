#!/usr/bin/env python3
"""Build the exhibition from source/data/inventory.json only.

No inferred object titles. Chapter titles come from source page headings.
Navigational typos are corrected where the intended year/host is unambiguous.
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
    "family=Fraunces:opsz,wght@9..144,400;9..144,500&"
    "family=Outfit:wght@300;400;500;600"
    "&display=swap"
)

NAV = [
    ("The collection", "archive.html"),
    ("Timeline", "index.html#timeline"),
    ("Story", "index.html#story"),
    ("Sale", "sale.html"),
    ("Contact", "contact.html"),
]

HOSTS = {
    1924: "Paris",
    1928: "Amsterdam",
    1930: "Uruguay",
    1934: "Italy",
    1938: "France",
    1950: "Brasil",
    1954: "Switzerland",
    1958: "Sweden",
    1962: "Chile",
    1966: "England",
    1970: "Mexico",
    1974: "Germany",
    1978: "Argentina",
    1982: "Spain",
    1986: "Mexico",
    1990: "Italy",
    1994: "USA",
    1998: "France",
    2002: "Korea / Japan",
    2006: "Germany",
    2010: "South Africa",
    2014: "Brasil",
    2018: "Russia",
    2022: "Qatar",
    2026: "Canada / USA / Mexico",
}

ROOM_LABELS = {
    "autographs": "Autographs and pictures",
    "information-boards": "Information boards",
    "fifa": "FIFA official items",
    "sports-equipment": "Sports equipment",
    "other": "Divers",
}

ROOM_ORDER = [
    "fifa",
    "information-boards",
    "sports-equipment",
    "autographs",
    "other",
]

DOCS = [
    ("English", "EN", "def_verkauf_fussballsammlung_helvetica_englisch.pdf"),
    ("German", "DE", "def_verkauf_fussballsammlung_helvetica_or.pdf"),
    ("French", "FR", "def_verkauf_fussballsammlung_helvetica_franz.pdf"),
    ("Spanish", "ES", "def_verkauf_fussballsammlung_helvetica_spain.pdf"),
]

COPY = {
    "site_title": "Top World - Cup - Collection",
    "span": "1930 – 2022",
    "olympics": "including Olympic Games 1924 / 1928",
    "contact_title": "Collection Football World - Cup 1930 - 2022",
    "sales_note": (
        "Please note, that you can find the information about the items in the "
        "sales documentation (PDF – Sales Document / Verkauf / Sale / Vente / Venta). "
        "If you have any questions, please do not hesitate to contact us."
    ),
    "highlights": "The highlights of the collection",
    "by": "by Thomas Käppeli",
    "intro_1": (
        "Since childhood, I've been collecting sports memorabilia related to football – "
        "over the last 50 years, this collection has grown with a lot of passion, many "
        "wonderful encounters, countless air miles, and, of course, a considerable amount of money."
    ),
    "intro_2": (
        "Always with the intention of opening an exhibition in 2030 for the 100th anniversary "
        "of the World Cup."
    ),
    "intro_3": (
        "Unfortunately, in recent years I've had serious health problems with my heart, so I "
        "lack the strength to set up my planned and much-desired exhibition."
    ),
    "intro_4": (
        "Therefore, it is with a heavy heart that I have now decided to sell my collection."
    ),
    "info_whole": (
        "The collection is only available for purchase as a whole. In total, this collection "
        "consists of approximately 500 exquisite pieces."
    ),
    "info_early": (
        "The collectibles from the period between 1924 and 1950 are almost exclusively "
        "secondhand, acquired from the families of the players of that era."
    ),
    "info_uruguay": (
        "The unique items from Uruguay come from the collection of RONY ALMEIDA and were "
        "personally presented to me by his son, GABRIEL ALMEIDA, in Los Angeles, USA."
    ),
    "info_montevideo": (
        "These collectibles were on loan from the Almeida family to the Football Museum in "
        "Montevideo until 2022."
    ),
    "info_combi": (
        "The collectibles from 1934 and 1938 come from the family estate of GIAMPIERO COMBI "
        "(goalkeeper and captain of the 1934 World Cup champions, Kingdom of Italy)."
    ),
    "info_sources": (
        "Many rarities also originate from auction houses such as AGON Sportsworld Germany, "
        "eBay, Catawiki, etc."
    ),
    "info_auth": "The authenticity of the memorabilia can be verified at any time.",
    "info_view": (
        "Viewing the collection is possible at any time. I stand behind the authenticity and "
        "origin of the collection items to the best of my knowledge and belief."
    ),
    "empty_2026": "No items available for this World Cup.",
    "autograph_note": 'More original autographs in the file "Information Boards"',
}

MOSAIC = [
    ("s6", "1930-uruguay", "img_3106_1536x2048.jpg", "1930"),
    ("s3", "1930-uruguay", "img_3107_1536x2048.jpg", "1930"),
    ("s3", "1954-switzerland", "img_3170_2048x1536.jpg", "1954"),
    ("s4", "1966-england", "img_3248_1371x2048.jpg", "1966"),
    ("s4", "1970-mexico", "img_3278.jpg", "1970"),
    ("s4", "1934-italy", "img_3134_1536x2048.jpg", "1934"),
    ("s8", "1930-uruguay", "img_3119_2048x1536.jpg", "1930"),
    ("s4", "1990-italy", "img_3348_2048x1982.jpg", "1990"),
    ("s3", "1950-brasil", "img_3146_1536x2048.jpg", "1950"),
    ("s3", "fifa", "img_3018_2048x1631.jpg", "FIFA"),
    ("s3", "autographs", "das_wunder_von_bern_2048x803.jpg", "Autographs"),
    ("s3", "2022-qatar", "img_3384_1762x2048.jpg", "2022"),
    ("s4", "1974-germany", "img_3292_1805x2048.jpg", "1974"),
    ("s4", "1986-mexico", "img_3329_2048x1536.jpg", "1986"),
    ("s4", "2014-brasil", "img_3364_1536x2048.jpg", "2014"),
    ("s4", "2002-korea-japan", "img_3357_2048x1322.jpg", "2002"),
    ("s4", "sports-equipment", "img_3396_2048x1536.jpg", "Sports equipment"),
    ("s4", "information-boards", "img_3155_2048x1536.jpg", "Information boards"),
]

HERO = [
    ("p0", "1930-uruguay", "img_3106_1536x2048.jpg"),
    ("p1", "1930-uruguay", "img_3107_1536x2048.jpg"),
    ("p2", "1930-uruguay", "img_3119_2048x1536.jpg"),
    ("p3", "1954-switzerland", "img_3170_2048x1536.jpg"),
]


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


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


def page_assets(page_name: str) -> list[dict]:
    return [
        a
        for a in INV["assets"]
        if a.get("sourcePage") == page_name
        and a.get("localPath")
        and not a.get("navChrome")
        and not a.get("error")
    ]


def media_rel(folder: str, filename: str) -> str:
    return f"media/{folder}/{filename}"


def derived_rel(folder: str, filename: str) -> str:
    path = OUT / "derived" / folder / filename
    if path.exists():
        return f"derived/{folder}/{filename}"
    return media_rel(folder, filename)


def asset_folder(asset: dict) -> str:
    rel = Path(asset["localPath"])
    parts = rel.parts
    if "assets" in parts:
        return parts[parts.index("assets") + 1]
    return asset.get("tournamentFolder") or ""


def src_for(asset: dict, prefix: str = "") -> tuple[str, str]:
    folder = asset_folder(asset)
    name = Path(asset["localPath"]).name
    return prefix + derived_rel(folder, name), prefix + media_rel(folder, name)


def chapter_href(page: dict) -> str:
    if page["kind"] in {"olympic", "world-cup"}:
        return f"world-cups/{page['folder']}.html"
    return f"collections/{page['folder']}.html"


def prefix_for(href: str) -> str:
    return "../" if "/" in href else ""


def heading_for(page: dict) -> str:
    year = page.get("year")
    if year in HOSTS:
        kind = "Olympic Games" if page.get("kind") == "olympic" else "World Cup"
        return f"{kind} {year} {HOSTS[year]}"
    return ROOM_LABELS.get(page["folder"], page.get("title") or page["file"])


def host_for(page: dict) -> str:
    year = page.get("year")
    if year in HOSTS:
        return HOSTS[year]
    return heading_for(page)


def object_link(
    thumb: str,
    full: str,
    meta: str,
    cls: str = "",
    eager: bool = False,
    width: int | None = None,
    height: int | None = None,
) -> str:
    wh = ""
    if width and height:
        wh = f' width="{width}" height="{height}"'
    return (
        f'<a class="{cls}" href="{esc(full)}" data-object data-full="{esc(full)}" '
        f'data-alt="" data-meta="{esc(meta)}">'
        f'<img src="{esc(thumb)}" alt="" loading="{"eager" if eager else "lazy"}"{wh}></a>'
    )


def piece_html(
    asset: dict,
    prefix: str,
    eager: bool = False,
    extra_attrs: str = "",
    meta: str = "",
) -> str:
    thumb, full = src_for(asset, prefix)
    width = asset.get("width") or ""
    height = asset.get("height") or ""
    wh = ""
    if width and height:
        wh = f' width="{esc(width)}" height="{esc(height)}"'
    return (
        f'<figure class="piece"{extra_attrs}>'
        f'<a href="{esc(full)}" data-object data-full="{esc(full)}" '
        f'data-alt="" data-meta="{esc(meta)}">'
        f'<img src="{esc(thumb)}" alt="" loading="{"eager" if eager else "lazy"}" '
        f'decoding="async"{wh}></a></figure>'
    )


def piece_grid(
    assets: list[dict],
    prefix: str,
    eager_n: int = 2,
    extra_class: str = "",
    heading: str = "",
) -> str:
    if not assets:
        return ""
    cls = "piece-grid"
    if extra_class:
        cls += f" {extra_class}"
    cells = [
        piece_html(asset, prefix, eager=i < eager_n, meta=heading)
        for i, asset in enumerate(assets)
    ]
    return f'<div class="{cls}">{"".join(cells)}</div>'


def all_collection_assets() -> list[dict]:
    items: list[dict] = []
    for page in tournament_pages() + collection_pages():
        items.extend(page_assets(page["file"]))
    return items


def document(title: str, body: str, prefix: str, extra_body: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(COPY['site_title'])} · {esc(COPY['span'])} · {esc(COPY['olympics'])}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/exhibition.css?v=type19">
  <script src="{prefix}js/exhibition.js?v=type19" defer></script>
</head>
<body>
{body}
{viewer()}
{extra_body}
</body>
</html>
"""


def mast(prefix: str, current: str = "") -> str:
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if current == href else ""
        links.append(f'<a href="{prefix}{href}"{cur}>{esc(label)}</a>')
    return f"""<a class="skip" href="#main">Skip to collection</a>
<header class="mast">
  <a class="brand" href="{prefix}index.html">
    <span class="brand-mark" aria-hidden="true">TW</span>
    <span class="brand-copy">
      <b>Top World - Cup - Collection</b>
      <small>1930 — 2022</small>
    </span>
  </a>
  <nav class="nav" aria-label="Primary">{''.join(links)}</nav>
  <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
</header>"""


def timeline(prefix: str, current_year: int | None = None) -> str:
    items = []
    for page in tournament_pages():
        year = page.get("year")
        href = prefix + chapter_href(page)
        cur = ' aria-current="page"' if year == current_year else ""
        items.append(
            f'<a class="t-{year}" href="{href}"{cur}><span class="y">{esc(year)}</span>'
            f'<span class="h">{esc(host_for(page))}</span></a>'
        )
    return f"""<div class="chrono" id="timeline">
  <div class="chrono-intro"><span>Collection</span><b>1930 — 2022</b></div>
  <nav class="timeline" aria-label="World Cup chronology">{''.join(items)}</nav>
</div>"""


def foot(prefix: str) -> str:
    links = "".join(
        f'<a href="{prefix}{href}">{esc(label)}</a>' for label, href in NAV
    )
    return f"""<footer class="site-foot">
  <a class="brand" href="{prefix}index.html">
    <span class="brand-mark" aria-hidden="true">TW</span>
    <span class="brand-copy"><b>Top World - Cup - Collection</b><small>1930 — 2022</small></span>
  </a>
  <nav>{links}</nav>
</footer>"""


def viewer() -> str:
    return """<div class="viewer" id="viewer" hidden role="dialog" aria-modal="true" aria-label="Photograph">
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


def feature_stage(assets: list[dict], heading: str, prefix: str) -> str:
    n = len(assets)
    if n == 0:
        return ""
    if n == 1:
        stage = "stage-1"
        take = 1
    elif n == 2:
        stage = "stage-2"
        take = 2
    elif n <= 4:
        stage = "stage-3"
        take = min(3, n)
    else:
        stage = "stage-many"
        take = min(5, n)
    cells = []
    for i, asset in enumerate(assets[:take]):
        thumb, full = src_for(asset, prefix)
        cells.append(object_link(thumb, full, heading, f"obj o{i}", eager=i < 2))
    return f'<div class="feature-stage {stage}">{"".join(cells)}</div>'


def write_home() -> None:
    uruguay = next(p for p in tournament_pages() if p.get("year") == 1930)
    u_assets = page_assets(uruguay["file"])
    rooms = []
    for folder in ROOM_ORDER:
        page = next((p for p in collection_pages() if p["folder"] == folder), None)
        if not page:
            continue
        count = len(page_assets(page["file"]))
        label = ROOM_LABELS[folder]
        if folder == "autographs":
            name_html = (
                '<span class="n" data-rooms="v17">'
                "<span>Autographs</span>"
                '<span class="n-rest">and pictures</span>'
                "</span>"
            )
        else:
            name_html = f'<span class="n">{esc(label)}</span>'
        rooms.append(
            f'<a href="{esc(chapter_href(page))}">'
            f'<span class="k">Collection</span>'
            f"{name_html}"
            f'<span class="c">{count} photographs</span></a>'
        )
    hero_assets = []
    for _cls, folder, name in HERO:
        match = next(
            (
                a
                for a in all_collection_assets()
                if asset_folder(a) == folder and Path(a["localPath"]).name == name
            ),
            None,
        )
        if match:
            hero_assets.append(match)
    wall_assets = all_collection_assets()
    body = f"""{mast("", "index.html")}
<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy">
      <p class="eyebrow">{esc(COPY["site_title"])}</p>
      <h1 id="hero-title">World - Cup<br><em>Collection</em><span>1930 — 2022</span></h1>
      <p class="lede">{esc(COPY["olympics"])}</p>
      <div class="actions">
        <a class="btn" href="world-cups/1930-uruguay.html">1930 Uruguay</a>
        <a class="btn-ghost" href="archive.html">The collection</a>
      </div>
    </div>
    <div class="hero-stage" aria-label="Photographs from the collection">
      {piece_grid(hero_assets, "", eager_n=4, extra_class="piece-grid--hero", heading=COPY["site_title"])}
      <div class="hero-year" aria-hidden="true">1930</div>
    </div>
    <a class="scroll-cue" href="#timeline"><span>1930</span><i></i><span>2022</span></a>
  </section>
  {timeline("")}
  <section class="feature t-1930" aria-labelledby="feature-1930">
    <div class="feature-copy">
      <p class="chapter-kicker">World Cup 1930 Uruguay</p>
      <p class="chapter-year" id="feature-1930">1930</p>
      <p class="chapter-host">Uruguay</p>
      <p class="feature-note">{esc(COPY["info_uruguay"])} {esc(COPY["info_montevideo"])}</p>
      <a class="btn-ghost" href="world-cups/1930-uruguay.html">1930 Uruguay</a>
    </div>
    {piece_grid(u_assets, "", eager_n=len(u_assets), heading="World Cup 1930 Uruguay")}
  </section>
  <nav class="rooms" aria-label="Collection groupings">{''.join(rooms)}</nav>
  <section class="story" id="story">
    <div class="story-head">
      <p class="eyebrow">{esc(COPY["by"])}</p>
      <h2>{esc(COPY["highlights"])}</h2>
      <p>{esc(COPY["intro_2"])}</p>
    </div>
    <div class="milestones">
      <article>
        <h3>Since childhood</h3>
        <p>{esc(COPY["intro_1"])}</p>
      </article>
      <article>
        <h3>2030</h3>
        <p>{esc(COPY["intro_2"])}</p>
      </article>
      <article>
        <h3>Montevideo until 2022</h3>
        <p>{esc(COPY["info_montevideo"])}</p>
      </article>
      <article>
        <h3>Sale</h3>
        <p>{esc(COPY["intro_3"])} {esc(COPY["intro_4"])}</p>
      </article>
    </div>
  </section>
  <section class="wall" id="collection">
    <div class="wall-head">
      <div>
        <p class="eyebrow">{esc(COPY["site_title"])}</p>
        <h2>World - Cup<br><em>Collection</em></h2>
      </div>
      <div>
        <p>{esc(COPY["info_whole"])}</p>
        <a class="btn-ghost" href="archive.html">The collection</a>
      </div>
    </div>
    {piece_grid(wall_assets, "", eager_n=8, extra_class="piece-grid--wall", heading=COPY["site_title"])}
  </section>
  <section class="sale">
    <div class="sale-count"><b>~500</b><span>pieces · only as a whole</span></div>
    <div class="sale-panel">
      <p class="eyebrow">Sale</p>
      <h2>{esc(COPY["intro_4"])}</h2>
      <p>{esc(COPY["info_whole"])}</p>
      <p>{esc(COPY["info_view"])}</p>
      <p>{esc(COPY["sales_note"])}</p>
      <div class="actions" style="margin-top:1.6rem">
        <a class="btn" href="sale.html">Sale</a>
        <a class="btn-ghost" href="contact.html" style="color:inherit;border-color:rgba(18,17,14,.28)">Contact</a>
      </div>
    </div>
  </section>
</main>
{foot("")}"""
    (OUT / "index.html").write_text(
        document(COPY["site_title"], body, ""),
        encoding="utf-8",
    )


def neighbours(page: dict) -> tuple[dict | None, dict | None]:
    pages = tournament_pages() + collection_pages()
    idx = next((i for i, p in enumerate(pages) if p["file"] == page["file"]), None)
    if idx is None:
        return None, None
    prev = pages[idx - 1] if idx > 0 else None
    nxt = pages[idx + 1] if idx < len(pages) - 1 else None
    return prev, nxt


def sequence_html(assets: list[dict], heading: str, prefix: str) -> str:
    if not assets:
        return ""
    chunks = []
    i = 0
    n = len(assets)
    mode = 0
    while i < n:
        if mode % 3 == 2 and i + 3 <= n:
            group = assets[i : i + 3]
            cells = []
            for asset in group:
                thumb, full = src_for(asset, prefix)
                cells.append(object_link(thumb, full, heading))
            chunks.append(f'<div class="cluster">{"".join(cells)}</div>')
            i += 3
        elif mode % 4 == 3:
            asset = assets[i]
            thumb, full = src_for(asset, prefix)
            chunks.append(
                f'<div class="sequence-full">{object_link(thumb, full, heading)}</div>'
            )
            i += 1
        else:
            asset = assets[i]
            thumb, full = src_for(asset, prefix)
            chunks.append(
                f'<div class="sequence-row"><figure>{object_link(thumb, full, heading)}</figure></div>'
            )
            i += 1
        mode += 1
    return f'<section class="sequence">{"".join(chunks)}</section>'


def write_chapter(page: dict) -> None:
    heading = heading_for(page)
    assets = page_assets(page["file"])
    year = page.get("year")
    href = chapter_href(page)
    dest = OUT / href
    dest.parent.mkdir(parents=True, exist_ok=True)
    rel = prefix_for(href)
    if year:
        year_label = str(year)
        host = HOSTS[year]
    else:
        year_label = ROOM_LABELS.get(page["folder"], heading)
        host = ""
    note = ""
    if year == 1930:
        note = f'<p class="feature-note">{esc(COPY["info_uruguay"])} {esc(COPY["info_montevideo"])}</p>'
    elif year in {1934, 1938}:
        note = f'<p class="feature-note">{esc(COPY["info_combi"])}</p>'
    elif page["folder"] == "autographs":
        note = f'<p class="feature-note">{esc(COPY["autograph_note"])}</p>'
    if year == 2026 and not assets:
        note = f'<p class="feature-note">{esc(COPY["empty_2026"])}</p>'
    feature_cls = "feature"
    if year:
        feature_cls = f"feature t-{year}"
    if page["folder"] == "autographs":
        chapter_year_html = (
            '<span class="n-line">Autographs</span>'
            '<span class="n-line">and pictures</span>'
        )
        chapter_year_class = "chapter-year has-lines"
    else:
        chapter_year_html = esc(year_label or heading)
        chapter_year_class = "chapter-year"
    prev, nxt = neighbours(page)
    prev_html = (
        f'<a href="{rel}{chapter_href(prev)}">{esc(heading_for(prev))}</a>'
        if prev
        else "<span></span>"
    )
    next_html = (
        f'<a href="{rel}{chapter_href(nxt)}">{esc(heading_for(nxt))}</a>'
        if nxt
        else "<span></span>"
    )
    body = f"""<div class="interior chapter-page">
{mast(rel, href)}
<main id="main">
  {timeline(rel, year)}
  <section class="{feature_cls}">
    <div class="feature-copy">
      <p class="chapter-kicker">{esc(heading)}</p>
      <p class="{chapter_year_class}">{chapter_year_html}</p>
      {f'<p class="chapter-host">{esc(host)}</p>' if host else ""}
      {note}
    </div>
    {piece_grid(assets, rel, eager_n=len(assets) if len(assets) <= 40 else 12, heading=heading)}
  </section>
  <nav class="chapter-nav{f' t-{year}' if year else ''}">{prev_html}{next_html}</nav>
</main>
{foot(rel)}
</div>"""
    dest.write_text(
        document(f"{heading} · {COPY['site_title']}", body, rel),
        encoding="utf-8",
    )


def write_archive() -> None:
    folders = []
    cards = []
    seen = set()
    for page in tournament_pages() + collection_pages():
        folder = page["folder"]
        if folder not in seen:
            folders.append((folder, heading_for(page)))
            seen.add(folder)
        for asset in page_assets(page["file"]):
            cards.append(
                piece_html(
                    asset,
                    "",
                    extra_attrs=(
                        f' data-archive-item data-folder="{esc(folder)}"'
                    ),
                    meta=heading_for(page),
                )
            )
    buttons = ['<button type="button" data-folder="all" aria-pressed="true">All</button>']
    for folder, label in folders:
        buttons.append(
            f'<button type="button" data-folder="{esc(folder)}">{esc(label)}</button>'
        )
    body = f"""<div class="interior">
{mast("", "archive.html")}
<main id="main">
  <div class="page-hero">
    <p class="eyebrow">{esc(COPY["site_title"])}</p>
    <h1>The collection</h1>
  </div>
  {timeline("")}
  <div class="archive-tools" id="archive-filter">{''.join(buttons)}</div>
  <div class="piece-grid piece-grid--many piece-grid--wall piece-grid--archive">{''.join(cards)}</div>
</main>
{foot("")}
</div>"""
    (OUT / "archive.html").write_text(
        document(f"The collection · {COPY['site_title']}", body, ""),
        encoding="utf-8",
    )


def write_sale() -> None:
    docs = "".join(
        f'<a href="documents/{esc(name)}"><b>{esc(label)}</b><span>{esc(code)} · PDF</span></a>'
        for label, code, name in DOCS
    )
    body = f"""<div class="interior">
{mast("", "sale.html")}
<main id="main">
  <div class="page-hero">
    <p class="eyebrow">{esc(COPY["by"])}</p>
    <h1>Sale</h1>
  </div>
  <article class="prose light">
    <h2>{esc(COPY["highlights"])}</h2>
    <p>{esc(COPY["intro_1"])}</p>
    <p>{esc(COPY["intro_2"])}</p>
    <p>{esc(COPY["intro_3"])}</p>
    <p>{esc(COPY["intro_4"])}</p>
    <h2>Information about the collection</h2>
    <p>{esc(COPY["info_whole"])}</p>
    <p>{esc(COPY["info_early"])}</p>
    <p>{esc(COPY["info_uruguay"])}</p>
    <p>{esc(COPY["info_montevideo"])}</p>
    <p>{esc(COPY["info_combi"])}</p>
    <p>{esc(COPY["info_sources"])}</p>
    <p>{esc(COPY["info_auth"])}</p>
    <p>{esc(COPY["info_view"])}</p>
    <p>{esc(COPY["sales_note"])}</p>
    <div class="docs">{docs}</div>
    <p style="margin-top:2rem"><a class="btn" href="contact.html">Contact</a></p>
  </article>
</main>
{foot("")}
</div>"""
    (OUT / "sale.html").write_text(
        document(f"Sale · {COPY['site_title']}", body, ""),
        encoding="utf-8",
    )


def write_contact() -> None:
    body = f"""<div class="interior">
{mast("", "contact.html")}
<main id="main">
  <div class="page-hero">
    <p class="eyebrow">{esc(COPY["site_title"])}</p>
    <h1>Contact</h1>
  </div>
  <section class="prose">
    <p>{esc(COPY["contact_title"])}</p>
    <div class="contacts">
      <article>
        <h3>Bernhard Spahni</h3>
        <a href="mailto:bspahni@me.com">bspahni@me.com</a>
        <a href="tel:+41798458592">+41 79 8458592</a>
      </article>
      <article>
        <h3>Jason Knight</h3>
        <a href="mailto:Jason@cultureandcommerce.co.uk">Jason@cultureandcommerce.co.uk</a>
        <a href="tel:+447940730856">+44 (0)7940 730 856</a>
      </article>
    </div>
  </section>
</main>
{foot("")}
</div>"""
    (OUT / "contact.html").write_text(
        document(f"Contact · {COPY['site_title']}", body, ""),
        encoding="utf-8",
    )


def write_sitemap() -> None:
    urls = ["index.html", "archive.html", "sale.html", "contact.html"]
    for page in tournament_pages() + collection_pages():
        urls.append(chapter_href(page))
    (OUT / "sitemap.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")


def ensure_links() -> None:
    media = OUT / "media"
    docs = OUT / "documents"
    if not media.exists():
        media.symlink_to((ROOT / "source" / "assets").resolve())
    if not docs.exists() and (ROOT / "source" / "documents").exists():
        docs.symlink_to((ROOT / "source" / "documents").resolve())


def main() -> None:
    (OUT / "world-cups").mkdir(parents=True, exist_ok=True)
    (OUT / "collections").mkdir(parents=True, exist_ok=True)
    ensure_links()
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
