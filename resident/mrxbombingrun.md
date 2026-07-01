---
title: MrxBombingRun
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, bombing run]
---

# MrxBombingRun

*Module: mrxbombingrun.lua*

## Overview
The `MrxBombingRun` module is a support system for executing bombing runs in the game. It extends the base `MrxSupport` class to provide functionality specific to dropping bombs from an aircraft.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `sDeliveryVehicle`: Name of the delivery vehicle used for the bombing run.
- `uDeliveryVehicle`: GUID of the delivery vehicle.
- `uOwner`: GUID of the player who initiated the bombing run.
- `uJet`: GUID of the aircraft performing the bombing run.
- `uSpawnedBomb`: GUID of the bomb dropped during the bombing run.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the bombing run using the module's prototype. Initializes the support system with a designator and sets the owner and recruit.

### `DesignationCallback(self)`
Called when the bombing run is designated. Spawns an aircraft at a calculated position relative to the camera, sets its target, and initiates the bombing run by calling `DropBomb`. Also plays voice-over announcements for the airstrike.

### `DropBomb(self)`
Drops bombs from the aircraft towards the designated target. Calculates the spawn and target positions, normalizes the vector, and spawns two bombs with slight variations in position and velocity.

### `BombExplodes(self, uBomb)`
Called when a bomb explodes. Currently does nothing but can be extended to handle post-explosion logic.

## Events
- Listens for custom event (not explicitly defined in this file) to trigger the designation callback.
- Listens for bomb explosion events to call `BombExplodes`.

## Notes for modders
- Ensure that the bombing run is properly designated and activated by calling the appropriate functions.
- Customize the delivery vehicle, target positions, and bomb properties as needed.
- Extend the `BombExplodes` function to handle any post-explosion effects or logic.