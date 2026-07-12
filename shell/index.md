---
title: Shell Modules
nav_order: 9
has_children: true
has_toc: false
---

# Shell Modules

Reference pages for `src/shell/` — the front-end/main-menu build of the engine (attract mode, splash
screens, the online server browser, load screens) as opposed to [Resident Modules](../resident/)'
in-game HUD context.

> **Status: new, first pass from static source reading only.** Not confirmed by playing the game yet.

**22 of these 28 files are byte-for-byte identical to an already-documented [Resident Modules](../resident/)
page** — verified by hash comparison, not just similar-looking. Rather than duplicate those pages (and risk
the two descriptions silently drifting apart from each other later), each identical file gets a short
pointer page here noting its shell-context caller and linking to the existing Resident Modules page for
the actual documentation. Only the **6 true shell-only files** get the full
Overview/Inheritance/Instance pattern/Functions/Events/Notes treatment:

- **[shell](shell)** — the literal entry stub.
- **[ShellBootstrap](shellbootstrap)** — splash screens, auto-connect/auto-load branching, main-menu
  hand-off.
- **[MrxShellBootstrap](mrxshellbootstrap)** — a small GUI-loaded readiness gate.
- **[MrxGui_ShellOnly](mrxgui_shellonly)** — the shell's own facade over `MrxGuiBase` (screen fades, a
  HUD-message stub).
- **[MrxGuiBootstrap_ShellOnly](mrxguibootstrap_shellonly)** — the shell's stubbed-out counterpart to
  `resident/mrxguibootstrap` (same function names, empty bodies — there's no gameplay HUD to manage from
  the main menu).
- **[MrxSoundShellBootstrap](mrxsoundshellbootstrap)** — audio ducking/fade categories and music-cue
  bindings for the front end.

Given the small size (28 files total, most of them one-paragraph pointers) this section stays a flat
list rather than splitting into further categories — use the sidebar or the search bar to find a specific
module.

## Modules in this category

- **[MrxGui](mrxgui)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGui_ShellOnly](mrxgui_shellonly)** — A facade module that imports `MrxGuiBase` and re-exposes a large chunk of its widget API as flat globals (`AddWidget`, `Widget`, `ImageWidget`, `GetWidgetByName`, etc.), wired up in `Init()`.
- **[MrxGuiAttractLayout](mrxguiattractlayout)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiAttractMode](mrxguiattractmode)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiBase](mrxguibase)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiBootstrap_ShellOnly](mrxguibootstrap_shellonly)** — The shell build's counterpart to [`MrxGuiBootstrap`](../resident/mrxguibootstrap): same function names (`ToggleHud`, `CreatePlayerHud`, `DeleteHud`, `DeleteAllHuds`, `SetSatelliteOverlay`, `SetOnGuiLoadedFunc`), but every one of them is an empty stub here.
- **[MrxGuiCinematic](mrxguicinematic)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiCinematicLayout](mrxguicinematiclayout)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiDialogBox](mrxguidialogbox)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiLoadLayout](mrxguiloadlayout)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiLoadScreen](mrxguiloadscreen)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiLTIPrecache](mrxguiltiprecache)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiLtiPrecacheLayout](mrxguiltiprecachelayout)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiManager](mrxguimanager)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiNumericBox](mrxguinumericbox)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[mrxguishell](mrxguishell)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiShellBootstrap](mrxguishellbootstrap)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxGuiShellLayout](mrxguishelllayout)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxMultipageMenu](mrxmultipagemenu)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxMusic](mrxmusic)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxShellBootstrap](mrxshellbootstrap)** — A small readiness-gate module that tracks whether the shell's GUI has finished loading and whether the local player has joined, so a caller can be notified once both are true.
- **[MrxSound](mrxsound)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxSoundBanks](mrxsoundbanks)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxSoundCategories](mrxsoundcategories)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[MrxSoundShellBootstrap](mrxsoundshellbootstrap)** — Sets up the front end's audio: ducking/fade rules for five mix categories, 69 per-faction and per-region music-cue bindings, then calls `MrxSound.Initialize()`.
- **[MrxUtilShell](mrxutil_shell)** — Byte-for-byte identical to the linked resident/ module — see below for its shell-context role.
- **[Shell](shell)** — `Shell` is the front-end build's top-level entry module — the literal script the engine calls into to start the main-menu/attract-mode build, analogous to a level's master script.
- **[ShellBootstrap](shellbootstrap)** — `ShellBootstrap` is the front-end build's top-level startup orchestrator — it plays the EA/Pandemic splash movies, waits on an asset-precache gate, then routes into auto-connect, auto-lobby, auto-server, autoload, or the main menu proper.
