# wellmanifest/gui — Universal GUI DSL & Verification Standard

Standardized declarative specification for web application interfaces, SaaS admin dashboards, and diagnostic control panels with automated TestQL and autogrammar contract verification.

## Features

- **Declarative GUI DSL**: Panel surfaces (toolbars, view modes, URL chrome) in `wellmanifest.gui/dsl/v1`.
- **Generic page DSL**: Landing, marketplace, article, form, auth, and panel appearance in `wellmanifest.gui/page/v1` (kind + landmarks + visual budgets).
- **Layout Standardization**: Enforces `.item-section-toolbar` **only** on `page.kind=panel`. Public pages keep footer + heading outline.
- **State & URL Synchronization**: Layered query persistence — `tab` / section `view` plus chrome (`viewport`, `item_view`, `organization`, `lang`, `currency`, `theme`, `last`, `trail`).
- **Autogrammar & TestQL Test Harness**: Automated structural assertions for element visibility, mode transition validation, and regression testing.

## Placement & Governance

- `HOME`: `wellmanifest`
- `SHAPE`: `domain_pack`
- `ADOPT`: `wellmanifest/gui`

## Quick Start

Validate a GUI DSL manifest against autogrammar rules:
```bash
./project.sh check
```
Observe live pages into `page/v1` (Chrome CDP, no extra runtime):
```bash
python3 scripts/probe-visual.py --out-dir examples/pages \
  --intents marketplace,panel \
  'http://127.0.0.1:8781/marketplace' \
  'http://127.0.0.1:8781/?action=contact&viewport=pc'
```
Run TestQL assertions:
```bash
./project.sh test
```
