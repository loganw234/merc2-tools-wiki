---
title: OpenTankHatch
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle]
verified: true
verified_note: deeper pass — re-confirmed the whole 7-line file (stateless, no Event.* calls, fires once on activation, driver-seat only); added Vehicle namespace cross-links and clarified the fire-once/DriverHatch behavior
---

# OpenTankHatch

*Module: opentankhatch.lua*

## Overview
The `OpenTankHatch` module is designed to open the driver hatch of a tank vehicle when it is activated. It checks if there is a driver in the vehicle; if not, it opens the hatch.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless utility module (no `Create`/instance pattern). It does not track any per-instance state.

## Functions
### `OnActivate(guid, args)`
Called when the object instance is activated. It reads `Vehicle.GetRiders(guid, "driver")` (defaulting to an
empty table) and, if the first driver slot is empty (`uRiders[1] == nil`), calls
`Vehicle.OpenDoor(guid, "DriverHatch")`. `args` is accepted but unused. Both calls are from the
[`Vehicle`](../namespaces/vehicle) namespace.

## Events
No `Event.*` calls appear anywhere in this file (only 7 lines total). Unlike the common `OnActivate`/`Event.ObjectHibernation`/`Awake` idiom seen elsewhere in `resident/`, `OnActivate` here does all its work immediately and synchronously — it does not defer to an `Awake` via a hibernation event. `OnActivate` itself is presumably invoked directly by the engine when the world object activates, but there is no visible event registration in this module.

## Notes for modders
- This module is designed to be used with tank vehicles.
- The door name `"DriverHatch"` is the one hard-coded string here — the vehicle model must have a door with
  exactly that name for [`Vehicle.OpenDoor`](../namespaces/vehicle) to do anything.
- It only fires once, on activation, and never re-checks: if a driver leaves later, the hatch is not
  re-opened. It only checks the **driver** seat (`Vehicle.GetRiders(guid, "driver")`), ignoring passengers/
  gunners.