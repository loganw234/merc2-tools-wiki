---
title: AntiAir
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: EnemyBlippable
tags: [anti-air, radar, missile]
---

# AntiAir

*Module: antiair.lua*

## Overview
The `AntiAir` module represents anti-aircraft systems in the game. It manages the activation and deactivation of these systems based on player proximity and handles their radar blips, sound cues, and homing lock-on behavior. The module supports four tiers: basic, medium, advanced, and jammer, each with different properties and behaviors.

## Inheritance
- Inherits from: `EnemyBlippable`
- Imports: `MrxSupport`, `HomingMissile`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tPrototype`: Defines the properties of each anti-air tier.
- `tEvent`: Stores event handles for proximity and distance events.
- `_tLockOns`: Manages homing lock-on states.
- `_tLockOnState`: Tracks targeting and targeted states for players.
- `_tLockOnUpdates`: Handles updates to lock-on states.

## Functions
### `Init(param)`
Initializes the module by setting up metatables for each prototype in `_tPrototype`.

### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It sets up an event to call `Awake` once the object leaves hibernation.

### `Awake(uGuid, iArg)`
Creates a new per-instance table for the object using the module's prototype and activates the anti-air system if within range or creates nearness events otherwise.

### `OnDeactivate(uGuid)`
Tears down the per-instance table by deleting proximity and distance events and calling the base class's `OnDeactivate`.

### `CreateNearnessEvent(uGuid, iArg)`
Creates an event to activate the anti-air system when the player comes within range.

### `ActivateWithEvents(uGuid, iArg)`
Activates the anti-air system and creates a distance event to deactivate it when the player moves out of range.

### `DeactivateWithEvents(uGuid, iArg)`
Deactivates the anti-air system and creates a nearness event to reactivate it when the player comes back within range.

### `ActivateAA(uGuid, iArg)`
Activates the anti-air system by creating an instance based on the prototype for the given tier.

### `CreateDistanceEvent(uGuid, iArg)`
Creates an event to deactivate the anti-air system when the player moves out of range.

### `SetBlipped(oSelf, bCalledByDriver)`
Adds a radar objective and marker for the object. Registers with `MrxSupport.AddAntiAir` if hostile.

### `ClearBlipped(oSelf, bCalledByDriver)`
Removes the radar objective and marker for the object. Clears any active homing lock-on states and unregisters from `MrxSupport.RemoveAntiAir`.

### `_CooldownComplete()`
Resets the alert cooldown flag after a sound cue has been played.

### `_SetSound(bPlay, sCue)`
Plays sound cues based on the type of event and manages cooldowns to prevent rapid alerts.

### `_UpdateHomingState(uPlayerGuid, bTargeted, sAction, bTransfer)`
Updates the targeting and targeted states for players and plays appropriate sound cues.

### `_HomingLockStart(oWidget, tData)`
Initializes a homing lock-on state for an anti-air system.

### `_HomingLockUpdate(oWidget, tData)`
Updates the homing lock-on state based on the lock percentage and player proximity.

### `_HomingLockClear(oWidget, tData, nEvent)`
Clears the homing lock-on state and resets related fields.

### `_HomingLaunched(oWidget, tData)`
Handles the launch of a homing missile by calling into `HomingMissile._HomingLaunched`.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for proximity events (`Event.ObjectProximity`) to activate and deactivate the anti-air system based on player distance.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the anti-air system.
- Customize the behavior by modifying `_tPrototype` fields such as `nAARange`, `sTexture`, and `tMarker`.
- Be aware of the homing lock-on subsystem, which drives targeting tones and visual cues.
- Network synchronization (`bNetSync`) may affect multiplayer behavior, especially in terms of sound cues and radar blips.