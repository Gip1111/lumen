#!/usr/bin/env bash
set -e

echo "--- Lumen Package Build Script ---"

for pkg in packages/*; do
    if [ -d "$pkg" ]; then
        echo "Building $(basename "$pkg")..."
        # makepkg -s --noconfirm
    fi
done

echo "Package builds complete (simulated)."
