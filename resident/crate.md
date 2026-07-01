---
title: Crate
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [winchable, blip]
---

# Crate

*Module: crate.lua*

## Overview
The `Crate` module represents a winchable crate object in the game world. It manages the crate's blip marker on the minimap and handles its winching state.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks:
- `Marker`: The GUID of the blip marker added to the minimap.
- `Winched`: An event handle for the crate's winching state.

## Functions
### `OnActivate(uGuid)`
Called when the crate instance is spawned/activated. Initializes the crate's state and sets up an event listener for its hibernation state.

### `Awake(uGuid)`
Handles the crate's awakening from hibernation. If the crate is not winched, it adds a blip marker to the minimap. If the crate is winched, it removes any existing blip marker.

### `OnDeactivate(uGuid)`
Called when the crate instance is being torn down (despawned/unloaded). Removes any existing blip marker and deletes all associated events.

### `OnDeath(uGuid)`
Called when the underlying object of the crate dies. Deactivates the crate instance by calling `OnDeactivate`.

## Events
- Listens for: `Event.ObjectHibernation` to handle the crate's awakening.
- Listens for: `Event.ObjectWinched` to update the blip marker based on the crate's winching state.

## Notes for modders
- The crate uses a blip marker with texture `"pickup_crate_2"` and size `48`.
- When the crate is winched, its blip marker is removed from the minimap.
- Ensure that `OnDeactivate` is called to clean up resources when the crate instance is no longer needed.