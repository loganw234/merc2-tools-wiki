---
title: MrxCombatAirPatrol
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, combat]
---

# MrxCombatAirPatrol

*Module: mrxcombatairpatrol.lua*

## Overview
The `MrxCombatAirPatrol` module is a support system for aerial combat. It provides functionality to deploy an aircraft with missiles and target enemy vehicles within a specified range. This module inherits from `MrxSupport` and uses the `MrxSupportDesignatorSmoke` module for designating targets.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support system.
- `sDeliveryVehicle`: The name of the delivery vehicle used for deploying the aircraft.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the deployed aircraft.
- `oDesignator`: An instance of `MrxSupportDesignatorSmoke` used for designating targets.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the support system. Initializes the designator with specific properties and sets up the owner, recruit, and module name.

### `DesignationCallback(self)`
Called when the target designation is complete. Finds spawn and target points relative to the camera, deploys an aircraft using `Airstrike.Flyby`, and schedules a voice-over announcement for the airstrike.

### `Strike(self)`
Executes the strike by finding all flying targets within a specified range. For each valid target (not controlled by PMC), it schedules a missile launch with a delay based on the number of targets.

### `LaunchMissile(self, uTarget)`
Launches a missile at the specified target. Calculates the direction vector from the aircraft to the target, normalizes it, and spawns the ordnance using `Airstrike.SpawnTargettedOrdnance`. It also blips the aircraft on the radar with a red color.

## Events
- Listens for custom event (not explicitly defined in this script) to trigger `DesignationCallback` when the target designation is complete.
- Listens for custom event (not explicitly defined in this script) to trigger `Strike` when the strike should be executed.

## Notes for modders
- Ensure that the owner's GUID (`uPlayerGuid`) is correctly passed to `Create` to properly manage ownership and control of the support system.
- Customize the designator properties by modifying fields like `tColor`, `nWidth`, and `sTexture` in the `MrxSupportDesignatorSmoke` instance.
- Be aware that network synchronization may affect multiplayer behavior, especially when deploying aircraft and launching missiles.