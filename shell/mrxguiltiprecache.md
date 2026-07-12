---
title: MrxGuiLTIPrecache
parent: Shell Modules
nav_order: 16
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiLTIPrecache

*Byte-for-byte identical to [`resident/MrxGuiLTIPrecache`](../resident/mrxguiltiprecache) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Behavior for the "LTI_precache" screen shown right after the intro movies: `_Initialize` builds its Flash
widget, and `_LTIPrecacheDone`/`_LTIPrecacheSmokeDone2` report back to `LTILibName.LTIPrecacheDone()` to
unblock the bootstrap. It's reached via `MrxGuiShellBootstrap.EnterPrecache()`, which the shell-only
top-level `ShellBootstrap.StartPrecache()` calls immediately after the EA/Pandemic logo movies finish
playing.
