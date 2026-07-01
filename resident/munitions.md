---
title: Munitions
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [munition, pickup, support]
---

# Munitions

*Module: munitions.lua*

## Overview
The `Munitions` module manages the behavior and interactions of munition objects in the game world. It handles various aspects such as blipping, tagging, picking up, and network synchronization for different types of munitions (support, fuel, cash). The module also manages tutorial messages and voice-over (VO) cues related to these interactions.

## Inheritance
- Inherits from: `Blippable`
- Imports: `MrxGui`, `MrxPlayState`, `MrxPmc`, `MrxSupportData`, `MrxTutorialManager`, `MrxUtil`, `MrxVoSequence`, and `MrxMunitionsPickup`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `nStock`: The type of munition (support, fuel, or cash).
- `bTagged`: Indicates whether the munition has been tagged.
- `bPickedUp`: Indicates whether the munition has been picked up.
- `tContextActions`: Context actions available for the munition.
- `bBlipped`: Indicates whether the munition is currently blipped on the radar.

## Functions

### OnActivate(uGuid, uRuntimeOwner, nStock)
- **Description**: Called when the world object instance is spawned/activated.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
  - `uRuntimeOwner`: Runtime owner of the object.
  - `nStock`: Stock type of the munition.
- **Behavior**: Creates an event to call `Awake` when the object leaves hibernation.

### Awake(uGuid, nStock)
- **Description**: Initializes the instance and sets up blip/marker textures, adds context actions, and registers proximity-near events.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
  - `nStock`: Stock type of the munition.
- **Behavior**: Sets various properties based on the stock type (support, fuel, or cash), adds a context action, and sets up nearness events.

### OnDeactivate(uGuid)
- **Description**: Called when the instance is being torn down.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
- **Behavior**: Handles immediate pickup of hibernated munitions if necessary and calls `Blippable.OnDeactivate`.

### HideTutorialMessage(uGuid)
- **Description**: Hides a tutorial message and deletes the associated event.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.

### SetAllowBlippedVO(bAllow)
- **Description**: Sets whether blipped VO messages are allowed.
- **Parameters**:
  - `bAllow`: Boolean flag to allow or disallow blipped VO messages.

### PlayBlippedVO(nStock)
- **Description**: Plays a blipped VO message based on the stock type and current state.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Behavior**: Checks conditions and plays the appropriate VO cue, sets cooldown timers, and updates played hint flags.

### Near(self)
- **Description**: Called when the player enters the near proximity of the object.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Plays a blipped VO message if in free play mode, sets the object as blipped, sends a network event, and registers farness events.

### Far(self)
- **Description**: Called when the player exits the near proximity of the object.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Clears the blipped state, unregisters farness events, and registers nearness events again.

### AddContextAction(self)
- **Description**: Adds a context action to the object for tagging purposes.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Adds a context action based on the stock type and whether the object is in a vehicle. Handles vehicle-specific events as well.

### CanActionTarget(uGuid, uHero, nStock)
- **Description**: Checks if the munition can be targeted by the player.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
  - `uHero`: Player character GUID.
  - `nStock`: Stock type of the munition.
- **Behavior**: Enforces various conditions such as taggable status, fuel capacity, and support stock limits. Shows tutorial messages if necessary.

### Actioned(self, uHero)
- **Description**: Called when a context action is performed on the object.
- **Parameters**:
  - `self`: The instance table.
  - `uHero`: Player character GUID.
- **Behavior**: Checks if the munition can be targeted and calls `ActionTarget` if conditions are met.

### ActionTarget(uGuid)
- **Description**: Handles the successful action on the object, updating various states and playing VO cues.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
- **Behavior**: Updates context actions, changes marker colors, pulses markers, sends network events, marks the munition as tagged, and plays VO sequences.

### HumanControlled(self, uCharacter)
- **Description**: Handles when a human character takes control of the object (e.g., entering a vehicle).
- **Parameters**:
  - `self`: The instance table.
  - `uCharacter`: Character GUID.
- **Behavior**: Deletes the current instance and sets up events for exiting the vehicle.

### Delete(self)
- **Description**: Tears down the per-instance table, unregistering from various events and updating states.
- **Parameters**:
  - `self`: The instance table.
- **Behavior**: Removes context actions, clears blipped state, deletes events, updates tagged counters, and posts relevant events.

### OnDeath(uGuid)
- **Description**: Called when the object's underlying object dies.
- **Parameters**:
  - `uGuid`: Unique runtime object handle.
