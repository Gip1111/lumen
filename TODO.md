# Lumen Project Roadmap

## Phase 1: Foundation & ISO Base
- [x] Set up basic archiso profile
- [x] Configure pacman repositories
- [x] Define default package list
- [ ] Test ISO build in CI environment
- [ ] Verify Secure Boot signature injection

## Phase 2: Branding & Desktop Environment
- [x] Implement initial KDE Plasma 6 theme metadata
- [x] Configure initial desktop layout (kdeglobals)
- [ ] Finalize custom icons and wallpapers
- [ ] Set up Plymouth splash screen

## Phase 3: Hardware & Drivers
- [x] Integrate hardware detection logic (DriverManager)
- [x] Implement driver recommendation tool
- [ ] Add support for non-PCI devices (USB, etc.)
- [ ] Implement actual driver installation backend (pacman wrapper)

## Phase 4: AI Assistant Core (lumen-aid)
- [x] Develop daemon backbone (Python/systemd)
- [x] Implement Ollama backend integration
- [x] Create initial tool-calling architecture
- [ ] Implement conversation persistence (SQLite)
- [ ] Add more system context (journald logs, network state)

## Phase 5: AI Overlay UI
- [x] Build initial Qt/QML overlay interface
- [x] Implement socket communication with daemon (Bridge)
- [ ] Add user confirmation dialogs for destructive tools
- [ ] Implement message history view and clear action

## Phase 6: Installer & Software Store
- [ ] Configure Calamares for Lumen branding
- [ ] Customize Calamares modules (partitioning, user setup)
- [ ] Fork/customize Pamac for Lumen Store
- [ ] Integrate unified search (pacman/AUR/Flatpak)

## Phase 7: Polish & Release
- [x] Initial CI/CD pipeline for ISO and package builds
- [ ] Comprehensive system testing on real hardware
- [ ] User + developer docs (MkDocs)
- [ ] First Public Alpha Release
