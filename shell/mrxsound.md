---
title: MrxSound
parent: Shell Modules
nav_order: 25
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxSound

*Byte-for-byte identical to [`resident/MrxSound`](../resident/mrxsound) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
Defines the paired `EnterShellState()`/`ExitShellState()` functions for the front end specifically —
called directly from `MrxGuiShell._OpenShell`/`_CloseShell` to load the `ui_shell`/`ui_hud`/`music` sound
and wave banks and transition to the "shell" music state. The rest of this file's paired Enter/Exit
functions (pause, cinematic, attract, PDA, hijack, survival) are the same shared state façade used by both
trees — written once to serve every caller regardless of which build reaches them.
