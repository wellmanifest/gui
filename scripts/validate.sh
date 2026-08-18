#!/usr/bin/env bash
# Validate wellmanifest/gui schemas and examples (propose-only pack).
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

fail() { echo "GUI-VALIDATE-001: $*" >&2; exit 1; }

[[ -f VERSION ]] || fail "VERSION missing"
[[ -f standard/gui.standard.v1.json ]] || fail "standard missing"
[[ -f schemas/gui-dsl.schema.json ]] || fail "schema missing"
[[ -f schemas/gui-page.schema.json ]] || fail "page schema missing"
[[ -f examples/panel.gui.json ]] || fail "example missing"
[[ -f examples/pages/observed-marketplace.page.json ]] || fail "page example missing"

python3 - <<'PY'
import json, sys
from pathlib import Path

root = Path(".")
version = (root / "VERSION").read_text().strip()
standard = json.loads((root / "standard/gui.standard.v1.json").read_text())
schema = json.loads((root / "schemas/gui-dsl.schema.json").read_text())
page_schema = json.loads((root / "schemas/gui-page.schema.json").read_text())
example = json.loads((root / "examples/panel.gui.json").read_text())

assert version == "1.4.0", version
assert standard.get("version") == 5
assert standard.get("placement", {}).get("home") == "wellmanifest"
assert standard.get("placement", {}).get("shape") == "domain_pack"
assert standard.get("authority") == "propose-only"
assert schema.get("$id") == "https://wellmanifest.com/schemas/gui-dsl/v1"
assert page_schema.get("$id") == "https://wellmanifest.com/schemas/gui-page/v1"
assert example.get("schema") == "wellmanifest.gui/dsl/v1"
assert example.get("placement", {}).get("adopt") == "wellmanifest/gui"

CREATE = {"add", "import", "create", "register"}

# identities-style createControl on every viewSwitch in the example
for surface in example.get("surfaces", []):
    vs = surface.get("viewSwitch")
    if vs is None:
        continue
    cc = vs.get("createControl")
    assert cc is not None, f"{surface.get('id')}: createControl required"
    assert cc.get("placement") == "primary-button-left", (
        f"{surface.get('id')}: createControl.placement must be primary-button-left"
    )
    mode = cc.get("mode")
    assert mode in CREATE, f"{surface.get('id')}: invalid create mode {mode}"
    modes = vs.get("modes") or []
    assert mode not in modes, (
        f"{surface.get('id')}: create mode {mode} must not appear inside viewSwitch.modes"
    )
    assert not (CREATE & set(modes)), (
        f"{surface.get('id')}: viewSwitch.modes must be presentation-only"
    )

chat = next((s for s in example["surfaces"] if s.get("kind") == "system-chat"), None)
assert chat is not None, "example must declare system-chat"
assert chat["systemChat"]["persistence"]["primary"] in ("account-hosting", "server-config", "env")

principle_ids = {p.get("id") for p in standard.get("principles", [])}
assert "create-primary-button-left" in principle_ids
assert "responsive-default-view" in principle_ids
assert "page-kind" in principle_ids
assert "visual-budget" in principle_ids
assert "compare-kind-first" in principle_ids
assert "view-switch-create-last" not in principle_ids

profiles = standard.get("page_profiles") or {}
for kind in ("landing", "marketplace", "article", "form", "auth", "panel"):
    assert kind in profiles, kind
    assert "visualBudgets" in profiles[kind]

market = json.loads((root / "examples/pages/observed-marketplace.page.json").read_text())
landing = json.loads((root / "examples/pages/observed-landing.page.json").read_text())
cmp_ml = json.loads((root / "examples/pages/compare-marketplace-landing.json").read_text())
cmp_intent = json.loads((root / "examples/pages/compare-intent-contact.json").read_text())
assert market.get("schema") == "wellmanifest.gui/page/v1"
assert market["page"]["kind"] == "marketplace"
assert any(d["code"] == "GUI-VIS-TYPE-001" for d in market.get("defects") or [])
assert landing["page"]["kind"] == "landing"
assert landing["page"]["intentKind"] == "panel"
assert any(d["code"] == "GUI-PAGE-KIND-001" for d in landing.get("defects") or [])
assert cmp_ml.get("schema") == "wellmanifest.gui/page-compare/v1"
assert cmp_ml.get("comparable") == "cross-kind"
assert cmp_intent.get("comparable") == "intent-mismatch"

print("ok: wellmanifest/gui validate")
PY

scenario="$root/examples/testql/gui-standardization.testql"
grep -q 'ADOPT: wellmanifest/gui' "$scenario" || fail "TestQL example missing ADOPT cite"
grep -q 'SET gui_driver' "$scenario" || fail "TestQL example missing gui_driver"
grep -q 'section-add-button' "$scenario" || fail "TestQL example missing identities-style Add button assert"

echo "validated $(cat VERSION)"
