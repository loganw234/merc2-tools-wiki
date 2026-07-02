---
title: SupportAirplane
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable, MrxFactionManager
tags: [support, aircraft, radar]
---

# SupportAirplane

*Module: supportairplane.lua*

## Overview
The `SupportAirplane` module is responsible for managing support aircraft in the game. It handles the creation and configuration of radar blips for these aircraft based on their faction, labels, and relation to the PMC (Player Managed Company). The module also ensures that certain aircraft are marked as unkillable if they have the "PMC" label.

## Inheritance
- Inherits from: `OrientedBlippable`, `MrxFactionManager`
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tColor`: The color of the radar blip based on the aircraft's faction.
- `sTexture`: The texture used for the radar blip icon, determined by the aircraft's label.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It creates a new per-instance table for the object using the module's prototype. It then determines the faction of the aircraft and sets its color based on the relation to the PMC. If the aircraft has the "PMC" label, it marks it as unkillable. Finally, it sets the radar blip icon texture based on the aircraft's label and activates the blip.

Exact icon-by-label mapping, read directly from source — `OnActivate` checks `Object.HasLabel(uGuid, ...)`
against each of these in order and swaps the default `"temp_radar_icon_airplane"` texture accordingly:

| Label | Icon texture |
|---|---|
| `C130` | `temp_radar_icon_c130` |
| `Mig27` | `temp_radar_icon_mig27` |
| `F35` | `temp_radar_icon_f35` |
| `b2` | `temp_radar_icon_b2` |
| `f117` | `temp_radar_icon_f117` |
| `a10` | `temp_radar_icon_a10` |
| `ov10` | `temp_radar_icon_ov10` |
| `cruisemissile` | `temp_radar_icon_cruisemissile` |

Same relation-based coloring as [`VehicleBlippable`](vehicleblippable) (ally/neutral/enemy at the same
±60 thresholds), plus a PMC-specific green not present on the shared base class, and this module doesn't
inherit `VehicleBlippable` at all — it reimplements the same color logic locally against
`OrientedBlippable` directly instead.

## Events
Doesn't defer to `Event.ObjectHibernation` like most other `Vehicles` pages — `OnActivate` creates the
instance and configures the blip immediately, with no wait for the object to leave hibernation first.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to manage the lifecycle of support aircraft.
- Customize radar blip colors by modifying the faction relation logic or directly setting `tColor`.
- Adjust radar blip textures by changing the label checks and corresponding texture assignments.
- Be aware that marking an aircraft as unkillable with the "PMC" label may affect gameplay balance.