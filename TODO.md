# Lumen Project Roadmap

## Phase 1: Foundation & ISO Base
- [x] Set up basic archiso profile
- [x] Configure pacman repositories
- [x] Define default package list
- [/] Test ISO build in CI environment (In progress)
- [x] Verify Secure Boot signature injection logic

## Phase 2: Branding & Desktop Environment
- [x] Implement initial KDE Plasma 6 theme metadata
- [x] Configure initial desktop layout (kdeglobals)
- [ ] Finalize custom icons and wallpapers
- [x] Set up initial Plymouth splash screen configuration

## Phase 3: Hardware & Drivers
- [x] Integrate hardware detection logic (DriverManager)
- [x] Implement driver recommendation tool
- [x] Implement driver installation backend (pacman wrapper)
- [ ] Add support for non-PCI devices (USB, etc.)

## Phase 4: AI Assistant Core (lumen-aid)
- [x] Develop daemon backbone (Python/systemd)
- [x] Implement Ollama backend integration
- [x] Create initial tool-calling architecture
- [x] Implement conversation persistence (SQLite)
- [ ] Add more system context (journald logs, network state)

## Phase 5: AI Overlay UI
- [x] Build initial Qt/QML overlay interface
- [x] Implement socket communication with daemon (Bridge)
- [x] Implement tool confirmation logic in daemon
- [ ] Add user confirmation dialogs in QML UI
- [ ] Implement message history view and clear action

## Phase 6: Installer & Software Store
- [x] Configure Calamares for Lumen branding
- [x] Create Calamares installation sequence
- [ ] Fork/customize Pamac for Lumen Store
- [ ] Integrate unified search (pacman/AUR/Flatpak)

## Phase 7: Polish & Release
- [x] Initial CI/CD pipeline for ISO and package builds
- [x] User + developer documentation (Initial version)
- [ ] Comprehensive system testing on real hardware
- [ ] First Public Alpha Release
