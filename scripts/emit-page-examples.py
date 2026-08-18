#!/usr/bin/env python3
"""Emit checked-in wellmanifest.gui/page/v1 examples from last live probes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gui_page import PACK_VERSION, build_page, compare_pages, page_profiles

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "pages"
PLACEMENT = {
    "home": "subactor",
    "shape": "runtime_service",
    "adopt": "wellmanifest/gui",
    "runtimeOwner": "subactor",
}


def dump(name: str, data: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def declared_shell(kind: str, page_id: str, title: str, url: str, extra_landmarks: dict, chrome: dict) -> dict:
    profiles = page_profiles()
    profile = profiles[kind]
    return {
        "schema": "wellmanifest.gui/page/v1",
        "$schema": "https://wellmanifest.com/schemas/gui-page/v1",
        "id": page_id,
        "version": PACK_VERSION,
        "title": title,
        "placement": PLACEMENT,
        "page": {
            "kind": kind,
            "intentKind": kind,
            "role": profile["role"],
            "source": "declared",
            "url": url,
            "family": profile["family"],
        },
        "structure": {
            "landmarks": {
                "main": True,
                "footer": kind != "auth",
                "h1": title,
                "form": kind in {"form", "auth"},
                "article": kind == "article",
                "listing": kind == "marketplace",
                "headingOutline": [{"tag": "H1", "text": title}],
                **extra_landmarks,
            },
            "chrome": chrome,
        },
        "visual": {
            "budgets": profile["visualBudgets"],
            "counts": {"fontFamilies": 0, "colors": 0, "fontSizes": 0},
            "tokens": {"fontFamilies": [], "colors": [], "fontSizes": []},
        },
        "defects": [],
        "appliesPrinciples": profile["appliesPrinciples"],
    }


def main() -> int:
    probe1 = json.loads((ROOT / "examples/probes/visual-probe-1.json").read_text())
    probe2 = json.loads((ROOT / "examples/probes/visual-probe-2.json").read_text())

    def structure_from_legacy(raw: dict) -> dict:
        s = raw.get("structure") or {}
        headings = s.get("headings") or []
        h1 = next((h["text"] for h in headings if h.get("tag") == "H1"), None)
        return {
            "landmarks": {
                "main": bool(s.get("main")),
                "footer": bool(s.get("siteFooter")),
                "h1": h1,
                "form": False,
                "article": False,
                "listing": "marketplace" in (raw.get("url") or ""),
                "headingOutline": headings,
            },
            "chrome": {
                "itemSectionToolbar": bool(s.get("itemSectionToolbar")),
                "itemViewSwitch": bool(s.get("itemViewSwitch")),
                "sectionAddButton": bool(s.get("sectionAddButton")),
                "sectionViewToolbar": bool(s.get("sectionViewToolbar")),
                "viewport": bool(s.get("viewport")),
                "itemView": bool(s.get("itemView")),
                "hamburger": bool(s.get("hamburger")),
            },
        }

    marketplace = build_page(
        url=probe1["url"],
        title=probe1["title"],
        structure=structure_from_legacy(probe1),
        tokens=probe1["tokens"],
        source="observed",
        intent_kind="marketplace",
        page_id="subactor.www/marketplace",
        placement=PLACEMENT,
    )
    landing = build_page(
        url=probe2["url"],
        title=probe2["title"],
        structure=structure_from_legacy(probe2),
        tokens=probe2["tokens"],
        source="observed",
        intent_kind="panel",
        page_id="subactor.www/observed-contact-url",
        placement=PLACEMENT,
    )

    empty_chrome = {
        "itemSectionToolbar": False,
        "itemViewSwitch": False,
        "sectionAddButton": False,
        "sectionViewToolbar": False,
        "viewport": False,
        "itemView": False,
        "hamburger": False,
    }
    panel_chrome = {
        **empty_chrome,
        "itemSectionToolbar": True,
        "itemViewSwitch": True,
        "sectionAddButton": True,
        "sectionViewToolbar": True,
        "viewport": True,
        "itemView": True,
        "hamburger": True,
    }
    declared_panel = declared_shell(
        "panel",
        "subactor.www/panel.contact",
        "Kontakty",
        "http://127.0.0.1:8781/?action=contact&viewport=pc&item_view=table&lang=pl&currency=PLN&theme=dark&organization=info-softreck",
        {},
        panel_chrome,
    )
    declared_form = declared_shell(
        "form",
        "example.product/contact-form",
        "Kontakt",
        "https://example.test/contact",
        {},
        empty_chrome,
    )
    declared_article = declared_shell(
        "article",
        "example.product/legal-privacy",
        "Polityka prywatności",
        "https://example.test/legal/privacy",
        {},
        empty_chrome,
    )

    dump("observed-marketplace.page.json", marketplace)
    dump("observed-landing.page.json", landing)
    dump("declared-panel-contact.page.json", declared_panel)
    dump("declared-form.page.json", declared_form)
    dump("declared-article.page.json", declared_article)
    dump("compare-marketplace-landing.json", compare_pages(marketplace, landing))
    dump("compare-intent-contact.json", compare_pages(declared_panel, landing))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
