---
title: MrxTaskJobCollectType
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [mission, collectible]
verified: true
verified_note: 'deeper pass: confirmed all functions; documented that the child objective is
  MrxTaskObjectiveDestroy (bDspCollectible=true), the CollectableInvalidated label mechanism, and the
  per-item cash reward via Object.GetCashValue + MrxPmc.AddCashQty; cross-linked MrxPmc/MrxStatsManager/
  MrxTaskObjectiveDestroy; corrected Events section (callbacks are objective config fields, not events).'
---

# MrxTaskJobCollectType

*Module: mrxtaskjobcollecttype.lua*

## Overview
The `MrxTaskJobCollectType` module is responsible for managing a mission task where the player needs to collect a quota of label-filtered items. It handles the setup, tracking, and completion of such tasks, providing feedback through objectives and granting rewards upon successful collection.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `MrxPmc`, `MrxStatsManager`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskJob`](mrxtaskjob)'s class-factory pattern** (itself inherited from
[`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general mechanism),
identified by name/lineage rather than a world-object GUID. Key fields:
- `_sLabelFilter`: The label filter for the items to collect.
- `_nQuota`: The quota of items that need to be collected.
- `_oObjective`: The objective instance managing the collection task.
- `_tCollectedItems`: A table tracking which items have been collected.
- `_bSkipInitialNotifications`: Whether initial notifications should be skipped.

## Functions
### `_SetLabelFilter(self, sLabelFilter)`
Sets the label filter for the items to collect. This function is used to specify which items are relevant for the collection task.

### `_SetQuota(self, nQuota)`
Sets the quota of items that need to be collected. This function determines how many items must be gathered to complete the task.

### `_Go(self)`
The activation entry point. Replays any previously-collected items from `self._tSaveData.tCollected`
(marking each collected + disabling it, building an exclude list), then creates the child objective — a
[`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy) named `"CollectType"` with `bDspCollectible = true`,
`sTgtLabelFilter = self._sLabelFilter`, `nQuota = self._nQuota`, and `vTgtExclude` = the already-collected
GUIDs. Its `fOnPartComplete(uGuid)` is where the actual collect reward happens:
[`MrxStatsManager.CompleteToolboxPart`](mrxstatsmanager), then `Object.GetCashValue(uGuid)` →
[`MrxPmc.AddCashQty`](mrxpmc)`(nReward, true, "[Generic.Collectibles]")`, updates the objective's short
description to the item's localized name, records the item, and calls the inherited `_TargetComplete`.
`fOnComplete` → `self:Complete()`, `fOnCancel` → `self:Cancel()`.

{: .note }
> Collection is implemented on top of the **destroy** objective ([`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy)
> with `bDspCollectible`), not a dedicated "collect" objective — "collecting" a label-filtered item is
> modeled as destroying/consuming it.

### `_DisableCollectable(uGuid)`
Adds the `"CollectableInvalidated"` label to an item (`Object.AddLabel`). This is how an already-collected
item is taken out of play on load/replay so it can't be collected twice. Note this is a **module-level
function** (no `self`), called as a bare `_DisableCollectable(uGuid)`.

### `_SetCollectName(self, sCollectName)`
Sets the name for the collection task. This function is used to provide a descriptive name for the task in the game interface.

### `_RecordCollectedItem(self, uGuid)`
Records an item as having been collected. This function updates the internal tracking of collected items and can be called when an item is successfully collected.

### `LoadAssets(self, tSaveData)`
Loads saved data related to the collection task. It restores the state of previously collected items by disabling them if necessary.

### `SaveInstance(self)`
Saves the current state of the collection task. It records which items have been collected so that the progress can be preserved across game sessions.

## Events
No `Event.*` calls of its own. The proximity/VO event wiring comes from [`MrxTaskJob`](mrxtaskjob) (only if
the subclass calls `_CreateNearbyEvent` — this one does not). `fOnPartComplete`/`fOnComplete`/`fOnCancel` are
**config callbacks on the child [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy)**, not event
subscriptions — the objective invokes them directly.

## Notes for modders
- `_SetLabelFilter(sLabelFilter)` + `_SetQuota(nQuota)` are the two required setup calls before `_Go` — the
  label filter picks which world items count, the quota sets how many. Each collected item pays out its own
  `Object.GetCashValue`, credited as `[Generic.Collectibles]`.
- Save/replay uses the `"CollectableInvalidated"` label to disable items already collected; if you author
  custom collectables, that label is what marks one "spent."
- `_SetCollectName` stores `self._sCollectName` but nothing in this file reads it — it's effectively dead
  here (a decompiler-visible setter with no consumer in this module).