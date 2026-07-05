---
title: BountyCopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [support, winch]
verified: true
verified_note: deeper pass — corrected Events section (_DeployWinch fires on the cargo's Event.ObjectHibernation "awake", not a timer; only the 0.1s AttachCargo delay is Event.TimerRelative); re-confirmed the cargo-label spawn table and tFlash/sTexture/nSize prototype config; added inheritance-chain cross-links.
---

# BountyCopter

*Module: bountycopter.lua*

## Overview
The `BountyCopter` module is a world-spawn helper that drops supply crates via winch. It supports three types of cargo: Blueprints, Treasure, and Light MG. The copter identifies the type based on labels and spawns the appropriate supply drop.

## Inheritance
- Inherits from: [`VehicleBlippable`](vehicleblippable) (→ [`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable) → [`Inheritable`](inheritable))
- Imports: none

## Instance pattern
Real per-`uGuid` instance pattern, but supplied entirely by the inheritance chain — `bountycopter.lua` defines
no `Create` of its own. `Start` calls `oPrototype:Create(uGuid, uRuntimeOwner)`, which resolves up the chain to
[`VehicleBlippable.Create`](vehicleblippable) (which calls [`OrientedBlippable`](orientedblippable) →
[`Blippable`](blippable) → [`Inheritable.Create`](inheritable), the code that actually builds the instance
table, `setmetatable`s it, and registers it in `tInstance`).

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
- `Event.ObjectHibernation` — registered **twice**: in `OnActivate` on the copter (`uGuid`, `"awake"`) to
  call `Start`, and again in `Start` on the spawned cargo object (`uCargo`, `"awake"`) to call
  `_DeployWinch` once the cargo itself wakes up. `_DeployWinch` is **not** a timer — it waits for the cargo
  to leave hibernation, so the winch only deploys after the crate has actually spawned in.
- `Event.TimerRelative` — in `_DeployWinch`, a fixed **0.1s** delay after `Object.SetWinchState(uGuid,
  "deployed")` before calling `AttachCargo` (giving the winch a frame to deploy before the cargo is clamped
  to it).

## Notes for modders
- Ensure that `OnActivate` is called appropriately to manage the copter's lifecycle.
- Customize the cargo type by adding or removing labels (`Blueprints`, `Treasure`) on the copter instance.
- Be aware of the winch deployment and attachment delays, which may need adjustment for different scenarios.