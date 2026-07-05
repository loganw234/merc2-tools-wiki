---
title: Mine
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mine, proximity]
verified: true
verified_note: noted uVehicleFilter is created/configured in Init but never actually used (only uHumanFilter is referenced in the proximity event); corrected OnActivate/OnDeath/Explode details and events section against source.
---

# Mine

*Module: mine.lua*

## Overview
The `Mine` module represents a mine object in the game. It handles the activation, deactivation, and explosion of mines. When activated, it plays an animation and sets up a proximity trigger for human targets. Upon death, it schedules an explosion with different delays based on whether the target is human or a vehicle.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
This module does not follow the per-instance object pattern (keyed by `uGuid`). It manages global state for mine objects, such as event handlers and filters.

## Functions
### `Init()`
Creates `uHumanFilter` and `uVehicleFilter` via `ObjectFilter.Create()` (each only if not already set),
and configures them with `ObjectFilter.SetFilter(uHumanFilter, "human")` /
`ObjectFilter.SetFilter(uVehicleFilter, "vehicle")`. Called once when the module is loaded.
**`uVehicleFilter` is created and configured here but never actually referenced anywhere else in this
file** — only `uHumanFilter` is used, in `OnActivate`'s proximity event. Dead filter as far as this
module's own code goes (it's possible another module reads the same global, but no such reference exists
in this file).

### `Deinit()`
Sets `uHumanFilter` and `uVehicleFilter` to `nil`. This function is called when the module is unloaded.
Note: it does not touch the module-level `uEvent` table.

### `OnActivate(uGuid, uOwner, nArg)`
Called when a mine object is activated. Plays the `"global_weapon_c4land_60thsec"` material animation
(looping — `true`). If `nArg == 2`, registers an `Event.ObjectProximity` listener (filtered to
`uHumanFilter`, distance `< 1`) that calls `Object.Kill(uGuid)` directly as its callback — i.e. a
human-proximity kill mine. If `nArg` is anything else, no proximity trigger is set up (the mine is
presumably triggered some other way, e.g. by damage/explosion from elsewhere).

### `OnDeactivate(uGuid, nArg)`
Called when a mine object is deactivated. Stops the `"global_weapon_c4land_60thsec"` animation and
deletes `uEvent[uGuid]` (`Event.Delete` on whatever's stored there, `nil` if `OnActivate` never set a
proximity event for this `uGuid`), then clears the table entry.

### `OnDeath(uGuid)`
Called when a mine object dies. Cues the `"wpn_bomb_timer_01_finalstage"` sound, clears
`uEvent[uGuid]`, and reads `Object.GetPosition(uGuid)`. If a position was returned, schedules `Explode`
via `Event.TimerRelative` — after **0.75s** with type `"human"` if `Object.HasLabel(uGuid, "HumanMine")`
is true, otherwise after **0.25s** with type `"veh"`.

### `Explode(uGuid, x, y, z, sType)`
Stops the `"wpn_bomb_timer_01_finalstage"` sound and spawns an explosion prefab at `(x, y, z)`:
`"Explosion (Grenade)"` for `sType == "human"`, `"Explosion (AT Mine)"` for `sType == "veh"`, and
`"Explosion (Water Mine)"` for any other value of `sType`. Note `OnDeath` only ever passes `"human"` or
`"veh"` — the third branch (water mine) has no call site in this file.

## Events
- Listens for `Event.ObjectProximity` (registered in `OnActivate`, only when `nArg == 2`) to call
  `Object.Kill` directly when a human-filtered object gets within 1 unit.
- Listens for `Event.TimerRelative` (registered in `OnDeath`) to call `Explode` after a 0.75s or 0.25s delay.

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately to manage global state.
- Use `OnActivate`, `OnDeactivate`, and `OnDeath` to control the lifecycle of mine objects.
- The proximity-kill behavior (`nArg == 2`) only applies to human targets via `uHumanFilter`; there is no
  vehicle-proximity equivalent wired up in this file despite `uVehicleFilter` existing.
- Customize the proximity trigger radius (currently `1`) and explosion delays (`0.75`/`0.25`) by
  modifying the corresponding literals in `OnActivate`/`OnDeath`.
- No network synchronization calls (`Net.*`) appear anywhere in this file — multiplayer behavior for
  mines, if any, is handled elsewhere (e.g. engine-level object replication).