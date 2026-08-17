#!/usr/bin/env python3
"""Download selected documentary photos from the live collection site."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

BASE = "https://www.top-world-cup-collection.ch/rc_images/"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "images"

# slug -> list of (remote filename, local filename)
FETCH: list[tuple[str, str]] = [
    # Named pieces
    ("img_3106_1536x2048.jpg", "petrone.jpg"),
    ("img_3425_1560x2048.jpg", "fifa-1904.jpg"),
    ("img_3200_1536x2048.jpg", "kocsis.jpg"),
    ("img_3199_1536x2048.jpeg", "1954-medal-obverse.jpg"),
    ("img_3170_2048x1536.jpg", "1954-ticket.jpg"),
    # 1930 sequence (skip lead, already petrone)
    ("img_3107_1536x2048.jpg", "1930-02.jpg"),
    ("img_3109_1536x2048.jpg", "1930-03.jpg"),
    ("img_3108_1536x2048.jpg", "1930-04.jpg"),
    ("img_3111_1536x2048.jpg", "1930-05.jpg"),
    ("img_3119_2048x1536.jpg", "1930-06.jpg"),
    ("img_3112_1536x2048.jpg", "1930-07.jpg"),
    ("img_3113_1536x2048.jpg", "1930-08.jpg"),
    # 1954 sequence extras
    ("img_3201_1536x2048.jpg", "1954-04.jpg"),
    ("img_3202_1536x2048.jpeg", "1954-05.jpg"),
    ("img_3204_1536x2048.jpg", "1954-06.jpg"),
    ("img_3208_2048x1536.jpg", "1954-07.jpg"),
    ("img_3205_1536x2048.jpg", "1954-08.jpg"),
    # FIFA extras
    ("img_3045_1536x2048.jpg", "fifa-02.jpg"),
    ("img_3032_2048x1505.jpg", "fifa-03.jpg"),
    ("img_3027_2048x1863.jpg", "fifa-04.jpg"),
    ("img_3048_1536x2048.jpg", "fifa-05.jpg"),
    ("img_3058_1536x2048.jpg", "fifa-06.jpg"),
    ("img_3018_2048x1631.jpg", "fifa-07.jpg"),
    ("img_3019_2048x1880.jpg", "fifa-08.jpg"),
    # Index thumbs (first image per remaining issue)
    ("img_3096_1536x2048.jpg", "thumb-1924.jpg"),
    ("img_3102_1536x2048.jpg", "thumb-1928.jpg"),
    ("img_3115a.jpg", "thumb-1934.jpg"),
    ("img_3999.jpg", "thumb-1938.jpg"),
    ("img_3114a1.jpg", "thumb-1950.jpg"),
    ("img_3213_2048x1536.jpg", "thumb-1958.jpg"),
    ("img_3230_1765x2048.jpeg", "thumb-1962.jpg"),
    ("img_3248_1371x2048.jpg", "thumb-1966.jpg"),
    ("img_3278.jpg", "thumb-1970.jpg"),
    ("img_3299.jpg", "thumb-1974.jpg"),
    ("img_3311_1309x2048.jpg", "thumb-1978.jpg"),
    ("img_3321_2048x1124.jpg", "thumb-1982.jpg"),
    ("img_3328_1775x2048.jpg", "thumb-1986.jpg"),
    ("img_3348_2048x1982.jpg", "thumb-1990.jpg"),
    ("img_3354_2048x1344.jpg", "thumb-1994.jpg"),
    ("ticket_1.jpg", "thumb-1998.jpg"),
    ("img_3361_2048x1536.jpg", "thumb-2002.jpg"),
    ("img_3334_1536x2048.jpg", "thumb-2006.jpg"),
    ("img_3335_1536x2048.jpg", "thumb-2010.jpg"),
    ("img_3364_1536x2048.jpg", "thumb-2014.jpg"),
    ("img_3373_1536x2048.jpg", "thumb-2018.jpg"),
    ("img_3384_1762x2048.jpg", "thumb-2022.jpg"),
    ("das_wunder_von_bern_2048x803.jpg", "thumb-autographs.jpg"),
    ("img_3176_1536x2048.jpg", "thumb-information-boards.jpg"),
    ("img_3151_2048x1981.jpeg", "thumb-sports-equipment.jpg"),
    ("img_3046_2048x1536.jpg", "thumb-divers.jpg"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for remote, local in FETCH:
        dest = OUT / local
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"skip {local}")
            continue
        url = BASE + remote
        print(f"get {local}")
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                dest.write_bytes(r.read())
        except Exception as exc:
            print(f"FAIL {local}: {exc}")
    # Convenience aliases for dressed-room thumbs
    aliases = {
        "thumb-1930.jpg": "petrone.jpg",
        "thumb-1954.jpg": "1954-ticket.jpg",
        "thumb-fifa.jpg": "fifa-1904.jpg",
    }
    for dest_name, src_name in aliases.items():
        src = OUT / src_name
        dest = OUT / dest_name
        if src.exists() and not dest.exists():
            shutil.copyfile(src, dest)
    print(f"done → {OUT}")


if __name__ == "__main__":
    main()
