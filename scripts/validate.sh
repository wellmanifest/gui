#!/usr/bin/env bash
# Validate wellmanifest/gui schemas and examples (propose-only pack).
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

fail() { echo "GUI-VALIDATE-001: $*" >&2; exit 1; }

[[ -f VERSION ]] || fail "VERSION missing"
[[ -f standard/gui.standard.v1.json ]] || fail "standard missing"
[[ -f schemas/gui-dsl.schema.json ]] || fail "schema missing"
[[ -f examples/panel.gui.json ]] || fail "example missing"

python3 - <<'PY'
import json, sys
from pathlib import Path

root = Path(".")
standard = json.loads((root / "standard/gui.standard.v1.json").read_text())
schema = json.loads((root / "schemas/gui-dsl.schema.json").read_text())
example = json.loads((root / "examples/panel.gui.json").read_text())

assert standard.get("placement", {}).get("home") == "wellmanifest"
assert standard.get("placement", {}).get("shape") == "domain_pack"
assert standard.get("authority") == "propose-only"
assert schema.get("$id") == "https://wellmanifest.com/schemas/gui-dsl/v1"
assert example.get("schema") == "wellmanifest.gui/dsl/v1"
assert example.get("placement", {}).get("adopt") == "wellmanifest/gui"

# createLast invariant on every viewSwitch in the example
for surface in example.get("surfaces", []):
    vs = surface.get("viewSwitch")
    if vs is not None:
        assert vs.get("createLast") is True, f"{surface.get('id')}: createLast must be true"
        modes = vs.get("modes") or []
        create = set(vs.get("createModes") or [])
        if create:
            for m in create:
                assert m in modes, f"{surface.get('id')}: create mode {m} not in modes"
                assert modes.index(m) == len(modes) - 1 or modes[-1] in create, (
                    f"{surface.get('id')}: create-like mode must be last in modes"
                )

chat = next((s for s in example["surfaces"] if s.get("kind") == "system-chat"), None)
assert chat is not None, "example must declare system-chat"
assert chat["systemChat"]["persistence"]["primary"] in ("account-hosting", "server-config", "env")

print("ok: wellmanifest/gui validate")
PY

scenario="$root/examples/testql/gui-standardization.testql"
grep -q 'ADOPT: wellmanifest/gui' "$scenario" || fail "TestQL example missing ADOPT cite"
grep -q 'SET gui_driver' "$scenario" || fail "TestQL example missing gui_driver"

echo "validated $(cat VERSION)"
