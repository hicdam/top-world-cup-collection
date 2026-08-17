#!/usr/bin/env python3
"""Copy and structure checks for the design POC."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = SITE / "data" / "collection.json"

FORBIDDEN = (
    "goddess",
    "journey",
    "iconic",
    "stunning",
    "timeless",
    "discover",
    "welcome to",
    "write to the house",
    "the first goddess",
)
EM_DASH = "\u2014"
SALE = "only available for purchase as a whole"


def fail(message: str) -> None:
    print(f"FAIL {message}")
    sys.exit(1)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    required = [
        SITE / "index.html",
        SITE / "collection.html",
        SITE / "contact.html",
        SITE / "404.html",
        SITE / "1930.html",
        SITE / "1954.html",
        SITE / "fifa.html",
        SITE / "piece" / "petrone.html",
        SITE / "piece" / "fifa-1904.html",
        SITE / "piece" / "kocsis.html",
        SITE / "styles.css",
        SITE / "site.js",
        SITE / "images" / "petrone.jpg",
        SITE / "images" / "fifa-1904.jpg",
        SITE / "images" / "kocsis.jpg",
    ]
    for path in required:
        if not path.exists() or path.stat().st_size < 20:
            fail(f"missing {path.relative_to(ROOT)}")

    collection = (SITE / "collection.html").read_text(encoding="utf-8")
    for issue in data["issues"]:
        if f'{issue["slug"]}.html' not in collection:
            fail(f"collection index missing {issue['slug']}")
        page = SITE / f"{issue['slug']}.html"
        if not page.exists():
            fail(f"missing issue page {issue['slug']}.html")

    html_files = list(SITE.rglob("*.html"))
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        if EM_DASH in text:
            fail(f"em dash in {path.relative_to(ROOT)}")
        lower = text.lower()
        for word in FORBIDDEN:
            if word in lower:
                fail(f"forbidden {word!r} in {path.relative_to(ROOT)}")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    contact = (SITE / "contact.html").read_text(encoding="utf-8")
    if SALE not in contact:
        fail("contact missing sale-as-a-whole sentence")
    if SALE in home:
        fail("home must not contain sale-as-a-whole sentence")
    if "Jules Rimet Cup of Pedro Petrone" not in home:
        fail("home missing Petrone title")

    print("ok")


if __name__ == "__main__":
    main()
