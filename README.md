# Lumen 💡

Lumen is a desktop Linux distribution built on Arch Linux, designed to be as approachable as Windows while leveraging the power of a rolling-release base.

## 🚀 Key Features

- **Integrated AI Assistant**: A natural-language interface (`lumen-aid`) that helps you manage your system, install software, and diagnose hardware issues.
- **Hardware Compatibility**: Works out-of-the-box on recent consumer hardware with intelligent driver management.
- **Windows-like Approachability**: Familiar layout, unified software store, and sane defaults that just work.
- **Modern Desktop**: Built on KDE Plasma 6 with a polished, cohesive identity.
- **Arch Power, Lumen Simplicity**: The flexibility of Arch Linux without the configuration overhead.

## 🏗️ Project Status

Lumen is currently in early development (Alpha). We are focused on building the core AI daemon and a robust ISO build pipeline.

## 📂 Repository Structure

- `iso/`: Archiso profile for building the bootable image.
- `lumen-ai/`: The heart of the project—AI daemon, overlay UI, and tools.
- `installer/`: Calamares configuration and custom modules.
- `desktop/`: Themes, layouts, and visual assets.
- `packages/`: PKGBUILDs for Lumen-specific components.

## 🛠️ Development

## 🚀 CI/CD & Secure Boot

Lumen uses a fully automated build pipeline via GitHub Actions.

- **Automated Builds**: Every push to `main` triggers an ISO build.
- **Secure Boot**: The generated ISO is injected with `shim` and signed `grub` binaries, allowing it to boot on modern hardware with Secure Boot enabled.
- **Release Tracking**: Tags (e.g., `v0.1-alpha`) automatically create a GitHub Release with the ISO as an asset.

To build manually in a local Arch environment:

```bash
make iso
```

## 📜 License

Lumen is open-source software. See individual component directories for specific licensing information.
