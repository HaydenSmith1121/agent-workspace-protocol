#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INSTALLER="$SCRIPT_DIR/skill/agent-workspace-protocol/scripts/install.py"

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  printf '%s\n' "Python 3 is required. Install Python and ensure python3 is on PATH." >&2
  exit 1
fi

exec "$PYTHON" "$INSTALLER" "$@"
