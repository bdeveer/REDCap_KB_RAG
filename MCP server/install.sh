#!/bin/bash
# REDCap MCP Server — one-time setup script
#
# Usage:
#   1. Fill in your REDCap API URLs below (remove any you don't need)
#   2. Run:  bash install.sh
#
# Works with the Claude desktop app (Cowork) — no Claude Code CLI needed.
# After running, fully quit and relaunch Claude for the servers to appear.

set -e

# ── CONFIGURE THESE ───────────────────────────────────────────────────────────
REDCAP_URL_PROD="https://redcap.school.wakehealth.edu/api/"
REDCAP_URL_TEST="https://redcap-test.wakehealth.edu/api/"
REDCAP_URL_DEV="https://redcapdev.school.wakehealth.edu/api/"
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_FILE="$SCRIPT_DIR/redcap_mcp_server.py"

# ── Find Python 3.10+ ─────────────────────────────────────────────────────────
find_python() {
    for cmd in python3.13 python3.12 python3.11 python3.10 python3 python; do
        if command -v "$cmd" &>/dev/null; then
            major=$("$cmd" -c 'import sys; print(sys.version_info.major)' 2>/dev/null)
            minor=$("$cmd" -c 'import sys; print(sys.version_info.minor)' 2>/dev/null)
            if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON=$(find_python) || {
    echo ""
    echo "ERROR: Python 3.10 or later is required but none was found."
    echo "Install it with Homebrew:  brew install python@3.11"
    echo "Then re-run this script."
    exit 1
}

PYTHON_PATH="$(command -v "$PYTHON")"
echo "==> Using $PYTHON_PATH ($(${PYTHON} --version))"

# ── Install dependencies ──────────────────────────────────────────────────────
echo "==> Installing Python dependencies..."
"$PYTHON" -m pip install --quiet "mcp[cli]" requests

# ── Write to Claude desktop config ───────────────────────────────────────────
# The Claude desktop app reads MCP server config from:
#   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

mkdir -p "$CONFIG_DIR"

echo "==> Updating $CONFIG_FILE ..."

"$PYTHON" - <<PYEOF
import json, os, sys

config_file = os.path.expanduser("$CONFIG_FILE")
server_file = "$SERVER_FILE"
python_path = "$PYTHON_PATH"

# Load existing config or start fresh
if os.path.exists(config_file):
    with open(config_file) as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            config = {}
else:
    config = {}

if "mcpServers" not in config:
    config["mcpServers"] = {}

# Register the three environments
config["mcpServers"]["redcap-prod"] = {
    "command": python_path,
    "args": [server_file],
    "env": {"REDCAP_URL": "$REDCAP_URL_PROD"}
}
config["mcpServers"]["redcap-test"] = {
    "command": python_path,
    "args": [server_file],
    "env": {"REDCAP_URL": "$REDCAP_URL_TEST"}
}
config["mcpServers"]["redcap-dev"] = {
    "command": python_path,
    "args": [server_file],
    "env": {"REDCAP_URL": "$REDCAP_URL_DEV"}
}

with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

print(f"  Written to {config_file}")
PYEOF

echo ""
echo "✓ Done! Three MCP servers registered: redcap-prod, redcap-test, redcap-dev"
echo ""
echo "Next step: fully quit Claude (Cmd+Q) and relaunch it."
echo ""
echo "Then in any conversation you can say things like:"
echo "  'Check my REDCap connection on redcap-prod, token ABC123'"
echo "  'Export records from redcap-test, token XYZ789'"
echo ""
echo "To set a default token per environment so you don't type it every call,"
echo "add a REDCAP_TOKEN entry to the env block in:"
echo "  $CONFIG_FILE"
