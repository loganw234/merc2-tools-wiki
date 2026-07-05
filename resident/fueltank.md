---
title: Fueltank
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [fuel, fx]
verified: true
verified_note: 'deeper pass: re-confirmed both functions; added a Module constants section (trigger state hash 0x7687DF41, emitters fx_EmitFlameOilrigTower/fx_EmitSmokeStack, 12-20s delay) and actionable Notes, cross-linked oilrig/islandfortress; prior Events fix (OnStateChange is an engine hook, only Event.TimerRelative is a real Event.Create) still holds'
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

## Module constants & tunables
- Trigger state hash: `"0x7687DF41"` — `OnStateChange` only reacts when the incoming state hash stringifies to
  this value; every other state is ignored.
- Emitters (looked up via `ObjectState.GetStringHash`): flame `"fx_EmitFlameOilrigTower"` (started on the
  trigger) then `"fx_EmitSmokeStack"` (swapped in by `_StartSmoke`). Swap these two strings to re-skin the
  burn.
- Flame-to-smoke delay: `Math.randf(12, 20)` seconds (inline literal).

## Notes for modders
- The two emitter template strings are the whole mod lever here — change `"fx_EmitFlameOilrigTower"` /
  `"fx_EmitSmokeStack"` to alter the flame/smoke visuals, or the `Math.randf(12, 20)` range to change how long
  the flame burns before it becomes a smoke stack.
- `OnStateChange` is engine-invoked and gated on the exact hash `"0x7687DF41"`; if you retarget it to a
  different world-state, change that literal to match the new state's hash.
- The same `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)` emitter-swap convention shows up on
  [oilrig](oilrig) and [islandfortress](islandfortress) — those are the pages to compare against for the
  wider destructible-FX pattern.