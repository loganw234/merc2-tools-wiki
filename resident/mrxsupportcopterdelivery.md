---
title: MrxSupportCopterDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, delivery, helicopter]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxSupportCopterDelivery

*Module: mrxsupportcopterdelivery.lua*

## Overview
The `MrxSupportCopterDelivery` module is responsible for delivering a flyable helicopter to the player's designated point. It inherits from `MrxSupport` and provides functionality to spawn, land, and manage the delivery of a helicopter. The module also handles the AI behavior of the helicopter driver (Ewan) after landing.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oTarget`: The target location for the delivery.
- `sDeliveryVehicle`: The type of vehicle to be delivered (helicopter).
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sFinalDestination`: The final destination point after landing.
- `oDesignator`: The designator object used for marking the drop zone.
- `uOwnerGuid`: The GUID of the owner of the support operation.
- `DamageEvent`: Event handle for damage detection on the helicopter.
- `LandGoal`: AI goal for landing the helicopter.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the helicopter delivery operation. Initializes the designator with blue smoke and sets the recruit to "Copter".

### `DesignationCallback(self)`
Called when the designator is used. Spawns the helicopter at a calculated position near the camera, sets its orientation towards the target, and starts a voice sequence.

### `_WaitCallback(self, uHeli)`
A placeholder function that currently does nothing.

### `_HeliReady(self, uHeli)`
Called when the helicopter is spawned and ready. Adds it to the disposer, sets up damage detection, and creates an AI goal for landing the helicopter at the designated target.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point after the helicopter lands.

### `_VehicleLanded(self, uHeli, uDriver, nState)`
Called when the helicopter lands. Handles the outcome of the landing (success or failure), refunds costs if necessary, and sets up the AI behavior for Ewan to exit the vehicle and fade out.

### `ExitedVehicle(self, uDriver)`
Called when Ewan exits the vehicle. Starts a voice sequence, creates an event to remove Ewan after hibernation, and makes the recruit available again in the support manager.

### `CheckEwan(self, uDriver)`
Checks if Ewan is still visible. If not, removes him and deletes associated events.

## Events
- Listens for custom event `DesignationCallback` to spawn the helicopter.
- Listens for `Event.ObjectHibernation` to handle the readiness of the helicopter.
- Listens for `Event.ObjectInSeat` to manage Ewan's exit from the vehicle.
- Listens for a persistent timer `CheckEwan` to ensure Ewan is removed if he disappears.

## Notes for modders
- Ensure that the designator callback is properly set up and triggered to spawn the helicopter.
- Customize the voice sequences by modifying the `tVo` table in `ExitedVehicle`.
- Be aware of the AI behavior and timing for Ewan's exit and fade out after landing.
- The module handles network synchronization implicitly through inherited functions, so ensure that the network state is consistent across clients.