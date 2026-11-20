#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

port="${1:-8080}"

echo "Starting local static server for sim-lab on port ${port}"
echo "Open:"
echo "  http://localhost:${port}/sim-lab/atoms/"
echo "  http://localhost:${port}/sim-lab/engine/"
echo
python3 -m http.server "${port}"

