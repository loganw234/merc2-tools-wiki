---
title: MrxGuiLoadLayout
parent: Shell Modules
nav_order: 14
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiLoadLayout

*Byte-for-byte identical to [`resident/MrxGuiLoadLayout`](../resident/mrxguiloadlayout) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Layout for the "Loading Screen" widget (background plus a "Loading" text label), bound to
`MrxGuiLoadScreen.HandleInit`/`HandleStateChangeEvent`. It's the very first GUI layout the front end
loads — `MrxGuiShellBootstrap.Init()` calls `MrxGuiBase.LoadGUIFile("MrxGuiLoadLayout", LoadMovieLayouts)`
before anything else in the bootstrap chain runs.
