---
title: MrxGuiShellLayout
parent: Shell Modules
nav_order: 22
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiShellLayout

*Byte-for-byte identical to [`resident/MrxGuiShellLayout`](../resident/mrxguishelllayout) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Layout data for the "Shell" widget itself (a background plus a text placeholder), whose
`EventHandlerFile`/`EventHandlers` point straight at `mrxguishell.lua`'s functions (`HandleServerAdd`/
`Remove`/`Update`, `HandleInput`, `HandleInitializationEvent`, `HandleGameStateChangeEvent`). Loaded by
`MrxGuiShellBootstrap.EnterShell()`/`LoadShell()` — this is the widget tree the entire main menu hangs
off of.
