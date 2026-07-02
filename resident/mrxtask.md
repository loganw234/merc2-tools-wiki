---
title: MrxTask
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [task, mission]
---

# MrxTask

*Module: mrxtask.lua*

## Overview
The `MrxTask` module is the base class for all mission-related tasks in the game. It manages the lifecycle of tasks, including their configuration, activation, completion, and cancellation. Each task can have child tasks, forming a hierarchical tree structure. The module also handles asset loading, event management, and state transitions.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxLayerManager`, `MrxTaskState`, `MrxTimer`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tChildren`: A table of child tasks, keyed by name.
- `_tConfig`: Configuration settings for the task.
- `_bCleanedUp`: Indicates whether the task has been cleaned up.
- `_oTimer`: A timer associated with the task.
- `_tEvents`: Handles for events registered by the task.
- `_nState`: The current state of the task (latent, active, completed, cancelled).
- `_tSaveData`: Saved data for the task.

## Functions
### `Create(mModule, self)`
Creates a new instance of the `MrxTask` module. Initializes the task's configuration and children map.

### `Cleanup(self)`
Cleans up the task by removing it from its parent, stopping any associated timers, deleting registered events, and cleaning up child tasks. Marks the task as cleaned up.

### `IsLiveConfigureable(self, sConfigKey)`
Checks if a given configuration key can be modified while the task is active.

### `ReinterpretConfig(self)`
Reinterprets the task's configuration after it has been activated.

### `CreateChild(self, tConfig)`
Creates and configures a new child task under this task. Activates the child task and returns it.

### `Activated(self)`
Activates the task by setting its state to active and starting any associated timers or time limits.

### `Complete(self)`
Marks the task as completed, cleans up resources, and issues completion callbacks.

### `Cancel(self)`
Cancels the task, cleans up resources, and issues cancellation callbacks.

### `_SetState(self, nState)`
Sets the current state of the task. Propagates the new state to child tasks if the task is completed or cancelled.

### `_IssueStateChangeCallbacks(self)`
Issues callbacks for state changes based on the current state of the task.

### `_SetChildrenState(self, nState)`
Recursively sets the state of all child tasks to the specified state.

### `_ResetState(self)`
Resets the task's state to latent.

### `IsLatent(self)`
Checks if the task is in a latent (inactive) state.

### `IsActive(self)`
Checks if the task is active.

### `IsCompleted(self)`
Checks if the task has been completed.

### `IsCancelled(self)`
Checks if the task has been cancelled.

### `_GetState(self)`
Returns the current state of the task.

### `Configure(self, tConfig)`
Configures the task with the provided settings. Allows configuration during both latent and active states, with restrictions on live configuration keys.

### `GetConfig(self)`
Retrieves the current configuration of the task.

### `AddCallback(self, sConfigKey, fCallback, tData)`
Adds a callback to the specified configuration key. The callback is executed when the task's state changes or assets are loaded.

### `Activate(self, tSaveData)`
Activates the task by resetting its state and loading necessary assets. If a module name is provided in the configuration, it dynamically imports the module.

### `_ModuleLoaded(self, mModule)`
Handles the dynamic import of a module for the task. Sets the module as the metatable for the task instance and proceeds with asset loading.

### `PreLoadAssets(self)`
A placeholder function intended for pre-loading assets before full asset loading.

### `LoadAssets(self, tSaveData)`
Loads necessary assets for the task. Adds layers to the layer manager if specified in the configuration.

### `AssetsLoaded(self)`
Called when all assets have been loaded. Issues any registered callbacks and activates the task.

### `_IssueAssetsLoadedCallbacks(self)`
Issues callbacks for asset loading completion.

### `_AddChild(self, oChild)`
Adds a child task to this task's children map.

### `_RemoveChild(self, sChildName)`
Removes a child task from this task's children map.

### `GetChild(self, sChildName)`
Retrieves a child task by name.

### `_AddChildren(self, tChildren)`
Adds multiple child tasks to this task's children map.

### `GetChildren(self)`
Retrieves the map of all child tasks.

### `GetName(self)`
Returns the name of the task as specified in its configuration.

### `GetTitle(self)`
Returns the title of the task as specified in its configuration.

### `GetParent(self)`
Retrieves the parent task of this task.

### `GetLineage(self)`
Generates a lineage string representing the hierarchical path from the root to this task.

### `SaveInstance(self)`
Saves the current state of the task, including its state and any saved data.

### `_GetSaveData(self)`
Retrieves the saved data for the task.

### `_SetSaveData(self, tSaveData)`
Sets the saved data for the task.

### `_GetRewards(self)`
Returns default rewards (cash and fuel) associated with completing the task. Default values are zero.

### `_CanCompleteViaCheatMenu()`
Indicates whether the task can be completed via the cheat menu. Returns true by default.

### `_CreateEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)`
Creates an event and registers it with the task. The event is automatically cleaned up when the task is cleaned up.

### `_CreatePersistentEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)`
Creates a persistent event and registers it with the task. Persistent events are not automatically cleaned up.

### `GetStub(self)`
Returns the task instance itself as a stub.

### `_SetTask(self, oTask)`
Sets an associated task for this task.

### `GetTask(self)`
Retrieves the associated task.

## Events
- Listens for custom events to manage task state and asset loading.
- Issues callbacks for state changes and asset loading completion.

## Notes for modders
- Ensure that tasks are properly activated and cleaned up to avoid resource leaks.
- Use the `Configure` function to set or modify task configurations, especially during development.
- Be cautious with live configuration keys to avoid unintended behavior while tasks are active.
- Utilize callbacks to handle state changes and asset loading events for custom task logic.