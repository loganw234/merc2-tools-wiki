---
title: ShootingGalleryTarget
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [shooting gallery]
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
Listens for `Event.StateChange` to call `OnStateChange` when a shooting gallery target's state changes.

## Notes for modders
- Ensure that the state hashes used in `OnStateChange` match those defined in your game logic.
- This module does not require any specific initialization or cleanup beyond what is provided by the engine.