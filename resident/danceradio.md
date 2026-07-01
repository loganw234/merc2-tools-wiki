---
title: Danceradio
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [lifestyle prop, animation]
---

# Danceradio

*Module: danceradio.lua*

## Overview
The `Danceradio` module is a lifestyle prop that allows players to perform a dance animation. It provides functionality to handle the activation of the radio, manage player interactions, and synchronize animations across the network.

## Inheritance
- Inherits from: `none`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance table). It tracks the following key fields:
- `tEvents`: A table to store event handles.
- `bAssetLoaded`: A boolean indicating whether the animation asset has been loaded.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the object instance is activated. This function immediately returns without doing anything.

### `OnActivateOld(uGuid, iArg)`
An older activation handler that loads an animation asset and sets up event listeners for the object's hibernation state.

### `OnDeactivate(uGuid)`
Called when the object instance is deactivated. Unloads the animation asset if it was loaded and deletes any registered events.

### `SetupActivationEvents(uGuid)`
Sets up context actions and event listeners for the object, allowing players to interact with it.

### `OnUse(uCharacter, uGuid)`
Handles player interactions with the radio. It determines which player is using the radio, sends a network event if on the server, disables weapons, plays an animation, and sets up a timer to re-enable weapons after the animation completes.

### `Finished(uGuid, uCharacter)`
Called when the dance animation completes. Re-enables weapons for the player and resets the context action.

### `NetEventCallback(nEventType, tArgs)`
A callback function that handles network events. It processes incoming dance requests from other players.

## Events
- Listens for `Event.ObjectHibernation` to call `SetupActivationEvents` when the object leaves hibernation.
- Listens for custom event `DanceRadio` to handle incoming dance requests from other players.

## Notes for modders
- The current implementation of `OnActivate` is disabled (returns immediately). If you want to use this module, consider re-enabling or modifying it.
- Ensure that the animation asset `"player_mattias_bare_technoviking"` is correctly referenced and available in your game assets.
- Be aware that network synchronization (`Net.SendCustomEvent`) may affect multiplayer behavior.