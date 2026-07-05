---
title: Emplaced
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, gunner]
verified: true
verified_note: 'deeper pass: corrected the Instance pattern (bare uEvent[uGuid] bookkeeping, not "stateless"), split the two Event.ObjectInSeat Gunner enter/exit subscriptions, surfaced the Graphics.Camera.SetFocusParams(0,0,2,2,600,4,0) tunable + "Gunner" seat, and replaced vacuous Notes with the real camera lever + local-player-only caveat'
---

# Emplaced

*Module: emplaced.lua*

## Overview
The `Emplaced` module manages the behavior of emplaced weapons, specifically handling events related to a player entering and exiting a gunner seat. It sets camera focus parameters when a player enters the seat and restores them when they exit.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
Bare `tGuids`-style bookkeeping, **not** stateless and **not** the `Inheritable` rich-instance pattern.
State lives in one module-level global table, `uEvent`, keyed by `uGuid` (`uEvent[uGuid] = uEvent[uGuid] or
{}`), holding just two handles per active weapon: `uEvent[uGuid].Enter` and `uEvent[uGuid].Exit`. There is no
`Create`/`setmetatable`/`tInstance` factory. `Init()` seeds the table and `Deinit()` drops it wholesale.

## Functions
### `Init()`
Initializes the `uEvent` table if it hasn't been initialized yet.

### `Deinit()`
Sets the `uEvent` table to `nil`, effectively cleaning up any stored event handles.

### `OnActivate(uGuid, uOwner, nArg)`
Called when an emplaced weapon instance is activated. It sets up an event to call `Activate` once the object leaves hibernation.

### `Activate(uGuid)`
Creates an enter event for the specified `uGuid`.

### `CreateEnterEvent(uGuid)`
Creates an event that listens for a player entering the gunner seat and calls the `Enter` function when triggered.

### `CreateExitEvent(uGuid, uChar)`
Creates an event that listens for a player exiting the gunner seat and calls the `Exit` function when triggered.

### `Enter(uChar, uGuid)`
Handles the event where a player enters the gunner seat. It checks if the character is controlled by a local player and sets the camera focus parameters accordingly. Then, it creates an exit event for the same seat.

### `Exit(uChar, uGuid)`
Handles the event where a player exits the gunner seat. It checks if the character is controlled by a local player and restores the camera focus parameters to their default state. Then, it creates an enter event for the same seat.

### `OnDeactivate(uGuid, nArg)`
Called when an emplaced weapon instance is deactivated. It deletes any stored enter and exit events associated with the specified `uGuid`.

## Events
- **Creates** `Event.ObjectHibernation` (`OnActivate`) to call `Activate` when the object leaves hibernation.
- **Creates** `Event.ObjectInSeat` with the `"Gunner"` seat + `"enter"` filter (`CreateEnterEvent`) to call
  `Enter`. Stored as `uEvent[uGuid].Enter`.
- **Creates** `Event.ObjectInSeat` with the `"Gunner"` seat + `"exit"` filter (`CreateExitEvent`) to call
  `Exit`. Stored as `uEvent[uGuid].Exit`. The enter/exit listeners are re-armed alternately (`Enter` creates
  the exit listener, `Exit` re-creates the enter listener), so only one is live at a time.
- `OnActivate`/`OnDeactivate` are engine lifecycle callbacks, not `Event.*` subscriptions.

## Module constants & tunables
- Seat name filter: `"Gunner"` (both enter and exit events).
- Camera on entering the seat: `Graphics.Camera.SetFocusParams(0, 0, 2, 2, 600, 4, 0)`; on exit:
  `Graphics.Camera.RestoreFocusParams(0, 0)`. These seven numbers are the whole "zoom/focus feel" of manning
  the emplaced weapon — the only real tuning lever in the file.

## Notes for modders
- The single meaningful mod lever is the camera call: change the `Graphics.Camera.SetFocusParams(...)`
  arguments to alter how the view snaps when the player mounts the gun (see the
  [Camera namespace](../namespaces/camera) / [Graphics namespace](../namespaces/graphics)).
- Only **local player** characters trigger the focus change — non-players and remote players hit an early
  return with a `Debug.Printf` log line ("A non-player triggered this event!"), so don't rely on this for AI
  gunners.