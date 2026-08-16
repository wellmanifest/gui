# wellmanifest/gui — Universal GUI DSL & Verification Standard

Standardized declarative specification for web application interfaces, SaaS admin dashboards, and diagnostic control panels with automated TestQL and autogrammar contract verification.

## Features

- **Declarative GUI DSL**: Define toolbars, view modes, forms, matrix tables, and list footers in structured JSON/YAML schemas.
- **Layout Standardization**: Enforces `.item-section-toolbar`, inline SVG iconography, and responsive mode switching.
- **State & URL Synchronization**: Universal query parameter persistence for deep-linking (`tab`, `view`, `filter`, `registry`).
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
Run TestQL assertions:
```bash
./project.sh test
```
