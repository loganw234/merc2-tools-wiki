---
title: MrxSupportDesignatorFlare
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
verified: true
verified_note: "deeper pass: surfaced the flare model asset (global_weapon_sw500) and the Flare Projectile Stage 2 spawn-on-complete, documented water-drop validation + AA none, and the Init/Deinit asset lifecycle; cross-linked base + Airstrike"
---

# MrxSupportDesignatorFlare

*Module: mrxsupportdesignatorflare.lua*

## Overview
`MrxSupportDesignatorFlare` is the flare-marker [designator](mrxsupportdesignator) subtype. Unlike a [beacon](mrxsupportdesignatorbeacon) (which only *marks*), a flare **spawns its own visual** on completion: when designation finishes it drops a `"Flare Projectile Stage 2"` [ordnance](../namespaces/airstrike) at the flare's location. It can be placed on water (its validation allows it).

## Inheritance
- Inherits from: [`MrxSupportDesignator`](mrxsupportdesignator)
- Imports: none

## Instance pattern
**Same class-factory pattern as `MrxSupportDesignator`, not per-`uGuid`** — `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no
`tInstance` registry. It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignateOnDeath`: Indicates whether designation should occur on death.
- `bDesignationComplete`: Indicates whether the designation process is complete.
- `sDesignationType`: The type of designator, set to "Flare Designator".
- `fValidationFunction`: The function used to validate drop zones, set to `MrxSupportDesignator.ValidateWaterDropZone`.
- `tCallbackList`: A list of callbacks for the designation process.
- `sAATestLevel`: The AA test level, set to "none".
- `nX`, `nY`, `nZ`: Position coordinates of the designator.
- `uGuid`: The unique identifier of the designator.

## Functions
### `Init()` / `Deinit()`
Engine lifecycle hooks (called by the module loader, **not** the modder). `Init` preloads the flare's world model with `Pg.LoadAsset("global_weapon_sw500", "model")`; `Deinit` unloads it. This is the standard load/unload pattern for a designator that has a physical item model.

### `Create(self, oNewDesignator)`
Stamps the flare fields: `sDesignationType = "Flare Designator"`, `sAATestLevel = "none"` (never AA-blocked), `bDesignateOnDeath = true`, and `fValidationFunction = MrxSupportDesignator.ValidateWaterDropZone` (so it can be placed on water). Crucially, it **registers its own completion callback**: `oNewDesignator:AddCompleteCallback(DesignationCompleteCallback, {oNewDesignator})` — the flare visual is self-contained, it doesn't wait on a parent support.

### `DesignationCompleteCallback(self)`
On completion, reads the designator's `uGuid` position and spawns `"Flare Projectile Stage 2"` there via [`Airstrike.SpawnOrdnance`](../namespaces/airstrike) with a tiny downward drift (`0, -2, 0`) and no detonation params — the lit flare effect itself.

### `GetType(self)`
Returns `"flare"`.

## Events
None. `DesignationCompleteCallback` runs via the base class's callback list (registered in `Create`), not an `Event.Create` subscription.

## Module constants & tunables
Set in `Create` / the callback (no module-level `local`s):
- Model asset: `"global_weapon_sw500"` (loaded/unloaded by `Init`/`Deinit`).
- Spawned effect: `"Flare Projectile Stage 2"` (see the [Airstrike template list](../namespaces/airstrike#confirmed-ordnance-template-name-strings)).
- `sDesignationType = "Flare Designator"`, `sAATestLevel = "none"`, `bDesignateOnDeath = true`.
- Validation: `MrxSupportDesignator.ValidateWaterDropZone` (water-placement allowed).

## Notes for modders
- The flare is the one designator that spawns a visual on its own (`DesignationCompleteCallback`) — swap `"Flare Projectile Stage 2"` there for a different [Airstrike template](../namespaces/airstrike#confirmed-ordnance-template-name-strings) to reskin the marker.
- `sAATestLevel = "none"` means a flare mark is never denied by anti-air; set it if you want otherwise.
- `bDesignateOnDeath = true` (vs. the beacon's `false`) means the flare auto-completes designation if its object is destroyed — a real behavioral difference from a beacon.