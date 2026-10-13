#!/usr/bin/env python3
"""Check colors.toml against the Omarchy palette contract and this theme's links."""

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")

REQUIRED = [
    "mode",
    "accent",
    "cursor",
    "selection",
    "muted",
    "background",
    "dark_background",
    "darker_background",
    "lighter_background",
    "foreground",
    "dark_foreground",
    "light_foreground",
    "bright_foreground",
    "selection_foreground",
    "selection_background",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "orange",
    "brown",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "hyprland_active_border",
    *[f"color{index}" for index in range(16)],
]

SAME = (
    ("accent", "bright_magenta"),
    ("accent", "color13"),
    ("cursor", "hyprland_active_border"),
    ("selection", "selection_background"),
    ("foreground", "color7"),
    ("bright_foreground", "color15"),
    ("darker_background", "color0"),
    ("muted", "color8"),
    ("red", "color1"),
    ("green", "color2"),
    ("yellow", "color3"),
    ("blue", "color4"),
    ("magenta", "color5"),
    ("cyan", "color6"),
    ("bright_red", "color9"),
    ("bright_green", "color10"),
    ("bright_yellow", "color11"),
    ("bright_blue", "color12"),
    ("bright_cyan", "color14"),
)

SNOW = "#FAF6F3"


def fail(message: str) -> None:
    print(f"palette: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    path = ROOT / "colors.toml"
    colors = tomllib.loads(path.read_text(encoding="utf-8"))
    missing = [key for key in REQUIRED if key not in colors]
    if missing:
        fail("missing keys: " + ", ".join(missing))
    if colors["mode"] != "light":
        fail(f"mode is {colors['mode']!r}, expected light")
    for key in REQUIRED:
        if key == "mode":
            continue
        value = colors[key]
        if not isinstance(value, str) or not HEX.match(value):
            fail(f"{key} is not a #RRGGBB color: {value!r}")
    for left, right in SAME:
        if colors[left].lower() != colors[right].lower():
            fail(f"{left} {colors[left]} and {right} {colors[right]} should match")
    if colors["cursor"].lower() != SNOW.lower():
        fail(f"cursor {colors['cursor']} should be snow {SNOW}")
    print(f"palette ok ({len(REQUIRED) - 1} colors, accent {colors['accent']})")


if __name__ == "__main__":
    main()
