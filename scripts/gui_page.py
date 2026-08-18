"""Shared wellmanifest.gui/page/v1 helpers (propose-only, no runtime)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PACK_ROOT = Path(__file__).resolve().parents[1]
STANDARD_PATH = PACK_ROOT / "standard" / "gui.standard.v1.json"
PAGE_SCHEMA = "wellmanifest.gui/page/v1"
COMPARE_SCHEMA = "wellmanifest.gui/page-compare/v1"
PACK_VERSION = "1.4.0"

FAMILY = {
    "landing": "marketing",
    "marketplace": "commerce",
    "article": "content",
    "form": "account",
    "auth": "account",
    "panel": "workspace",
    "unknown": "marketing",
}

ROLE = {
    "landing": "public",
    "marketplace": "public",
    "article": "public",
    "form": "public",
    "auth": "public",
    "panel": "authenticated",
    "unknown": "public",
}


def load_standard() -> dict[str, Any]:
    return json.loads(STANDARD_PATH.read_text(encoding="utf-8"))


def page_profiles(standard: dict[str, Any] | None = None) -> dict[str, Any]:
    data = standard or load_standard()
    profiles = data.get("page_profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise RuntimeError("standard.page_profiles missing")
    return profiles


def infer_kind(url: str, title: str, structure: dict[str, Any]) -> str:
    chrome = structure.get("chrome") or {}
    landmarks = structure.get("landmarks") or {}
    blob = f"{url} {title}".lower()
    headings = landmarks.get("headingOutline") or []
    if chrome.get("itemSectionToolbar"):
        return "panel"
    if landmarks.get("form") and re.search(r"login|signin|sign-in|register|auth", blob):
        return "auth"
    if landmarks.get("form") and re.search(r"contact|kontakt", blob):
        return "form"
    if re.search(r"legal|privacy|terms|compare|porown", blob):
        return "article"
    if "marketplace" in blob or "catalog" in blob or "registry" in blob:
        return "marketplace"
    if landmarks.get("listing") and len(headings) < 4:
        return "marketplace"
    if landmarks.get("form") and not landmarks.get("listing") and len(headings) <= 3:
        return "form"
    if landmarks.get("article") and len(headings) <= 4:
        return "article"
    if len(headings) >= 4:
        return "landing"
    return "unknown"


def _slug_from_url(url: str, kind: str) -> str:
    path = re.sub(r"^https?://[^/]+", "", url or "")
    path = path.split("?", 1)[0].strip("/") or kind
    slug = re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")
    return slug or kind


def defects_for_page(page: dict[str, Any]) -> list[dict[str, Any]]:
    meta = page.get("page") or {}
    visual = page.get("visual") or {}
    structure = page.get("structure") or {}
    landmarks = structure.get("landmarks") or {}
    chrome = structure.get("chrome") or {}
    budgets = visual.get("budgets") or {}
    counts = visual.get("counts") or {}
    defects: list[dict[str, Any]] = []

    kind = meta.get("kind") or "unknown"
    intent = meta.get("intentKind")
    if intent and intent != kind:
        defects.append({
            "code": "GUI-PAGE-KIND-001",
            "severity": "error",
            "message": f"intent kind {intent} but observed/declared {kind}",
        })

    fonts = int(counts.get("fontFamilies") or 0)
    colors = int(counts.get("colors") or 0)
    sizes = int(counts.get("fontSizes") or 0)
    if fonts > int(budgets.get("fontFamilies") or 3):
        defects.append({
            "code": "GUI-VIS-FONT-001",
            "severity": "warn",
            "message": f"{fonts} font families (budget {budgets.get('fontFamilies')})",
        })
    if colors > int(budgets.get("colors") or 16):
        defects.append({
            "code": "GUI-VIS-COLOR-001",
            "severity": "warn",
            "message": f"{colors} unique colors (budget {budgets.get('colors')})",
        })
    if sizes > int(budgets.get("fontSizes") or 8):
        defects.append({
            "code": "GUI-VIS-TYPE-001",
            "severity": "warn",
            "message": f"{sizes} font sizes (budget {budgets.get('fontSizes')})",
        })

    if not landmarks.get("footer"):
        defects.append({
            "code": "GUI-VIS-STRUCT-002",
            "severity": "error",
            "message": "missing footer.footer",
        })
    if not landmarks.get("h1"):
        defects.append({
            "code": "GUI-VIS-STRUCT-003",
            "severity": "info",
            "message": "no H1 heading",
        })
    if landmarks.get("main") is False:
        defects.append({
            "code": "GUI-VIS-STRUCT-004",
            "severity": "error",
            "message": "missing main landmark",
        })
    if kind == "article" and not landmarks.get("article"):
        defects.append({
            "code": "GUI-VIS-STRUCT-005",
            "severity": "warn",
            "message": "kind=article missing article landmark",
        })
    applies = page.get("appliesPrinciples") or []
    if "heading-outline" in applies:
        outline = landmarks.get("headingOutline") or []
        tags = {
            str(row.get("tag") or "").upper()
            for row in outline
            if isinstance(row, dict)
        }
        if tags and "H1" in tags and "H2" not in tags:
            defects.append({
                "code": "GUI-VIS-STRUCT-006",
                "severity": "warn",
                "message": "heading outline has H1 but no H2",
            })

    needs_chrome = kind == "panel" or intent == "panel"
    if needs_chrome and not chrome.get("itemSectionToolbar"):
        defects.append({
            "code": "GUI-PAGE-CHROME-001",
            "severity": "error",
            "message": "panel chrome missing .item-section-toolbar",
        })
    return defects


def build_page(
    *,
    url: str,
    title: str,
    structure: dict[str, Any],
    tokens: dict[str, Any],
    source: str,
    intent_kind: str | None = None,
    page_id: str | None = None,
    placement: dict[str, Any] | None = None,
    profiles: dict[str, Any] | None = None,
) -> dict[str, Any]:
    profiles = profiles or page_profiles()
    kind = infer_kind(url, title, structure)
    profile = profiles.get(kind) or profiles["unknown"]
    budgets = profile["visualBudgets"]
    counts = {
        "fontFamilies": int(tokens.get("fontFamilyCount") or 0),
        "colors": int(tokens.get("colorCount") or 0),
        "fontSizes": int(tokens.get("fontSizeCount") or 0),
    }
    applies = list(profile.get("appliesPrinciples") or [])
    page = {
        "schema": PAGE_SCHEMA,
        "$schema": "https://wellmanifest.com/schemas/gui-page/v1",
        "id": page_id or f"observed/{_slug_from_url(url, kind)}",
        "version": PACK_VERSION,
        "title": title or kind,
        "placement": placement or {
            "home": "subactor",
            "shape": "runtime_service",
            "adopt": "wellmanifest/gui",
            "runtimeOwner": "subactor",
        },
        "page": {
            "kind": kind,
            "role": ROLE.get(kind, "public"),
            "source": source,
            "url": url,
            "family": FAMILY.get(kind, "marketing"),
        },
        "structure": structure,
        "visual": {
            "budgets": {
                "fontFamilies": int(budgets["fontFamilies"]),
                "colors": int(budgets["colors"]),
                "fontSizes": int(budgets["fontSizes"]),
            },
            "counts": counts,
            "tokens": {
                "fontFamilies": list(tokens.get("fonts") or []),
                "colors": list(tokens.get("colors") or []),
                "fontSizes": list(tokens.get("fontSizes") or []),
            },
        },
        "appliesPrinciples": applies,
    }
    if intent_kind:
        page["page"]["intentKind"] = intent_kind
    page["defects"] = defects_for_page(page)
    return page


def compare_pages(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    lp, rp = left.get("page") or {}, right.get("page") or {}
    lk, rk = lp.get("kind"), rp.get("kind")
    li, ri = lp.get("intentKind"), rp.get("intentKind")
    same_url = bool(lp.get("url") and lp.get("url") == rp.get("url"))
    intent_fail = bool((li and li != lk) or (ri and ri != rk))
    defects: list[dict[str, Any]] = []
    if same_url and intent_fail:
        comparable = "intent-mismatch"
        reason = "Intent kind does not match observed/declared kind."
        defects.append({
            "code": "GUI-PAGE-KIND-001",
            "severity": "error",
            "message": reason,
        })
    elif lk != rk:
        comparable = "cross-kind"
        reason = f"Different page.kind ({lk} vs {rk}) — do not treat as same-surface drift."
    else:
        comparable = "same-kind"
        reason = "Same page.kind — visual deltas are same-surface drift."
    if lk != rk:
        defects.append({
            "code": "GUI-PAGE-KIND-002",
            "severity": "warn",
            "message": f"Different page.kind ({lk} vs {rk}) — do not treat as same-surface drift.",
        })

    lt = (left.get("visual") or {}).get("counts") or {}
    rt = (right.get("visual") or {}).get("counts") or {}
    ls = (left.get("structure") or {}).get("chrome") or {}
    rs = (right.get("structure") or {}).get("chrome") or {}
    deltas: list[dict[str, Any]] = []
    for key, kind in (
        ("fontFamilies", "font-families"),
        ("colors", "colors"),
        ("fontSizes", "font-sizes"),
    ):
        lv, rv = int(lt.get(key) or 0), int(rt.get(key) or 0)
        if lv != rv:
            deltas.append({"kind": kind, "left": lv, "right": rv, "delta": rv - lv})
    for key in (
        "itemSectionToolbar",
        "itemViewSwitch",
        "sectionAddButton",
        "viewport",
    ):
        if bool(ls.get(key)) != bool(rs.get(key)):
            deltas.append({
                "kind": f"structure.{key}",
                "left": bool(ls.get(key)),
                "right": bool(rs.get(key)),
            })
    if ((left.get("page") or {}).get("kind") != (right.get("page") or {}).get("kind")):
        deltas.append({
            "kind": "page.kind",
            "left": lk,
            "right": rk,
        })
    return {
        "schema": COMPARE_SCHEMA,
        "$schema": "https://wellmanifest.com/schemas/gui-page-compare/v1",
        "id": f"compare/{(left.get('id') or 'left').replace('/', '-')}-vs-{(right.get('id') or 'right').replace('/', '-')}",
        "version": PACK_VERSION,
        "placement": {
            "home": "wellmanifest",
            "shape": "domain_pack",
            "adopt": "wellmanifest/gui",
        },
        "left": {
            "id": left.get("id"),
            "kind": lk,
            "intentKind": li,
            "title": left.get("title"),
            "url": (left.get("page") or {}).get("url"),
            "source": (left.get("page") or {}).get("source"),
        },
        "right": {
            "id": right.get("id"),
            "kind": rk,
            "intentKind": ri,
            "title": right.get("title"),
            "url": (right.get("page") or {}).get("url"),
            "source": (right.get("page") or {}).get("source"),
        },
        "comparable": comparable,
        "reason": reason,
        "deltas": deltas,
        "defects": defects,
        "notes": [
            "Compare kind first, then landmarks, then token budgets.",
            "Colors/fonts HOME stays wellmanifest/brand + product brand — this is observed evidence.",
            "Panel collections still use wellmanifest.gui/dsl/v1 surfaces.",
        ],
    }
