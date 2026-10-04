# Changelog

## [1.6.0] - 2026-10-04
### Added
- **Conversational stream purity and process isolation** principle: chat streams must not be polluted with raw process stdout/stderr; executions route to dedicated Process/Terminal views.
- **Bidirectional workspace URL state synchronization** principle: multi-pane workspaces deterministically serialize layout, window order, pane views, focus, dialog, active tab, user query, target device, and action telemetry via `replaceState`.
- **Window media recording controls** principle: standard Play/Stop recording controls on pane headers and window tools menus for WebM capture.
- Expanded `url_query_contract.params` with `layout`, `order`, `panes`, `focus`, `dialog`, `q`, `user`, `targetPane`, `targetEnv`, `act`, `lastClick`.

## [1.5.0] - 2026-08-30
### Added
- Negative action-surface invariants: visible controls must resolve and dispatch
  from one versioned registry; separately authored presentation and execution
  lists are non-conformant.
- Capability-truth rule for keyboard, pointer, completion, arrow, and submit
  hints.
- Bounded runtime-provenance and observation-currency rules so stale checkouts,
  caches, and mixed-source projections are not presented as canonical/current.

## [1.4.0] - 2026-08-18
### Fixed
- `infer_kind`: a page with a form and `contact`/`kontakt` in the URL or title
  is `form`, even when a marketing heading outline is still long.
- Probe `listing` landmark also matches `main table` (not only product class names).
- `infer_kind`: a listing landmark alone does not override a long marketing
  heading outline (landing preview tables stay `landing`).
- `kind=article` without an `article` landmark is `GUI-VIS-STRUCT-005`.
- A `heading-outline` page with H1 and no H2 is `GUI-VIS-STRUCT-006`.

### Added
- Generic **page DSL** `wellmanifest.gui/page/v1` for landing, marketplace,
  article, form, auth, and panel. Panel collection contracts stay on
  `wellmanifest.gui/dsl/v1`.
- Per-kind visual budgets (font families, colors, font sizes) and defect
  codes (`GUI-VIS-*`, `GUI-PAGE-KIND-001/002`, `GUI-PAGE-CHROME-001`).
- Compare document `wellmanifest.gui/page-compare/v1`: kind first, then
  landmarks, then tokens (`same-kind` | `cross-kind` | `intent-mismatch`).
- Probe emits page documents: `scripts/probe-visual.py --intents …`.
- Examples under `examples/pages/` from live `:8781` marketplace and the
  contact URL (observed as landing, not panel).

## [1.3.0] - 2026-08-18
### Changed
- Split the URL contract: `view=` is section/create mode only; presentation is
  `item_view=` plus `viewport=`. Chrome also writes `lang`, `currency`, `theme`,
  `organization`, `last`, `trail`, `menu`.
- Viewport defaults: tablet/mobile → `cards`, pc → `table`. Compact viewports
  hide the rail and use a hamburger drawer; 375px must not overflow.
- `organization=` is the tenant slug; `org=` stays a collection filter.
- Tab changes `pushState` (with `last`/`trail`); chrome uses `replaceState`.
- Contextual work tabs (projects/tasks/calendar) leave the organization rail.
  Rail `<summary>` opens `tab=group-<id>`. `support` is retired from the
  registry enum and aliases to tasks.
- One `<footer class="footer">` on public and app chrome.
- TestQL/docs: withdrawn “create last in the switch”; added chrome, 375px,
  support-retired and footer asserts.

## [1.2.0] - 2026-08-18
### Added
- **Global item-view delegation**: Section toolbars delegate standard item presentation (`cards | list | table`) to `#global-item-view` without redundant ad-hoc inline buttons.
- **Workspace rail organization navigation**: Standardized uncollapsed primary rail organization switcher (`#active-organization`) with `+ Nowa organizacja…` create option and automatic focus transition to `tab=configuration`.
- Enforced single-source switcher constraint (disallowing duplicate tenant switcher in top navbar).

## [1.1.0] - 2026-08-16
### Changed
- Canonical create UX is **identities-style**: primary Add button left of
  `.item-view-switch` inside `.section-view-toolbar` (presentation modes only).
- Supersedes create-last-inside-view-switch; TestQL, DSL example, and validators
  assert Add-left + `view=add|import` URL sync.
- Device-aware default view when URL has no `view=`: desktop → table,
  tablet/portrait → list, smartphone → panels(=cards).

## [1.0.0] - 2026-08-16
### Added
- Initial release of the `wellmanifest/gui` universal domain pack.
- Canonical GUI DSL specification schema (`subactor.adopt.wellmanifest-gui/v1`).
- Autogrammar validation rules for toolbar, view switch, iconography, and URL state persistence.
- TestQL contract verification assertions for web GUI rendering and mode transitions.
