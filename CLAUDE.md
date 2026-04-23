# Lumen — Project Context for Claude Code

## What Lumen is

Lumen is a desktop Linux distribution built on **Arch Linux**, designed to feel as approachable as Windows while leveraging the power of a rolling-release base. Its defining feature is **a deeply integrated AI assistant** that can understand natural-language requests and perform system actions (install packages, diagnose hardware, fix drivers, configure services) through a sandboxed tool-calling architecture.

Target user: a Windows/macOS refugee who wants a modern, polished Linux desktop that "just works" on recent consumer hardware and where solving problems doesn't require reading five forum threads.

Not a goal: being minimal, being a developer-first distro, being yet another Ubuntu reskin.

## Core pillars (in priority order)

1. **Hardware compatibility out of the box.** Recent kernel, full `linux-firmware`, intelligent driver manager, fallback strategies for undocumented devices.
2. **AI-assisted problem solving.** `lumen-aid` daemon + overlay UI, pluggable LLM backends (Ollama local default, API backends optional), sandboxed tool calling.
3. **Windows-like approachability.** Familiar layout, unified software store (pacman + AUR + Flatpak under one UI), pre-installed codecs and common apps, graphical installer with sane defaults.
4. **Distinctive but not gratuitous UX.** Built on KDE Plasma 6, customized with a coherent Lumen identity. Not a full new DE.
5. **Sustainable by a small team.** Reuse existing infrastructure (archiso, Calamares, pamac fork, chwd-style driver DB). Build custom only what delivers Lumen's core value.

## Repository layout

```
lumen/
├── CLAUDE.md              # this file
├── README.md              # public-facing project description
├── DECISIONS.md           # architectural decisions + rationale (append-only)
├── TODO.md                # what's missing / next steps
├── Makefile               # top-level build targets
├── iso/                   # archiso profile
│   ├── airootfs/          # files copied into the live ISO root
│   ├── packages.x86_64    # packages included in the ISO
│   ├── profiledef.sh
│   └── pacman.conf
├── installer/             # Calamares config + custom modules
├── desktop/               # Plasma theme, layout, wallpapers, Plymouth
│   ├── theme/
│   ├── layout/
│   └── plymouth/
├── lumen-ai/              # AI assistant
│   ├── daemon/            # lumen-aid (Python, systemd user service)
│   ├── overlay/           # Qt/QML overlay UI
│   ├── backends/          # Ollama, Anthropic, OpenAI adapters
│   └── tools/             # tool implementations (install, diagnose, etc.)
├── lumen-drivers/         # hardware detection + driver installer
├── lumen-store/           # unified software store (pamac fork initially)
├── packages/              # PKGBUILDs for Lumen-branded packages
│   ├── lumen-ai/
│   ├── lumen-drivers/
│   ├── lumen-desktop-theme/
│   └── ...
├── repo/                  # scripts for maintaining the Lumen pacman repo
├── docs/                  # user + developer docs (mkdocs)
├── scripts/               # build, test, release helpers
└── .github/workflows/     # CI/CD
```

## Tech stack and conventions

**Languages:**
- **Python 3.12+** for `lumen-aid` daemon, tool implementations, build scripts. Type hints mandatory, `ruff` for lint/format, `mypy --strict` for type checking.
- **Rust** only where it earns its complexity (performance-critical paths, long-running services where Python GC is a problem). Default to Python first.
- **C++/Qt 6 + QML** for the overlay UI and any native Plasma integration.
- **POSIX shell** for system scripts. **No bashisms** in anything that ships in the ISO — must run under `dash`. Scripts under `scripts/` for dev tooling may use bash.
- **YAML** for configs (Calamares, CI). **TOML** for Python project configs. No JSON for human-edited files.

**Naming:**
- All Lumen-specific packages prefixed with `lumen-` (e.g. `lumen-ai`, `lumen-desktop-theme`, `lumen-drivers`).
- Daemons end in `-aid` or `-d` (e.g. `lumen-aid` for the AI daemon). User-facing CLI tools have short names (e.g. `lumen`, `lumen-doctor`).
- Python modules: `snake_case`. Qt/QML components: `PascalCase`. Shell scripts: `kebab-case.sh`.

**Code style:**
- Python: `ruff format` + `ruff check` with rules `E,F,I,UP,B,SIM,RUF`. Line length 100.
- Rust: `rustfmt` default + `clippy -- -D warnings`.
- Commit messages: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `ci:`). Scope optional but encouraged (e.g. `feat(lumen-ai): add network diagnose tool`).

**Testing:**
- Python: `pytest`, aim for meaningful tests on tool logic and backend adapters, not 100% coverage theater.
- ISO: QEMU smoke test in CI (boot to graphical target, SDDM up, `lumen-aid` active).
- Manual test checklist in `docs/testing.md` for each release.

