#!/usr/bin/env python3
"""Observe live pages into wellmanifest.gui/page/v1 (propose-only, no runtime)."""

from __future__ import annotations

import argparse
import asyncio
import json
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websockets

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gui_page import build_page, compare_pages

EXTRACT_JS = r"""
() => {
  const nodes = Array.from(document.querySelectorAll("body *")).slice(0, 5000);
  const fonts = new Map();
  const colors = new Map();
  const sizes = new Map();
  for (const el of nodes) {
    const s = getComputedStyle(el);
    if (s.display === "none" || s.visibility === "hidden") continue;
    const ff = (s.fontFamily || "").split(",")[0].replace(/['"]/g, "").trim();
    if (ff) fonts.set(ff, (fonts.get(ff) || 0) + 1);
    for (const prop of ["color", "backgroundColor", "borderTopColor"]) {
      const c = s[prop];
      if (!c || c === "rgba(0, 0, 0, 0)" || c === "transparent") continue;
      colors.set(c, (colors.get(c) || 0) + 1);
    }
    if (s.fontSize) sizes.set(s.fontSize, (sizes.get(s.fontSize) || 0) + 1);
  }
  const pick = (m, n) => Array.from(m.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([value, count]) => ({ value, count }));
  const sel = (q) => Boolean(document.querySelector(q));
  const headings = Array.from(document.querySelectorAll("h1,h2,h3"))
    .slice(0, 16)
    .map((h) => ({ tag: h.tagName, text: (h.textContent || "").trim().slice(0, 80) }));
  const h1 = headings.find((h) => h.tag === "H1");
  return {
    title: document.title,
    url: location.href,
    structure: {
      landmarks: {
        main: sel("main, [role=main], #root"),
        footer: sel("footer.footer"),
        h1: h1 ? h1.text : null,
        form: sel("form"),
        article: sel("article"),
        listing: sel("[data-listing], .marketplace-grid, .partner-list, .catalog-list"),
        headingOutline: headings,
      },
      chrome: {
        itemSectionToolbar: sel(".item-section-toolbar"),
        itemViewSwitch: sel(".item-view-switch"),
        sectionAddButton: sel(".section-add-button"),
        sectionViewToolbar: sel(".section-view-toolbar"),
        viewport: sel("#global-viewport"),
        itemView: sel("#global-item-view"),
        hamburger: sel(".mobile-menu-toggle"),
      },
    },
    tokens: {
      fonts: pick(fonts, 8),
      fontFamilyCount: fonts.size,
      colors: pick(colors, 16),
      colorCount: colors.size,
      fontSizes: pick(sizes, 10),
      fontSizeCount: sizes.size,
    },
  };
}
"""


def free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def wait_json(url: str, timeout: float = 15.0, method: str = "GET") -> dict:
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            req = urllib.request.Request(url, method=method)
            with urllib.request.urlopen(req, timeout=2) as resp:
                return json.loads(resp.read().decode())
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(0.2)
    raise RuntimeError(f"CDP not ready at {url}: {last}")


async def cdp_extract(ws_url: str, page_url: str) -> dict:
    async with websockets.connect(ws_url, max_size=8_000_000) as ws:
        msg_id = 0

        async def send(method: str, params: dict | None = None) -> dict:
            nonlocal msg_id
            msg_id += 1
            await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                raw = json.loads(await ws.recv())
                if raw.get("id") == msg_id:
                    if "error" in raw:
                        raise RuntimeError(raw["error"])
                    return raw.get("result") or {}

        await send("Page.enable")
        await send("Runtime.enable")
        await send("Page.navigate", {"url": page_url})
        deadline = time.time() + 12
        while time.time() < deadline:
            try:
                raw = json.loads(await asyncio.wait_for(ws.recv(), timeout=1.0))
            except TimeoutError:
                continue
            if raw.get("method") in {"Page.loadEventFired", "Page.domContentEventFired"}:
                break
        await asyncio.sleep(1.5)
        result = await send(
            "Runtime.evaluate",
            {"expression": f"({EXTRACT_JS})()", "returnByValue": True, "awaitPromise": True},
        )
        value = (result.get("result") or {}).get("value")
        if not isinstance(value, dict):
            raise RuntimeError(f"evaluate returned {result!r}")
        return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe live pages into gui page DSL")
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--chrome", default="google-chrome")
    parser.add_argument(
        "--intents",
        default="",
        help="Comma-separated page kinds aligned to URL order (e.g. marketplace,panel)",
    )
    args = parser.parse_args()
    intents = [part.strip() or None for part in args.intents.split(",")] if args.intents else []

    port = free_port()
    user_dir = Path("/tmp/wellmanifest-gui-probe-chrome")
    user_dir.mkdir(parents=True, exist_ok=True)
    chrome = subprocess.Popen(
        [
            args.chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--remote-allow-origins=*",
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_dir}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_json(f"http://127.0.0.1:{port}/json/version")
        pages = []
        for idx, url in enumerate(args.urls):
            tab = wait_json(
                f"http://127.0.0.1:{port}/json/new?{urllib.parse.quote(url, safe='')}",
                method="PUT",
            )
            raw = asyncio.run(cdp_extract(tab["webSocketDebuggerUrl"], url))
            intent = intents[idx] if idx < len(intents) else None
            page = build_page(
                url=raw.get("url") or url,
                title=raw.get("title") or "",
                structure=raw.get("structure") or {},
                tokens=raw.get("tokens") or {},
                source="observed",
                intent_kind=intent,
            )
            pages.append(page)
            print(json.dumps(page, ensure_ascii=False, indent=2))
        if len(pages) >= 2:
            print(json.dumps(compare_pages(pages[0], pages[1]), ensure_ascii=False, indent=2))
        if args.out_dir:
            out = Path(args.out_dir)
            out.mkdir(parents=True, exist_ok=True)
            for idx, page in enumerate(pages):
                (out / f"observed-{idx + 1}.page.json").write_text(
                    json.dumps(page, ensure_ascii=False, indent=2) + "\n"
                )
            if len(pages) >= 2:
                (out / "compare.json").write_text(
                    json.dumps(compare_pages(pages[0], pages[1]), ensure_ascii=False, indent=2) + "\n"
                )
            print(f"wrote {out}", file=sys.stderr)
    finally:
        chrome.terminate()
        try:
            chrome.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
