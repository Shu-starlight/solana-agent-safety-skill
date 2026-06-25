#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_ROOT="$HOME/.claude/skills"
YES=false

usage() {
  cat <<'EOF'
Solana Agent Safety Skill installer

Usage:
  ./install.sh [-y|--yes] [--path PATH]

Options:
  -y, --yes      Skip confirmation prompt
  --path PATH    Install under PATH instead of ~/.claude/skills
  -h, --help     Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes)
      YES=true
      shift
      ;;
    --path)
      DEST_ROOT="${2:?--path requires a value}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

DEST_DIR="$DEST_ROOT/solana-agent-safety"

echo "Installing solana-agent-safety skill"
echo "Source: $ROOT_DIR/skill"
echo "Target: $DEST_DIR"

if [[ "$YES" != true ]]; then
  read -r -p "Proceed? [Y/n] " reply
  case "$reply" in
    n|N|no|NO)
      echo "Installation cancelled"
      exit 0
      ;;
  esac
fi

mkdir -p "$DEST_ROOT"
rm -rf "$DEST_DIR"
mkdir -p "$DEST_DIR"
cp -R "$ROOT_DIR/skill/." "$DEST_DIR/"

echo "Installed to $DEST_DIR"
echo "Try: Use solana-agent-safety to review this Solana agent transaction pipeline."
