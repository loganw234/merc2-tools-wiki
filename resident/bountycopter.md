---
title: BountyCopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [support, winch]
---

# BountyCopter

*Module: bountycopter.lua*

## Overview
The `BountyCopter` module is a world-spawn helper that drops supply crates via winch. It supports three types of cargo: Blueprints, Treasure, and Light MG. The copter identifies the type based on labels and spawns the appropriate supply drop.

## Inheritance
- Inherits from: `VehicleBlippable`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tFlash`: The flash color of the radar blip.
- `sTexture`: Texture used for the radar blip.
- `nSize`: Size of the radar blip.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It logs a debug message and sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Determines the type of cargo based on labels (`Blueprints`, `Treasure`) and spawns the corresponding supply drop at a position above the copter. Sets up an event to deploy the winch and attach the cargo.

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