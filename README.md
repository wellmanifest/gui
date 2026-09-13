# wellmanifest/gui — Universal GUI DSL & Verification Standard

Standardized declarative specification for web application interfaces, SaaS admin dashboards, and diagnostic control panels with TestQL and autogrammar binding contracts and static example checks.

## Features

- **Declarative GUI DSL**: Panel surfaces (toolbars, view modes, URL chrome) in `wellmanifest.gui/dsl/v1`.
- **Generic page DSL**: Landing, marketplace, article, form, auth, and panel appearance in `wellmanifest.gui/page/v1` (kind + landmarks + visual budgets).
- **Layout Standardization**: Enforces `.item-section-toolbar` **only** on `page.kind=panel`. Public pages keep footer + heading outline.
- **State & URL Synchronization**: Layered query persistence — `tab` / section `view` plus chrome (`viewport`, `item_view`, `organization`, `lang`, `currency`, `theme`, `last`, `trail`).
- **Autogrammar & TestQL bindings**: Example assertions for element visibility, mode transitions, and regression testing; runtime execution belongs to the adopter testkit.

## Placement & Governance

- `HOME`: `wellmanifest`
- `SHAPE`: `domain_pack`
- `ADOPT`: `wellmanifest/gui`

## Quick Start

Run the pack’s static contract and example checks:
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
This pack does not bundle a TestQL runner. `./project.sh test` and
`./project.sh testql` return exit code **2** with `GUI-TESTQL-UNAVAILABLE`.
Execute the [example scenario](examples/testql/gui-standardization.testql) in
an adopter’s configured testkit; see [TestQL binding](docs/TESTQL.md).

Whole-site (sitemap, nav, SEO, cross-page drift) lives in the composing pack
[`wellmanifest/webpage`](https://github.com/wellmanifest/webpage) —
`wellmanifest.webpage/site-audit/v1`.
