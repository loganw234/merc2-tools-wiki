---
title: MrxCarpetBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
---

# MrxCarpetBomb

*Module: mrxcarpetbomb.lua*

## Overview
The `MrxCarpetBomb` module is a support system that allows players to deploy carpet bomb airstrikes. It inherits from the `MrxSupport` module and utilizes the `MrxSupportDesignatorSatellite` for target designation. The module manages the deployment of multiple bomb lines over time, creating a series of explosions at designated intervals.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSatellite`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `nTotalLines`: Total number of bomb lines to deploy.
- `nRemainingLines`: Number of remaining bomb lines to deploy.
- `nTimeInterval`: Time interval between each explosion.
- `uJet`: GUID of the jet performing the airstrike.
- `nHeading`: Heading direction for bomb deployment.
- `uOwner`: GUID of the player or entity owning the support.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new instance of the carpet bomb support system. Initializes the total and remaining lines, sets the time interval, creates a designator satellite, assigns the recruit "Fiona", sets the owner, and specifies the module name as "MrxCarpetBomb".

### `DesignationCallback(self)`
Called when the target is designated. Retrieves the target coordinates, calculates the spawn position for the jet, and initiates the airstrike by calling `Airstrike.Flyby`. Also plays the airstrike voice-over.

### `DropBomb(oAirstrike)`
Handles the dropping of bombs. Spawns a carpet bomb line at the calculated position and sets up the next explosion callback with a timer.

### `NextExplosionCallback(oAirstrike)`
Called after each bomb line is dropped. Spawns the next bomb line, updates the remaining lines count, and schedules the next explosion if there are more lines to drop.

### `explode()`
Triggers an explosion at the player's current position. This function is not part of the per-instance pattern but is a standalone utility function for creating explosions.

## Events
- Listens for custom event (not explicitly defined in the script) to trigger the designation callback.
- Uses `Event.TimerRelative` to schedule the next bomb line drop and explosion.

## Notes for modders
- Ensure that the `DesignationCallback` is properly triggered to initiate the airstrike.
- Customize the number of lines, time interval, and other parameters by modifying the instance fields.
- Be aware that the `explode` function can be used independently to create explosions at any position.