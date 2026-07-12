---
title: MrxGuiAttractLayout
parent: Shell Modules
nav_order: 8
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiAttractLayout

*Byte-for-byte identical to [`resident/MrxGuiAttractLayout`](../resident/mrxguiattractlayout) — see that
page for full documentation of its functions, inheritance, and events.*

## In the shell context
This is the layout data for the "Attract" widget shown once nobody's touched a controller for a while —
loaded by `MrxGuiShellBootstrap.LoadMovieLayouts()` (`MrxGuiBase.LoadGUIFile("MrxGuiAttractLayout")`) in
the same pass that loads the cinematic layout. Its `GuiInitialization` handler points straight at
`MrxGuiAttractMode.HandleInit`, so the two files are a matched layout/logic pair that only make sense
loaded together.
