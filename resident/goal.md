---
title: Goal
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [goal, soccer]
verified: true
verified_note: "deeper pass: re-confirmed all 3 functions and both Event.Create subscriptions against source; surfaced the reward constant (100000), the VO cue Fiona.va3fio12, and the hardcoded boundary names LR_Goal / _global_soccergoal 0x000b0982; replaced vacuous lifecycle boilerplate with actionable levers"
---

# Goal

*Module: goal.lua*

## Overview
The `Goal` module implements a soccer easter egg. When a ball object enters the `LR_Goal` boundary — and a specific named marker (`_global_soccergoal 0x000b0982`) exists in the world — it plays a Fiona voice-over, awards the player 100,000 cash via [MrxPmc](mrxpmc), and removes the goal from the world (fires only once). This is a small, self-contained example of a boundary-triggered reward.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `MrxVoSequence`, `MrxPmc`

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
single module-level global table, `tEvents = tEvents or {}`, with no `Create`/`Delete`/`setmetatable`
anywhere. Each activated object gets a small sub-table entry in `tEvents`, not a full instance object with
inherited methods:
- `tEvents[uGuid]`: initialized to `{}` in `OnActivate`. Its only stored field is `.GoalVO`, the handle of
  the `Event.Boundary` subscription created in `SetupGoal`, so it can be deleted on deactivate.

{: .note }
> `tEvents` is a module-level global, not per-instance state — every activated object shares the one table,
> keyed by `uGuid`. This is fine here because entries are cleaned up in `OnDeactivate`.

## Functions
### `OnActivate(uGuid)`
Called when the goal instance is activated. It logs a debug message and sets up an event to call `SetupGoal` once the object leaves hibernation.

### `OnDeactivate(uGuid)`
Called when the goal instance is deactivated. It logs a debug message, deletes any associated voice-over events, and cleans up the `tEvents` table entry for this GUID.

### `SetupGoal(uBallGuid)`
Registers an `Event.Boundary` subscription (filter `{uBallGuid, LR_Goal, "enter"}`) so that when the ball
crosses into the `LR_Goal` boundary, the reward fires. Guarded twice: it only registers if
`Pg.GetGuidByName("LR_Goal")` resolves, and the reward body only runs if
`Pg.GetGuidByName("_global_soccergoal 0x000b0982")` also exists. On success it plays VO cue `Fiona.va3fio12`
via [MrxVoSequence](mrxvosequence)`.Start`, calls [MrxPmc](mrxpmc)`.AddCashQty(100000)`, and
`Object.Remove`s the `LR_Goal` object. The boundary handle is stored in `tEvents[uBallGuid].GoalVO`.

## Events
- `Event.ObjectHibernation` — registered in `OnActivate` with filter `{uGuid, "awake"}`; fires `SetupGoal`
  once the object leaves hibernation. This is a real `Event.Create` subscription.
- `Event.Boundary` — registered in `SetupGoal` (see above) to detect the ball entering `LR_Goal`.

Note: `OnActivate`/`OnDeactivate` are engine lifecycle callbacks, not event subscriptions.

## Notes for modders
- **Reward knob:** `MrxPmc.AddCashQty(100000)` in `SetupGoal` sets the payout; the VO cue is the literal
  `"Fiona.va3fio12"`. Both are hardcoded in the closure.
- **One-shot:** `Object.Remove(Pg.GetGuidByName("LR_Goal"))` destroys the goal on trigger, so it fires
  exactly once per session — there is no re-arm path.
- **Named-object dependency:** the effect only works if two named world objects exist — the boundary
  `LR_Goal` and the marker `_global_soccergoal 0x000b0982`. If either is missing (e.g. renamed in a mod),
  nothing happens silently.