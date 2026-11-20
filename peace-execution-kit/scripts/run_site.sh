#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
port="${1:-8080}"

echo "Serving Peace Execution Kit on port ${port}"
echo "Open: http://localhost:${port}/"
python3 -m http.server "${port}"

