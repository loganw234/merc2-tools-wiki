---
title: MrxTutorial
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tutorial, manager]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxTutorial

*Module: mrxtutorial.lua*

## Overview
The `MrxTutorial` module is responsible for managing in-game tutorials. It handles the activation, completion, and cancellation of tutorials, as well as setting up event-driven criteria for these actions.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxTutorialManager`

## Instance pattern
**Not per-`uGuid`** — same class-factory pattern used elsewhere in `resident/`: `Create(mModule, self)` is
`self = self or {}; setmetatable(self, {__index = mModule}); return self`, no `tInstance` registry. It
tracks the following key fields:
- `_tEvents`: A table to store handles of created events.
- `sName`: The name of the tutorial.

## Functions
### `Create(mModule, self)`
Constructs a new per-instance table for the tutorial using the module's prototype. Initializes an empty table for event handles.

### `DestroyEvents(self)`
Destroys all registered events by deleting them and clearing the `_tEvents` table.

### `GetName(self)`
Returns the name of the tutorial.

### `ActivateTutorial(self, bDontNetSync)`
Activates the current tutorial using `MrxTutorialManager.SetCurrentTutorial`. Destroys any existing events and sets up completion or activation criteria based on success.

### `EndTutorial(self, bComplete)`
Ends the current tutorial using `MrxTutorialManager.HideCurrentTutorial`. Destroys all registered events and either destroys the tutorial if completed or sets up activation criteria otherwise.

### `SetupActivationCriteria(self)`
Sets up the criteria for activating the tutorial. This function is currently empty.

### `SetupCompletionCriteria(self)`
Sets up the criteria for completing the tutorial by creating a relative timer event that triggers `EndTutorial` after 20 seconds.

### `SetupCancellationCriteria(self)`
Sets up the criteria for canceling the tutorial. This function is currently empty.

### `_CreateEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)`
Creates an event with the specified ID and arguments, registers it as a callback, and stores its handle in `_tEvents`.

### `_CreatePersistentEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)`
Creates a persistent event with the specified ID and arguments, registers it as a callback, and stores its handle in `_tEvents`.

## Events
- Listens for custom events to manage tutorial lifecycle (activation, completion, cancellation).

## Notes for modders
- Ensure that `ActivateTutorial` and `EndTutorial` are called appropriately to manage the tutorial's lifecycle.
- Customize event-driven criteria by extending `SetupActivationCriteria`, `SetupCompletionCriteria`, or `SetupCancellationCriteria`.
- Be aware of network synchronization (`bDontNetSync`) when activating tutorials in multiplayer scenarios.