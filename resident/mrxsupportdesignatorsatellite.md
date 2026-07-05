---
title: MrxSupportDesignatorSatellite
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [satellite, support]
verified: true
verified_note: "deeper pass: surfaced module-level defaults (zoom 170, radius 100, cost 5000), documented the PDA-map mini-game flow (BeginSatelliteDesignation -> end/cancel callbacks -> PostEndStep gate), the satellite view enter/exit sounds; flagged the sAATestLevel = bil typo; cross-linked base + consumers"
---

# MrxSupportDesignatorSatellite

*Module: mrxsupportdesignatorsatellite.lua*

## Overview
`MrxSupportDesignatorSatellite` is the most elaborate [designator](mrxsupportdesignator) subtype: instead of throwing an item, the player enters a top-down PDA/satellite view and targets through a mini-game (rotating dial into success sectors). It manages zoom, radius, cost, the satellite-view enter/exit sounds, and the end/cancel/gate callback flow. Used by [`MrxSatelliteGuidedBomb`](mrxsatelliteguidedbomb), [`MrxSurgicalStrike`](mrxsurgicalstrike), and [`MrxRocketArtillery`](mrxrocketartillery).

## Inheritance
- Inherits from: [`MrxSupportDesignator`](mrxsupportdesignator)
- Imports: [`MrxSupport`](mrxsupport), [`MrxGuiManager`](mrxguimanager), [`MrxSupportManager`](mrxsupportmanager), [`MrxPmc`](mrxpmc), [`MrxGuiSatellite`](mrxguisatellite), [`MrxSound`](mrxsound)

## Instance pattern
**Same class-factory pattern as `MrxSupportDesignator`, not per-`uGuid`** — `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no
`tInstance` registry. It tracks the following key fields:
- `nStartZoom`: Initial zoom level for the satellite view.
- `nMinZoom`: Minimum zoom level allowed.
- `nMaxZoom`: Maximum zoom level allowed.
- `nRadius`: Radius of the designated area.
- `tSectors`: Data for the mini-game sectors (if used).
- `nCost`: Cost associated with using the satellite designator.

## Functions
### `SetZoomLimits(self, nMinZoom, nMaxZoom, nStartZoom)`
Sets or updates the zoom limits and start zoom level for the satellite view. If any parameter is omitted, it defaults to the current value.

### `SetRadius(self, nRadius)`
Sets or updates the radius of the designated area.

### `SetMinigameSectors(self, tSectorData)`
Sets the sector data for the mini-game used in the satellite designator.

### `SetCost(self, nCost)`
Sets or updates the cost associated with using the satellite designator.

### `ShouldSuppressIconAnimationOnDirectUse(self)`
Returns true to suppress icon animation when the satellite designator is used directly.

### `Create(self, oNewDesignator)`
Stamps the satellite fields (`sDesignationType = "Satellite Designator"`) plus the zoom/radius/cost/sector values, carrying the module-level defaults through unless the prototype overrides them.

{: .warning }
> `Create` sets `oNewDesignator.sAATestLevel = bil` — `bil` is an **undefined global**, so this evaluates to `nil`. The likely intent was `nil` anyway (satellite strikes leave AA-gating to the parent support / `PostEndStep`), so the effect is harmless, but `bil` is a decompile typo, not a real variable. Don't reference `bil`.

### `Commence(self, bFireImmediately)`
Begins the process of using the satellite designator. It equips the designator to the player and sets up the PDAMap mode with appropriate parameters.

### `GetType(self)`
Returns the type of the support designator, which is `"satellite"`.

### `BeginSatelliteDesignation(self)`
Enters the satellite view and sets up the mini-game or direct targeting based on whether a minigame is used. It also handles callbacks for successful targeting, cancellation, and post-end steps.

### `SatelliteTargettingEnd(oDesignator, uGuid, x, y, z)`
Handles the end of the satellite targetting process. Updates the designated location, exits the satellite view, and schedules a post-end step.

### `SatelliteTargettingCancel(oDesignator)`
Handles the cancellation of the satellite targetting process. Exits the satellite view and resets callbacks.

### `PostEndStep(oDesignator)`
Performs checks for AA level, fuel availability, and recruit cooldown before completing the designation.

### `_DelayDesignationComplete(oDesignator)`
Delays the completion of the designation if the recruit is available.

### `DoNothing()`
A trivial function that does nothing. Used as a placeholder callback.

## Events
No `Event.Create` subscriptions. The flow is callback-driven: `Commence` → `Airstrike.EquipDesignator(..., BeginSatelliteDesignation, ...)`; targeting end/cancel are registered via `Player.SetPDAMapModeCallback` / `SetPDAMapModeCancelCallback` and `MrxGuiManager.SetSatelliteSuccessCallback`. The only timer is a single `Event.TimerRelative` of **0.2s** in `SatelliteTargettingEnd` before `PostEndStep` runs.

## Module constants & tunables
Module-level globals (top of file) — these are real defaults you can read/override:
- `nStartZoom = 170`, `nMinZoom = 170`, `nMaxZoom = 170` — all equal by default, i.e. **zoom is locked** unless a support calls `SetZoomLimits`.
- `nRadius = 100` — designated-area radius.
- `tSectors = false` — no mini-game sectors by default (direct targeting); a support sets them via `SetMinigameSectors`.
- `nCost = 5000` — default satellite cost (overridden per-support: e.g. [`MrxSatelliteGuidedBomb`](mrxsatelliteguidedbomb) uses 1000, [`MrxSurgicalStrike`](mrxsurgicalstrike) uses 0).
- Satellite view audio: `MrxSound.EnterSatelliteView()` / `ExitSatelliteView()` bracket the PDA session.

## Notes for modders
- The three default zoom values are identical, so zoom does nothing until a support widens them with `SetZoomLimits(nMin, nMax, nStart)` — a common "why won't it zoom" gotcha.
- `tSectors = false` means the mini-game is off unless a support supplies sectors; the number and width of sectors is the difficulty knob (compare the wide sectors in [`MrxSurgicalStrike`](mrxsurgicalstrike) vs. the narrow ones in [`MrxRocketArtillery`](mrxrocketartillery)).
- The affordability/AA/recruit gate lives in `PostEndStep` (runs 0.2s after targeting ends): it routes denials through [`MrxSupport.DenialMessage`](mrxsupport) and only calls `CompleteDesignation` if the recruit is available.
- `_DelayDesignationComplete` and `DoNothing` are helpers (`DoNothing` is a placeholder callback handed to `SetPDAMapModeCallback` after targeting, to avoid re-entry).