---
title: MrxGunship
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, gunship]
---

# MrxGunship

*Module: mrxgunship.lua*

## Overview
The `MrxGunship` module is responsible for managing a support vehicle (AC130) that provides aerial fire support to players. It inherits from the `MrxSupport` module and uses additional modules like `MrxSupportDesignatorSmoke` and `MrxUtil` to handle designator smoke, validation functions, and utility operations.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uJet`: The GUID of the AC130 jet.
- `uOwner`: The GUID of the player who owns this support vehicle.
- `oDesignator`: An instance of `MrxSupportDesignatorSmoke` used for designating targets.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the AC130 support vehicle. Initializes the designator with specific properties and sets the owner, recruit, and module name.

### `DesignationCallback(self)`
Called when the player designates a target. Calculates spawn and target positions based on camera coordinates, normalizes vectors, starts a voice sequence, and initiates the jet's flyby to the designated location.

### `Salvo(self, uLastTarget)`
Handles the salvo of missiles fired by the AC130. Spawns multiple timed missile launches towards identified targets within a specified radius, ensuring they are valid and alive.

### `LaunchMissile(self, uTarget)`
Launches a single missile towards the target. Calculates the normalized vector from the jet to the target, plays sound effects, spawns muzzle flash particles, and spawns ordnance with calculated velocity.

### `_ValidateDropZone(fCallback, nX, nY, nZ, oSupport)`
A private function used for validating drop zones. Tests the designated location using AI functions and calls a callback with validation results.

## Events
- Listens for custom event `DesignationCallback` to handle target designation.
- Listens for custom event `Salvo` to manage missile salvoes.

## Notes for modders
- Ensure that the `Create` function is called appropriately to initialize the support vehicle instance.
- Use the `DesignationCallback` to trigger the AC130's flyby and subsequent missile salvoes.
- Customize target validation by modifying the `_ValidateDropZone` function or its parameters.
- Be aware of the dependencies on other modules like `MrxSupportDesignatorSmoke` and `MrxUtil` for proper functionality.