#!/usr/bin/env python3
"""Write docs/src/palette.html from colors.toml so the specimen cannot drift."""

import html
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = tomllib.loads((ROOT / "colors.toml").read_text(encoding="utf-8"))
OUT = ROOT / "docs" / "src" / "palette.html"

SECTIONS = [
    (
        "Surfaces",
        [
            ("darker_background", "dusty stone"),
            ("dark_background", "soft stone"),
            ("background", "stone"),
            ("lighter_background", "pale paper"),
            ("selection", "petal wash"),
        ],
    ),
    (
        "Text",
        [
            ("dark_foreground", "bark"),
            ("foreground", "blossom heart"),
            ("light_foreground", "rose"),
            ("bright_foreground", "deep heart"),
        ],
    ),
    (
        "Jewelry",
        [
            ("accent", "faded pink"),
            ("cursor", "snow"),
            ("blue", "sky"),
            ("cyan", "mist"),
        ],
    ),
    (
        "Warm scale",
        [
            ("red", "petal crimson"),
            ("bright_red", "bright crimson"),
            ("brown", "bark"),
            ("orange", "clay"),
            ("yellow", "pollen"),
            ("bright_yellow", "bright pollen"),
        ],
    ),
    (
        "Cool scale",
        [
            ("green", "moss"),
            ("bright_green", "bright moss"),
            ("magenta", "sakura"),
            ("bright_magenta", "faded pink"),
        ],
    ),
]


def chip(key: str, role: str | None) -> str:
    value = COLORS[key]
    role_html = f'<p class="role">{html.escape(role)}</p>' if role else ""
    return (
        '<article class="card">'
        f'<p class="key">{html.escape(key)}</p>'
        f'<div class="chip" style="background:{html.escape(value)}"></div>'
        f'<p class="hex">{html.escape(value)}</p>'
        f"{role_html}"
        "</article>"
    )


def section(title: str, items: list[tuple[str, str]], columns: int) -> str:
    cards = "\n".join(chip(key, role) for key, role in items)
    return (
        f'<section><h2>{html.escape(title)}</h2>'
        f'<div class="grid" style="grid-template-columns:repeat({columns}, 1fr)">'
        f"{cards}</div></section>"
    )


def ansi_rows() -> str:
    cards = "\n".join(chip(f"color{i}", None) for i in range(16))
    return (
        "<section><h2>ANSI 0–15</h2>"
        '<div class="grid ansi" style="grid-template-columns:repeat(8, 1fr)">'
        f"{cards}</div></section>"
    )


def main() -> None:
    accent = COLORS["accent"]
    snow = COLORS["cursor"]
    stone = COLORS["background"]
    heart = COLORS["foreground"]
    muted = COLORS["muted"]
    paper = COLORS["lighter_background"]
    sky = COLORS["blue"]
    parts = [
        section("Surfaces", SECTIONS[0][1], 5),
        section("Text", SECTIONS[1][1], 4),
        section("Jewelry", SECTIONS[2][1], 4),
        section("Warm scale", SECTIONS[3][1], 6),
        section("Cool scale", SECTIONS[4][1], 4),
        ansi_rows(),
    ]
    body = "\n".join(parts)
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Cherry Blossom Day palette</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: {html.escape(stone)}; }}
  .sheet {{
    width: 1280px;
    background: {html.escape(stone)};
    color: {html.escape(heart)};
    padding: 48px 48px 40px;
    font-family: "Noto Sans", "Liberation Sans", sans-serif;
  }}
  header {{ margin-bottom: 28px; }}
  .eyebrow {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.42em;
    color: {html.escape(muted)};
  }}
  h1 {{
    margin-top: 10px;
    font-family: "Noto Serif", "Liberation Serif", serif;
    font-size: 48px;
    font-weight: 560;
    letter-spacing: 0.06em;
    color: {html.escape(heart)};
  }}
  .lede {{
    margin-top: 10px;
    max-width: 780px;
    font-family: "Noto Serif", "Liberation Serif", serif;
    font-size: 18px;
    line-height: 1.45;
    color: {html.escape(COLORS["light_foreground"])};
  }}
  section {{ margin-top: 26px; }}
  h2 {{
    margin-bottom: 12px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: {html.escape(accent)};
  }}
  .grid {{ display: grid; gap: 14px 12px; }}
  .card {{ min-width: 0; }}
  .key {{
    font-family: "Liberation Mono", monospace;
    font-size: 12px;
    letter-spacing: 0.01em;
    color: {html.escape(COLORS["light_foreground"])};
    white-space: nowrap;
  }}
  .chip {{
    margin-top: 6px;
    height: 48px;
    border-radius: 3px;
    box-shadow: inset 0 0 0 1px rgba(110, 36, 56, 0.12);
  }}
  .hex {{
    margin-top: 6px;
    font-family: "Liberation Mono", monospace;
    font-size: 13px;
    letter-spacing: 0.04em;
    color: {html.escape(heart)};
  }}
  .role {{
    margin-top: 2px;
    font-size: 12px;
    color: {html.escape(muted)};
  }}
  .ansi .chip {{ height: 36px; }}
  footer {{
    margin-top: 28px;
    padding-top: 16px;
    border-top: 1px solid {html.escape(COLORS["dark_background"])};
    font-family: "Liberation Mono", monospace;
    font-size: 13px;
    line-height: 1.5;
    color: {html.escape(muted)};
  }}
  footer b {{ color: {html.escape(accent)}; font-weight: 500; }}
  .end {{
    margin-top: 22px;
    height: 4px;
    background: linear-gradient(90deg, {html.escape(accent)}, {html.escape(sky)}, {html.escape(snow)});
  }}
</style>
</head>
<body>
  <div class="sheet">
    <header>
      <p class="eyebrow">COLORS.TOML</p>
      <h1>Palette</h1>
      <p class="lede">Ground is dusty stone. Accent is faded pink. Body text is blossom heart. Focus jewelry is snow. Pink lives in the jewelry, never the floor.</p>
    </header>
    {body}
    <footer>
      accent, bright_magenta, and color13 are <b>{html.escape(accent)}</b>.
      cursor and hyprland_active_border are <b>{html.escape(snow)}</b>.
      mode is light. icons are Yaru-magenta.
    </footer>
    <div class="end"></div>
  </div>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(document, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
