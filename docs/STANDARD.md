# GUI standardization (normative)

Authority: **propose-only**. Adopters implement; this pack does not grant
production mutation or merge rights.

## Objects

| Object | Role |
| --- | --- |
| GUI DSL document | Declares surfaces, toolbar, view-switch, URL state, TestQL binding |
| Standard JSON | Machine principles + URL/TestQL contracts (`standard/gui.standard.v1.json`) |
| TestQL scenario | Driver + asserts for toolbar, create-last, URL sync |
| Runtime adopt pin | Thin pointer in product repo (version/path), never a second SSOT |

## Invariants

1. Create/import/add/register is last in every view-switch.
2. URL query is the shareable panel state; no full reload for tab/view changes.
3. Toolbar + SVG icons on every multi-mode section.
4. Infinite-scroll (or equivalent) on production collections.
5. System chat durable URL: account/hosting + server injection; localStorage optional only.
6. Pack content is versioned; consumers pin adopt revision.

## Adopting

1. Declare `placement.adopt: wellmanifest/gui` on the runtime ticket/intent.
2. Pin the HOME pack revision in the product adopt map (pointer, not copy).
3. Implement selectors/classes consistent with the DSL example (or map them in the DSL document).
4. Ship TestQL scenarios that assert create-last + URL sync + toolbar visibility.
5. Do not fork principles into a Subactor-only “standard” file as a second HOME.
