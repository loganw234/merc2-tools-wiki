---
title: MrxGuiManager
parent: Shell Modules
nav_order: 18
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiManager

*Byte-for-byte identical to [`resident/MrxGuiManager`](../resident/mrxguimanager) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
`CreateGui`/`ToggleHud`/`DeleteGui` build and manage the in-mission player HUD (ammo, minimap, satellite,
PDA) — real, functional code kept in this build because `MrxGuiCinematic` imports it and calls
`ToggleHud`/`GetHudState` to hide the HUD around cutscenes that can play from the shell bootstrap flow.
But the shell-only `MrxGuiBootstrap_ShellOnly` module overrides `CreatePlayerHud`/`ToggleHud`/`DeleteHud`/
`DeleteAllHuds` with empty no-op stubs instead of ever calling this file's `CreateGui` — there's no
gameplay HUD to build from the main menu, so `CreateGui` itself never actually runs here even though the
code is identical.
