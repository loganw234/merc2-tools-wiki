---
title: MrxTutorial
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tutorial, manager]
verified: true
verified_note: "deeper pass: re-confirmed all functions/Imports against source; clarified this is the overridable base tutorial class (empty Setup*Criteria hooks are extension points, SetupCompletionCriteria's 20s timer is the only concrete default), corrected the Events section (no custom-event listening in this file), made modder notes actionable"
---

# MrxTutorial

*Module: mrxtutorial.lua*

## Overview
`MrxTutorial` is the **base class for a single tutorial**. It handles the activation / completion / cancellation
lifecycle and the bookkeeping of the events that drive it. It is deliberately generic: the three
`Setup*Criteria` hooks are where a concrete tutorial subclass defines *when* it activates, completes, and
cancels. Out of the box only `SetupCompletionCriteria` does anything (a 20-second auto-complete timer). The
manager that owns the current tutorial and its net-sync is [`MrxTutorialManager`](mrxtutorialmanager).

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
**Empty in the base class — an override point.** A subclass fills this in to register the event(s) (via
`_CreateEvent`/`_CreatePersistentEvent`) whose firing should call `ActivateTutorial`. Called when a tutorial
can't activate yet (or after it ends without completing), so it re-arms itself for next time.

### `SetupCompletionCriteria(self)`
Sets up the criteria for completing the tutorial by creating a relative timer event that triggers `EndTutorial` after 20 seconds.

### `SetupCancellationCriteria(self)`
**Empty in the base class — an override point.** A subclass registers the event(s) that should end the
tutorial *without* completing it (e.g. the player did the wrong thing), typically calling
`EndTutorial(self, false)`.

### `_CreateEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)`
Creates an event with the specified ID and arguments, registers it as a callback, and stores its handle in `_tEvents`.

### `_CreatePersistentEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)`
Creates a persistent event with the specified ID and arguments, registers it as a callback, and stores its handle in `_tEvents`.

## Events
This base class **subscribes to nothing itself**. It only provides the plumbing: `_CreateEvent` wraps
`Event.Create` and `_CreatePersistentEvent` wraps `Event.CreatePersistent`, both stashing the handle in
`self._tEvents` so `DestroyEvents` can tear the whole set down at once. The only event the base class actually
creates is the `Event.TimerRelative` (20 s) in `SetupCompletionCriteria`. Subclasses use these helpers to
register their own criteria events.

## Notes for modders
- **To build a real tutorial, subclass this and override the `Setup*Criteria` hooks** using `self:_CreateEvent`
  / `self:_CreatePersistentEvent` — always create your events through those wrappers so `DestroyEvents` cleans
  them up (otherwise you leak event handles between activations).
- The default `SetupCompletionCriteria` auto-completes after **20 seconds**; override it if your tutorial
  should complete on a real gameplay condition instead of a timeout.
- `ActivateTutorial(self, bDontNetSync)` returns whether activation succeeded; on failure it falls back to
  `SetupActivationCriteria` to try again later. Pass `bDontNetSync = true` on the receiving side in co-op so you
  don't echo the net event back.