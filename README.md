# Top World Cup Collection

Premium digital exhibition of Thomas Käppeli's World Cup collection.

Built only from the live source site and the four official sales documents.

**Do not invent copy, captions, object identities, or imagery.**

## Source of truth

- Crawl: `python3 scripts/crawl_source.py`
- Inventory: `source/data/inventory.json`
- Manifest: `source/data/manifest.json`
- Canonical HTML copy: `source/data/copy.json`
- Gaps (do not fill): `source/GAPS.md`
- Assets: `source/assets/{tournament}/` (original filenames)
- Sales PDFs: `source/documents/`

## Exhibition

```bash
python3 scripts/generate_exhibition.py
python3 -m http.server 8766 --directory exhibition
```

Open http://127.0.0.1:8766/

Live preview: https://top-world-cup-collection.netlify.app

```bash
# publish an update
rsync -a --copy-links --exclude thumbs --exclude '.DS_Store' exhibition/ /tmp/twcc-netlify/
netlify deploy --prod --dir=/tmp/twcc-netlify
```

The collection is sold only as a whole. There are no individual prices or buy buttons.

Photographs are associated with a tournament only because that is the page they appear on. Item names in the sales PDFs are not paired to files.
