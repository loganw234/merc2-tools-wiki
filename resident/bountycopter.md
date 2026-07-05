---
title: BountyCopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [support, winch]
verified: true
verified_note: confirmed real per-uGuid pattern via VehicleBlippable->OrientedBlippable->Blippable->Inheritable chain; clarified tFlash/sTexture/nSize as prototype-level config, not per-instance fields; corrected OnActivate description (no debug log call in this file); noted Create is inherited, not overridden here.
---

# BountyCopter

*Module: bountycopter.lua*

## Overview
The `BountyCopter` module is a world-spawn helper that drops supply crates via winch. It supports three types of cargo: Blueprints, Treasure, and Light MG. The copter identifies the type based on labels and spawns the appropriate supply drop.

## Inheritance
- Inherits from: `VehicleBlippable` (which itself inherits `OrientedBlippable` -> `Blippable` -> `Inheritable`)
- Imports: `none`

## Instance pattern
Real per-`uGuid` instance pattern, but supplied entirely by the inheritance chain — `bountycopter.lua` defines
no `Create` of its own. `Start` calls `oPrototype:Create(uGuid, uRuntimeOwner)`, which resolves up the chain to
`VehicleBlippable.Create` (which calls `OrientedBlippable.Create` -> `Blippable.Create` -> `Inheritable.Create`,
the code that actually builds the instance table, `setmetatable`s it, and registers it in `tInstance`).

The module-level globals are **not** per-instance fields — they're prototype config values that every instance
falls back to via the metatable `__index`, read by `Blippable.AddObjective` (in `blippable.lua`) as
`self.tFlash`, `self.sTexture`, `self.nWidth or self.nSize`:
- `tFlash`: `{255, 255, 255}` — flash color used for the radar blip when flashing.
- `sTexture`: `"temp_radar_icon_helicopter"` — radar blip texture.
- `nSize`: `5` — radar blip width/height (used since `nWidth`/`nHeight` aren't set).

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Sets up an event to call `Start` once the object leaves hibernation (`Event.ObjectHibernation`, `"awake"`). No
debug logging in this file (unlike `VehicleBlippable.Start`, which does log).

### `Start(uGuid, uRuntimeOwner, iArg)`
Determines the type of cargo based on labels (`Blueprints`, `Treasure`) and spawns the corresponding supply drop at a position above the copter. Creates the instance via `oPrototype:Create(uGuid, uRuntimeOwner)` (inherited, see above), then sets up an event to deploy the winch and attach the cargo.

Exact spawn names and logic, read directly from source — checked in this order, first label match wins:

| Label present | `Pg.Spawn(...)` name |
|---|---|
| `Blueprints` | `"Supply Drop (Blueprints)"` |
| `Treasure` | `"Supply Drop (Treasure)"` |
| *(neither)* | `"Supply Drop (Light MG)"` — the default |

Spawned 200 units above the copter's own position (`y + 200`), then winched down via `_DeployWinch`.

### `_DeployWinch(uGuid, uCargo)`
Deploys the winch on the copter and sets up an event to attach the cargo after a short delay.

### `AttachCargo(uGuid, uCargo)`
Attaches the supply drop to the deployed winch.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for `Event.TimerRelative` to call `_DeployWinch` after a short delay to deploy the winch.
- Listens for `Event.TimerRelative` to call `AttachCargo` after another short delay to attach the cargo.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to manage the copter's lifecycle.
- Customize the cargo type by adding or removing labels (`Blueprints`, `Treasure`) on the copter instance.
- Be aware of the winch deployment and attachment delays, which may need adjustment for different scenarios.