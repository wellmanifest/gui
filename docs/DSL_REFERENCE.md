# GUI DSL reference

Schema: [`schemas/gui-dsl.schema.json`](../schemas/gui-dsl.schema.json)  
`$id`: `https://wellmanifest.com/schemas/gui-dsl/v1`

## Minimal document

```json
{
  "schema": "wellmanifest.gui/dsl/v1",
  "id": "example.product/panel",
  "version": "1.0.0",
  "placement": {
    "home": "subactor",
    "shape": "runtime_service",
    "adopt": "wellmanifest/gui",
    "runtimeOwner": "subactor"
  },
  "urlState": {
    "strategy": "replaceState",
    "params": {
      "tab": "tab",
      "view": "view",
      "nested": ["project", "host", "org", "registry", "tag", "filter"]
    }
  },
  "surfaces": [
    {
      "id": "hosts",
      "kind": "section",
      "tab": "hosts",
      "toolbar": {
        "selector": ".item-section-toolbar",
        "titleSelector": ".panel-section-title",
        "icon": "svg-inline"
      },
      "viewSwitch": {
        "selector": ".view-switch",
        "modes": ["cards", "table", "list", "add"],
        "createLast": true,
        "createModes": ["add"]
      },
      "infiniteScroll": {
        "footerSelector": ".infinite-scroll-footer",
        "hook": "useInfiniteScroll"
      },
      "prependOnCreate": true
    }
  ],
  "testql": {
    "driver": "playwright",
    "scenarioRefs": ["examples/testql/gui-standardization.testql"]
  }
}
```

## View-switch ordering

Presentation modes first; **create-like modes last**. Validators and TestQL
must treat any create/import/add/register control that is not last as a failure.

## URL state

| Param | Meaning |
| --- | --- |
| `tab` | Top-level surface |
| `view` | Active view-switch mode |
| nested (`project`, `host`, `org`, …) | Selection under a tab |
| `registry` / `tag` / `filter` | Connector catalog controls |

Use `history.replaceState` (default) so shared links restore state without reload.

## System chat

When `kind: system-chat`:

- `persistence.primary` is `account-hosting`, `server-config`, or `env`
- optional `injectionGlobal` (e.g. `__SUBACTOR_OPENWEBUI_URL__`)
- `optionalBrowserOverride: localStorage` is never the sole durability path
- `gracefulFailure: true` when the upstream chat service is down
