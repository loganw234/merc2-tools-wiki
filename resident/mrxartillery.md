---
title: MrxArtillery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, artillery]
---

# MrxArtillery

*Module: mrxartillery.lua*

## Overview
The `MrxArtillery` module is responsible for managing the deployment and behavior of artillery support in the game. It inherits from `MrxSupport` and uses `MrxSupportDesignatorBeacon` for target designation and `MrxVoSequence` for voice-over sequences.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorBeacon`, `MrxVoSequence`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator beacon used for target designation.
- `uOwner`: The GUID of the player who owns this support.
- `sRecruit`: The recruit name associated with this support.
- `sDeliveryVehicle`: The delivery vehicle used for artillery deployment.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sAmmo`: The type of ammunition used (e.g., "Artillery Shell").
- `nWidth`: The width parameter affecting the spread of missiles.
- `tVO`: Table of voice-over sequences.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new instance of `MrxArtillery` and initializes it with the given player GUID. Sets up the designator beacon, owner, recruit, delivery vehicle, and module name.

### `DesignationCallback(self)`
Handles the target designation callback. Retrieves the target coordinates from the designator, sets the ammunition type and width, and schedules multiple missiles to fall towards the target using timers. Also starts a voice-over sequence based on the player's faction.

### `TriggerFallingMissile(self)`
Triggers the falling of a missile towards the designated target. Adjusts the target coordinates with random offsets for spread and spawns the ordnance using the `Airstrike.SpawnOrdnance` function.

## Events
- Listens for custom event (not specified in the provided code) to trigger `DesignationCallback`.
- Uses `Event.TimerRelative` to schedule missile launches and beacon removal.

## Notes for modders
- Ensure that `Create` is called with a valid player GUID to properly initialize the artillery support.
- Customize the ammunition type, width, and voice-over sequences by modifying the respective fields.
- Be aware of the random spread applied to missile targets to ensure balanced gameplay.