---
title: Beacon
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [weapon, timer]
verified: true
verified_note: corrected Instance pattern (module-level tEvents keyed by uGuid, not the setmetatable/tInstance pattern) and clarified Events section (OnActivate/OnDeactivate are engine lifecycle hooks, not Event.* listeners).
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

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called in the correct order when extending or modifying beacon behavior.
- The `tEvents` table is used to manage event handles, so be cautious when modifying it directly.