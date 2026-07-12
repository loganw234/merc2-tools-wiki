---
title: MrxGuiAttractMode
parent: Shell Modules
nav_order: 9
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiAttractMode

*Byte-for-byte identical to [`resident/MrxGuiAttractMode`](../resident/mrxguiattractmode) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Drives the attract-mode movie loop itself: `HandleInit` wires up the `GuiGameStateChange`/`ControllerInput`
handlers, `_Open` plays the next attract movie and calls `MrxSound.EnterAttractState()`, and any controller
input calls `Sys.RequestGameState("Shell")` to end attract mode and open the main menu. It's the direct
event-handler target named by `MrxGuiAttractLayout`'s `GuiInitialization` binding, so the pair is only ever
loaded together.
