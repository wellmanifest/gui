# Page DSL examples (`wellmanifest.gui/page/v1`)

| File | What it shows |
| --- | --- |
| `observed-marketplace.page.json` | Live `/marketplace` — 5 colors, 6 sizes → `GUI-VIS-TYPE-001` |
| `observed-landing.page.json` | Contact URL rendered the marketing homepage, not the panel |
| `declared-panel-contact.page.json` | What `action=contact` *should* be (`kind=panel`) |
| `declared-form.page.json` | Generic public form profile |
| `declared-article.page.json` | Generic legal/article profile |
| `compare-marketplace-landing.json` | `cross-kind` — do not score as panel drift |
| `compare-intent-contact.json` | `intent-mismatch` — declared panel vs observed landing |

Regenerate observed files from a running product:

```bash
python3 scripts/emit-page-examples.py
# or live:
python3 scripts/probe-visual.py --intents marketplace,panel --out-dir /tmp/gui-pages \
  'http://127.0.0.1:8781/marketplace' \
  'http://127.0.0.1:8781/?action=contact&viewport=pc&item_view=table&lang=pl&currency=PLN&theme=dark&organization=info-softreck'
```
