# Top World Cup Collection POC Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a local, English, static magazine site of the collection that Käppeli and Käser can react against.

**Architecture:** One JSON file is the content store. A small Python generator writes static HTML from that JSON plus a shared CSS file. Images are local copies of the existing site, cropped only in CSS. Period tokens are CSS classes on the issue slug. No framework, no backend, no mailbox.

**Tech Stack:** Static HTML, CSS, a little JS for the contact form. Python 3 stdlib to generate pages and run checks. Any static file server for preview.

## Global Constraints

- Copy is theirs. Light tidy only. No invented headlines, no house metaphor, no em dashes, no AI filler.
- Sale-as-a-whole appears only on Contact, in his words.
- No official FIFA marks, Willie, or trophy-as-logo in chrome.
- Mobile first. One column. Desktop is a wider measure, not a new layout.
- No prices, cart, CMS, i18n, F1, or live mail.
- Paper `#f3eee4`, ink `#14110e`, house rule `#9a2b24`.

**Spec:** `docs/superpowers/specs/2026-08-17-top-world-cup-collection-poc-design.md`

---

## File map

- Create: `site/data/collection.json` — tournaments, rooms, pieces, his copy
- Create: `site/styles.css` — house + period tokens
- Create: `site/site.js` — contact form confirm only
- Create: `scripts/ingest_images.py` — download selected images from the live site
- Create: `scripts/generate.py` — write HTML from JSON
- Create: `scripts/check_site.py` — copy audit + required pages + index years
- Create: `site/index.html`, `site/collection.html`, `site/contact.html`, `site/404.html`
- Create: `site/{year}.html` for every year/room slug
- Create: `site/piece/petrone.html`, `site/piece/fifa-1904.html`, `site/piece/kocsis.html`
- Create: `site/images/*` — local documentary photos

---

### Task 1: Content store and images

**Files:**
- Create: `site/data/collection.json`
- Create: `scripts/ingest_images.py`
- Create: `site/images/*`

**Interfaces:**
- Consumes: live site `rc_images/`, English sales PDF text already extracted
- Produces: `collection.json` with `issues[]`, `pieces[]`, `copy`, `contacts`; local JPEGs named `{slug}-{id}.jpg`

- [ ] **Step 1:** Write `collection.json` with every year and special room from the current homepage, period chips from the spec, dressed rooms 1930 / 1954 / FIFA, cover piece Petrone, supporting pieces Goldpin FIFA 1904 and Kocsis. Copy strings taken from the PDF (introduction, information, viewing, item titles and notes). No em dashes.

- [ ] **Step 2:** Write and run `scripts/ingest_images.py` to download: Petrone (`img_3106`), FIFA pin (`img_3425`), all 1954 page images, remaining 1930 page images, first image of every other year/room for the index. Store under `site/images/`.

- [ ] **Step 3:** Confirm files exist: `site/data/collection.json`, `site/images/petrone.jpg`, `site/images/fifa-1904.jpg`, at least one image per issue that has photos on the live site.

- [ ] **Step 4:** Commit `docs(data): add collection JSON and ingested images`

---

### Task 2: House CSS, generator, and pages

**Files:**
- Create: `site/styles.css`
- Create: `scripts/generate.py`
- Create: `site/*.html`, `site/piece/*.html`

**Interfaces:**
- Consumes: `collection.json` shape from Task 1
- Produces: static pages matching spec slugs (`/`, `/collection`, `/1930`, `/1954`, `/fifa`, `/piece/petrone`, `/contact`)

- [ ] **Step 1:** Write house CSS (cream paper, ink, red rule, serif + condensed grotesque, one-column measure) and period classes `.era-1930`, `.era-1954`, `.era-fifa`. Image grade via CSS filter. Mobile first.

- [ ] **Step 2:** Write `scripts/generate.py` that emits: home (type then Petrone, Also in this issue, link to collection), collection index (every issue, chip, thumb, their year title), year/room pages (lead + vertical sequence, no invented captions), three piece pages, contact (his introduction + form), 404.

- [ ] **Step 3:** Run `python3 scripts/generate.py` and open `site/index.html` structure: masthead, Petrone title exactly as tidied from the PDF, no em dash in output.

- [ ] **Step 4:** Commit `feat(site): generate ink-on-paper magazine pages`

---

### Task 3: Form, checks, local server

**Files:**
- Create: `site/site.js`
- Create: `scripts/check_site.py`

**Interfaces:**
- Consumes: generated HTML
- Produces: form confirm state; check script exit 0

- [ ] **Step 1:** Form: name, email, message, optional piece. Required name/email/message. Confirm state lists the two emails. No network send.

- [ ] **Step 2:** `check_site.py` fails if: a required page is missing; collection HTML lacks any issue slug from JSON; any HTML contains `—` or forbidden words (`goddess`, `journey`, `iconic`, `stunning`, `timeless`, `discover`, `welcome to`); contact page lacks “only available for purchase as a whole”; home contains that sale sentence.

- [ ] **Step 3:** Run checks. Serve `site/` locally. Verify phone and desktop: home, collection, 1930, 1954, FIFA, Petrone, contact, form confirm, 2026 empty year, 404.

- [ ] **Step 4:** Commit `feat(site): contact form and site checks`

---

## Spec coverage

| Spec section | Task |
|---|---|
| IA five surfaces | 2 |
| Whole collection listed | 1 + 2 |
| Ink on paper + Room period | 2 |
| Their copy only | 1 + 3 |
| Sale only on Contact | 2 + 3 |
| Photography ingest + grade | 1 + 2 |
| Form, no mailbox | 3 |
| Empty year / 404 | 2 |
| Out of scope (no CMS/i18n/shop) | all |
