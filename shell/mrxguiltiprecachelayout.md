---
title: MrxGuiLtiPrecacheLayout
parent: Shell Modules
nav_order: 17
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiLtiPrecacheLayout

*Byte-for-byte identical to [`resident/MrxGuiLtiPrecacheLayout`](../resident/mrxguiltiprecachelayout) —
see that page for full documentation of its functions, inheritance, and events.*

## In the shell context
Layout for the "LTI_precache" widget above; its `GuiGameStateChange`/`GuiInitialization` handlers point at
`MrxGuiLTIPrecache.HandleStateChangeEvent`/`_Initialize`. Loaded by `MrxGuiShellBootstrap.EnterPrecache()`
(`MrxGuiBase.LoadGUIFile("MrxGuiLTIPrecacheLayout", PrecacheScreenLoaded)`) — the first real screen the
front end shows, before the Shell widget tree itself even exists.
