#!/usr/bin/env bash
# Tile every scene still into one contact sheet for review — a strip of
# thumbnails is how a human catches the one off-model frame in seconds.
#
#   contact_sheet.sh <ad-folder>
set -euo pipefail

DIR="$1"
COUNT=$(ls "$DIR/stills"/scene-*.png 2>/dev/null | wc -l | tr -d ' ')
[ "$COUNT" -gt 0 ] || { echo "No stills in $DIR/stills yet." >&2; exit 1; }
COLS=$(( COUNT >= 5 ? 5 : COUNT ))
ROWS=$(( (COUNT + COLS - 1) / COLS ))
ffmpeg -y -v error -pattern_type glob -i "$DIR/stills/scene-*.png" \
  -filter_complex "scale=270:480,tile=${COLS}x${ROWS}:padding=8:color=white" \
  -frames:v 1 "$DIR/contact-sheet.png"
echo "$DIR/contact-sheet.png"
