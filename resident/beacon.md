---
title: Beacon
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [weapon, timer]
verified: true
verified_note: 'deeper pass: re-confirmed the whole source; added Module constants (material animation "global_weapon_beacon", sound cue "wpn_bomb_timer_01_armed", 1s arm timer) and replaced vacuous Notes with actionable levers; Instance pattern + Events already correct'
---

# Beacon

*Module: beacon.lua*

## Overview
The `Beacon` module represents a beacon object in the game world. It is responsible for playing animations and sound cues when the beacon is activated or deactivated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Not the `Inheritable`/`setmetatable`/`tInstance` per-`uGuid` pattern — there's no `Create`/`Awake`, no
prototype table. Instead it's a plain module-level table `tEvents`, initialized once by `Init()` and
keyed directly by `uGuid`, holding just the one timer-event handle per active beacon (`tEvents[uGuid] =
Event.Create(...)`, cleared in `OnDeactivate`). Lightweight per-object state without the class-factory
machinery.

## Functions
### `Init()`
Initializes the `tEvents` table if it hasn't been initialized yet. This function runs once when the module is loaded.

### `OnActivate(uGuid, args)`
Called when the beacon object is activated by the engine. It plays a material animation and sets up a timer event to play a sound cue after 1 second.

### `OnDeactivate(uGuid, args)`
Called when the beacon object is deactivated by the engine. It stops the material animation and the sound cue, deletes the timer event, and clears the corresponding entry in the `tEvents` table.

## Events
- `OnActivate(uGuid, args)` / `OnDeactivate(uGuid, args)` are engine-invoked lifecycle hooks (not
  `Event.*` subscriptions) — called directly by the engine when the beacon object activates/deactivates.
- **Creates:** `Event.TimerRelative` (1-second one-shot) inside `OnActivate`, whose callback is
  `Sound.CueSound` (an engine API call, not a self-defined function) — plays the `wpn_bomb_timer_01_armed`
  cue. The handle is stored in `tEvents[uGuid]` and deleted via `Event.Delete` in `OnDeactivate`.
- **Fires:** none

## Module constants & tunables
- Material animation: `"global_weapon_beacon"` — started (looping, `true`) in `OnActivate` via
  `Object.PlayMaterialAnimation`, stopped in `OnDeactivate` via `Object.StopMaterialAnimation`. Swap this
  string to change the beacon's visual pulse.
- Sound cue: `"wpn_bomb_timer_01_armed"` — cued via `Sound.CueSound` 1 second after activation, stopped via
  `Sound.StopSound` on deactivate.
- Arm delay: the `Event.TimerRelative` fires after `1` second (inline literal, not a named constant).

## Notes for modders
- Both real levers are the two template strings above: the visual (`"global_weapon_beacon"`) and the audio
  (`"wpn_bomb_timer_01_armed"`). Change either to re-skin the beacon without touching its logic.
- `OnActivate` and `OnDeactivate` are engine lifecycle hooks (see [Object](../namespaces/object) and
  [Sound](../namespaces/sound) for the primitives used) — the engine pairs them, so if you override
  `OnActivate` remember to also stop the animation/sound and delete the timer in `OnDeactivate` or the beacon
  will keep pulsing/beeping after it despawns.