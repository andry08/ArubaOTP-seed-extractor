#!/usr/bin/env bash
#
# Default launcher for ArubaOTP-seed-extractor.
#
# It installs the pinned dependencies into an isolated environment and runs the
# tool in a single step. The only prerequisite is uv: https://docs.astral.sh/uv/
#
# Usage (same arguments as scripts/main.py):
#   ./launch.sh extract <validation_code> -q
#   ./launch.sh generate -s <seed>
#   ./launch.sh printqr
#
set -euo pipefail

# Resolve the directory of this script so it works from any current directory
# (seed.json keeps living next to the scripts, since sys.path[0] is unchanged).
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec uv run --project "$DIR" python "$DIR/scripts/main.py" "$@"
