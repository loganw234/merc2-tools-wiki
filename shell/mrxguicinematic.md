---
title: MrxGuiCinematic
parent: Shell Modules
nav_order: 11
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiCinematic

*Byte-for-byte identical to [`resident/MrxGuiCinematic`](../resident/mrxguicinematic) — see that page for
full documentation of its functions, inheritance, and events.*

## In the shell context
Full-screen movie and subtitle playback, whose layout is loaded by the same
`MrxGuiShellBootstrap.LoadMovieLayouts()` call that loads the attract layout — meaning pre-rendered
cinematics can play straight out of the bootstrap sequence (e.g. between the intro logos and the shell),
not only mid-mission. It imports `MrxGuiManager` to hide/restore the player HUD (`ToggleHud`/
`GetHudState`) around playback and `MrxSound` to enter/exit the cinematic audio state, both of which
behave identically whether reached from the front end or a mission.
