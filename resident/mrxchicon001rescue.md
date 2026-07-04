---
title: MrxChiCon001Rescue
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportPickup
tags: [support, rescue]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxChiCon001Rescue

*Module: mrxchicon001rescue.lua*

## Overview
The `MrxChiCon001Rescue` module defines the behavior for a rescue copter support pickup. It inherits from `MrxSupportPickup` and provides functionality to spawn a rescue helicopter, designate a landing zone, and extract prisoners within a specified radius.

## Inheritance
- Inherits from: `MrxSupportPickup`
- Imports: `MrxChiCon001Rescue`, `MrxVoSequence`

## Instance pattern
**Same class-factory pattern as [`MrxSupportPickup`](mrxsupportpickup)/[`MrxSupport`](mrxsupport), not
per-`uGuid`** — `Create(oSelf, uOwnerGuid)` builds a new table via `setmetatable`/`__index`, exactly like
its parent chain. No `OnActivate`/`Awake`, no `tInstance` registry. It tracks the following key fields:
- `oTarget`: The target for the rescue operation.
- `sDeliveryVehicle`: The name of the delivery vehicle (rescue helicopter).
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `oDesignator`: The designator object used to mark the landing zone.

## Functions
### `Create(oSelf, uOwnerGuid)`
Creates a new per-instance table for the rescue support pickup. Initializes the target, sets up the delivery vehicle, and configures the designator with validation functions.

### `AddSupport()`
Adds the rescue copter option to the player's support menu. Iterates through all players and adds an item to their "Support Menu" widget.

### `RemoveSupport()`
Removes the rescue copter option from the player's support menu. Iterates through all players and removes the "Rescue Copter" item from their "Support Menu" widget.

### `DesignationCallback(oSelf)`
Handles the designation callback when a landing zone is marked. Spawns the rescue helicopter at the designated location, sets its orientation, plays a voice sequence, and waits for it to land.

### `_WaitCallback(oSelf, uHeli)`
A helper function that creates an AI goal for the helicopter to land at the designated target location.

### `_VehicleLanded(oSelf, uHeli, uDriver, nState)`
Handles the event when the vehicle lands. Checks if the landing was successful and extracts prisoners within a 60m radius. If no prisoners are found or the landing fails, it aborts the operation and sends the helicopter home.

## Events
- Listens for custom events related to designation and vehicle landing through internal callbacks.

## Notes for modders
- Ensure that `AddSupport` and `RemoveSupport` are called appropriately to manage the rescue copter option in the support menu.
- Customize the behavior by modifying fields like `sDeliveryVehicle` or adjusting the extraction radius.
- Be aware of network synchronization settings if extending this module for multiplayer use.