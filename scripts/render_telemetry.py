#!/usr/bin/env python3
"""Render the normalized profile snapshot into a committed static telemetry SVG."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "config" / "profile-data.json"
OUTPUT = ROOT / "assets" / "telemetry" / "github-telemetry.svg"

VOID = "#0A0A12"
DARK = "#12121F"
PANEL = "#1A1A2E"
GHOST = "#E8E8F0"
SOFT = "#A0A0B8"
CYAN = "#00F0FF"
GREEN = "#39FF14"
EDGE = "#2A2A3D"


def esc(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def metric_card(x: int, y: int, width: int, label: str, value: object, accent: str) -> str:
    return f'''<g>
  <rect x="{x}" y="{y}" width="{width}" height="72" rx="2" fill="{PANEL}" stroke="{EDGE}"/>
  <rect x="{x}" y="{y}" width="4" height="72" fill="{accent}"/>
  <text x="{x + 16}" y="{y + 23}" class="label">{esc(label)}</text>
  <text x="{x + 16}" y="{y + 54}" class="value" fill="{accent}">{esc(value)}</text>
</g>'''


def main() -> None:
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    metrics = data["metrics"]
    width, height = 960, 278
    cards = [
        ("REPOSITORIES", metrics["repositories"], CYAN),
        ("LANGUAGES", metrics["languages"], CYAN),
        ("CONTRIBUTIONS", metrics["contributions"], GREEN),
        ("COMMITS", metrics["commits"], GREEN),
        ("PULL REQUESTS", metrics["pull_requests"], GREEN),
        ("ISSUES", metrics["issues"], GREEN),
        ("STARS", metrics["stars"], GREEN),
    ]
    margin, gap = 24, 12
    card_width = (width - margin * 2 - gap * 3) // 4
    parts = [
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">GitHub telemetry for {esc(data["login"])}</title>
<desc id="desc">A generated static dashboard showing repositories, languages, contributions, commits, pull requests, issues, and stars.</desc>
<rect width="{width}" height="{height}" fill="{VOID}"/>
<rect x="10" y="10" width="{width - 20}" height="{height - 20}" rx="3" fill="{DARK}" stroke="{CYAN}" stroke-width="1"/>
<path d="M10 48H950M24 246H936" stroke="{EDGE}"/>
<path d="M24 48H194" stroke="{CYAN}" stroke-width="2"/>
<text x="24" y="36" class="title">[04] GITHUB.TELEMETRY</text>
<text x="936" y="36" text-anchor="end" class="meta">SNAPSHOT // {esc(data["generated_at"][:10])}</text>
<style>
.title {{ fill:{GHOST}; font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:20px; font-weight:700; letter-spacing:1px; }}
.meta {{ fill:{SOFT}; font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:12px; letter-spacing:.5px; }}
.label {{ fill:{SOFT}; font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:11px; letter-spacing:1px; }}
.value {{ font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:28px; font-weight:700; }}
.footer {{ fill:{SOFT}; font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:11px; letter-spacing:.5px; }}
</style>'''
    ]
    for index, (label, value, accent) in enumerate(cards):
        row, col = divmod(index, 4)
        x = margin + col * (card_width + gap)
        y = 66 + row * 84
        parts.append(metric_card(x, y, card_width, label, value, accent))
    parts.append(
        f'<text x="24" y="266" class="footer">SOURCE: AUTHENTICATED GITHUB GRAPHQL // WINDOW: LAST 365 DAYS // GENERATED ASSET</text>'
    )
    parts.append("</svg>\n")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
