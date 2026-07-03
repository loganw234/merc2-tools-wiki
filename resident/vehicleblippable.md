---
title: VehicleBlippable
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [vehicle, blip]
verified: true
verified_note: color/relation thresholds and instance-vs-module-level state read directly from source
---

# VehicleBlippable

*Module: vehicleblippable.lua*

## Overview
The `VehicleBlippable` module is responsible for managing radar and off-screen world markers for vehicles. It handles the blip color based on the driver's relation to the PMC faction, ensuring that the vehicle's blip accurately reflects its status (ally, neutral, enemy, empty, or PMC). This module also listens for driver enter/exit events and faction attitude changes to update the blip accordingly.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). Genuine per-instance fields, set in `Create`:
- `DriverEnter` / `DriverExit`: persistent event handles for the driver-seat enter/exit events, cleaned up
  in `Delete`.
- `Attitude`: persistent event handle for this vehicle's faction-attitude-change event, also cleaned up in
  `Delete`.
- `tColor` (inherited from [`Blippable`](blippable)): the field `SetBlipped` actually writes to
  (`oSelf.tColor = oSelf.tColorPmc`, etc.) — this is the one that changes per-instance based on who's
  driving.

`tColorAlly`/`tColorNeutral`/`tColorEnemy`/`tColorEmpty`/`tColorPmc` are **not per-instance state** —
they're plain module-level constants declared once at the top of `vehicleblippable.lua`. Every instance
reads the same shared tables (reachable via `self.tColorAlly` etc. through the prototype-inheritance
fallback, same mechanism as [`Inheritable`](inheritable)); nothing ever writes a different value onto a
specific instance.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the vehicle instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Checks if the vehicle is alive and creates a new per-instance table for the vehicle using the module's prototype.

### `Create(oPrototype, uGuid, uRuntimeOwner)`
Creates a new per-instance table for the vehicle. It sets up event listeners for driver enter/exit events and faction attitude changes, and initializes the blip color based on the current state.

### `Delete(self)`
Tears down the per-instance table by clearing any active blips and calling the base class's `Delete`.

### `SetBlipped(oSelf, uVehicle)`
Updates the vehicle's blip color based on the driver's relation to the PMC faction. It also clears the blip if a player is controlling the vehicle.

Exact color/relation thresholds, read directly from source:

| Condition | RGB | Meaning |
|---|---|---|
| No driver | `100, 100, 100` (gray) | Empty vehicle |
| Driver has `"pmc"` label | `0, 255, 0` (green) | Your own faction |
| Relation to PMC ≥ 60 | `0, 127, 255` (blue) | Ally |
| Relation to PMC ≤ -60 | `255, 0, 0` (red) | Enemy |
| -60 < relation < 60 | `230, 230, 255` (near-white) | Neutral |
| A **player** is driving | — | Blip is cleared entirely — no blip shown for a player-driven vehicle, regardless of faction |

This is the same ally/neutral/enemy/empty/PMC color language used across most of the `Vehicles` category
(`autogunship`, `supportairplane`, and others reimplement slightly different variants of the same scheme
locally rather than importing this one).

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for `Event.ObjectInSeat` (`DriverEnter`, `DriverExit`) to update the blip color on driver changes.
- Listens for faction attitude change events to recolor the blip based on updated relations.

## Notes for modders
- **Modifying `tColorAlly`/`tColorNeutral`/`tColorEnemy`/`tColorEmpty`/`tColorPmc` changes the color for
  every vehicle using this module at once** — they're shared module-level constants, not per-instance
  settings. `import("VehicleBlippable"); VehicleBlippable.tColorEnemy = {255, 255, 0}` would recolor every
  enemy vehicle's blip yellow, globally.
- Faction attitude changes automatically recolor blips already on-screen (via the `Attitude` persistent
  event) — you don't need to manually refresh vehicle blips after changing a relation with
  [`MrxFactionManager.SetRelation`](mrxfactionmanager).
- `autogunship` and `supportairplane` (also in this category) reimplement slightly different variants of
  the same ally/neutral/enemy/empty/PMC scheme locally rather than importing this module — worth checking
  if you want a consistent look across custom vehicle types.