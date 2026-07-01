---
title: MrxMOAB
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxDaisyCutter
tags: [support, bomb]
---

# MrxMOAB

*Module: mrxmoab.lua*

## Overview
The `MrxMOAB` module is a specialized support module for the MOAB (Massive Ordnance Air Blast) weapon. It extends the functionality of the `MrxDaisyCutter` module to handle specific behaviors and configurations related to deploying and detonating MOABs using a C130 delivery vehicle.

## Inheritance
- Inherits from: `MrxDaisyCutter`
- Imports: `MrxSupportDesignatorSmoke`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: An instance of `MrxSupportDesignatorSmoke` used for designating targets.
- `uPlayerGuid`: The GUID of the player who owns this support module.
- `sRecruit`: The name of the recruit associated with this support module ("Fiona").
- `sModuleName`: The name of the module ("MrxMOAB").
- `sDeliveryVehicle`: The name of the delivery vehicle ("Support Vehicle (C130)").
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The name of the bomb projectile ("MOAB Projectile").
- `uBomb`: The GUID of the bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Constructs a new per-instance table for the MOAB support module. Initializes the designator with no validation function, sets the owner and recruit, assigns the module name, and configures the delivery vehicle and bomb details based on predefined names.

## Events
- Listens for engine events through inherited methods from `MrxDaisyCutter`.

## Notes for modders
- Ensure that the player GUID (`uPlayerGuid`) is correctly set to manage ownership of the support module.
- Customize the designator's validation function if needed by modifying or replacing `_NoValidation`.
- Be aware that this module inherits behaviors and configurations from `MrxDaisyCutter`, which may affect its functionality.