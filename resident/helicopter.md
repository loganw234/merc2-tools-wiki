---
title: Helicopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, blip]
verified: true
verified_note: removed unconfirmed OnDeactivate reference (no such function in source); clarified tFlash/sTexture/nSize are shared prototype-level globals read by the inherited Create chain, not per-instance fields; traced full inheritance chain (VehicleBlippable -> OrientedBlippable -> Blippable -> Inheritable)
---

# Helicopter

*Module: helicopter.lua*

## Overview
The `Helicopter` module represents a helicopter vehicle in the game. It's a very thin file — 16 lines,
only 2 functions — that inherits from `VehicleBlippable` for its actual radar-blip behavior and only
supplies the blip's cosmetic properties (flash color, texture, size) plus the standard activation
boilerplate.

## Inheritance
- Inherits from: `VehicleBlippable` (via `inherit("VehicleBlippable")`)
- Chain: `VehicleBlippable` → `OrientedBlippable` → `Blippable` → `Inheritable` (confirmed by reading each
  file in turn — `VehicleBlippable` starts with `inherit("OrientedBlippable")`, which starts with
  `inherit("Blippable")`, which starts with `inherit("Inheritable")`).
- Imports: none

## Instance pattern
Real per-`uGuid` instance pattern, inherited from the chain above (not defined in this file itself).
`Start()` calls `oPrototype:Create(uGuid, uRuntimeOwner)`, which resolves up the chain to
`VehicleBlippable.Create` → `OrientedBlippable.Create`/`Blippable`-level setup → ultimately
`Inheritable.Create`, which builds the `setmetatable`/`__index` instance and registers it by `uGuid`.
This file itself tracks no per-instance fields — it only sets **shared, prototype-level globals** that
`Blippable.AddObjective` (further up the chain) reads via `self.tFlash`/`self.sTexture`/`self.nSize`
(falling back through the metatable when an instance doesn't override them):
- `tFlash = {255, 255, 255}`: flash color for the radar blip.
- `sTexture = "temp_radar_icon_helicopter"`: radar icon texture name.
- `nSize = 5`: radar blip size.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the helicopter instance is activated. Registers an `Event.ObjectHibernation` listener
(`{uGuid, "awake"}`) to call `Start` once the object leaves hibernation, forwarding all three original
arguments.

### `Start(uGuid, uRuntimeOwner, iArg)`
Reads `Object.GetHealth(uGuid)`; only if it's a number greater than 0 does it call
`getfenv():Create(uGuid, uRuntimeOwner)` to build the per-instance table via the inherited `Create` chain.
If health is 0/nil/dead, the instance is never created — the local `oInstance` result isn't stored
anywhere in this file either way (the created instance registers itself in the chain's own `tInstance`
table, not a local here).

**No `OnDeactivate` function exists anywhere in this file** — the previous version of this page's Notes
section referenced one; that doesn't check out against source. Any deactivation/cleanup behavior comes
entirely from whatever the inherited chain (`VehicleBlippable`/`OrientedBlippable`/`Blippable`) provides,
not from `helicopter.lua` itself.

## Events
- `Event.ObjectHibernation` — the only `Event.*` reference in this file, registered in `OnActivate` to
  defer real setup to `Start` until the object wakes up (the standard activation idiom used across most
  world-object scripts in this corpus).

## Notes for modders
- Ensure `OnActivate` is called by the engine as usual; there's no local `OnDeactivate` to worry about in
  this file — cleanup, if any, happens in the inherited chain.
- Customize blip properties by setting `tFlash`, `sTexture`, and `nSize` — these are prototype-level
  globals shared by every helicopter instance, not fields set per-instance at runtime.
- Be aware that the helicopter's blip/instance is only created if its health is a positive number at the
  moment `Start` runs (i.e., after it wakes from hibernation) — a dead-on-spawn helicopter never gets an
  instance at all.