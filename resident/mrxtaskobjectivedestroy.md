---
title: MrxTaskObjectiveDestroy
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective, destroy]
verified: true
verified_note: deeper pass — re-confirmed both persistent events (ObjectDeath + ScriptEvent "ClientKill"); documented the bHeroOnly config lever (credit only when a hero landed the kill) and the destroy-specific icon overrides; contrasted with MrxTaskObjectiveProtect (same shape, CancelPart instead of CompletePart)
---

# MrxTaskObjectiveDestroy

*Module: mrxtaskobjectivedestroy.lua*

## Overview
The `MrxTaskObjectiveDestroy` module is a specific type of task objective that requires the player to destroy certain game objects. It inherits from `MrxTaskObjective` and adds functionality to handle object destruction events, manage target lists, and provide appropriate icons for different UI elements.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `none`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields:
- `_tEvents`: A table to store event handles.
- `_uTgtObjFilter`: A filter for target objects.

## Functions
### `Activated(self)`
Called when the task objective is activated. It sets up persistent events to listen for object deaths and client kills, and registers them in the `_tEvents` table. It also asserts that the death event handle is valid.

### `_TargetDestroyed(self, uGuid, uCause, uKiller)`
The `Event.ObjectDeath` handler. If config `bHeroOnly` is set, it only counts the kill when `uKiller`
matches one of the players' hero characters (loops `Player.GetAllPlayers()` → `Player.GetCharacter`);
otherwise any death of a valid `userdata` target counts. On a counted kill it `RemoveTarget` + `CompletePart`.
This is the mirror image of [`MrxTaskObjectiveProtect`](mrxtaskobjectiveprotect), which shares this exact
shape but calls `CancelPart` (a protected target dying is a *failure*).

### `_GetShortDescription()`
Returns a short description string for the task objective.

### `GetInlineIcon(self)`
Returns an inline icon based on whether the objective is optional or not.

### `_GetTargetRadarIcon()`
Returns the radar icon for the target object.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon for the target object, depending on whether it's optional or not.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the target object.

### `_IsValidTarget(uGuid)`
A private function that checks if a given GUID is a valid target. It verifies if the GUID corresponds to any player character or an alive object.

## Events
Both `Event.CreatePersistent`, created in `Activated` and stored in `_tEvents`:
- **`Event.ObjectDeath`** (on `self._uTgtObjFilter`) → `_TargetDestroyed`.
- **`Event.ScriptEvent`** with name `"ClientKill"`, filtered by `ObjectFilter.Eval` on the target filter →
  an inline handler that `RemoveTarget` + `CompletePart` for the reported GUID. This is the co-op path so a
  kill made on a client still counts.

Inherits [`MrxTaskObjective`](mrxtaskobjective)'s `Event.TimerRelative` initial-notes timer.

## Notes for modders
- **`bHeroOnly`** (config) restricts credit to kills where a player's hero character was the killer — use it
  for "you personally must destroy X" objectives so an AI or environment kill doesn't count.
- **Choose targets via the filter**, not by editing this module: config `sTgtLabelFilter` /
  `vTgtInclude` / `vTgtExclude` / `nQuota` all flow into the inherited `_uTgtObjFilter` and quota.
- Destroy-specific art overrides: radar `"objective_destroy"`, world `"HUD_objective_destroy"`, PDA
  `"icon_destroy_1_mc"` / `"icon_destroy_2_mc"`, inline `"[objdestroy]"` / `"[objdestroy2]"`.