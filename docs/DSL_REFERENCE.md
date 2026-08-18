# GUI DSL reference

Schema: [`schemas/gui-dsl.schema.json`](../schemas/gui-dsl.schema.json)  
`$id`: `https://wellmanifest.com/schemas/gui-dsl/v1`

## Minimal document

```json
{
  "schema": "wellmanifest.gui/dsl/v1",
  "id": "example.product/panel",
  "version": "1.3.0",
  "placement": {
    "home": "subactor",
    "shape": "runtime_service",
    "adopt": "wellmanifest/gui",
    "runtimeOwner": "subactor"
  },
  "urlState": {
    "strategy": "layered",
    "params": {
      "tab": "tab",
      "view": "view",
      "item_view": "item_view",
      "viewport": "viewport",
      "chrome": ["lang", "currency", "theme", "organization", "last", "trail", "menu"],
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

## Viewport + item_view

`#global-viewport` writes `viewport=mobile|tablet|pc`. `#global-item-view`
writes `item_view=cards|list|table`. Defaults when `item_view=` is absent:

| Viewport | Default `item_view` |
| --- | --- |
| `pc` | `table` |
| `tablet` | `cards` |
| `mobile` | `cards` |

Do not write presentation into `view=`. Legacy `view=cards|table|list|panels`
MAY be read once and migrated to `item_view=`.

## URL state

| Param | Meaning |
| --- | --- |
| `tab` | Top-level surface, including `group-<id>` |
| `view` | Section/create mode only (`add` / `import` / …) |
| `item_view` | Presentation from `#global-item-view` |
| `viewport` | Preset from `#global-viewport` |
| `organization` | Active tenant slug |
| `org` | Project/collection filter |
| `last` / `trail` | Previous tab clicks |
| `lang` / `currency` / `theme` / `menu` | Other `nav-controls` chrome |
| nested (`project`, `host`, `registry`, `tag`, `filter`) | Selection under a tab |

History is **layered**: `pushState` on tab (so Back works), `replaceState` on
chrome. Shared links restore state without reload.

## Contextual work and groups

`projects`, `tasks` and `calendar` are contextual-chat actions, not organization
rail leaves. A rail group `<summary>` opens `tab=group-<id>`. `support` is not a
registry value; old URLs alias to `tasks`.

## System chat

When `kind: system-chat`:

- `persistence.primary` is `account-hosting`, `server-config`, or `env`
- optional `injectionGlobal` (e.g. `__SUBACTOR_OPENWEBUI_URL__`)
- `optionalBrowserOverride: localStorage` is never the sole durability path
- `gracefulFailure: true` when the upstream chat service is down
