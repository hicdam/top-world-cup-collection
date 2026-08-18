# Browser QA brief — Top World Cup Collection

**Target:** https://top-world-cup-collection.netlify.app  
**Executor:** Claude with browser tools  
**Viewport:** desktop **1920×1080** first, then **768×1024**, then **390×844**  
**Goal:** Confirm the live exhibition behaves correctly for a real visitor. Report pass / fail with evidence (URL + what you saw). Fix nothing unless asked.

---

## How to work

1. Open the target URL in a real browser session.
2. Execute every check below in order.
3. For each section, record **PASS**, **FAIL**, or **BLOCKED** with a one-line note.
4. Prefer interacting (click, scroll, open lightbox, follow links) over static screenshots alone.
5. Do not invent collection facts, captions, prices, or provenance while testing.
6. At the end, return a short scorecard and a punch list of failures only.

---

## 0. Smoke

| # | Check | Expect |
|---|--------|--------|
| 0.1 | Homepage loads | HTTP 200, title includes `Top World - Cup - Collection` |
| 0.2 | CSS/fonts load | Fraunces + Outfit from Google Fonts; page is not unstyled |
| 0.3 | No console-breaking JS | No repeated errors that break nav, lightbox, or filters |
| 0.4 | Favicon / blank page | Not a blank white/black failure screen |

---

## 1. Homepage — first viewport

| # | Check | Expect |
|---|--------|--------|
| 1.1 | Hero present | Dark cinematic opening with headline **World - Cup / Collection** and span **1930 — 2022** |
| 1.2 | Hero objects | Lifted cream mounts showing full pieces (not heavily cropped product cards) |
| 1.3 | Primary CTAs | **1930 Uruguay** and **The collection** work |
| 1.4 | Nav | Links: The collection, Timeline, Story, Sale, Contact — all reachable |
| 1.5 | Type | Large years use **Fraunces**; body/nav/labels use **Outfit** |

---

## 2. Chronology strip

| # | Check | Expect |
|---|--------|--------|
| 2.1 | Years present | Continuous run **1924 → 2026** including Olympic 1924 / 1928 |
| 2.2 | No gap rule | **No** vertical divider / gap between **1938** and **1950** |
| 2.3 | Host labels | Corrected hosts: **England** (not Emgland), **South Africa** (not Sauth Africa), **Canada / USA / Mexico** for 2026 |
| 2.4 | Colour ages | Each year cell has its own muted background; type/dots stay the same across years |
| 2.5 | Click-through | Click **1954**, **1938**, **1970**, **2022**, **2026** — each opens the matching chapter |
| 2.6 | Sticky | Strip remains usable while scrolling a long chapter |

---

## 3. Tournament chapters

Test at least: **1930** (many), **1938** (few), **1954** (mid), **2010** (single), **2026** (empty), **FIFA** room.

| # | Check | Expect |
|---|--------|--------|
| 3.1 | Year lockup | Giant off-white **year** in Fraunces; host in dark Outfit, overlapping the year |
| 3.2 | Ground colour | Chapter background matches that year’s chronology colour |
| 3.3 | Full set | Every photograph for that grouping appears (no missing tiles vs the inventory counts below) |
| 3.4 | Dense grid | On 1920×1080, tiles are compact (~6 across), not half-screen giants |
| 3.5 | Whole piece visible | Each tile shows the full object (`contain`), not a cropped crop |
| 3.6 | Lightbox | Click a tile → larger image; Esc / Close works; prev/next if multiple |
| 3.7 | Prev/next chapter | Footer chapter links move to neighbouring years/rooms |
| 3.8 | 2026 empty | Shows **No items available for this World Cup.** — no fake 2026 objects |
| 3.9 | Provenance copy | 1930 may show Almeida / Montevideo wording; 1934/1938 may show Combi wording — only as already on the page, not invented |

### Expected photograph counts (fail if clearly short)

| Grouping | Count |
|----------|------:|
| 1924 Paris | 4 |
| 1928 Amsterdam | 3 |
| 1930 Uruguay | 17 |
| 1934 Italy | 16 |
| 1938 France | 2 |
| 1950 Brasil | 28 |
| 1954 Switzerland | 15 |
| 1958 Sweden | 4 |
| 1962 Chile | 5 |
| 1966 England | 26 |
| 1970 Mexico | 23 |
| 1974 Germany | 16 |
| 1978 Argentina | 8 |
| 1982 Spain | 6 |
| 1986 Mexico | 11 |
| 1990 Italy | 12 |
| 1994 USA | 4 |
| 1998 France | 3 |
| 2002 Korea / Japan | 5 |
| 2006 Germany | 3 |
| 2010 South Africa | 1 |
| 2014 Brasil | 6 |
| 2018 Russia | 2 |
| 2022 Qatar | 13 |
| 2026 Canada / USA / Mexico | 0 |
| FIFA official items | 83 |
| Information boards | 34 |
| Sports equipment | 30 |
| Autographs and pictures | 6 |
| Divers | 3 |

