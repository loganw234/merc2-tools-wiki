---
title: MrxSupportDesignatorBeacon
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
---

# MrxSupportDesignatorBeacon

*Module: mrxsupportdesignatorbeacon.lua*

## Overview
The `MrxSupportDesignatorBeacon` module is a subclass of `MrxSupportDesignator` that handles the creation and management of beacon designators. Beacon designators are used to mark specific locations in the game world, typically for support operations like air strikes or supply drops.

## Inheritance
- Inherits from: `MrxSupportDesignator`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignateOnDeath`: Indicates whether designation should occur on death.
- `bDesignationComplete`: Indicates whether the designation process is complete.
- `sDesignationType`: The type of designator, set to "Beacon Designator".
- `fValidationFunction`: The validation function for the designator, set to nil.
- `tCallbackList`: A list of callbacks associated with the designator.
- `sAATestLevel`: The AA test level, set to "jammer".
- `nX`, `nY`, `nZ`: Coordinates of the designator in the world.
- `uGuid`: The unique GUID of the designator.

## Functions
### `Create(self, oNewDesignator)`
Creates a new per-instance table for the beacon designator using the module's prototype. Initializes various fields such as owner, designation type, and coordinates.

### `GetType(self)`
Returns the type of the designator, which is "beacon".

## Events
- Listens for none (this module does not subscribe to any engine events).

## Notes for modders
- Ensure that the `Create` function is called appropriately when initializing a new beacon designator.
- The `sAATestLevel` field is set to "jammer" by default, which may affect how the designator interacts with anti-air systems.
- Customize the designator's behavior by modifying fields like `bDesignateOnDeath` and `tCallbackList`.
- Be aware that the validation function (`fValidationFunction`) is not used in this module.