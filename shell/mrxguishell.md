---
title: mrxguishell
parent: Shell Modules
nav_order: 20
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# mrxguishell

*Byte-for-byte identical to [`resident/mrxguishell`](../resident/mrxguishell) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
This *is* the main-menu screen itself: `HandleInitializationEvent` creates the `shell.gfx` Flash movie and
wires up every `LTI*` ActionScript callback (video/input options, lobby hosting and joining, new-game
character select), and `HandleGameStateChangeEvent` opens it when `Sys.RequestGameState("Shell")` fires.
It's the literal `EventHandlerFile = "mrxguishell"` target named in `MrxGuiShellLayout`, reached via
`MrxGuiShellBootstrap.EnterShell()`/`LoadShell()`, and also hosts `OpenSkipToMissionDialog` (a
`Sys.IsFinalConfig()`-gated developer skip-to-mission menu) and `OpenInstallDialog` (shown when
`Junk.IsInstallable()` reports the game can install to HDD), both built on `MrxMultiPageMenu`.
