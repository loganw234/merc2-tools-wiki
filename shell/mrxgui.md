---
title: MrxGui
parent: Shell Modules
nav_order: 7
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGui

*Byte-for-byte identical to [`resident/MrxGui`](../resident/mrxgui) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
Imported directly by several other shell GUI modules as the `MrxGui.*` facade — `MrxGuiShell`'s
`_OpenShell`/`_CloseShell` call `MrxGui.FadeToColor`/`FadeFromColor` around the main-menu transition,
`MrxGuiAttractMode._Open` calls `MrxGui.FadeFromColor`, and `MrxGuiShellBootstrap.LoadMovieLayouts` calls
`MrxGui._InitFadeFlash()` directly to stand up the global fade widget. The `Init()` aliasing table this
file builds over `MrxGuiBase` is identical machinery regardless of which tree it's compiled into, so it's
shared verbatim rather than forked.
