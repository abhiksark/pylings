#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="$repo_root/docs/assets/demos"
vhs_bin="${VHS_BIN:-vhs}"

if ! command -v "$vhs_bin" >/dev/null 2>&1; then
  cat >&2 <<'EOF'
vhs is required to generate the demo GIF.

Install it with:
  brew install charmbracelet/tap/vhs

Then run:
  scripts/generate_demo_gif.sh

To use a specific binary:
  VHS_BIN=/path/to/vhs scripts/generate_demo_gif.sh
EOF
  exit 127
fi

mkdir -p "$output_dir"
rm -rf /tmp/pylings-demo
cd "$repo_root"
"$vhs_bin" docs/demo.tape
