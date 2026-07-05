---
title: MrxFollow
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, companion]
verified: true
verified_note: "deeper pass: surfaced the follow-role distance tunables (Min 2 / Max kMaxFollowDistance=30 / Move 4, re-acquire proximity 15), the context-action labels, and the five VO tables; documented the usage flow; all functions/events re-confirmed against source"
---

# MrxFollow

*Module: mrxfollow.lua*

## Overview
The `MrxFollow` module manages the escort/follow behavior for companion characters in the game. It handles toggling between follow and idle roles, managing voice-over sequences, and handling transitions into transit vehicles.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxVoSequence`](mrxvosequence)

## Instance pattern
**Not per-`uGuid` — same class-factory pattern as [`MrxTask`](mrxtask)**: `Create(mModule, self)` does
`self = self or {}; setmetatable(self, {__index = mModule})`, no `tInstance` registry anywhere in source.
Key fields:
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
Manages the AI role between `"Follow"` and `"Idle"` (via `Ai.Role`). On enable: turns off the actor's
`"LivingWorldBehaviour"`, forces friendly feeling toward the target if `Ai.GetFeeling < 0`
(`Ai.SetFeeling(..., 100)`), then creates a hard-priority `"Follow"` role with `MinDistance = 2`,
`MaxDistance = kMaxFollowDistance` (`30`), `MoveDistance = 4`, `Priority = "hiPri"`, and
`Callback = _OnFollowerCanceled`. It also wires the `mpPlayerLeft` and `transitStart` `Event.ScriptEvent`
listeners. On disable: tears those down and swaps in an `"Idle"` `hiPri` role. Fires start/stop VO unless
`bVOOverride` is set, then invokes the state-change callback with `(uGuid, bEnable)` appended.

### `_ToggleContextAction(self, bEnable)`
Adds or removes a context action for the actor via `Pg.AddContextAction`, using the localized labels
`"[ContextAction.Follow]"` (when idle) / `"[ContextAction.Stay]"` (when following), and wires an
`Event.ContextAction` listener that toggles `_Follow` when the player activates it.

### `_RemoveContextAction(self)`
Removes any existing context action for the actor.

### `_GetActorGuid(vActor)`
Retrieves the GUID of the actor based on its type (string or userdata).

### `_OnFollowerCanceled(self, uGuid, sReason)`
Handles cancellation of following due to various reasons ("targettoofar", "targethostile", "targetdead"). Triggers appropriate actions like losing or finding the target.

### `_OnFollowerLost(self)`
Plays the "lost" VO, then registers an `Event.ObjectProximity` listener that re-acquires the target
(`_OnFollowerFound`) once the actor comes within `15` metres (`"<", 15`) of `_vObjectToFollow`.

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
- **Distance tunables** (all in `_ToggleFollowingBehavior`/`_OnFollowerLost`): `"Follow"` role
  `MinDistance = 2`, `MaxDistance = kMaxFollowDistance = 30`, `MoveDistance = 4`; the lost-target
  re-acquire proximity is `15`. `kMaxFollowDistance` is a `local` inside `_ToggleFollowingBehavior`, so
  changing the leash means editing that function, not an instance field.
- **VO is driven by tables you supply on the instance**: `tStartFollowVO`, `tStopFollowVO`, `tLostVO`,
  `tFoundVO`, `tHostileVO` — each an array of cue entries `_PlayVO` cycles through (it wraps at the end and
  advances the matching `i*VOIdx`). Leave them unset for a silent companion.
- **The follow toggle also grabs a context action** (`"[ContextAction.Follow]"`/`"[ContextAction.Stay]"`),
  so the player gets an on-foot prompt to start/stop the escort — that's the intended player-facing hook.
- Usage flow: `SetActor` -> `SetObjectToFollow` (optional; defaults to the local character) ->
  `SetCallback` (optional) -> `Activate(true, bStartInFollowState)`. `Activate(false)` tears everything down.