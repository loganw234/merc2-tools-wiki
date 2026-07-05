---
title: MrxSupportDesignatorLaser
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
verified: true
verified_note: "deeper pass: surfaced the laser rangefinder model asset, documented the LaserFinished gate (AA medium/fuel/recruit checks -> SetDesignationParameters -> CompleteDesignation -> cooldown) and the custom Commence with EquipDesignator callback; cross-linked base + consumers"
---

# MrxSupportDesignatorLaser

*Module: mrxsupportdesignatorlaser.lua*

## Overview
`MrxSupportDesignatorLaser` is the laser-painter [designator](mrxsupportdesignator) subtype. Where a [beacon](mrxsupportdesignatorbeacon) or [smoke](mrxsupportdesignatorsmoke) marks a spot on the ground, the laser paints an **object** the player is aiming at: `Commence` equips the rangefinder and hands `LaserFinished` straight to [`Airstrike.EquipDesignator`](mrxsupportdesignator) as its completion callback, and `LaserFinished` reads the *painted object's* position. It gates completion behind AA, fuel, and recruit-availability checks before firing.

## Inheritance
- Inherits from: [`MrxSupportDesignator`](mrxsupportdesignator)
- Imports: [`MrxSupport`](mrxsupport), [`MrxSupportManager`](mrxsupportmanager), [`MrxPmc`](mrxpmc)

## Instance pattern
**Same class-factory pattern as `MrxSupportDesignator`, not per-`uGuid`** — `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no
`tInstance` registry. It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignationComplete`: Indicates whether the designation process is complete.
- `sDesignationType`: The type of designator, set to "Laser Designator".
- `fValidationFunction`: The validation function for the designator.
- `tCallbackList`: A list of callbacks associated with the designator.
- `sAATestLevel`: The AA test level required for the designator, set to "medium".
- `nX`, `nY`, `nZ`: Position coordinates of the designator.
- `uGuid`: The unique identifier for the designator instance.

## Functions
### `Init()` / `Deinit()`
Engine lifecycle hooks (called by the loader). `Init` preloads `Pg.LoadAsset("global_weapon_laserrangefinder", "model")`; `Deinit` unloads it.

### `Create(self, oNewDesignator)`
Stamps the laser fields: `sDesignationType = "Laser Designator"`, `sAATestLevel = "medium"`, and carries `fValidationFunction` through from the prototype (not forced like flare/smoke). No completion callback is registered here — completion is driven by `LaserFinished` instead.

### `Commence(self, bFireImmediately)`
Overrides the base. Equips the rangefinder and passes `LaserFinished` as the completion callback:
```lua
return Airstrike.EquipDesignator(self.uOwner, self.sDesignationType, LaserFinished, {self}, false)
```
(always `false` for `bFireImmediately`). Returns nothing if `uOwner` isn't a `userdata` handle.

### `LaserFinished(self, uGuid)`
The gate that runs when the player finishes painting an object. In order, it:
1. Denies with `"aa"` if `MrxSupport.TestAALevel(self.sAATestLevel)` fails (medium AA present).
2. Denies with `"fuel"` if the parent support's `GetFuelCost()` exceeds [`MrxPmc.GetFuelQty()`](mrxpmc).
3. Silently returns if the recruit isn't available ([`MrxSupportManager.IsRecruitAvailable`](mrxsupportmanager)).
4. Otherwise reads `Object.GetPosition(uGuid)`, calls `SetDesignationParameters(nX, nY, nZ, uGuid)`, `CompleteDesignation()` (base — fires the strike callbacks), and starts the recruit cooldown.

### `ShouldSuppressIconAnimationOnDirectUse(self)`
Returns `false` (the HUD icon animation is **not** suppressed for a laser — unlike the satellite designator, which returns `true`).

### `GetType(self)`
Returns `"laser"`.

## Events
None. `LaserFinished` is the `EquipDesignator` completion callback, not an `Event.Create` subscription; no timers are scheduled.

## Module constants & tunables
- Model asset: `"global_weapon_laserrangefinder"`.
- `sDesignationType = "Laser Designator"`, `sAATestLevel = "medium"` (blocked by medium+ AA).
- Denial reasons routed through [`MrxSupport.DenialMessage`](mrxsupport): `"aa"`, `"fuel"`.

## Notes for modders
- Unlike the other four subtypes, the laser paints a **`uGuid`** (the object under the reticle), not a ground coordinate — `LaserFinished` gets the object handle directly. That's what makes it usable for "lock this specific vehicle."
- The three-step gate (AA → fuel → recruit) in `LaserFinished` is the whole "can I fire?" logic; drop or reorder those checks in a fork to change denial behavior.
- `sAATestLevel = "medium"` means a laser strike is denied by medium or advanced AA (see [`MrxSupport.TestAALevel`](mrxsupport), where `"basic"` also escalates to test `"medium"`).