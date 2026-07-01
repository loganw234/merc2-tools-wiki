---
title: MrxFollow
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [ai, companion]
---

# MrxFollow

*Module: mrxfollow.lua*

## Overview
The `MrxFollow` module manages the escort/follow behavior for companion characters in the game. It handles toggling between follow and idle roles, managing voice-over sequences, and handling transitions into transit vehicles.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxVoSequence`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tEvents`: Table to store event handles.
- `iStartVOIdx`, `iStopVOIdx`, `iLostVOIdx`, `iFoundVOIdx`, `iHostileVOIdx`, `iHostileRecoveredVOIdx`: Indices for voice-over sequences.
- `_vActor`: The actor (character) that is following.
- `_vObjectToFollow`: The object or character being followed.
- `_fCallback`: Callback function for state changes.
- `_tCallbackData`: Data passed to the callback function.
- `bVOOverride`: Flag to override voice-over behavior.

## Functions
### `Create(mModule, self)`
Initializes a new instance of the `MrxFollow` module. Sets up metatable and initializes event indices.

### `SetActor(self, vActor)`
Sets the actor (character) that will be following.

### `SetObjectToFollow(self, vObjectToFollow)`
Sets the object or character to follow.

### `SetCallback(self, fCallback, tData)`
Sets a callback function and associated data for state changes.

### `Activate(self, bEnable, bStartInFollowState)`
Activates or deactivates the follow behavior. If enabled, it sets up the actor and target, toggles following behavior, and manages voice-over sequences. If disabled, it stops following and cleans up events.

### `_Follow(self, bEnable, vObjectToFollow)`
Toggles the follow behavior on or off for the specified object.

### `_ToggleFollowingBehavior(self, bEnable, vObjectToFollow)`
Manages the AI role between "Follow" and "Idle". Sets feelings, creates roles with callbacks, and manages voice-over sequences.

### `_ToggleContextAction(self, bEnable)`
Adds or removes a context action ("Follow"/"Stay") for the actor.

### `_RemoveContextAction(self)`
Removes any existing context action for the actor.

### `_GetActorGuid(vActor)`
Retrieves the GUID of the actor based on its type (string or userdata).

### `_OnFollowerCanceled(self, uGuid, sReason)`
Handles cancellation of following due to various reasons ("targettoofar", "targethostile", "targetdead"). Triggers appropriate actions like losing or finding the target.

### `_OnFollowerLost(self)`
Plays a voice-over sequence when the follower is lost and sets up an event to re-acquire the target when it gets close enough.

### `_OnFollowerFound(self)`
Plays a voice-over sequence when the follower is found and resumes following.

### `_OnFollowerHostile(self)`
Plays a voice-over sequence when the target becomes hostile.

### `_PlayVO(self, tTable, iIndex)`
Plays a voice-over sequence from a table of sequences. Cycles through the table if necessary.

### `_TransitEvalFn(tData)`
Evaluation function for transit events.

### `_OnTransitStart(self, tData)`
Handles entering a transit vehicle by attempting to board it and setting up an event for when the transit ends.

### `_OnTransitEnd(self, tData)`
Handles exiting a transit vehicle and sets up an event for when the transit starts again.

## Events
- Listens for `Event.ScriptEvent` with `"mpPlayerLeft"` to handle player leaving.
- Listens for `Event.ScriptEvent` with `"transitStart"` to handle entering transit vehicles.
- Listens for `Event.ObjectProximity` to re-acquire lost targets.
- Listens for `Event.ContextAction` to toggle follow/idle roles.

## Notes for modders
- Ensure that `Activate` is called appropriately to manage the follow behavior lifecycle.
- Customize voice-over sequences by modifying the indices and tables in the instance.
- Be aware of network synchronization and multiplayer implications when using this module.