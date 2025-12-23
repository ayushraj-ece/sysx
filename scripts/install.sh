#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/ayushraj-ece/sysx.git"

echo "Installing sysx..."

# Ensure Python is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required but not installed."
    exit 1
fi

# Ensure pipx is available
if ! command -v pipx >/dev/null 2>&1; then
    echo "pipx not found. Installing pipx..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    echo "pipx installed. Restart your shell if sysx is not found."
fi

# Install or upgrade sysx
if pipx list | grep -q sysx; then
    echo "sysx already installed. Upgrading..."
    pipx upgrade sysx
else
    pipx install git+$REPO_URL
fi

echo "sysx installation completed."
echo "Run: sysx --help"
