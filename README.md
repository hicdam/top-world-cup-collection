# Top World Cup Collection

Design POC for Thomas Käppeli and Norbert Käser to react against.

English, static, no shop. Copy is theirs. Spec: `docs/superpowers/specs/2026-08-17-top-world-cup-collection-poc-design.md`

## Run

```bash
python3 -m http.server 8765 --directory site
```

Open http://127.0.0.1:8765/

## Rebuild

```bash
python3 scripts/ingest_images.py
python3 scripts/generate.py
python3 scripts/check_site.py
```
