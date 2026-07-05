---
title: EnemyBlippable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [enemy, blip]
verified: true
verified_note: "deeper pass: surfaced exact color-table RGB values + their relation thresholds (ally>=60, enemy<=-60, neutral in-between, pmc by label, empty=no driver), cross-linked the full blip chain; all functions/events re-confirmed against source"
---

# EnemyBlippable

*Module: enemyblippable.lua*

## Overview
The `EnemyBlippable` module extends [`Blippable`](blippable) to manage radar objectives and off-screen
world markers specifically for vehicles, colored by the relationship between the vehicle's driver and the
PMC faction. Despite the name, the color logic covers ally/neutral/enemy/empty/PMC cases, not just "enemy"
— see `PickColor`. It is a sibling of [`OrientedBlippable`](orientedblippable)/[`VehicleBlippable`](vehicleblippable)
in the blip chain (all three inherit from `Blippable`).

## Inheritance
- Inherits from: [`Blippable`](blippable) (which itself inherits from [`Inheritable`](inheritable))
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
Per-instance object module (keyed by `uGuid`), but this file itself defines no `OnActivate`/`Awake` — those are inherited from `Blippable` (`Blippable.OnActivate` → `Awake` → `oPrototype:Create(uGuid, iArg)`, which resolves to this file's own `Create` since it overrides the parent). This file tracks the following key fields on the instance:
- `tColor`: The color of the radar objective (one of the module-level color tables below, selected by `PickColor`).
- `bHostile`: Set `true` only in the `nRelation <= -60` branch of `PickColor`; not reset in the other branches.
- `DriverEnter`: Persistent event handle for when a driver enters the vehicle.
- `DriverExit`: Persistent event handle for when a driver exits the vehicle.
- `Attitude`: Persistent attitude-change event handle from `MrxFactionManager.CreatePersistentAttitudeChangeEvent`.

## Functions
### `Create(oPrototype, uGuid, iArg)`
Overrides `Blippable.Create`. First calls bare `GetFromGuid(uGuid)` (resolves through the inheritance chain to `Inheritable.GetFromGuid`, i.e. `tInstance[uGuid]`) to reuse an existing instance if one is already registered for this `uGuid`; otherwise falls back to `Blippable.Create(oPrototype, uGuid, iArg)`. Then, if not already set, creates two **persistent** events: `DriverEnter` (`Event.ObjectInSeat` "Driver"/"enter", callback `oInstance.PickColor`) and `DriverExit` (`Event.ObjectInSeat` "Driver"/"exit", inline callback that calls `oInstance:ClearBlipped(true)`). Looks up the object's faction via `MrxUtil.GetFaction` and `MrxFactionManager.GetFactionAbbrev`, and if not already set, creates a persistent `Attitude` event via `MrxFactionManager.CreatePersistentAttitudeChangeEvent({sFactionAbbrev, "Pmc"}, ...)` whose callback clears, re-picks, and re-sets the blip. If a driver is already present (`Vehicle.GetDriver(uGuid)`), calls `PickColor` immediately.

### `Delete(self)`
Tears down the per-instance table by deleting any persistent events (`DriverEnter`, `Attitude`, `DriverExit`) and calling `Blippable.Delete(self)` (which itself calls `self:ClearBlipped()` if active, then `Inheritable.Delete`).

### `PickColor(self, uGuid)`
Determines the appropriate blip color based on the vehicle driver, via `Vehicle.GetDriver(uGuid)`. If the driver is player-controlled, calls `self:ClearBlipped()` and returns (no blip for player-driven vehicles). If there's a non-player driver, checks `Ai.GetRelation(uRider, Pg.GetGuidByName("PMC"))`: `pmc`-labeled → `tColorPmc`; `-60 < nRelation < 60` → `tColorNeutral`; `nRelation <= -60` → sets `bHostile = true` and `tColorEnemy`; `nRelation >= 60` → `tColorAlly`. If no driver at all, uses `tColorEmpty`. Whenever `self.tColor` ends up set, calls `self:SetBlipped(true)`. Note: `uRider` and `nRelation` are assigned without `local` in this function, so they are plain globals, not locals.

## Events
- Listens for `Event.ObjectInSeat` (Driver/enter and Driver/exit, both via `Event.CreatePersistent`) to call `PickColor` on enter and clear the blip on exit.
- Registers a persistent attitude-change event via `MrxFactionManager.CreatePersistentAttitudeChangeEvent` (not a raw `Event.*` constant) to refresh the blip when faction relations change.
- No `HideMarker` event is defined or referenced in this file — that behavior belongs to `Blippable` (which defines `HideMarker` as a plain function, and `tHiddenGuids` as the exclusion list `AddObjective` checks).

## Notes for modders
- This file has no `OnActivate`/`OnDeactivate` of its own — instance lifecycle (activation, hibernation wake, teardown call sites) is entirely inherited from `Blippable`/`Inheritable`. Only `Create`, `Delete`, and `PickColor` are overridden here.
- Customize blip properties by setting fields like `tColor`; the actual HUD/marker rendering (`AddObjective`/`RemoveObjective`, `bNetSync` handling) lives in `Blippable`, not this file.
- **Blip colors are module-level globals with exact `{r, g, b}` values you can change** (all plain
  globals, not `local`s):
  - `tColorAlly = {0, 127, 255}` (blue) — driver relation `>= 60`
  - `tColorNeutral = {230, 230, 255}` (near-white) — relation strictly between `-60` and `60`
  - `tColorEnemy = {255, 0, 0}` (red) — relation `<= -60` (also sets `self.bHostile = true`)
  - `tColorEmpty = {100, 100, 100}` (grey) — no driver
  - `tColorPmc = {0, 255, 0}` (green) — object or driver has the `"pmc"` label
  `PickColor` reads these as `self.tColorPmc`/`self.tColorNeutral`/etc., which resolve through the
  `__index` metatable up to these module globals — so editing the globals recolors every instance.
- The `Create` reuse-via-`GetFromGuid` pattern means calling `Create` again for a `uGuid` that already has a live instance returns the existing instance rather than creating a duplicate.