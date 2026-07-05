---
title: MrxSupportDesignatorBeacon
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
verified: true
verified_note: "deeper pass: confirmed the whole module is Create + GetType only; documented what makes a beacon differ (jammer AA level, bDesignateOnDeath=false, Beacon Designator type) and which strikes use it; cross-linked base + consumers"
---

# MrxSupportDesignatorBeacon

*Module: mrxsupportdesignatorbeacon.lua*

## Overview
`MrxSupportDesignatorBeacon` is the thrown-beacon [designator](mrxsupportdesignator) subtype. It's the simplest of the five — just a `Create` that stamps the beacon-specific fields plus a `GetType`. A beacon is a persistent object the strike can track (falling ordnance re-reads its live position — see [`MrxArtillery.TriggerFallingMissile`](mrxartillery)), and the base [`GetTarget`](mrxsupportdesignator) returns its `uGuid` so callers can remove it after the strike. Used by [`MrxArtillery`](mrxartillery), [`MrxCruiseMissile`](mrxcruisemissile), [`MrxStrategicMissile`](mrxstrategicmissile), and [`MrxHARMStrike`](mrxharmstrike).

## Inheritance
- Inherits from: [`MrxSupportDesignator`](mrxsupportdesignator)
- Imports: `none`

## Instance pattern
**Same class-factory pattern as `MrxSupportDesignator`, not per-`uGuid`** — `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no
`tInstance` registry. It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignateOnDeath`: Indicates whether designation should occur on death.
- `bDesignationComplete`: Indicates whether the designation process is complete.
- `sDesignationType`: The type of designator, set to "Beacon Designator".
- `fValidationFunction`: The validation function for the designator, set to nil.
- `tCallbackList`: A list of callbacks associated with the designator.
- `sAATestLevel`: The AA test level, set to "jammer".
- `nX`, `nY`, `nZ`: Coordinates of the designator in the world.
- `uGuid`: The unique GUID of the designator.

## Functions
### `Create(self, oNewDesignator)`
Stamps the beacon fields onto a fresh (or passed-in) table, then `setmetatable`s it to this module. Beacon-specific settings vs. the base: `sDesignationType = "Beacon Designator"`, `sAATestLevel = "jammer"`, `bDesignateOnDeath = false`, `fValidationFunction = nil`. Everything else (owner, coords, `uGuid`) is copied through from the prototype.

### `GetType(self)`
Returns `"beacon"`.

## Events
None — this module subscribes to no engine events and schedules no timers. All lifecycle is driven by the base class's callback list.

## Module constants & tunables
Set inside `Create` (there are no module-level `local`s):
- `sDesignationType = "Beacon Designator"` — the item [`Airstrike.EquipDesignator`](mrxsupportdesignator) hands the player.
- `sAATestLevel = "jammer"` — a beacon strike is only denied by a **jammer**, not by ordinary AA (the strongest "always allowed unless jammed" setting among the five subtypes).
- `bDesignateOnDeath = false` — designation does **not** auto-complete if the beacon object is destroyed.

## Notes for modders
- The `"jammer"` AA level is the beacon's defining trait: beacon-based strikes ([artillery](mrxartillery), [cruise](mrxcruisemissile), [strategic](mrxstrategicmissile), [HARM](mrxharmstrike)) ignore basic/medium/advanced AA and are only blocked by a jammer. Change `sAATestLevel` in `Create` to make them AA-blockable.
- `fValidationFunction` is deliberately `nil` here — a beacon can be dropped anywhere. Assign one of the base [`ValidateGroundDropZone`/`ValidateWaterDropZone`](mrxsupportdesignator) functions if you want placement restrictions.