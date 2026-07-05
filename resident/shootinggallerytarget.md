---
title: ShootingGalleryTarget
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [shooting gallery]
verified: true
verified_note: removed fabricated Event.StateChange claim — file has zero Event.* calls; OnStateChange is engine-invoked by naming convention, not a registered handler
---

# ShootingGalleryTarget

*Module: shootinggallerytarget.lua*

## Overview
The `ShootingGalleryTarget` module is responsible for handling state changes in shooting gallery targets. It listens for specific state changes and performs actions such as opening or closing doors on the target.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless utility module (no per-instance table). It does not track any persistent state.

## Functions
### `OnStateChange(uGuid, uiNodeHashName, uiStateHashName)`
Called when the state of a shooting gallery target changes. Converts the state hash to a string and checks if it matches specific values:
- If the state hash is `"0x7687DF41"`, it opens the door on the target.
- If the state hash is `"0xACB51200"`, it closes the door on the target.

## Events
This file contains **no `Event.*` calls at all** — no `Event.Create`, no `Event.StateChange` constant
reference. `OnStateChange` is invoked directly by the engine as a naming-convention callback on the
world-object script (the same mechanism that calls `OnActivate`/`OnDeath` on other modules without those
modules registering anything explicitly), not through an `Event.Create` registration in this file.

## Notes for modders
- Ensure that the state hashes used in `OnStateChange` match those defined in your game logic.
- This module does not require any specific initialization or cleanup beyond what is provided by the engine.
- `"0x7687DF41"` and `"0xACB51200"` are the only two state hashes checked; any other state change is a no-op here.