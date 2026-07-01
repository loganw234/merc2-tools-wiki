---
title: Emplaced
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, gunner]
---

# Emplaced

*Module: emplaced.lua*

## Overview
The `Emplaced` module manages the behavior of emplaced weapons, specifically handling events related to a player entering and exiting a gunner seat. It sets camera focus parameters when a player enters the seat and restores them when they exit.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It tracks event handles in the `uEvent` table, keyed by `uGuid`.

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
- Listens for `Event.ObjectHibernation` to call `Activate` when the object leaves hibernation.
- Listens for `Event.ObjectInSeat` (enter) to call `Enter` when a player enters the gunner seat.
- Listens for `Event.ObjectInSeat` (exit) to call `Exit` when a player exits the gunner seat.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage event lifecycle.
- Customize camera focus parameters by modifying the values passed to `Graphics.Camera.SetFocusParams`.
- Be aware that non-local players triggering these events will result in debug messages being logged.