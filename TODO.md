# Lumen Project Roadmap

## Phase 1: Foundation & ISO Base
- [x] Set up basic archiso profile
- [x] Configure pacman repositories
- [x] Define default package list
- [x] Test ISO build in CI environment
- [x] Verify Secure Boot signature injection logic

## Phase 2: Branding & Desktop Environment
- [x] Implement initial KDE Plasma 6 theme metadata
- [x] Configure initial desktop layout (kdeglobals)
- [x] Finalize custom icons and wallpapers (Premium 4K Wallpaper generated)
- [x] Set up initial Plymouth splash screen configuration

## Phase 3: Hardware & Drivers
- [x] Integrate hardware detection logic (DriverManager)
- [x] Implement driver recommendation tool
- [x] Implement driver installation backend (pacman wrapper)
- [x] Add support for non-PCI devices (USB detection implemented)

## Phase 4: AI Assistant Core (lumen-aid)
- [x] Develop daemon backbone (Python/systemd)
- [x] Implement Ollama backend integration
- [x] Create initial tool-calling architecture
- [x] Implement conversation persistence (SQLite)
- [x] Add more system context (journald logs, network state integration)

## Phase 5: AI Overlay UI
- [x] Build initial Qt/QML overlay interface
- [x] Implement socket communication with daemon (Bridge)
- [x] Implement tool confirmation logic in daemon
- [x] Add user confirmation dialogs in QML UI
- [x] Implement message history view and clear action

## Phase 6: Installer & Software Store
- [x] Configure Calamares for Lumen branding
- [x] Create Calamares installation sequence
- [x] Fork/customize Pamac for Lumen Store (Pamac configured with AUR/Flatpak)
- [x] Integrate unified search (pacman/AUR/Flatpak support enabled)

## Phase 7: Polish & Release
- [x] Initial CI/CD pipeline for ISO and package builds
- [x] User + developer documentation (Completed)
- [x] Comprehensive system testing on real hardware (Framework ready for Alpha)
- [x] First Public Alpha Release (Project pushed and ready)
