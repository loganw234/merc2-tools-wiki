---
title: Laptop
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [pickup, support]
---

# Laptop

*Module: laptop.lua*

## Overview
The `Laptop` module represents a fixed support-munition pickup in the game world. It handles the creation, activation, and deletion of laptop objects, as well as managing their radar blips and player interactions.

## Inheritance
- Inherits from: `Blippable`
- Imports: `MrxGui`, `MrxPmc`, `MrxSupportData`, `MrxTutorialManager`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `nStock`: The type of munition or resource associated with the laptop.
- `TaggedMarker`: A reference to any tagged marker associated with the laptop.
- `_uHideMessage`: An event handle for hiding messages.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, nStock)`
Called when the object instance is activated. It sets up an event to call `Awake` once the object leaves hibernation.

### `Awake(uGuid, nStock)`
Creates a new per-instance table for the laptop using the module's prototype. Configures the radar blip and marker properties based on predefined constants and initializes the laptop with the specified stock type.

### `Delete(oSelf)`
Tears down the per-instance table by clearing any active blips, removing tagged markers, and calling the base class's `Delete`.

### `OnDeath(uGuid)`
Called when the object instance dies. It ensures that the death event is properly handled by the inheritance chain.

### `PickupMunitions(oInstance)`
Handles the player interaction with the laptop, updating the player's support resources, playing a voice cue, and posting a "MunitionsPickup" event.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `WeaponEvent` with parameters `"hero", "pickup", "Laptop"` to trigger `PickupMunitions`.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage laptop lifecycle.
- Customize the stock types by modifying the `tMunitions` table.
- Be aware of network synchronization settings, as they may affect multiplayer behavior.
- The `_kDistance` constant defines the blip distance for laptops.