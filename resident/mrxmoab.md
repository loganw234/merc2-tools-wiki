---
title: MrxMOAB
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxDaisyCutter
tags: [support, bomb]
verified: true
verified_note: 'deeper pass: clarified this is a data-only subclass reusing all of MrxDaisyCutter''s drop/explosion pipeline, documented the local MOAB Projectile/C130 defaults, and flagged the non-local oDesignator module-global bug; cross-linked MrxDaisyCutter'
---

# MrxMOAB

*Module: mrxmoab.lua*

## Overview
`MrxMOAB` is a **data-only subclass** of [`MrxDaisyCutter`](mrxdaisycutter): the entire flight, drop and
detonation pipeline (`DesignationCallback`, `DropBomb`, `BombExplodes`, `CreateDebris`) is inherited
unchanged — this file only overrides `Create` to swap the projectile to **"MOAB Projectile"** and the
explosion default to `"Explosion (MOAB)"`. Everything the daisy-cutter page says about the drop applies here,
including the [unscaled-velocity `nSpeedScale` quirk](mrxdaisycutter#module-constants--tunables). The
screen-flash grade is the separate [Airstrike_Atmosphere_MOAB](airstrike_atomsphere_moab) object.

## Inheritance
- Inherits from: [`MrxDaisyCutter`](mrxdaisycutter) → [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke)

## Instance pattern
**Same class-factory pattern as [`MrxDaisyCutter`](mrxdaisycutter)/[`MrxSupport`](mrxsupport), not
per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new table via `setmetatable`/`__index`, exactly like
its parent chain. No `OnActivate`/`Awake`, no `tInstance` registry. It tracks the following key fields:
- `oDesignator`: An instance of `MrxSupportDesignatorSmoke` used for designating targets.
- `uPlayerGuid`: The GUID of the player who owns this support module.
- `sRecruit`: The name of the recruit associated with this support module ("Fiona").
- `sModuleName`: The name of the module ("MrxMOAB").
- `sDeliveryVehicle`: The name of the delivery vehicle ("Support Vehicle (C130)").
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The name of the bomb projectile ("MOAB Projectile").
- `uBomb`: The GUID of the bomb projectile.

## Module constants
Module-level **`local`** defaults (unreachable from outside; the instance fields set from them in `Create`
are the real customization surface — same story as [MrxDaisyCutter](mrxdaisycutter)):
- `sProjectileName = "MOAB Projectile"`
- `sExplosionName = "Explosion (MOAB)"` — **declared but never used** (dead, inherited-behavior detail).
- `sDeliveryVehicle = "Support Vehicle (C130)"`

## Functions
### `Create(self, uPlayerGuid)`
The only function defined here. Builds a smoke designator with `_NoValidation`, sets owner / recruit
`"Fiona"` / module name `"MrxMOAB"`, and copies the MOAB projectile + C-130 defaults onto the instance as
`self.sBomb`/`self.uBomb`/`self.sDeliveryVehicle`/`self.uDeliveryVehicle`. All other behavior comes from the
inherited [`MrxDaisyCutter`](mrxdaisycutter) functions.

{: .warning }
> `Create` assigns the designator to a bare `oDesignator = MrxSupportDesignatorSmoke:Create()` **without
> `local`**, so `oDesignator` becomes a **module-level global** shared across every MOAB instance rather than
> per-instance scratch. It is immediately handed to `SetDesignator`, so the shared global is harmless in
> practice, but it's a genuine scoping bug — do not read `oDesignator` expecting per-instance state.

## Events
- **No `Event.Create` subscriptions and no functions of its own beyond `Create`.** All event/timer behavior
  (e.g. the 1.5 s `CreateDebris` schedule) is inherited from [`MrxDaisyCutter`](mrxdaisycutter).

## Notes for modders
- **This module IS the "swap the daisy cutter for a bigger bomb" recipe** — the whole file is just
  `MrxDaisyCutter` with `uBomb` repointed. To make your own variant, do the same: inherit `MrxDaisyCutter`
  and override `Create` to set a different `sBomb`/`uBomb`.
- To change MOAB behavior beyond the projectile (blast, debris, timing), edit
  [`MrxDaisyCutter`](mrxdaisycutter) — those functions are shared, so changes there affect both weapons.