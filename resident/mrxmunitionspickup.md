---
title: MrxMunitionsPickup
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [pickup, transit]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxMunitionsPickup

*Module: mrxmunitionspickup.lua*

## Overview
The `MrxMunitionsPickup` module is responsible for handling the pickup of tagged munitions by a heli. It inherits from `MrxSupport` and manages the spawning, targeting, and retrieval of munitions by a designated vehicle. The module also handles voice-over sequences and faction infraction logic when munitions are picked up.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `Munitions`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oTarget`: The target for the pickup operation.
- `sDeliveryVehicle`: The name of the vehicle template used for delivery.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `oUpdateEvent`: An event handle for periodic updates.
- `oDesignator`: A designator object for targeting.
- `oFinalDestination`: The final destination point for the pickup operation.
- `bPickupInProgress`: A flag indicating if a pickup is currently in progress.
- `tImmediatePickupData`: Data used for immediate pickup operations.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the object using the module's prototype. Initializes the delivery vehicle and designator settings.

### `DesignationCallback(self)`
A callback function that handles designation events.

### `SetDeliveryVehicle(self, sVehicleTemplateName)`
Sets the delivery vehicle template name and updates the GUID accordingly.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point for the pickup operation.

### `_DesignatorCallback(self)`
Handles the designator callback logic, spawning the delivery vehicle at the designated target position and setting its orientation.

### `_WaitCallback(self, uHeli)`
Called after the heli wakes up. Starts a voice-over sequence, sets up damage event handling, and begins picking up munitions.

### `PickMunitionsTarget(self, uHeli)`
Detaches cargo from the winch, gets tagged munitions, and sets up events to handle various scenarios (e.g., no munitions, untagged munitions).

### `ImmediatePickup()`
Handles immediate pickup operations by cancelling relevant events, removing objects, and updating faction infraction logic.

### `Pickup(self, uHeli, uDriver, pu, nState)`
Handles the actual pickup of munitions. Updates faction infraction, picks up all tagged munitions, and returns the heli to its home position.

## Events
- Listens for custom event `DesignationCallback` to handle designation events.
- Listens for various other custom events (`NoMunitions`, `UntagMunitions`, etc.) to manage pickup operations.

## Notes for modders
- Ensure that `SetDeliveryVehicle` and `SetFinalDestination` are called appropriately to configure the pickup operation.
- Use `Pickup` and `ImmediatePickup` functions to control the pickup process.
- Customize voice-over sequences by modifying the `tVO` table in `_WaitCallback`.
- Be aware of faction infraction logic, as picking up munitions will add a +5 infraction per pickup.