#!/usr/bin/env bash
set -euo pipefail

deck_dir="${1:?Usage: export_decktape_pdf.sh <deck-dir> <qmd-file> <output-pdf> [size] [port]}"
qmd_file="${2:?Usage: export_decktape_pdf.sh <deck-dir> <qmd-file> <output-pdf> [size] [port]}"
output_pdf="${3:?Usage: export_decktape_pdf.sh <deck-dir> <qmd-file> <output-pdf> [size] [port]}"
size="${4:-1280x720}"
port="${5:-8765}"

if ! command -v quarto >/dev/null 2>&1; then
  echo "quarto not found on PATH" >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx not found on PATH; install Node.js/npm first" >&2
  exit 1
fi

abs_deck_dir="$(cd "$deck_dir" && pwd)"
qmd_path="$abs_deck_dir/$qmd_file"
output_path="$abs_deck_dir/$output_pdf"

quarto render "$qmd_path"

python3 -m http.server "$port" --directory "$abs_deck_dir" >/tmp/quarto-revealjs-pdf-server.log 2>&1 &
server_pid="$!"
cleanup() {
  kill "$server_pid" >/dev/null 2>&1 || true
}
trap cleanup EXIT

sleep 1
npx --yes decktape reveal --size "$size" --pause 1200 --load-pause 2500 \
  "http://127.0.0.1:$port/index.html" "$output_path"

echo "Wrote $output_path"
