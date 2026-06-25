#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$ROOT_DIR/scripts/validate_agent_policy.py" "$ROOT_DIR/templates/agent-policy.example.json"

echo "Validation complete"
