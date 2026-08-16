# TestQL / autogrammar binding

HOME pack: `wellmanifest/gui` (propose-only). Runtime scenarios live with the
product testkit; this pack ships the binding contract and an example scenario.

## Driver

```text
SET gui_driver "playwright"
```

Products may map `gui_driver` to autogrammar or another harness. The driver
must support: navigate (`GUI_START`), wait, click, visible/text asserts, and
`GUI_EVAL` for URL/order checks.

## Required asserts (contract)

From `standard/gui.standard.v1.json` → `testql_contract.required_assertions`:

1. Section toolbar visible
2. View-switch visible when multi-mode
3. Create/import control is last in the switch
4. URL reflects `tab` / `view` without full reload
5. Infinite-scroll footer on production collections

## Example

See [`examples/testql/gui-standardization.testql`](../examples/testql/gui-standardization.testql).

Adopters should keep a thin copy or symlink under their testkit that cites:

```text
# ADOPT: wellmanifest/gui
# HOME: https://github.com/wellmanifest/gui
```

Do not restate principles in the TestQL file; assert behavior against the HOME pack.
