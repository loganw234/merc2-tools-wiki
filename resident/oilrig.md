---
title: Oilrig
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [oilrig, destruction]
---

# Oilrig

*Module: oilrig.lua*

## Overview
The `Oilrig` module manages the destruction sequence of oil rig objects in the game. It handles state changes that trigger various destruction events, including sound cues, camera shakes, and timed emitter sequences. The module also ensures proper cleanup when the oil rig is deactivated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxLayerManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tOilrigEvents`: A table to store event handles for each oil rig instance.
- `tTGLayers`: A mapping of GUIDs to layer names used for managing game layers.

## Functions
### `Init()`
Initializes the module by setting up global tables `_tOilrigEvents` and `tTGLayers` if they haven't been initialized yet.

### `Deinit()`
Cleans up all event handles for each oil rig instance and resets the global tables `_tOilrigEvents` and `tTGLayers`.

### `OnDeactivate(uGuid, args)`
Called when the oil rig instance is deactivated. It cleans up any ongoing destruction events and removes associated layers if the object is no longer alive.

### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Handles state changes for the oil rig. When the state hash matches `0x28825D4C`, it initiates the destruction sequence by removing relevant game layers, playing sound cues, shaking the camera, and setting up timed events for various destruction steps. For other states like `0x694683EB`, it plays specific sound cues and shakes the camera.

### `_CleanupOilrigEvents(uiGuid)`
Cleans up all event handles associated with a specific oil rig instance by deleting each event and removing the entry from `_tOilrigEvents`.

### `_FinishDestruction(uiGuid)`
Stops any ongoing camera shake effects and cleans up destruction events for the specified oil rig instance. It then posts an `oilrigDestroyed` event.

### `_DestroyBuildingA(uOilrig)`
Destroys specific parts of building A linked to the oil rig by calling `_DestroyLinkedGuid` with appropriate arguments and scheduling subsequent steps using `_ProcessNextEvent`.

### `_DestroyBuildingB(uOilrig)`
Destroys specific parts of building B linked to the oil rig in a similar manner as `_DestroyBuildingA`.

### `_DestroyBuildingC(uOilrig)`
Destroys specific parts of building C linked to the oil rig.

### `_DestroyBuildingD(uOilrig)`
Destroys specific parts of building D linked to the oil rig.

### `_DestroyOilrigSequence(uOilrig, uNodeHashName)`
Manages the main destruction sequence for the oil rig by starting various emitters, destroying linked objects, setting states, and scheduling subsequent steps using `_ProcessNextEvent`.

### `_ProcessNextEvent(uiGuid, tEventTable, iIndex)`
Processes the next event in a given event table for a specific oil rig instance. It calls the function associated with the current event, schedules the next event if necessary, and handles timing variations.

### `_DestroyLinkedGuid(uParent, sLinkName)`
Destroys a linked object by getting its GUID and calling `Object.Kill` on it. If the linked object does not exist, it logs an error message.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `HideMarker` to remove objectives for hidden objects.

## Notes for modders
- Ensure that `OnDeactivate` is called appropriately to manage cleanup of destruction events and layers.
- Customize the destruction sequence by modifying or extending the `_DestroyOilrigSequence` function.
- Be aware that camera shakes and sound cues are used extensively during the destruction process, which may affect player experience.
- The module uses a timed event system (`_ProcessNextEvent`) to coordinate various destruction steps with delays.