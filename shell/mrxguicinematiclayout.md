---
title: MrxGuiCinematicLayout
parent: Shell Modules
nav_order: 12
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiCinematicLayout

*Byte-for-byte identical to [`resident/MrxGuiCinematicLayout`](../resident/mrxguicinematiclayout) — see
that page for full documentation of its functions, inheritance, and events.*

## In the shell context
Layout data for the "Cinematic Placeholder" widget (background image, picture, placeholder text,
subtitle, and supersubtitle children), paired 1:1 with `MrxGuiCinematic`'s event handlers. Loaded by
`MrxGuiShellBootstrap.LoadMovieLayouts()` in the same pass as the attract layout, so this widget tree
exists in the shell build whether or not a mission is ever entered.
