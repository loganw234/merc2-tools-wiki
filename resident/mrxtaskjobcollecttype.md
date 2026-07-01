---
title: MrxTaskJobCollectType
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [mission, collectible]
---

# MrxTaskJobCollectType

*Module: mrxtaskjobcollecttype.lua*

## Overview
The `MrxTaskJobCollectType` module is responsible for managing a mission task where the player needs to collect a quota of label-filtered items. It handles the setup, tracking, and completion of such tasks, providing feedback through objectives and granting rewards upon successful collection.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `MrxPmc`, `MrxStatsManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
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
Activates the collection task by excluding already completed targets, adding the task to the PDA, and setting up the objective module. It also handles any previously collected items by disabling them and recording their collection status.

### `_DisableCollectable(uGuid)`
Disables a collectable item by adding the "CollectableInvalidated" label to it. This function is used internally to prevent further collection of already collected items.

### `_SetCollectName(self, sCollectName)`
Sets the name for the collection task. This function is used to provide a descriptive name for the task in the game interface.

### `_RecordCollectedItem(self, uGuid)`
Records an item as having been collected. This function updates the internal tracking of collected items and can be called when an item is successfully collected.

### `LoadAssets(self, tSaveData)`
Loads saved data related to the collection task. It restores the state of previously collected items by disabling them if necessary.

### `SaveInstance(self)`
Saves the current state of the collection task. It records which items have been collected so that the progress can be preserved across game sessions.

## Events
- Listens for engine events through the inherited `MrxTaskJob` methods.
- Responds to internal callbacks within the objective module (`fOnPartComplete`, `fOnComplete`, `fOnCancel`) to handle task completion, cancellation, and individual item collection.

## Notes for modders
- Ensure that `_SetLabelFilter` and `_SetQuota` are called appropriately before activating the task.
- Use `_RecordCollectedItem` to manually record collected items if needed.
- Customize the label filter and quota to fit specific mission requirements.
- Be aware of network synchronization settings if the task is used in multiplayer scenarios.