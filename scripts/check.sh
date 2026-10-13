#!/usr/bin/env bash
# Validate the theme palette, plates, and wallpaper set.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/check_palette.py

required=(
  colors.toml
  icons.theme
  preview.png
  backgrounds/1-hanami-path.jpg
  backgrounds/2-hillside-picnic.jpg
  backgrounds/3-ukiyoe-avenue.jpg
  backgrounds/4-swirl-buck-sakura.jpg
  backgrounds/5-shotengai-90s.jpg
  backgrounds/6-station-street-90s.jpg
  backgrounds/7-wordmark.jpg
  backgrounds/8-omarchy-emblem.jpg
  backgrounds/9-omarchy-pixel.jpg
  backgrounds/10-omarchy-tategaki.jpg
  docs/banner.png
  docs/palette.png
  README.md
  LICENSE
)
for path in "${required[@]}"; do
  if [[ ! -s $path ]]; then
    echo "missing $path" >&2
    exit 1
  fi
done

if [[ "$(tr -d '[:space:]' < icons.theme)" != "Yaru-magenta" ]]; then
  echo "icons.theme should name Yaru-magenta" >&2
  exit 1
fi

if [[ ! -e light.mode ]]; then
  echo "missing light.mode" >&2
  exit 1
fi
if [[ -s light.mode ]]; then
  echo "light.mode should be empty" >&2
  exit 1
fi

expect_size() {
  local path="$1"
  local want="$2"
  local got
  got="$(magick identify -format '%wx%h' "$path")"
  if [[ "$got" != "$want" ]]; then
    echo "$path is $got, expected $want" >&2
    exit 1
  fi
}

expect_size docs/banner.png 1600x680
expect_size preview.png 1168x784

palette_size="$(magick identify -format '%wx%h' docs/palette.png)"
if [[ "$palette_size" != 1280x* ]]; then
  echo "docs/palette.png is $palette_size, expected width 1280" >&2
  exit 1
fi

for image in preview.png docs/banner.png docs/palette.png backgrounds/*.jpg; do
  magick identify "$image" >/dev/null
done

echo "cherry-blossom-day check ok"
