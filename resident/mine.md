---
title: Mine
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mine, proximity]
verified: true
verified_note: "deeper pass: re-confirmed all 5 functions; consolidated the high-value constants (proximity radius 1, delays 0.75s/0.25s, animation global_weapon_c4land_60thsec, sound wpn_bomb_timer_01_finalstage, and the three Explosion (...) spawn prefabs) into a tunables block; re-confirmed uVehicleFilter is dead in this file"
---

# Mine

*Module: mine.lua*

## Overview
The `Mine` module represents a mine object in the game. It handles the activation, deactivation, and explosion of mines. When activated, it plays an animation and sets up a proximity trigger for human targets. Upon death, it schedules an explosion with different delays based on whether the target is human or a vehicle.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
Not the `Inheritable` rich-instance pattern — no `Create`/`setmetatable`/`tInstance` registry. State lives
in module-level globals:
- `uEvent`: `uGuid -> proximity-event handle` (only populated for `nArg == 2` mines).
- `uHumanFilter`, `uVehicleFilter`: shared `ObjectFilter` handles built once in `Init` (the vehicle one is
  dead — see Functions).

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

## Module constants & tunables
| Value | Where | Role |
| --- | --- | --- |
| `"global_weapon_c4land_60thsec"` | `OnActivate`/`OnDeactivate` | looping material animation (the blinking C4) |
| `1` | `OnActivate` proximity filter | trigger radius (distance `<` 1) for `nArg == 2` mines |
| `"wpn_bomb_timer_01_finalstage"` | `OnDeath`/`Explode` | pre-detonation "beep" sound cue |
| `0.75` / `0.25` s | `OnDeath` | fuse delay — 0.75 s for `HumanMine`-labelled, else 0.25 s |
| `"Explosion (Grenade)"` | `Explode` (`"human"`) | spawned via `Pg.Spawn` at the mine's position |
| `"Explosion (AT Mine)"` | `Explode` (`"veh"`) | spawned for non-`HumanMine` mines |
| `"Explosion (Water Mine)"` | `Explode` (else) | third branch — **no call site in this file** |

## Notes for modders
- **The two mine flavors** are chosen at activation by `nArg` (== 2 → human proximity-kill) and at death by
  the `"HumanMine"` object label (grenade blast + 0.75 s vs. AT-mine blast + 0.25 s). Change those to
  re-tune behavior.
- **`nArg` matters:** only `nArg == 2` arms a proximity trigger. Any other value leaves the mine inert to
  proximity — it must be detonated some other way (damage/`OnDeath` from elsewhere).
- The proximity-kill path only filters `uHumanFilter`; `uVehicleFilter` is built in `Init` but never
  referenced here, so there is no vehicle-proximity trigger in this module.
- Swap the `Pg.Spawn("Explosion (...)")` prefab names to change the blast effect. The `"Explosion (Water
  Mine)"` branch is unreachable from this file's own code path.
- No `Net.*` calls appear here — multiplayer replication of mines, if any, is engine-level, not scripted.