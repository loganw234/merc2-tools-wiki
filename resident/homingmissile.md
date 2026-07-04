---
title: HomingMissile
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [vehicle, blip]
---

# HomingMissile

*Module: homingmissile.lua*

## Overview
The `HomingMissile` module represents a homing missile in the game world. It inherits from the `Blippable` module to manage radar blips and adds specific behavior for flashing blips at regular intervals.

## Inheritance
- Inherits from: `Blippable`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `bActive`: Indicates whether the missile is active.
- `tColor`: The default color of the radar blip.
- `tFlash`: The flash color of the radar blip.
- `sTexture`: Texture used for the radar blip (not set in this module).
- `nSize`: Size of the radar blip.
- `nSortOrder`: Sort order of the radar blip.
- `bFlash`: Indicates whether the blip is currently flashing.
- `TimerEvent`: Handle to the timer event that controls the flash interval.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the missile instance is activated. It creates a new per-instance table for the object using the module's prototype.

### `SetBlipped(oSelf)`
Adds a radar blip and marker for the missile. Sets up a timer to flash the blip every 0.1 seconds if not already set up.

### `ClearBlipped(oSelf)`
Removes the radar blip and marker for the missile. Deletes the timer event if it exists.

### `_HomingLaunched(oWidget, tData)`
A helper function that activates the missile when it is launched. It sets the missile as active and calls `SetBlipped` to add its blip.

**Confirmed: this does not spawn or fire the missile itself, despite the module name — it only reacts to
one that already exists.** `tData` carries a reference to an already-live missile object (`uAmmoGuid` per
the calling convention used at [`AntiAir`](antiair)'s own `_HomingLaunched`, which just forwards here).
The real spawn/launch is handled by something native, outside this file entirely — see
[`AntiAir`](antiair)'s notes and [`Junk.SpawnHomingProjectile`](../namespaces/junk#alarms--gameplay) for
the likely (unconfirmed) mechanism, and [`Airstrike`](../namespaces/airstrike) for the *other*, confirmed
projectile-spawning namespace this module does **not** use.

## Events
- Listens for custom event `_HomingLaunched` to activate the missile and set up its blip.

## Notes for modders
- Ensure that `OnActivate` and `ClearBlipped` are called appropriately to manage the missile's blip lifecycle.
- Customize blip properties by setting fields like `tColor`, `tFlash`, and `nSize`.
- Be aware that the flash interval is set to 0.1 seconds, which may affect visual feedback in multiplayer scenarios.