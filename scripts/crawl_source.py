#!/usr/bin/env python3
"""Crawl the live collection site into a source-of-truth inventory.

Does not invent captions, titles, or object identities.
Preserves original filenames and maps them to source URLs.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ORIGIN = "https://www.top-world-cup-collection.ch/"
OUT_ASSETS = ROOT / "source" / "assets"
OUT_DOCS = ROOT / "source" / "documents"
OUT_PAGES = ROOT / "source" / "pages"
OUT_DATA = ROOT / "source" / "data"
UA = "TopWorldCupCollectionCrawler/1.0 (source preservation)"

PAGE_SLUGS = {
    "index.html": {"kind": "home", "year": None, "folder": "home"},
    "1924.html": {"kind": "olympic", "year": 1924, "folder": "1924-paris"},
    "1928.html": {"kind": "olympic", "year": 1928, "folder": "1928-amsterdam"},
    "1930.html": {"kind": "world-cup", "year": 1930, "folder": "1930-uruguay"},
    "1934.html": {"kind": "world-cup", "year": 1934, "folder": "1934-italy"},
    "1938.html": {"kind": "world-cup", "year": 1938, "folder": "1938-france"},
    "1950.html": {"kind": "world-cup", "year": 1950, "folder": "1950-brasil"},
    "1954.html": {"kind": "world-cup", "year": 1954, "folder": "1954-switzerland"},
    "1958.html": {"kind": "world-cup", "year": 1958, "folder": "1958-sweden"},
    "1962.html": {"kind": "world-cup", "year": 1962, "folder": "1962-chile"},
    "1966.html": {"kind": "world-cup", "year": 1966, "folder": "1966-england"},
    "1970.html": {"kind": "world-cup", "year": 1970, "folder": "1970-mexico"},
    "1974.html": {"kind": "world-cup", "year": 1974, "folder": "1974-germany"},
    "1978.html": {"kind": "world-cup", "year": 1978, "folder": "1978-argentina"},
    "1982.html": {"kind": "world-cup", "year": 1982, "folder": "1982-spain"},
    "1986.html": {"kind": "world-cup", "year": 1986, "folder": "1986-mexico"},
    "1990.html": {"kind": "world-cup", "year": 1990, "folder": "1990-italy"},
    "1994.html": {"kind": "world-cup", "year": 1994, "folder": "1994-usa"},
    "1998.html": {"kind": "world-cup", "year": 1998, "folder": "1998-france"},
    "2002.html": {"kind": "world-cup", "year": 2002, "folder": "2002-korea-japan"},
    "2006.html": {"kind": "world-cup", "year": 2006, "folder": "2006-germany"},
    "2010.html": {"kind": "world-cup", "year": 2010, "folder": "2010-south-africa"},
    "2014.html": {"kind": "world-cup", "year": 2014, "folder": "2014-brasil"},
    "2018.html": {"kind": "world-cup", "year": 2018, "folder": "2018-russia"},
    "2022.html": {"kind": "world-cup", "year": 2022, "folder": "2022-qatar"},
    "2026.html": {"kind": "world-cup", "year": 2026, "folder": "2026-canada-usa-mexico"},
    "autographs.html": {"kind": "collection", "year": None, "folder": "autographs"},
    "information_boards.html": {
        "kind": "collection",
        "year": None,
        "folder": "information-boards",
    },
    "fifa_items.html": {"kind": "collection", "year": None, "folder": "fifa"},
    "sports_equipment.html": {
        "kind": "collection",
        "year": None,
        "folder": "sports-equipment",
    },
    "divers.html": {"kind": "collection", "year": None, "folder": "other"},
    "contact.html": {"kind": "contact", "year": None, "folder": "contact"},
}

NAV_IMAGE_HINTS = (
    "preview",
    "return",
    "next",
    "back",
    "home",
    "button",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self._in_title = False
        self.headings: list[dict] = []
        self._heading: str | None = None
        self._heading_parts: list[str] = []
        self.texts: list[str] = []
        self.links: list[dict] = []
        self.images: list[dict] = []
        self.iframes: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: v or "" for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag in {"h1", "h2", "h3", "h4"}:
            self._heading = tag
            self._heading_parts = []
        elif tag == "script" or tag == "style":
            self._skip = True
        elif tag == "a":
            href = ad.get("href", "")
            if href:
                self.links.append({"href": href, "title": ad.get("title", "")})
        elif tag == "img":
            self.images.append(
                {
                    "src": ad.get("src", ""),
                    "alt": ad.get("alt", ""),
                    "title": ad.get("title", ""),
                    "width": ad.get("width", ""),
                    "height": ad.get("height", ""),
                }
            )
        elif tag == "iframe":
            src = ad.get("src", "")
            if src:
                self.iframes.append(src)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag in {"h1", "h2", "h3", "h4"} and self._heading:
            text = " ".join("".join(self._heading_parts).split())
            if text:
                self.headings.append({"tag": self._heading, "text": text})
            self._heading = None
        elif tag in {"script", "style"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        if self._in_title:
            self.title_parts.append(data)
        if self._heading:
            self._heading_parts.append(data)
        cleaned = " ".join(data.split())
        if cleaned:
            self.texts.append(cleaned)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def jpeg_size(data: bytes) -> tuple[int | None, int | None]:
    if data[:2] != b"\xff\xd8":
        return None, None
    i = 2
    while i < len(data) - 8:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in {0xC0, 0xC1, 0xC2}:
            h = int.from_bytes(data[i + 5 : i + 7], "big")
            w = int.from_bytes(data[i + 7 : i + 9], "big")
            return w, h
        if marker == 0xD8 or marker == 0xD9:
            i += 2
            continue
        length = int.from_bytes(data[i + 2 : i + 4], "big")
        i += 2 + length
    return None, None


def png_size(data: bytes) -> tuple[int | None, int | None]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def image_size(path: Path, data: bytes) -> tuple[int | None, int | None]:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_size(data)
    if suffix == ".png":
        return png_size(data)
    return None, None


def absolute(href: str, base: str = SOURCE_ORIGIN) -> str:
    return urllib.parse.urljoin(base, href)


def is_nav_image(src: str) -> bool:
    name = Path(urllib.parse.urlparse(src).path).name.lower()
    return any(hint in name for hint in NAV_IMAGE_HINTS)


def main() -> None:
    for path in (OUT_ASSETS, OUT_DOCS, OUT_PAGES, OUT_DATA):
        path.mkdir(parents=True, exist_ok=True)

    pages = []
    assets = []
    documents = []
    seen_checksums: dict[str, str] = {}
    all_copy: list[dict] = []

    for page_name, meta in PAGE_SLUGS.items():
        url = absolute(page_name)
        print(f"page {page_name}")
        try:
            raw = fetch(url)
        except urllib.error.URLError as exc:
            pages.append(
                {
                    "url": url,
                    "file": page_name,
                    "error": str(exc),
                    **meta,
                }
            )
            continue
        (OUT_PAGES / page_name).write_bytes(raw)
        html = raw.decode("utf-8", "replace")
        parser = PageParser()
        parser.feed(html)
        title = " ".join("".join(parser.title_parts).split())
        body_copy = []
        for text in parser.texts:
            if text == title:
                continue
            if text not in body_copy:
                body_copy.append(text)
        page_record = {
            "url": url,
            "file": page_name,
            "title": title,
            "headings": parser.headings,
            "bodyCopy": body_copy,
            "links": [
                {
                    "href": link["href"],
                    "absolute": absolute(link["href"], url),
                    "title": link["title"],
                }
                for link in parser.links
            ],
            "iframes": [absolute(src, url) for src in parser.iframes],
            **meta,
        }
        pages.append(page_record)
        for text in body_copy:
            all_copy.append(
                {
                    "text": text,
                    "sourceUrl": url,
                    "sourcePage": page_name,
                    "kind": meta["kind"],
                    "year": meta["year"],
                }
            )

        folder = OUT_ASSETS / meta["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        for image in parser.images:
            src = image["src"]
            if not src:
                continue
            abs_url = absolute(src, url)
            original_name = Path(urllib.parse.urlparse(abs_url).path).name
            if not original_name:
                continue
            dest = folder / original_name
            nav = is_nav_image(src)
            try:
                data = fetch(abs_url)
            except urllib.error.URLError as exc:
                assets.append(
                    {
                        "sourceUrl": abs_url,
                        "sourcePage": page_name,
                        "error": str(exc),
                        "originalFilename": original_name,
                        "navChrome": nav,
                    }
                )
                continue
            dest.write_bytes(data)
            checksum = hashlib.sha256(data).hexdigest()
            width, height = image_size(dest, data)
            duplicate_of = seen_checksums.get(checksum)
            if not duplicate_of:
                seen_checksums[checksum] = str(dest.relative_to(ROOT))
            assets.append(
                {
                    "id": checksum[:12],
                    "sourceUrl": abs_url,
                    "localPath": str(dest.relative_to(ROOT)),
                    "filename": original_name,
                    "type": dest.suffix.lower().lstrip(".") or "unknown",
                    "bytes": len(data),
                    "width": width,
                    "height": height,
                    "tournamentFolder": meta["folder"],
                    "year": meta["year"],
                    "kind": meta["kind"],
                    "caption": None,
                    "alt": image["alt"] or None,
                    "titleAttr": image["title"] or None,
                    "sourcePage": page_name,
                    "checksum": checksum,
                    "duplicateOf": duplicate_of,
                    "navChrome": nav,
                    "confidence": "page-association-only",
                    "note": (
                        "Assigned to this tournament/page because that is the "
                        "source page on the live site. No item identity is inferred."
                    ),
                }
            )
            time.sleep(0.05)

        for iframe in page_record["iframes"]:
            if not iframe.lower().endswith(".pdf"):
                continue
            name = Path(urllib.parse.urlparse(iframe).path).name
            dest = OUT_DOCS / name
            print(f"  pdf {name}")
            if not dest.exists():
                try:
                    dest.write_bytes(fetch(iframe))
                except urllib.error.URLError as exc:
                    documents.append(
                        {"sourceUrl": iframe, "error": str(exc), "sourcePage": page_name}
                    )
                    continue
            documents.append(
                {
                    "title": name,
                    "sourceUrl": iframe,
                    "localPath": str(dest.relative_to(ROOT)),
                    "type": "pdf",
                    "bytes": dest.stat().st_size,
                    "sourcePage": page_name,
                    "associatedTournament": None,
                }
            )

    # Homepage sales-doc note and F1 sibling
    home_html = (OUT_PAGES / "index.html").read_text(encoding="utf-8", errors="replace")
    f1 = "https://www.top-world-cup-collection.ch/f1/"
    extra = {
        "formula1CollectionUrl": f1 if "f1" in home_html.lower() else None,
        "homepageSalesNote": None,
    }

    inventory = {
        "sourceOrigin": SOURCE_ORIGIN,
        "crawledAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pages": pages,
        "assets": assets,
        "documents": documents,
        "copy": all_copy,
        "extra": extra,
        "gaps": [
            {
                "id": "no-item-captions-on-html-pages",
                "detail": (
                    "HTML year pages contain images without per-object captions. "
                    "Item names live only in the sales PDFs, not bound to image files."
                ),
            },
            {
                "id": "pdf-item-to-image-unmapped",
                "detail": (
                    "Sales PDF lists item titles. Images are not labelled on the site. "
                    "Do not pair a PDF title to a photograph unless later verified."
                ),
            },
            {
                "id": "2026-empty",
                "detail": "2026.html exists and has no collection photographs.",
            },
            {
                "id": "olympic-years-not-world-cups",
                "detail": "1924 Paris and 1928 Amsterdam are Olympic pages on the source site.",
            },
        ],
    }

    (OUT_DATA / "inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    manifest = [
        {
            "localPath": asset.get("localPath"),
            "sourceUrl": asset.get("sourceUrl"),
            "checksum": asset.get("checksum"),
            "sourcePage": asset.get("sourcePage"),
        }
        for asset in assets
        if asset.get("localPath")
    ]
    (OUT_DATA / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    collection_only = [a for a in assets if a.get("localPath") and not a.get("navChrome")]
    print(
        f"done pages={len(pages)} assets={len(collection_only)} "
        f"docs={len(documents)} → {OUT_DATA}"
    )


if __name__ == "__main__":
    main()
