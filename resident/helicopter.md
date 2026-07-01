---
title: Helicopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, blip]
---

# Helicopter

*Module: helicopter.lua*

## Overview
The `Helicopter` module represents a helicopter vehicle in the game. It inherits from `VehicleBlippable`, which provides radar blipping functionality. The module is responsible for initializing and managing helicopter instances, ensuring they are properly set up when activated.

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
Called when the helicopter instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Creates a new per-instance table for the helicopter using the module's prototype if the helicopter's health is greater than 0.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage helicopter lifecycle.
- Customize blip properties by setting fields like `tFlash`, `sTexture`, and `nSize`.
- Be aware that the helicopter will only be initialized if its health is greater than 0.