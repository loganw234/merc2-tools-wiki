---
title: MrxSupportDesignatorLaser
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
---

# MrxSupportDesignatorLaser

*Module: mrxsupportdesignatorlaser.lua*

## Overview
The `MrxSupportDesignatorLaser` module is responsible for managing the behavior and lifecycle of a laser designator support system in the game. It handles the creation, activation, and completion of laser designations, ensuring that they meet the necessary criteria such as AA test levels, fuel availability, and recruit availability.

## Inheritance
- Inherits from: `MrxSupportDesignator`
- Imports: `MrxSupport`, `MrxSupportManager`, `MrxPmc`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignationComplete`: Indicates whether the designation process is complete.
- `sDesignationType`: The type of designator, set to "Laser Designator".
- `fValidationFunction`: The validation function for the designator.
- `tCallbackList`: A list of callbacks associated with the designator.
- `sAATestLevel`: The AA test level required for the designator, set to "medium".
- `nX`, `nY`, `nZ`: Position coordinates of the designator.
- `uGuid`: The unique identifier for the designator instance.

## Functions
### `Init()`
Initializes the module by loading the necessary asset for the laser rangefinder model.

### `Deinit()`
Unloads the asset for the laser rangefinder model when the module is deinitialized.

### `Create(self, oNewDesignator)`
Creates a new per-instance table for the laser designator using the module's prototype. It initializes various fields such as owner, designation status, type, validation function, callback list, AA test level, and position coordinates.

### `Commence(self, bFireImmediately)`
Begins the process of equipping the laser designator for a designated target. It checks if the owner is valid and then uses the `Airstrike.EquipDesignator` function to start the designation process. The `LaserFinished` callback is registered to handle the completion of the designation.

### `LaserFinished(self, uGuid)`
Handles the completion of the laser designation process. It checks for AA test level denials, fuel availability, and recruit availability before setting the design parameters and completing the designation. It also starts a cooldown on the recruited support unit.

### `ShouldSuppressIconAnimationOnDirectUse(self)`
Returns false, indicating that the icon animation should not be suppressed when the designator is used directly.

### `GetType(self)`
Returns the type of the designator, which is "laser".

## Events
- Listens for custom event triggers within the `Commence` and `LaserFinished` functions to manage the designation process.

## Notes for modders
- Ensure that the `Init` and `Deinit` functions are called appropriately to manage asset loading and unloading.
- Use the `Create` function to initialize new instances of the laser designator with appropriate parameters.
- Customize the behavior of the laser designator by modifying fields such as `sAATestLevel`, `fValidationFunction`, and position coordinates.
- Be aware that AA test levels, fuel availability, and recruit availability may affect the usability of the designator in multiplayer scenarios.