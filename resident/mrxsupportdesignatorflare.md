---
title: MrxSupportDesignatorFlare
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
---

# MrxSupportDesignatorFlare

*Module: mrxsupportdesignatorflare.lua*

## Overview
The `MrxSupportDesignatorFlare` module is a subclass of `MrxSupportDesignator` that handles the creation and management of flare designators. It sets up specific properties for flares, including their designation type, validation function, and callback logic.

## Inheritance
- Inherits from: `MrxSupportDesignator`
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignateOnDeath`: Indicates whether designation should occur on death.
- `bDesignationComplete`: Indicates whether the designation process is complete.
- `sDesignationType`: The type of designator, set to "Flare Designator".
- `fValidationFunction`: The function used to validate drop zones, set to `MrxSupportDesignator.ValidateWaterDropZone`.
- `tCallbackList`: A list of callbacks for the designation process.
- `sAATestLevel`: The AA test level, set to "none".
- `nX`, `nY`, `nZ`: Position coordinates of the designator.
- `uGuid`: The unique identifier of the designator.

## Functions
### `Init()`
Called during module initialization. Loads the asset for the global weapon model used by flares.

### `Deinit()`
Called during module deinitialization. Unloads the asset for the global weapon model used by flares.

### `Create(self, oNewDesignator)`
Creates a new per-instance table for the flare designator using the module's prototype. Sets various properties such as owner, designation type, validation function, and position coordinates. Adds a complete callback to handle designation completion.

### `DesignationCompleteCallback(self)`
Called when the designation process is complete. Retrieves the position of the designator and spawns an ordnance ("Flare Projectile Stage 2") at that location.

### `GetType(self)`
Returns the type of the designator, which is "flare".

## Events
- none

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately to manage asset loading/unloading.
- Customize flare properties by setting fields like `uOwner`, `nX`, `nY`, and `nZ`.
- Be aware that the validation function (`MrxSupportDesignator.ValidateWaterDropZone`) may affect where flares can be designated.