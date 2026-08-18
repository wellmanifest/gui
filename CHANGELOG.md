# Changelog

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