## Architectural principles

**Security and trust boundaries:**
- `lumen-aid` runs as the user, never root. Privileged actions go through `pkexec` / polkit rules with explicit user confirmation dialogs.
- Every destructive tool action (install, remove, modify config, run command) requires an explicit user confirmation in the overlay UI. The LLM never silently executes anything with side effects.
- LLM backends are untrusted input. Tool arguments are validated with schemas before execution. No shell interpolation of LLM output — arguments passed as argv, never concatenated.
- API keys for cloud backends stored in `libsecret` (kwallet/gnome-keyring), never in plaintext config.

**Offline-first:**
- The default Ollama backend must work with zero internet (after initial model download). A user with no connection must still get a usable assistant, even if less capable.
- Cloud backends are opt-in and clearly marked.

**Honest UX:**
- When something doesn't work, say so clearly with actionable next steps. No fake "everything's fine" states.
- Driver manager distinguishes: supported / partially supported / unsupported / unknown. Never lies.
- AI assistant says "I don't know" or "I'm not confident" instead of hallucinating. System prompt enforces this.

**Reuse over rebuild:**
- Calamares for installer (not custom).
- Pamac as base for Lumen Store (fork, don't rewrite).
- `chwd` database for hardware matching (contribute upstream where possible).
- KDE Plasma as DE base (theme and customize, don't fork).

## The AI assistant (lumen-aid) — key design

- **Protocol:** JSON-RPC 2.0 over Unix socket at `$XDG_RUNTIME_DIR/lumen-aid.sock`.
- **Backends:** abstract `Backend` class with `chat(messages, tools) -> stream`. Concrete: `OllamaBackend`, `AnthropicBackend`, `OpenAIBackend`. Selectable per-conversation.
- **Tools:** registered via `@tool` decorator, each with a JSON schema for args, a human description, and a `requires_confirmation: bool`. Tool implementations live in `lumen-ai/tools/`.
- **Conversation state:** ephemeral by default, optionally persisted to `~/.local/state/lumen-ai/history.db` (SQLite) if user enables it.
- **Context injection:** daemon automatically adds system context (distro version, kernel, recent errors from journal, network state) to the system prompt, capped at a sensible token budget.
- **Streaming:** responses stream token-by-token to the overlay via the socket. Tool calls interrupt streaming, show a confirmation dialog, resume after approval.

## Build and release flow

- **Local dev:** `make iso` builds a ISO in a local Arch container. `make test` runs unit tests. `make lint` runs all linters.
- **CI:** GitHub Actions builds ISO on every push to `main` (as artifact) and on tags `v*` (as release asset). Separate workflow builds individual packages and publishes to the Lumen pacman repo.
- **Versioning:** SemVer-ish. `0.x.y` during alpha. Tags trigger releases. Codenames optional (e.g. `0.1 "Ember"`).
- **Repo hosting:** Lumen pacman repo on GitHub Pages initially, migration path to Cloudflare R2 when scale requires it.

## What to do when uncertain

- Read `DECISIONS.md` before proposing changes to architecture — the answer may already be there.
- Prefer small, reviewable diffs. One feature or fix per commit.
- If a change touches the ISO contents, note it in `TODO.md` under "needs ISO rebuild test".
- When adding a dependency, justify it: size, maintenance status, alternatives considered. Lumen is lean by default.
- When in doubt about UX, default to what a Windows user would expect, not what a Linux purist would prefer.

## What NOT to do

- Don't fork Arch. We are an Arch-based distro with our own repo, not a new base distro.
- Don't write a new DE. Plasma is the base.
- Don't add a dependency on systemd-alternatives. We are systemd-only.
- Don't ship bleeding-edge unstable components in stable releases. The AUR helper auto-installs, but the ISO itself ships only tested versions.
- Don't let the AI assistant perform destructive actions without explicit confirmation. Ever.
- Don't hardcode paths that assume a specific user. Use `$HOME`, `$XDG_*` variables.
- Don't commit binary blobs to the main repo. Use Git LFS or external hosting for wallpapers, models, large assets.

## Glossary

- **ISO**: the bootable live+installer image Lumen ships.
- **Lumen repo**: our custom pacman repository hosting `lumen-*` packages and selected rebuilds.
- **chwd**: Configurable Hardware Detection (from Manjaro/CachyOS), the pattern we follow for driver auto-detection.
- **Overlay**: the always-accessible AI UI invoked by Super+Space, not a persistent window.
- **Tool**: a function exposed to the LLM via function calling (install_package, diagnose_network, etc.).
- **Backend**: an LLM provider (Ollama, Anthropic, OpenAI).
