# Top World Cup Collection · design POC

**Date:** 2026-08-17  
**Status:** design locked in brainstorm; waiting on spec review before a plan  
**Purpose:** a designed site the collectors can react against. Not a shop. Not a production CMS. English only.

Source collection: [top-world-cup-collection.ch](https://www.top-world-cup-collection.ch/)  
Holders: Thomas Paul Käppeli (Wattenwil) and Norbert Käser (Schmitten)

---

## 1. Job of this POC

Show the whole collection as a magazine, not a wall of photos. The site should feel as considered as the objects. Football people with money should want to look. The collectors should have something concrete to like, dislike, and correct.

Success is reaction. If they argue about a cover, a year, or a sentence, the POC has done its job.

It is not success to finish every photograph, wire a mailbox, or replace the live .ch site.

---

## 2. Decisions (locked)

| Topic | Decision |
|---|---|
| Job | Showcase the collection. Private contact. No prices. |
| Commercial truth | The collection is only for sale as a whole (~500 pieces). Said in Thomas’s words on Contact. Not on the cover. |
| Name | Keep **Top World Cup Collection**. |
| Language | English only. |
| Shape | **The Issue** (GQ / Huck). Not a district map. Not an object grid. |
| Visual | **Ink on paper**: cream stock, black type, one blood-red house rule. |
| Home layout | **Type, then the object**: kicker, title, their copy, then the photograph. |
| How much collection | All of it is listed. Depth is behind a door. Not 25 equal photo dumps. |
| Period | **Room**. Each issue has a period layer. The house does not change. |
| Photography | Grade and isolate existing shots. A few cover still-lifes if we make them. |
| Copy | **Their words, light tidy only.** No new tone. |
| Enquire | Their contact line. Form on Contact. A piece may end with the same contact line. It is not a checkout. |
| Stack | Static HTML, CSS, a little JS. No framework, no CMS, no shop. |

---

## 3. Information architecture

Five surfaces. Everything else is a variant.

1. **The issue (home)**  
   One cover piece. Kicker, their title, their sentences, photograph. Then “Also in this issue” as a short list (two supporting pieces). Then a way into the collection index. This is not a directory.

2. **The collection**  
   Every tournament and every special room as an archive index. Each row: year, host, one accent chip, one image if we have one, their short title for that year (e.g. `World Cup URUGUAY 1930`). 1924 Paris and 1928 Amsterdam Olympics sit at the top of the run. Special rooms after 2026: Autographs / pictures, Information boards, FIFA official items, Sports equipment, Divers.

3. **An issue of a year (or a special room)**  
   Same rhythm as home. Lead object from Thomas’s highlights where we have one. Then the rest of that year’s pieces as a designed sequence (title + image). Not a thumbnail wall.

4. **A piece**  
   Their title, their dates if given, their note if given, the photograph at full scale. Last line: “If you have any questions, please do not hesitate to contact us.” linking to Contact. No price. No “enquire about this piece” as a product CTA.

5. **Contact**  
   “The highlights of the collection” / by Thomas Käppeli. His introduction and “Information about the collection”, lightly tidied. Viewing line. Both contacts as in the sales document. A small form (name, email, message). Designed confirm state. No live mailbox required.

POC builds all five. Other years exist as index rows. If a year has images on the current site, the year page can be a light issue (lead image + sequence). If it does not, the row still exists and the page says only the year title.

Cover for the POC homepage: **Jules Rimet Cup of Pedro Petrone** (Uruguay 1930). Supporting pieces in the “Also in this issue” list: **Goldpin FIFA 1904**, and **Top Scorer Medal SANDOR KOCSIS** (1954). The Genève ticket may appear in the 1954 sequence as an untitled photograph if it has no PDF label.

---

## 4. Visual system (house)

Constant on every page.

- Paper: cream `#f3eee4`. Ink: `#14110e`. House rule: `#9a2b24`.
- Masthead: `Top World Cup Collection` plus one word, `Collection` or `Contact`.
- Type: a readable serif for titles and body (Georgia or an equivalent we host). A small caps / wide-tracked sans for kickers and the masthead.
- Mobile first. Phone is the designed canvas. Desktop is the same column, wider measure, not a new layout.
- Photography sits on the paper. Crop in. Isolate the object from tablecloth where we can. Slight grade (contrast up, saturation a little down). No fake studio backgrounds except for any cover still-lifes we generate.
- No official FIFA World Cup logos, no World Cup Willie as a mark, no trophy silhouette used as branding. Photographs of objects that already carry marks are documentary and allowed.

---

## 5. Period layer (Room)

The house never changes. An issue may change four things only:

1. Accent colour  
2. Display type character (italic Deco vs grotesque vs jeweller’s serif)  
3. One ornament (a rule, a hairline, a small geometric)  
4. Paper temperature (cream shifted warm, pink, or cooler)

Source order: the object first, then that tournament’s print culture.

Do not recreate official posters. Do not put Leupin’s 1954 mark, Willie, or a Jules Rimet outline in the chrome.

### POC rooms (fully dressed)

| Issue | Period layer | Taken from |
|---|---|---|
| 1930 Uruguay | Lithograph red `#8a2a24`, celeste `#1f4f6b`, brass `#c9a227`. Italic display. A short deco stripe. Warmer paper. | Laborde poster language + Petrone cup (brass, green marble) |
| 1954 Switzerland | Dusty pink paper `#f7ebe6`, ink, Swiss red `#c8102e`. Grotesque display. Small cross-in-circle as ornament, not a logo lockup. | Genève ticket already on the current site + three-language Swiss print culture |
| FIFA official | Navy `#0e1624`, brass `#c4a46a`, silk cream. Hairline rules. | 1904 gold pin in its box |

### Index tokens (chip only)

Every other year and special room gets a three-colour chip on the collection index so the run of time is visible. Those pages stay house unless we later dress them. Tokens:

| Year / room | Chip |
|---|---|
| 1924 Paris Olympics | gold / navy / cream |
| 1928 Amsterdam Olympics | black / orange / cream |
| 1934 Italy | green / red / cream |
| 1938 France | navy / red / cream |
| 1950 Brasil | green / gold / blue |
| 1958 Sweden | yellow / blue / black |
| 1962 Chile | teal / red / pale |
| 1966 England | red / navy / cream (geometry only; no Willie) |
| 1970 Mexico | pink / orange / black |
| 1974 West Germany | black / orange / cream |
| 1978 Argentina | sky / gold / cream |
| 1982 Spain | red / yellow / blue |
| 1986 Mexico | earth red / gold / dark |
| 1990 Italy | green / red / cream |
| 1994 USA | blue / red / yellow |
| 1998 France | blue / red / cream |
| 2002 Korea / Japan | black / red / cream |
| 2006 Germany | night / cream / brass |
| 2010 South Africa | black / gold / earth |
| 2014 Brasil | green / gold / blue |
| 2018 Russia | red / gold / cream |
| 2022 Qatar | maroon / sand / ink |
| 2026 Canada / USA / Mexico | blue / red / green |
| Autographs | ink / cream / house red |
| Information boards | gold / ink / cream |
| Sports equipment | leather / grass / cream |
| Divers | house ink / cream / house red |

---

## 6. Copy

This is a hard rule. The last correction in brainstorm overrode “their facts, our sentences”.

**Use their copy.** Source of truth:

- English sales document: `https://www.top-world-cup-collection.ch/rc_images/def_verkauf_fussballsammlung_helvetica_englisch.pdf`
- Existing site lines, especially: “If you have any questions, please do not hesitate to contact us.”
- Item titles and notes as written (e.g. “Jules Rimet Cup of PEDRO PETRONE”, “Goldpin FIFA 1904”, “The collection is only available for purchase as a whole.”)

**Light tidy only**

- Spelling: Medale → Medal, Smal → Small, OLYPIC → Olympic, disaproved → disapproved, weights → weighs, REREGRINO → Peregrino when it is clearly a typo of a name he spelled correctly nearby.
- Keep contractions as he wrote them.
- Line breaks for the screen. Do not rewrite.
- Title case on masthead and nav. Keep his item titles.

**Forbidden**

- New headlines (“The first goddess”, “The cup for the first winners”, “Fifty years, toward 2030”).
- A house voice, magazine deks, metaphors we invented.
- The word “house” as a brand metaphor on the site. He says **collection**.
- Em dashes.
- AI filler (“crafted”, “journey”, “iconic”, “stunning”, “timeless”, “welcome to”, “discover”).
- Prices, inventing provenance, or adding facts that are not in the PDF or on the current site.

If a photograph on the current site has no label in the PDF, the page shows the image and the year title only. Do not caption it with a guess.

Nav and UI chrome (Collection, Contact, Also in this issue, Send) are allowed as functional labels. Keep them plain.

---

## 7. Contact and form

Contact carries Thomas’s introduction and the sale-as-a-whole paragraph, in his words.

Form fields: name, email, message. Optional: which piece (free text).

Submit on the POC: client-side required fields, then a confirm state using his register: thank you and the two emails as printed.

```
tk@Top-World-Cup-Collection.ch
nk@Top-World-Cup-Collection.ch
```

Do not build Resend, a backend, or a mailbox. `mailto:` on the addresses is enough if someone wants a real send.

Missing fields: stay on the form, mark the field. Do not invent a witty error.

---

## 8. Content and photography

Ingest from the live site. Do not hotlink in the shipped POC.

- Year pages and special rooms listed on the homepage of the current site.
- Images under `rc_images/`.
- English sales PDF for titles, notes, introduction, contacts.

POC dressed rooms: 1930 (Petrone cup as lead), 1954, FIFA. Home uses the Petrone cup.

Image treatment: crop, isolate, grade. Keep enough of the object. Do not retouch marks or engravings.

If we generate cover still-lifes, they are extras beside the documentary photo, never a replacement that hides the real object.

---

## 9. Technical shape

```
/                    home (the issue)
/collection          index of every year and room
/1930                year issue
/1954                year issue
/fifa                special room
/piece/petrone       piece
/piece/fifa-1904     piece
/contact             introduction, viewing, form
/styles.css
/data/collection.json
/images/…
```

Other year slugs (`/1966`, `/autographs`, …) may exist as light pages so the index does not 404.

`collection.json` is the only content store: tournaments, rooms, pieces, copy strings taken from the PDF. Period tokens live in CSS, keyed by the same slug.

Static files. Open locally with any static server. No build step required unless we add one for image compression. No framework.

Mobile first CSS. One column. Type measure about 32–40rem on desktop. Touch targets for nav and form.

---

## 10. Empty, missing, error

| State | Behaviour |
|---|---|
| Year with photos but no PDF labels | Year title + images. No invented captions. |
| Year with no photos | Index row remains. Page is the year title and a line back to the collection. |
| Broken image | Cream field, no icon cartoon, no alt-as-headline. |
| Form incomplete | Inline, plain. |
| Form submitted | Confirm with the two emails. |
| Unknown URL | Simple 404 in house style: “Top World Cup Collection” and a link to Collection. |

---

## 11. Out of scope

- Replacing the live .ch site or setting up hosting/DNS
- German / French / Spanish
- F1 collection
- Piece-by-piece sale, prices, cart
- CMS, auth, analytics, newsletter
- Official FIFA identity as chrome
- Rewriting Thomas’s voice
- Dressing every year at Room intensity in this POC

---

## 12. Check before we call the POC done

- Phone and a desktop width. Home, collection, 1930, 1954, FIFA, one piece, contact, form confirm.
- Every year and special room from the current site appears on `/collection`.
- Copy audit: no em dashes, no invented headlines, no “house” metaphor, piece text traceable to the PDF or left uncaptioned.
- No official tournament logo in the chrome.
- Form does not pretend to have sent mail.
- Period on 1930, 1954, FIFA is visible and still reads as one magazine.

---

## 13. What they should react to

When we show this to Käppeli and Käser, the useful questions are:

1. Is the cover the right object?
2. Is the sale paragraph on Contact enough, or too much?
3. Are his titles and notes shown as he wants them?
4. Does each year feeling different help, or should the paper stay identical?
5. What is missing from the index?

The POC is a prompt. Their answers write the next pass.
