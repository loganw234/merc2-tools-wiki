---
title: OpenTankHatch
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle]
verified: true
verified_note: fixed fabricated Events section (no Event.* calls in source — OnActivate here has no Event.Create wiring, unlike the OnActivate/ObjectHibernation idiom used elsewhere)
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
Called when the object instance is activated. It checks if there is a driver in the vehicle; if no driver is found, it opens the driver hatch.

## Events
No `Event.*` calls appear anywhere in this file (only 7 lines total). Unlike the common `OnActivate`/`Event.ObjectHibernation`/`Awake` idiom seen elsewhere in `resident/`, `OnActivate` here does all its work immediately and synchronously — it does not defer to an `Awake` via a hibernation event. `OnActivate` itself is presumably invoked directly by the engine when the world object activates, but there is no visible event registration in this module.

## Notes for modders
- This module is designed to be used with tank vehicles.
- Ensure that the vehicle has a door named "DriverHatch" for this script to work correctly.
- The script does not handle cases where multiple drivers might be present; it only checks for the presence of one driver.