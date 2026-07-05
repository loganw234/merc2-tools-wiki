---
title: MrxRocketArtillery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, artillery]
verified: true
verified_note: "deeper pass: added ordnance/spread constants (Rocket Artillery Projectile, width 100/height 50, 30 shells over 8s) and the satellite minigame sectors; flagged the undefined ActivateDelay reference; cross-linked satellite designator + Airstrike"
---

# MrxRocketArtillery

*Module: mrxrocketartillery.lua*

## Overview
`MrxRocketArtillery` is a satellite-designated rocket barrage. Unlike the beacon-based [`MrxArtillery`](mrxartillery), the player targets it through the satellite mini-game ([`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite)), then 30 rockets walk across an oriented rectangle centered on the mark. It inherits from [`MrxSupport`](mrxsupport) and uses [`MrxVoSequence`](mrxvosequence) / [`MrxUtil`](mrxutil) for the announcer line.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite), [`MrxVoSequence`](mrxvosequence), [`MrxUtil`](mrxutil)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oDesignator`: The designator satellite used for targeting.
- `uOwner`: The GUID of the player who owns this support system.
- `sRecruit`: The recruit name associated with this support system.
- `sModuleName`: The module name, set to "MrxRocketArtillery".

## Functions
### `Create(self, uPlayerGuid)`
Builds the instance. Creates a [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite), gives it three mini-game sectors `{{35,55},{170,190},{305,325}}`, clears its `sAATestLevel` (so this strike is **not** blocked by anti-air), sets recruit `"Fiona"`, and names the module `"MrxRocketArtillery"`.

### `DesignationCallback(self)`
Fires when the satellite designation completes. Reads the mark, then builds two normalized basis vectors from the hero→target line — a **width** vector (perpendicular) and a **height** vector (along the aim direction) — so the 30-round pattern is a rectangle *oriented toward wherever the player was aiming*, not axis-aligned. Constants inline: `sAmmo = "Rocket Artillery Projectile"`, `nWidth = 100`, `nHeight = 50`, `nShells = 30`, `nTime = 8`. Each round's offset is computed along those two vectors and scheduled with [`Event.TimerRelative`](../namespaces/event) at `3 + i * (nTime / nShells)`. Ends with a random Chinese-soldier "artillery/incoming" VO line via [`MrxVoSequence.Start`](mrxvosequence).

### `TriggerFallingMissile(tData, uPlayer)`
Spawns one rocket via [`Airstrike.SpawnOrdnance`](../namespaces/airstrike) at the pre-computed `tData` position (`nTargetY` is already `+250` above the mark, downward velocity `-100`, `"impact"`), attributed to `uPlayer`, with `ActivateDelay` passed as the spawn callback:
```lua
Airstrike.SpawnOrdnance(tData.sAmmo, tData.nTargetX, tData.nTargetY, tData.nTargetZ,
                        0, -100, 0, "impact", 1, uPlayer, ActivateDelay, {tData})
```

{: .warning }
> `ActivateDelay` is passed as the ordnance callback but is **not defined anywhere in `mrxrocketartillery.lua`**. The only `ActivateDelay` in the corpus lives in [`mrxstrategicmissile.lua`](mrxstrategicmissile); it is not inherited from [`MrxSupport`](mrxsupport) either. As written, this reference resolves to a `nil` global in this module's environment — i.e. the callback almost certainly does nothing here. Treat it as a decompiled/leftover artifact, not a working hook, unless you confirm otherwise in-game.

## Events
No event subscriptions. `DesignationCallback` is the designator's completion callback (wired in [`MrxSupport:Commence`](mrxsupport)); the only scheduling is the 30 [`Event.TimerRelative`](../namespaces/event) shell timers.

## Module constants & tunables
All inline in `Create` / `DesignationCallback` (no module-level `local`s):
- Ordnance template: `"Rocket Artillery Projectile"`.
- Pattern: `nWidth = 100`, `nHeight = 50`, `nShells = 30`, `nTime = 8` — a large aim-oriented rectangle, 30 rockets over ~8s.
- Satellite mini-game sectors: `{{35,55},{170,190},{305,325}}` (three narrow success bands).
- Anti-air: explicitly disabled (`oDesignator.sAATestLevel = nil`), unlike most strikes.

## Notes for modders
- `DesignationCallback` is a plain global — override it to retune the pattern (width/height/count) or swap the `"Rocket Artillery Projectile"` template for another [Airstrike template](../namespaces/airstrike#confirmed-ordnance-template-name-strings).
- To make this strike AA-blockable like the others, set the designator's `sAATestLevel` (e.g. `"medium"`) instead of leaving it `nil`.
- The oriented-rectangle math is the interesting bit: rotating your aim rotates the whole barrage footprint. Axis-aligned artillery (`MrxArtillery`) doesn't do this.