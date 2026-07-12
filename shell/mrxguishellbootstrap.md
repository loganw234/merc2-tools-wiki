---
title: MrxGuiShellBootstrap
parent: Shell Modules
nav_order: 21
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiShellBootstrap

*Byte-for-byte identical to [`resident/MrxGuiShellBootstrap`](../resident/mrxguishellbootstrap) — see that
page for full documentation of its functions, inheritance, and events.*

## In the shell context
The orchestration module chaining the whole pre-game flow together: `Init()` loads the loading-screen
layout then the attract/cinematic layouts, `EnterPrecache()`/`EnterShell()` load the LTI-precache and Shell
screens in turn, and `Reset()`/`ExitShell()` tear them down again. Between the five layout files it loads
directly (`MrxGuiLoadLayout`, `MrxGuiAttractLayout`, `MrxGuiCinematicLayout`, `MrxGuiLTIPrecacheLayout`,
`MrxGuiShellLayout`) and the logic modules those layouts bind their event handlers to, this file is the
load-order backbone that the shell-only top-level `ShellBootstrap.Init()`/`Start()` drives.
