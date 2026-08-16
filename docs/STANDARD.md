# GUI standardization (normative)

Authority: **propose-only**. Adopters implement; this pack does not grant
production mutation or merge rights.

## Objects

| Object | Role |
| --- | --- |
| GUI DSL document | Declares surfaces, toolbar, view-switch, URL state, TestQL binding |
| Standard JSON | Machine principles + URL/TestQL contracts (`standard/gui.standard.v1.json`) |
| TestQL scenario | Driver + asserts for toolbar, Add-left, URL sync |
| Runtime adopt pin | Thin pointer in product repo (version/path), never a second SSOT |

## Invariants

1. **Identities-style create**: primary Add/create button left of `.item-view-switch`
   inside `.section-view-toolbar`. View-switch is presentation modes only
   (no add/import/create/register mode). Clicking Add opens the create form and
   sets `view=add|import|…` (same URL contract as before).
2. **Responsive default view** when `view=` is absent (and no user pin): desktop →
   `table`; tablet/portrait → `list`; smartphone → `panels` (= `cards`). Explicit
   `view=` always wins; session pin must not fight the URL.
3. URL query is the shareable panel state; no full reload for tab/view changes.
4. Toolbar + SVG icons on every multi-mode section; Add + switch stretch as one bar.
5. Infinite-scroll (or equivalent) on production collections.
6. System chat durable URL: account/hosting + server injection; localStorage optional only.
7. Pack content is versioned; consumers pin adopt revision.

Superseded: create/import as last mode *inside* the view-switch (legacy
wellmanifest/gui note). Prefer identities layout; do not keep both patterns.

## Adopting

1. Declare `placement.adopt: wellmanifest/gui` on the runtime ticket/intent.
2. Pin the HOME pack revision in the product adopt map (pointer, not copy).
3. Implement selectors/classes consistent with the DSL example (or map them in the DSL document).
4. Ship TestQL scenarios that assert Add-left + URL sync + toolbar visibility.
5. Do not fork principles into a Subactor-only “standard” file as a second HOME.
