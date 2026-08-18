#!/usr/bin/env python3
"""Non-destructive image derivatives for the exhibition.

Source originals in source/assets/ are never modified.

Tiers:
- exhibition/derived/{folder}/{file}   max edge 1100px  (page display)
- exhibition/thumbs/{folder}/{file}    max edge 520px   (archive grid, mosaic)

Original filenames are preserved. Navigation chrome and errored assets are skipped.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INV = json.loads((ROOT / "source" / "data" / "inventory.json").read_text(encoding="utf-8"))

TIERS = {
    "derived": 1100,
    "thumbs": 520,
}


def eligible_assets() -> list[dict]:
    return [
        a
        for a in INV["assets"]
        if a.get("localPath")
        and not a.get("navChrome")
        and not a.get("error")
        and a.get("kind") not in {"home"}
    ]


def derive(asset: dict, tier: str, max_edge: int) -> bool:
    src = ROOT / asset["localPath"]
    if not src.exists():
        return False
    parts = Path(asset["localPath"]).parts
    folder = parts[parts.index("assets") + 1] if "assets" in parts else "misc"
    dest = ROOT / "exhibition" / tier / folder / src.name
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        scale = min(1.0, max_edge / max(w, h))
        if scale < 1.0:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    return True


def main() -> None:
    assets = eligible_assets()
    made = {tier: 0 for tier in TIERS}
    for tier, edge in TIERS.items():
        for asset in assets:
            if derive(asset, tier, edge):
                made[tier] += 1
    for tier, count in made.items():
        print(f"{tier}: {count} images")


if __name__ == "__main__":
    main()