Spot-check counts for **1938**, **1954**, **2010**, **FIFA** (FIFA may be sampled if too long: confirm grid is densely populated and scrolls to a large set, not a handful).

---

## 4. Homepage mid / lower sections

| # | Check | Expect |
|---|--------|--------|
| 4.1 | 1930 feature | Year/host lockup + all 17 Uruguay tiles |
| 4.2 | Rooms strip | FIFA, Information boards, Sports equipment, Autographs and pictures, Divers — counts look sane |
| 4.3 | Story | Supported milestones only; no invented biography |
| 4.4 | Collection wall | Large grid of real photographs; tiles clickable |
| 4.5 | Sale band | ~500 / only as a whole; links to Sale and Contact |
| 4.6 | Footer | No Formula 1 / “Visit also” link |

---

## 5. Archive

URL: `/archive.html`

| # | Check | Expect |
|---|--------|--------|
| 5.1 | Loads | Full archive grid of lifted tiles |
| 5.2 | Filters | Year/room filter buttons show/hide sets without breaking layout |
| 5.3 | Lightbox | Click opens larger view |
| 5.4 | All filter | Resetting to All restores the full set |

---

## 6. Sale

URL: `/sale.html`

| # | Check | Expect |
|---|--------|--------|
| 6.1 | Sale language | **Sale**, not Auction |
| 6.2 | Whole only | States collection sold **only as a whole**; ~500 pieces |
| 6.3 | No ecommerce | No prices, carts, Buy buttons, or individual lots |
| 6.4 | Documents | EN / DE / FR / ES PDFs open (200) |
| 6.5 | Copy source | Text remains Thomas Käppeli sale-statement wording (byline may still say by Thomas Käppeli) |
| 6.6 | Type | Long prose in Outfit; elegant, readable, not condensed label type |

---

## 7. Contact — critical

URL: `/contact.html`

| # | Check | Expect |
|---|--------|--------|
| 7.1 | Contacts are | **Bernhard Spahni** — `bspahni@me.com` — `+41 79 8458592` |
| 7.2 | And | **Jason Knight** — `Jason@cultureandcommerce.co.uk` — `+44 (0)7940 730 856` |
| 7.3 | Not present | No Thomas Paul Käppeli, Norbert Kaeser/Käser, Wattenwil, Schmitten, tk@ or nk@ addresses |
| 7.4 | Links | `mailto:` and `tel:` hrefs match the visible text |
| 7.5 | Layout | Do not fail for layout taste; only fail if content is wrong or unreadable |

---

## 8. Content / legal constraints (spot checks)

| # | Check | Expect |
|---|--------|--------|
| 8.1 | No auction framing | Search visible UI for “Auction” — should not appear as the sale model |
| 8.2 | No prices | No CHF/EUR/USD sale prices on objects |
| 8.3 | No fake captions | Photographs are not labelled with invented player/object titles from the PDF |
| 8.4 | No collector portrait claim | No implied verified portrait of Thomas as a real photo identity |

---

## 9. Responsive

Repeat a short path on **768×1024** and **390×844**: Homepage → timeline scroll → 1938 → lightbox → Contact.

| # | Check | Expect |
|---|--------|--------|
| 9.1 | Mobile nav | Menu opens/closes; destinations work |
| 9.2 | Timeline | Horizontally scrollable; years tappable |
| 9.3 | Grids | 2-column (or similar) tiles; still full-object; not overflowing viewport |
| 9.4 | Lightbox | Usable on small screens |
| 9.5 | Contact | Both contacts readable without horizontal page scroll |

---

## 10. Performance / polish (light)

| # | Check | Expect |
|---|--------|--------|
| 10.1 | Broken images | No obvious empty mounts or 404 images on homepage, 1938, 1954 |
| 10.2 | PDF weight | Opening one sales PDF succeeds; note if extremely slow |
| 10.3 | Deep links | Direct load of `/world-cups/1930-uruguay.html` and `/contact.html` works |

---

## Report format

Return exactly this structure:

```text
QA SCORECARD — top-world-cup-collection.netlify.app
Date / viewport: …

0 Smoke: …
1 Homepage: …
2 Chronology: …
3 Chapters: …
4 Homepage lower: …
5 Archive: …
6 Sale: …
7 Contact: …
8 Constraints: …
9 Responsive: …
10 Polish: …

FAILURES
- [id] short description — URL — what you saw

NOTES
- optional observations that are not failures
```

---

## Out of scope

- Redesigning the site
- Inventing missing captions or provenance
- Git / Netlify deploy configuration
