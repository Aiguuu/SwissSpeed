#!/usr/bin/env bash
set -euo pipefail

# Move to project root (script dir/..)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

if [ ! -d .venv ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip

if [ -f pyproject.toml ]; then
  echo "Installing package in editable mode..."
  python -m pip install -e .
else
  python -m pip install -r requirements.txt
fi

echo "Setup complete."

if [ "${1:-}" = "--run" ]; then
  if command -v map-ui >/dev/null 2>&1; then
    exec map-ui
  else
    exec python UI.py
  fi
fi
