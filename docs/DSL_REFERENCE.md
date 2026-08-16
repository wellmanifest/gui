# GUI DSL reference

Schema: [`schemas/gui-dsl.schema.json`](../schemas/gui-dsl.schema.json)  
`$id`: `https://wellmanifest.com/schemas/gui-dsl/v1`

## Minimal document

```json
{
  "schema": "wellmanifest.gui/dsl/v1",
  "id": "example.product/panel",
  "version": "1.1.0",
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
        "selector": ".item-view-switch",
        "modes": ["cards", "table", "list"],
        "createControl": {
          "placement": "primary-button-left",
          "toolbarSelector": ".section-view-toolbar",
          "buttonSelector": ".section-add-button",
          "mode": "add"
        }
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

## Create control + view-switch

**Identities style (canonical):** primary Add button left of the view-switch
inside `.section-view-toolbar`. View-switch holds presentation modes only.
Clicking Add opens the create form and sets `view` to the create mode id
(`add` / `import` / …). Do not put create modes inside the switch, and do not
keep both an Add button and a create mode in the switch.

## Responsive default view

When the shareable URL has **no** `view=` (and the user has not pinned a view in
session storage), pick a presentation mode from the viewport:

| Device | Default |
| --- | --- |
| Desktop | `table` |
| Small tablet or portrait/pivot | `list` |
| Smartphone | `panels` (alias of `cards`) |

Explicit `view=` always wins. Optional session pins must not override the URL.

## URL state

| Param | Meaning |
| --- | --- |
| `tab` | Top-level surface |
| `view` | Active presentation or create mode |
| nested (`project`, `host`, `org`, …) | Selection under a tab |
| `registry` / `tag` / `filter` | Connector catalog controls |

Use `history.replaceState` (default) so shared links restore state without reload.

## System chat

When `kind: system-chat`:

- `persistence.primary` is `account-hosting`, `server-config`, or `env`
- optional `injectionGlobal` (e.g. `__SUBACTOR_OPENWEBUI_URL__`)
- `optionalBrowserOverride: localStorage` is never the sole durability path
- `gracefulFailure: true` when the upstream chat service is down
