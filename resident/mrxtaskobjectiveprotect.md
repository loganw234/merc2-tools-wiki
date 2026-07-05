---
title: MrxTaskObjectiveProtect
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective]
verified: true
verified_note: deeper pass — confirmed this is the exact inverse of MrxTaskObjectiveDestroy: same single Event.ObjectDeath subscription and bHeroOnly branch, but _TargetDestroyed calls CancelPart (a protected target dying = failure); documented the defend-specific icon overrides
---

# MrxTaskObjectiveProtect

*Module: mrxtaskobjectiveprotect.lua*

## Overview
`MrxTaskObjectiveProtect` is a "keep these alive" objective — it fails the moment a target dies. Structurally
it is the **inverse of [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy)**: identical single
`Event.ObjectDeath` subscription and `bHeroOnly` branch, but its handler calls `CancelPart` (a dead target is
a loss) where Destroy calls `CompletePart`. It swaps in "defend" art and text.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `none`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields:
- `_tEvents.uDeathEvent`: Event handle for target death events.
- `_uTgtObjFilter`: Filter for target objects.

## Functions
### `Activated(self)`
Called when the task objective is activated. It sets up a persistent event listener for object deaths (`Event.ObjectDeath`) and registers it to call `_TargetDestroyed` when triggered.

### `_TargetDestroyed(self, uGuid, uCause, uKiller)`
Handles the event when a target object dies. Checks if the target should be removed based on configuration settings (e.g., `bHeroOnly`). If the target is valid, it removes the target and cancels any associated parts of the task.

### `_GetShortDescription()`
Returns a short description string for the objective, which is "[Generic.ObjectiveProtect]".

### `_IsValidTarget(uGuid)`
Checks if a given object GUID is a valid target. Returns true if the object is alive or matches any player character.

### `_GetTargetRadarIcon()`
Returns the radar icon for the target, which is "objective_defend".

### `GetInlineIcon(self)`
Returns an inline icon string based on the configuration of the objective. If the objective is optional, it returns "[objdefend2]"; otherwise, it returns "[objdefend]".

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA icon for the target based on whether the objective is optional. Returns "icon_defend_2_mc" if optional; otherwise, returns "icon_defend_1_mc".

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the target, which is "HUD_objective_defend".

## Events
- Listens for `Event.ObjectDeath` to call `_TargetDestroyed` when a target object dies.

## Notes for modders
- **There is no timed "success" here** — a protect objective only *fails* (on target death). Whatever
  parent mission/task owns it decides when protecting is "done enough" (e.g. a sibling objective completing,
  or a timer on the parent task). This class just watches for death.
- **`bHeroOnly`** narrows the fail condition to deaths caused by a player's hero — niche, but present (same
  branch as [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy)).
- Defend art overrides: radar `"objective_defend"`, world `"HUD_objective_defend"`, PDA
  `"icon_defend_1_mc"` / `"icon_defend_2_mc"`, inline `"[objdefend]"` / `"[objdefend2]"`.