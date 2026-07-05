---
title: Init
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [init, sound]
verified: true
verified_note: "deeper pass: surfaced the concrete tunables (material anim global_weapon_c4land_30thsec, sound cue wpn_bomb_timer_01_armed, 1s delay), pruned vacuous notes; Events section re-confirmed (only Event.TimerRelative is real)"
---

# Init

*Module: Init.lua*

## Overview
The `Init` module is responsible for initializing a global table to manage events and handling the activation and deactivation of world objects. It specifically manages a timer that triggers a sound cue when an object is activated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state but uses a global table `tEvents` to manage event handles associated with world objects.

## Functions
### `Init()`
Initializes the global `tEvents` table if it hasn't been initialized yet. This function ensures that there's a table available to store event handles for different world object instances.

### `OnActivate(uGuid, args)`
Called when a world object instance is activated. Plays the material animation `"global_weapon_c4land_30thsec"`
on the object (`Object.PlayMaterialAnimation`, looping), then schedules — via `Event.TimerRelative` with a
`1`-second delay, stored in `tEvents[uGuid]` — a `Sound.CueSound(uGuid, "wpn_bomb_timer_01_armed")` one second
after activation.

### `OnDeactivate(uGuid, args)`
Called when a world object instance is deactivated. Stops the `"global_weapon_c4land_30thsec"` material
animation (`Object.StopMaterialAnimation`), stops the `"wpn_bomb_timer_01_armed"` sound
(`Sound.StopSound`), deletes the timer event, and clears `tEvents[uGuid]`.

## Events
- Fires `Event.TimerRelative` (in `OnActivate`) to schedule `Sound.CueSound` one second after activation.
- `OnActivate` and `OnDeactivate` are engine-invoked lifecycle callbacks, not `Event.*` subscriptions —
  they are the entry/exit points the engine calls directly on world-object activate/deactivate, not
  something this module registers via `Event.Create`.

## Notes for modders
- **The tunables here are three strings and one number:** the material animation
  `"global_weapon_c4land_30thsec"`, the sound cue `"wpn_bomb_timer_01_armed"`, and the `1`-second delay in
  the `Event.TimerRelative` call. Swap those to change what an activated object animates/sounds like and how
  long it waits before the cue.
- The animation and cue names both reference C4/bomb-timer assets — this module is the "armed
  countdown" glue for a placeable explosive-style object, not a general-purpose base class.
- `Init()` only guards `tEvents` (`tEvents = tEvents or {}`); it doesn't need calling per-object. The
  engine drives `OnActivate`/`OnDeactivate` by naming convention — you don't call them yourself.