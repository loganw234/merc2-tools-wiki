---
title: MrxSupportDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, delivery]
---

# MrxSupportDelivery

*Module: mrxsupportdelivery.lua*

## Overview
The `MrxSupportDelivery` module is responsible for handling the delivery of cargo using a helicopter. It inherits from `MrxSupport` and provides functionality to spawn a helicopter, attach cargo to its winch, and deliver it to a designated target. This module is used in scenarios where players need reinforcements or supplies delivered via air.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `MrxGui`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `bCareless`: Indicates whether the delivery should be careless.
- `oTarget`: The target location for the delivery.
- `sDeliveryVehicle`: The name of the vehicle used for delivery ("UH1 Transport (PMC) (Driver)"). 
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sFinalDestination`: The final destination point for the delivery.
- `sCargoToDeliver`: The name of the cargo to deliver ("box").
- `uCargoToDeliver`: The GUID of the cargo to deliver.
- `nCargoDropHeight`: The height at which the cargo should be dropped (0.5).
- `bNeedsConnection`: A flag indicating if a connection is needed.
- `oUpdateEvent`: An event for updating the delivery process.
- `oDesignator`: The designator object used for targeting.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the delivery support module. Initializes various fields and sets up the designator with blue smoke color.

### `DesignationCallback(self)`
Calls `_DesignatorCallback` to handle the designation callback.

### `SetCargoGuid(self, uCargoTemplate)`
Sets the GUID of the cargo to deliver.

### `SetCargo(self, sCargoTemplateName)`
Sets the name of the cargo to deliver and calls `PickCargo` to select a specific cargo template.

### `PickCargo(self, sCargoTemplateName)`
Selects a random cargo template from a list if multiple options are provided. Sets the GUID of the selected cargo.

### `SetCareless(self, bCareless)`
Sets whether the delivery should be careless (no checks for nearby friendly soldiers).

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point for the delivery.

### `SetCargoDropHeight(self, sCargoTemplateName)`
Sets the height at which the cargo should be dropped during delivery.

### `_DesignatorCallback(self)`
Handles the designation callback. Spawns the cargo and helicopter, sets their positions and orientations, and deploys the winch to attach the cargo.

### `_DeployWinch(self, uHeli, uCargo)`
Deploys the winch on the helicopter, plays a voice-over cue for the faction, and sets up events to wait for the cargo to be awake before delivering it.

### `_WaitCallback(self, uHeli, uCargo)`
Handles the callback after the cargo is awake. Attaches the cargo to the winch, sets up damage events, and initiates the delivery process.

### `CargoDropped(self, uHeli, uCargo)`
Called when the cargo has been dropped. Sends the helicopter back home and disposes of the cargo.

## Events
- Listens for custom event `_DesignatorCallback` to handle designation.
- Listens for custom event `_DeployWinch` to deploy the winch.
- Listens for custom event `_WaitCallback` to wait for the cargo to be awake.
- Listens for custom event `CargoDropped` to handle post-delivery cleanup.

## Notes for modders
- Ensure that the delivery vehicle and cargo templates are correctly set up in the game data.
- Customize the delivery behavior by setting fields like `bCareless`, `nCargoDropHeight`, and `sFinalDestination`.
- Be aware of network synchronization (`Net.IsClient()`) to ensure proper behavior in multiplayer scenarios.
- Use `SetCargoGuid` or `SetCargo` to specify the cargo to be delivered.