- **Behavior**: Calls `Inheritable.OnDeath` and removes context actions if on the client side.

### IsCash(nStock)
- **Description**: Checks if the stock type is cash.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Returns**: Boolean indicating if the stock type is cash.

### IsFuel(nStock)
- **Description**: Checks if the stock type is fuel.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Returns**: Boolean indicating if the stock type is fuel.

### IsSupport(nStock)
- **Description**: Checks if the stock type is support.
- **Parameters**:
  - `nStock`: Stock type of the munition.
- **Returns**: Boolean indicating if the stock type is support.

### SetMunitionsTaggable(bTaggable)
- **Description**: Sets whether munitions are taggable and refreshes relevant states.
- **Parameters**:
  - `bTaggable`: Boolean flag to set munitions as taggable or not.
- **Behavior**: Updates the taggable state, sends network events if necessary, and refreshes context actions.

### AreMunitionsTaggable()
- **Description**: Checks if munitions are currently taggable.
- **Returns**: Boolean indicating if munitions are taggable.

### RefreshMunitions()
- **Description**: Refreshes context actions for all untagged and unpicked up munitions.
- **Behavior**: Iterates through instances, updates context actions based on stock type, and handles non-taggable states.

### SaveSingleton()
- **Description**: Saves the current state of various module-level variables.
- **Returns**: A table containing the saved state.

### LoadSingleton(tSaveData)
Loads saved data for the munitions module. If `tSaveData` is a table, it sets the munitions to be taggable or not based on `bMunitionsTaggable`, and updates various hint flags (`_bPlayedCashHint1`, `_bPlayedFuelHint1`, etc.) from the save data.

### PickupAllMunitions()
Iterates over all instances of munitions in `tInstance` and calls `PickupMunitions(uGuid)` for each one to pick up all munitions.

### PickupMunitions(uGuid)
Handles the pickup logic for a specific munition instance. It checks if the PDA widget is available, retrieves the munition instance from `tInstance`, and processes it based on its type (support, fuel, or cash). If valid, it updates the player's PMC stats, posts an event, sends a custom network event if on the server, marks the munition as picked up, deactivates it, and fades it out if not winched.

### GetTaggedMunition()
Returns the GUID of the first tagged munition found in `tInstance`. If no tagged munition is found, returns `nil`.

### IsMunitionTagged(uMunition)
Checks if a specific munition (identified by its GUID) is tagged. Returns `true` if tagged, otherwise `false`.

### ClientTagAndBlip(uGuid)
Tags and blips a specific munition on the client side. It updates the color of the objective and marker for the munition instance and pulses the marker.

### GetMunitionsCount()
Returns the count of tagged munitions (`_nTagged`). If no munitions are tagged, returns `false` with the message "nomunitions".

### NetEventCallback(nType, tArgs)
Handles network events related to munitions. It processes different event types such as setting munitions taggable, client stockpile queries and acknowledgments, pickup events, marker pulses, and checking if a munition is tagged.

### OnPlayerJoined()
Called when a player joins the game. If on the server, it sends a custom network event to set whether munitions are taggable based on the current state.

## Events

- **Event.ObjectHibernation**: Listens for this event to call `Awake` when the object leaves hibernation.
- **Event.PlayerNear**: Listens for this event to trigger the `Near` function when the player enters the near proximity of the object.
- **Event.PlayerFar**: Listens for this event to trigger the `Far` function when the player exits the near proximity of the object.
- **Event.ObjectDeath**: Listens for this event to call `OnDeath` when the object's underlying object dies.
- **Event.PlayerJoined**: Listens for this event to call `OnPlayerJoined` when a player joins the game.

## Notes for modders

1. **Call-order requirements**:
   - Ensure that `OnActivate` is called before any other lifecycle functions like `Awake`, `Near`, or `Far`.
   - `Delete` should be called when tearing down an instance to properly unregister events and update states.

2. **Pitfalls**:
   - Modifying module-level variables directly can have unintended side effects on all instances.
   - Ensure that network events are handled correctly to maintain consistency across clients.

3. **Tunables**:
   - `_kDistance`: Adjust this value to change the distance threshold for blip near/far.
   - `_nBlippedVOCoolDownTime`: Modify this value to adjust the cooldown time for blipped VO messages.

4. **Decompiler artifacts**:
   - Some local variables may appear unused or are assigned but never read, which is a decompiler artifact and should be ignored.