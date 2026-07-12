---
title: MrxGuiBase
parent: Shell Modules
nav_order: 10
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiBase

*Byte-for-byte identical to [`resident/MrxGuiBase`](../resident/mrxguibase) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
The foundational widget class library — `Widget`/`TextWidget`/`ImageWidget`/`FlashWidget`/`SpriteWidget`,
`WidgetManager`, the control-focus queue, and the `Event`-driven dispatch loop. Most other files in this
list import `MrxGuiBase` directly for these widget primitives (a few, like `MrxGuiManager`, reach them
indirectly through the `MrxGui` facade instead) — the Flash-backed main menu, dialog boxes, and loading
screens are built from exactly the same widget classes as the in-game HUD, so there's nothing
shell-specific to fork here.
