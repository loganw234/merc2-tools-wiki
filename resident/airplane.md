---
title: Airplane
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, blip]
---

# Airplane

*Module: airplane.lua*

## Overview
The `Airplane` module represents a specific type of vehicle in the game world. It inherits from `VehicleBlippable`, which means it can be blipped on radar and has properties related to vehicles. This module is responsible for initializing airplane instances when they are activated.

## Inheritance
- Inherits from: `VehicleBlippable`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tFlash`: The flash color of the radar objective.
- `sTexture`: Texture used for the radar objective.
- `nSize`: Size of the radar objective.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the airplane instance is activated. It creates a new per-instance table for the object using the module's prototype.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage airplane lifecycle.
- Customize blip properties by setting fields like `tFlash`, `sTexture`, and `nSize`.
- This module inherits from `VehicleBlippable`, so any vehicle-specific behavior or methods can be extended or overridden.