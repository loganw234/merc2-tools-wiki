---
title: MrxTankBuster
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxTankBuster

*Module: mrxtankbuster.lua*

## Overview
The `MrxTankBuster` module is a support system that provides an aerial strike capability to players. It uses a designated smoke marker to guide the airstrike and targets enemy tanks within a specified range.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support.
- `uJet`: The GUID of the aircraft performing the airstrike.
- `uDeliveryVehicle`: The vehicle used to deliver the ordnance.
- `oDesignator`: The designator object for guiding the strike.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new instance of the `MrxTankBuster` support system. Initializes the designator with specific properties and sets the owner, recruit, module name, and delivery vehicle.

### `DesignationCallback(self)`
Handles the designation callback for the airstrike. Calculates spawn and target points using the camera position, sets up the aircraft flight path, and schedules voice-over announcements.

### `Strike(self)`
Executes the airstrike by finding nearby enemy tanks and launching missiles at them. Ensures that only non-PMC-controlled vehicles are targeted.

### `LaunchMissile(self, uTarget)`
Launches a missile at a specified target. Calculates the direction vector from the aircraft to the target, normalizes it, and spawns the ordnance with the calculated velocity.

### `_ValidateDropZone(fCallback, nX, nY, nZ, oSupport)`
Validates the drop zone for the airstrike by testing the area using AI functions. Calls the provided callback with a success status and reason if the drop zone is not valid.

## Events
- Listens for custom event `DesignationCallback` to handle designation of the strike.
- Listens for custom event `Strike` to execute the actual attack.
- Listens for custom event `_ValidateDropZone` to validate the drop zone before executing the airstrike.

## Notes for modders
- Ensure that the player's GUID is correctly passed to the `Create` function to properly associate the support with the player.
- Customize the designator properties and validation logic as needed for different game scenarios.
- Be aware of the network synchronization settings if using this module in multiplayer environments.