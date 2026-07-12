---
title: StagingAct1
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 8
inherits: none
tags: [utility]
verified: false
---

# StagingAct1

## Overview
`StagingAct1` is a stateless world-dressing module: a small library of AI patrol-setup functions for the
Guerilla base (gate, trailer, road, earthmover, mover-arm, squad, and front patrols). It has no
`inherit()` and is never itself a mission or contract — `xQ!L.lua` `import()`s it once and calls
`StagingAct1.Start()` during gameplay setup, the same boot path that defaults a new game into
[`VzaCon001`](vzacon001).

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Stateless utility module — no `Create`/instance pattern, just module-level functions. `StartPatrol` does
briefly assign one **implicit global**, `tGoalParams` (assigned without `local`), but it's write-then-
immediately-read by the same call rather than meaningful shared state.

## Functions
### `Start()`
The only function `xQ!L.lua` actually calls. As written, it does nothing but log
`"***************Staging Act One is GO GO GO"` — **none of the 7 `GurBase*Patrol` functions below are
called from `Start()` or anywhere else in this file** (confirmed by direct search). Whatever sets these
patrols running in practice must do so some other way (e.g. a region/trigger volume's own embedded script
calling them by name), not through this module's own `Start()`.

### `GurBaseGatePatrol()` / `GurBaseTrailerPatrol()` / `GurBaseRoadPatrolOne()` / `GurBaseEarthmoverPatrol()` / `GurBaseMoverarmPatrol()` / `GurBaseSquadPatrolOne()` / `GurBaseRoadPatrolTwo()` / `GurBaseFrontPatrolOne()`
Each waits for a specific named actor object to wake, then calls `StartPatrol` with that actor, a matching
named path, `"loop"` mode, `"lowpri"` priority, and a fixed haste value (`.1`–`.5` depending on the
patrol). `GurBaseEarthmoverPatrol` has a bug: it waits on `Pg.GetGuidByName("\t")` — a literal tab
character — instead of `Pg.GetGuidByName("Guerilla_Earthmover_Patrol")`, the actor it actually passes to
`StartPatrol` once woken. As written, this function's hibernation-wake watch is on the wrong (almost
certainly nonexistent) object name and likely never fires.

### `StartPatrol(uActor, uTarget, mode, priority, haste)`
Shared helper: defaults `priority` to `"lowpri"` if not given, then schedules an `Ai.Goal` "PathMove" call
(1 second later, via `Event.TimerRelative`) with the given actor/target/mode/priority/haste.

## Events
- `Event.ObjectHibernation` — each `GurBase*Patrol` function waits for its actor to wake before arming the
  patrol.
- `Event.TimerRelative` — `StartPatrol`'s 1-second delay before issuing the actual `Ai.Goal`.

## Notes for modders
- Despite the name, calling `StagingAct1.Start()` does **not** start any of the patrols defined in this
  file — see the `Start()` entry above. If Guerilla-base patrols aren't behaving as expected, look for
  whatever else in the world data calls these `GurBase*Patrol` functions directly, rather than assuming
  `Start()` is the entry point.
- `GurBaseEarthmoverPatrol`'s `Pg.GetGuidByName("\t")` typo (a tab character instead of
  `"Guerilla_Earthmover_Patrol"`) means that one patrol's wake-watch almost certainly never fires as
  written.
- This module has no `inherit()` and isn't part of the `MrxTaskContract`/`MrxTaskJob` mission system at
  all — it's pure world-dressing, called once from the boot sequence rather than from a mission script.
