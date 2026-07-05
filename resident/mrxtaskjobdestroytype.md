---
title: MrxTaskJobDestroyType
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [task, destroy]
verified: true
verified_note: 'deeper pass: confirmed the whole 55-line source; documented the MrxTaskObjectiveDestroy child
  config (label-filter + quota, [Generic.StandingBounty] default desc, bDspBounty, bHeroOnly), and that
  _GetAutosaveMode returns false here (no per-kill autosave, unlike the MrxTaskJob default true); corrected
  the Events section; cross-linked MrxTaskObjectiveDestroy.'
---

# MrxTaskJobDestroyType

*Module: mrxtaskjobdestroytype.lua*

## Overview
The `MrxTaskJobDestroyType` module is a subclass of `MrxTaskJob` designed to handle tasks where the player must destroy objects filtered by a specific label. It manages the destruction quota, message display settings, and other related task properties.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `none`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskJob`](mrxtaskjob)'s class-factory pattern** (itself inherited from
[`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general mechanism),
identified by name/lineage rather than a world-object GUID. Key fields:
- `_sLabelFilter`: The label filter for the objects to be destroyed.
- `_nQuota`: The quota of objects that need to be destroyed.
- `_bDspMsg`: A boolean indicating whether messages should be displayed.
- `_bHeroOnly`: A boolean indicating if the task is only available to heroes.
- `_bSkipInitialNotifications`: A boolean indicating whether initial notifications should be skipped.
- `_oObjective`: The objective module instance for this task.

## Functions
### `_SetLabelFilter(self, sLabelFilter)`
Sets the label filter for the objects to be destroyed. This function is used to specify which objects should be targeted by the task.

### `_SetQuota(self, nQuota)`
Sets the quota of objects that need to be destroyed. This function determines how many objects must be destroyed to complete the task.

### `_SetMessageDisplay(self, bDspMsg)`
Sets whether messages should be displayed for this task. This function controls the visibility of in-game messages related to the task.

### `_Go(self, fCallback, tCallbackArgs)`
Creates the child [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy) (named `"DestroyType"`) driven by a
**label filter + quota** rather than a named target list: `sTgtLabelFilter = self._sLabelFilter`,
`nQuota = self._nQuota`, `bDspBounty = true`, `bHeroOnly = self._bHeroOnly`, `bDspMsg = self._bDspMsg`,
`bDspMsgUpd = false`, default short desc `"[Generic.StandingBounty]"`. `nPartsCompleted` is seeded from
`self._nTargetsComplete` so progress survives a reload. `fOnActivate` just runs `fCallback` (no nearby-event
wiring — unlike DestroySet, this class never calls `_CreateNearbyEvent`); `fOnPartComplete(uGuid)` → inherited
`_TargetComplete`; `fOnComplete`/`fOnCancel` → `Complete`/`Cancel`.

### `_SetHeroOnly(self, bHeroOnly)`
Sets whether the task is only available to heroes. This function restricts the availability of the task based on player character type.

### `_GetAutosaveMode()`
Overrides the [`MrxTaskJob`](mrxtaskjob) default (`true`) to return **`false`** — this job type does **not**
autosave after each kill. The inherited `_TargetComplete` reads this via `_GetAutosaveMode()`, so a
standing-bounty destroy count won't trigger the per-target `_Checkpoint`/autosave that DestroySet does. This
is the "kill N of a type" repeatable/standing bounty pattern, where checkpointing every kill would be noise.

## Events
No `Event.*` calls, and (unlike [`MrxTaskJobDestroySet`](mrxtaskjobdestroyset)) no proximity/VO event wiring —
`fOnActivate` here does not call `_CreateNearbyEvent`. The four `fOn*` entries are config callbacks on the
child [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy), invoked directly.

## Notes for modders
- **Setup calls:** `_SetLabelFilter` (which world objects count), `_SetQuota` (how many), optionally
  `_SetMessageDisplay(bDspMsg)` and `_SetHeroOnly(bHeroOnly)`. Hero-only restricts credit to the player
  heroes (not AI-driven kills), suited to standing bounties.
- **No autosave per kill** (see `_GetAutosaveMode`) — progress is still saved via `SaveInstance` at normal
  save points, but destroying one more of the type mid-mission won't checkpoint on its own.
- This is the type-filtered counterpart to [`MrxTaskJobDestroySet`](mrxtaskjobdestroyset) (named targets):
  use DestroyType for "destroy 5 of anything with label X," DestroySet for "destroy these specific objects."