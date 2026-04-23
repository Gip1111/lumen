# Lumen Development Guide

## Project Structure
- `lumen_ai/`: AI daemon and overlay UI.
- `lumen_drivers/`: Hardware detection logic.
- `iso/`: Archiso profile.
- `installer/`: Calamares configuration.

## Setup Development Environment
1. Clone the repository.
2. Run `make setup-dev`.
3. Start the daemon: `make run-daemon`.
4. Start the overlay: `make run-overlay`.

## Building the ISO
The ISO is built automatically via GitHub Actions. To build locally (requires Arch Linux):
```bash
make iso
```

## Adding Tools to the AI
Tools are defined in `lumen_ai/tools/`. Use the `@tool` decorator to register new capabilities.
