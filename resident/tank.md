---
title: Tank
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle]
verified: true
verified_note: clarified Create resolves via inherited VehicleBlippable/Inheritable chain (not defined locally); function/event coverage already matched source, no other changes needed
---

# Tank

*Module: tank.lua*

## Overview
The `Tank` module represents a tank vehicle in the game. It inherits from `VehicleBlippable` to add radar blip functionality and manage the tank's health upon activation.

## Inheritance
- Inherits from: `VehicleBlippable`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`), but `tank.lua` itself defines no `Create` —
`oPrototype:Create(uGuid, uRuntimeOwner)` in `Start` (line 23) resolves through the inherited chain
`VehicleBlippable` → `OrientedBlippable` → `Blippable` → `Inheritable`, none of which override `Create`
after `Inheritable`, so it bottoms out at `Inheritable.Create`: the standard
`setmetatable`/`tInstance[uGuid]` factory described on [Resident Modules](index). Module-level fields
(shared across all tank instances via prototype fallback, not set per-instance in this file):
- `tFlash`: the flash color of the radar blip — `{255, 255, 255}`.
- `sTexture`: the radar blip icon texture — `"temp_radar_icon_tank"`.
- `nSize`: the radar blip size — `5`.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the tank instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Creates a new per-instance table for the tank using the module's prototype. Logs "Tank Start" and checks if the tank's health is greater than zero before proceeding with initialization.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the tank's lifecycle.
- Customize radar blip properties by setting fields like `tFlash`, `sTexture`, and `nSize`.
- The tank will only be initialized if its health is greater than zero.