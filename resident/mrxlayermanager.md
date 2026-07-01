---
title: MrxLayerManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [layer management]
---

# MrxLayerManager

*Module: mrxlayermanager.lua*

## Overview
The `MrxLayerManager` module is responsible for managing dynamic and static layers in the game world. It provides functions to add, remove, and mark layers for addition or removal, as well as process these operations with callbacks. This module ensures that layer operations are handled efficiently and within a specified limit.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager utility module. It tracks the following key fields:
- `_tRequests`: A table to store pending layer requests.
- `_tOpQueue`: A table to queue operations for layers.
- `_tLoadedLayers`: A table to track loaded layers.
- `_tLayersToBeAdded`: A table to mark layers for addition.
- `_knRequestTypeAdd` and `_knRequestTypeRemove`: Constants for request types (add/remove).
- `_knLayerStatusUnloaded`, `_knLayerStatusPending`, and `_knLayerStatusLoaded`: Constants for layer statuses.
- `_nLayersBeingProcessed`: Counter for currently processing layers.
- `_knLayersToProcessCap`: Maximum number of concurrent layer operations.

## Functions
### `Init()`
Initializes the module by storing the original asset request maximum from the system.

### `Add(vLayers, fCallback, tCallbackArgs, bCullDupes, bStatic, bClientNeedsLoadingScreen)`
Adds specified layers to the operation queue. It processes each layer and adds it if it meets certain criteria (e.g., exists, not already loaded).

### `Remove(vLayers, fCallback, tCallbackArgs, bClientNeedsLoadingScreen)`
Removes specified layers from the operation queue. It processes each layer and removes it if it meets certain criteria (e.g., exists, not already unloaded).

### `RemoveDynamicLayers(fCallback, tCallbackArgs)`
Removes all dynamic layers by iterating through loaded layers and calling `Remove` with them.

### `RemoveAllLayers(tStaticLayers, fCallback, tCallbackArgs)`
Removes both static and dynamic layers. It combines the provided static layers with loaded layers and calls `Remove`.

### `MarkForRemoval(vLayers)`
Marks specified layers for removal by adding them to `_tLoadedLayers` as true values.

### `MarkForAddition(vLayers)`
Marks specified layers for addition by adding them to `_tLayersToBeAdded` as true values.

### `RemoveMarkedLayers(fCallback, tCallbackArgs)`
Removes all layers that are marked for removal and calls the provided callback with arguments when done.

### `ProcessMarkedLayers(fCallback, tCallbackArgs)`
Processes marked layers for addition or removal. It first removes marked layers and then adds them using callbacks.

### `_AddRequest(nRequestType, vLayers, fCallback, tCallbackArgs, bCullDupes, bStatic, bClientNeedsLoadingScreen)`
A private function to add a new request to the operation queue after processing each layer based on criteria like existence and current status.

### `_ProcessOpQueue()`
Processes the operation queue by handling pending operations within the specified limit (`_knLayersToProcessCap`). It updates the asset request maximum based on the number of pending operations.

### `_LayerStatusChange(sRequestType, sLayerName, sLayerType, bSuccess)`
A private function to handle changes in layer status (load/unload) and update internal state accordingly. It calls callbacks for completed requests.

### `SaveSingleton()`
Saves the current state of loaded layers by returning a list of dynamic and static layers.

### `LoadSingleton(tSaveData, fCallback, tCallbackData)`
Loads the saved data by finding intersections between dynamic and save data layers, then removing and adding layers as needed.

### `ResetState()`
Resets the internal state by clearing all request queues and loaded layer tables.

### `FindLayerIntersection(tR, tA)`
Finds the intersection of two lists of layers (`tR` and `tA`) by sorting them and comparing elements to determine which layers need to be removed or added.

## Events
- Listens for internal state changes through `_LayerStatusChange` to update operations and callbacks accordingly.

## Notes for modders
- Ensure that layer names are correctly formatted (lowercase) when adding or removing layers.
- Use `Add`, `Remove`, `MarkForRemoval`, and `MarkForAddition` functions to manage layers effectively.
- Be aware of the maximum number of concurrent operations (`_knLayersToProcessCap`) to avoid performance issues.
- Customize layer management by adjusting parameters like `bCullDupes`, `bStatic`, and `bClientNeedsLoadingScreen`.
- Use `SaveSingleton` and `LoadSingleton` for saving and loading layer states in game sessions.