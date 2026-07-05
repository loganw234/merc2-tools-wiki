---
title: Tank
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle]
verified: true
verified_note: deeper pass — re-confirmed the health>0 gate, single Event.ObjectHibernation, and tFlash/sTexture/nSize prototype globals; corrected the Notes (no local OnDeactivate) and added inheritance-chain cross-links
---

# Tank

*Module: tank.lua*

## Overview
The `Tank` module represents a tank vehicle in the game. It inherits from `VehicleBlippable` to add radar blip functionality and manage the tank's health upon activation.

## Inheritance
- Inherits from: [`VehicleBlippable`](vehicleblippable) (→ [`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable) → [`Inheritable`](inheritable))
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`), but `tank.lua` itself defines no `Create` —
`oPrototype:Create(uGuid, uRuntimeOwner)` in `Start` (line 23) resolves through the inherited chain
[`VehicleBlippable`](vehicleblippable) → [`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable)
→ [`Inheritable`](inheritable), none of which override `Create`
after `Inheritable`, so it bottoms out at [`Inheritable.Create`](inheritable): the standard
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
- `OnActivate` is the only lifecycle callback defined here — there is **no local `OnDeactivate`**; any
  teardown comes from the inherited [`VehicleBlippable`](vehicleblippable) chain.
- Customize radar blip properties by setting `tFlash`, `sTexture` (`"temp_radar_icon_tank"`), and `nSize` —
  shared prototype-level globals, so changing one recolors/re-icons every tank instance.
- The tank's blip/instance is only created if `Object.GetHealth(uGuid)` is a positive number at the moment
  `Start` runs (after it wakes from hibernation) — a dead-on-spawn tank never gets an instance. Watch for the
  `"Tank Start"` `Debug.Printf` line in logs to confirm `Start` fired.