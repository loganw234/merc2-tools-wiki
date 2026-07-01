---
title: MrxSoldierDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, delivery]
---

# MrxSoldierDelivery

*Module: mrxsoldierdelivery.lua*

## Overview
The `MrxSoldierDelivery` module is responsible for delivering troop reinforcements in the game. It inherits from `MrxSupport` and provides functionality to spawn a delivery vehicle, validate landing zones, and manage the behavior of the delivered soldiers.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oTarget`: The target for the delivery.
- `sDeliveryVehicle`: The template name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `oFinalDestination`: The final destination point for the soldiers.
- `oUpdateEvent`: An event handle for periodic updates.
- `oDesignator`: The designator object used to mark the landing zone.
- `sModuleName`: The name of the module.
- `bSupportComplete`: Indicates whether the support operation is complete.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the delivery operation using the module's prototype. Initializes the delivery vehicle and sets up the designator with validation functions.

### `DesignationCallback(self)`
A passthrough function that calls `_DesignatorCallback`.

### `SetDeliveryVehicle(self, sVehicleTemplateName)`
Sets the template name of the delivery vehicle and updates its GUID.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point for the soldiers.

### `_DesignatorCallback(self)`
Handles the callback when the designator is set. Spawns the delivery vehicle at a calculated position and sets it to land at the designated target.

### `_WaitCallback(self, uHeli, nTargetX, nTargetY, nTargetZ)`
Called after the helicopter is spawned. Plays a voice-over cue and sets up the landing goal for the helicopter.

### `AllOut(self, uHeli, uDriver, nState)`
Handles the outcome of the landing operation. If successful, deploys the soldiers to follow the player; if not, aborts the mission.

### `FollowTheLeader(self, tRiders, uHeli, uDriver)`
Sets up the AI roles for the delivered soldiers to follow the player character.

### `CheckForSoldiers(fCallback, nX, nY, nZ, self)`
Validates the landing zone by checking the number of friendly soldiers in the area. If there are fewer than 8, it proceeds with the validation; otherwise, it denies the operation.

## Events
- Listens for custom event `DesignationCallback` to handle the designator callback.
- Listens for custom event `_WaitCallback` to handle the wait callback after helicopter spawning.
- Listens for custom event `AllOut` to handle the outcome of the landing operation.
- Listens for custom event `FollowTheLeader` to set up the soldiers' AI roles.

## Notes for modders
- Ensure that `SetDeliveryVehicle` and `SetFinalDestination` are called appropriately to configure the delivery operation.
- Customize the voice-over cues by modifying the `tVOOnTheWay` table.
- Be aware of the validation logic in `CheckForSoldiers` to avoid triggering "toomanysoldiers" denials.
- Network synchronization is handled internally, so modders do not need to manage it directly.