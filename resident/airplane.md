---
title: Airplane
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, blip]
verified: true
verified_note: deeper pass — re-confirmed no Event.ObjectHibernation/Awake in this file (OnActivate calls Create synchronously, shadowing VehicleBlippable's hibernation-wait OnActivate); added cross-links to VehicleBlippable/OrientedBlippable up the inheritance chain
---

# Airplane

*Module: airplane.lua*

## Overview
The `Airplane` module represents a specific type of vehicle in the game world. It inherits from `VehicleBlippable`, which means it can be blipped on radar and has properties related to vehicles. This module is responsible for initializing airplane instances when they are activated.

## Inheritance
- Inherits from: [`VehicleBlippable`](vehicleblippable) (→ [`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable) → [`Inheritable`](inheritable))
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`), but note it does **not** use the
`Event.ObjectHibernation`/`Awake` deferral idiom seen elsewhere in this wiki. `airplane.lua` defines its
own top-level `OnActivate(uGuid, uRuntimeOwner, iArg)` which calls `oPrototype:Create(uGuid, uRuntimeOwner)`
**synchronously and immediately** — there is no `Awake` function in this file, and no
`Event.ObjectHibernation` reference anywhere in the source. This locally-defined `OnActivate` shadows the
`OnActivate` that `VehicleBlippable` itself defines (which *does* wait on `Event.ObjectHibernation` before
calling its own `Start`), since both live in the same global-per-file environment and airplane.lua's own
definition wins for airplane.lua's own activation. `Create` resolves through inheritance to
[`VehicleBlippable.Create`](vehicleblippable) (and from there up through
[`OrientedBlippable`](orientedblippable)/[`Blippable`](blippable)), which is what
actually builds the per-`uGuid` table and registers the driver-enter/exit and faction-attitude events.
Module-level fields (shared across all instances via the prototype, not instance-specific storage):
- `tFlash`: The flash color of the radar objective — `{255, 255, 255}`.
- `sTexture`: Texture used for the radar objective — `"temp_radar_icon_airplane"`.
- `nSize`: Size of the radar objective — `5`.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the airplane instance is activated. Immediately creates a new per-instance table for the
object using the module's prototype (`oPrototype:Create(uGuid, uRuntimeOwner)`) — `iArg` is accepted as a
parameter but not used in this function body.

## Events
No `Event.*` references appear anywhere in this file — `OnActivate` is an engine-invoked lifecycle
callback, not something that subscribes to an event. (Contrast with most other vehicle/blippable modules
in this wiki, which defer through `Event.ObjectHibernation` before creating their instance; this file does
not.)

## Notes for modders
- `OnActivate` fires and creates the instance immediately on activation — there's no hibernation wait to
  account for here, unlike many other `*Blippable`-derived modules.
- Customize blip properties by setting fields like `tFlash`, `sTexture`, and `nSize`.
- This module inherits from `VehicleBlippable`, so any vehicle-specific behavior or methods (driver
  enter/exit blip recoloring, faction attitude changes) can be extended or overridden via that chain.