---
title: Fueltank
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [fuel, fx]
verified: true
verified_note: corrected Events section — OnStateChange is an engine-invoked lifecycle hook (naming convention shared with oilrig.lua/islandfortress.lua/others), not something this file subscribes to via Event.Create; only Event.TimerRelative is a real Event.Create call here
---

# Fueltank

*Module: fueltank.lua*

## Overview
The `Fueltank` module manages the visual effects associated with a fuel tank object. Specifically, it handles starting and stopping flame and smoke emitters when certain state changes occur.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any specific state fields.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Engine-invoked lifecycle hook (see Events below) called when the object's world-state node changes. Converts `uiStateHashName` to a string via `Sys.GuidToString` and compares against the literal `"0x7687DF41"`. On match, starts the `"fx_EmitFlameOilrigTower"` emitter via `ObjectState.StartEmitter` and schedules `_StartSmoke` after a random `Math.randf(12, 20)`-second delay using `Event.TimerRelative`. Any other state hash is ignored (no `else` branch).

### `_StartSmoke(uiGuid, uiNodeHashName, fxName)`
Helper invoked only via the timer set up in `OnStateChange`. Stops the emitter named by `fxName` (the flame effect) and starts a new `"fx_EmitSmokeStack"` emitter in its place.

## Events
- `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)` is an engine-invoked callback, not something this file registers with `Event.Create` — the same naming/signature convention appears across other resident files (e.g. `oilrig.lua`, `islandfortress.lua`). No `Event.StateChange` constant is referenced anywhere in this file.
- `Event.TimerRelative` — the only real `Event.Create` call in this file, used to delay `_StartSmoke` after the flame starts.

## Notes for modders
- Ensure that `OnStateChange` is called appropriately to manage the visual effects of the fuel tank.
- Customize the flame and smoke emitters by modifying the associated effect names in the code.
- Be aware that the random timer interval affects when the smoke emitter starts.