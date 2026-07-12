---
title: Shell
parent: Shell Modules
nav_order: 1
inherits: none
tags: [shell]
verified: false
---

# Shell

## Overview
`Shell` is the front-end build's top-level entry module — the literal script the engine calls into to start the main-menu/attract-mode build, analogous to a level's master script. Its entire job is to import the two modules the rest of shell startup depends on and immediately hand off to `MrxShellBootstrap.Start()`. It carries no logic of its own beyond that hand-off.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxShellBootstrap`, `MrxGui`

## Instance pattern
Stateless entry-point module. No per-instance state and no module-level flags — its only two top-level names are the functions below.

## Functions

### Init()
The engine-called entry point for the shell build. Its entire body is one call, `MrxShellBootstrap.Start(_MyDummySetup)` — note it only supplies the first of `Start`'s two parameters (`fCallback`); the second (`tCallbackArgs`) is left `nil`.

### _MyDummySetup()
An empty no-op function, passed to `MrxShellBootstrap.Start` as its completion callback. The shell has nothing extra to run once `MrxShellBootstrap`'s readiness gate resolves, so it hands over a placeholder rather than `nil`.

## Events
None — this file makes no `Event.*` calls.

## Notes for modders
- `MrxGui` is imported here but never referenced anywhere in this file's 9 lines. That's not necessarily dead weight — `import()` can matter for load-order/side effects even when the importing file never touches the resulting namespace directly, so don't assume it's safe to strip.
- Because `_MyDummySetup` does nothing, and (see [MrxShellBootstrap](mrxshellbootstrap)) the readiness gate it's registered against doesn't appear to invoke stored completion callbacks anywhere visible in this corpus, swapping in a real callback here is currently the only place to hook "the shell has finished starting" — worth knowing even though the hook it feeds into looks dormant.
- If you're looking for the splash-screens/auto-connect/menu-routing logic, that's [ShellBootstrap](shellbootstrap) — a different module despite the near-identical name.
