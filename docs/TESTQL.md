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
3. Primary `.section-add-button` is left of the view-switch (not a create mode inside the switch)
4. URL writes `item_view` and `viewport` separately from section `view`
5. `viewport=tablet` defaults to `item_view=cards`; `viewport=pc` defaults to `table`
6. `organization` (tenant) is distinct from `org` (filter)
7. Tab change is shareable without reload and sets `last=`
8. `viewport=mobile` at 375px: no horizontal overflow, rail hidden, hamburger visible
9. No `support` organization-rail leaf; `tab=support` opens tasks
10. Infinite-scroll footer on production collections
11. One `<footer class="footer">` on public and app chrome

Legacy assert “create/import control is last in the switch” is **withdrawn**.

## Example

See [`examples/testql/gui-standardization.testql`](../examples/testql/gui-standardization.testql).

Adopters should keep a thin copy or symlink under their testkit that cites:

```text
# ADOPT: wellmanifest/gui
# HOME: https://github.com/wellmanifest/gui
```

Do not restate principles in the TestQL file; assert behavior against the HOME pack.
