# GUI standardization (normative)

Authority: **propose-only**. Adopters implement; this pack does not grant
production mutation or merge rights.

Pack version **1.3.0** (standard document version 4).

## Objects

| Object | Role |
| --- | --- |
| GUI DSL document | Declares surfaces, toolbar, view-switch, URL state, TestQL binding |
| Standard JSON | Machine principles + URL/TestQL contracts (`standard/gui.standard.v1.json`) |
| TestQL scenario | Driver + asserts for toolbar, Add-left, chrome URL, 375px |
| Runtime adopt pin | Thin pointer in product repo (version/path), never a second SSOT |

## Invariants

1. **Identities-style create**: primary Add/create button left of `.item-view-switch`
   inside `.section-view-toolbar`. View-switch is presentation modes only
   (no add/import/create/register mode). Clicking Add opens the create form and
   sets `view=add|import|…` (section mode only).
2. **Viewport preset + item_view**: `#global-viewport` writes `viewport=`.
   Defaults when `item_view=` is absent: tablet → `cards`, pc → `table`,
   mobile → `cards`. Presentation is never stored in `view=`.
3. **Layered URL**: tab changes `pushState` and set `last` / `trail`. Chrome
   (`viewport`, `item_view`, `lang`, `currency`, `theme`, `organization`, `menu`)
   uses `replaceState`. No full reload for tab or chrome changes.
4. **`organization=` vs `org=`**: tenant slug vs project/collection filter.
5. **Drawer vs rail**: pc shows the workspace rail and `#active-organization`.
   mobile/tablet hide the rail, use a hamburger drawer, `width: 100%`,
   `overflow-x: clip`. 375px must not scroll horizontally.
6. **Contextual work**: projects, tasks and calendar are chat actions, not
   organization-rail leaves. Rail `<summary>` opens `tab=group-<id>` overview.
7. **Support retired**: no `support` rail leaf; `tab=support` / `registry=support`
   alias to tasks.
8. **Global item-view delegation**: `#global-item-view` writes `item_view=`.
   Section toolbars must not duplicate standard mode buttons.
9. **One site footer**: `<footer class="footer">` on public pages and the app
   (SPA `#root` must not receive a second injected footer).
10. Infinite-scroll on production collections; SVG icons only; pack is versioned.

Superseded: create/import as last mode *inside* the view-switch (legacy
wellmanifest/gui note). Superseded: tablet default `view=list` and encoding
presentation in `view=`. Prefer identities layout + `item_view=`.

## Adopting

1. Declare `placement.adopt: wellmanifest/gui` on the runtime ticket/intent.
2. Pin the HOME pack revision in the product adopt map (pointer, not copy).
3. Implement selectors/classes consistent with the DSL example (or map them in the DSL document).
4. Ship TestQL scenarios that assert Add-left + chrome URL + 375px + no support leaf.
5. Do not fork principles into a Subactor-only “standard” file as a second HOME.
