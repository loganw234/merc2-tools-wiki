---
title: MrxSupportDesignatorSatellite
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [satellite, support]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxSupportDesignatorSatellite

*Module: mrxsupportdesignatorsatellite.lua*

## Overview
The `MrxSupportDesignatorSatellite` module is responsible for handling the satellite designator support type in the game. It manages the mini-game mechanics, zoom levels, radius, and cost associated with using a satellite to designate targets.

## Inheritance
- Inherits from: `MrxSupportDesignator`
- Imports: `MrxSupport`, `MrxGuiManager`, `MrxSupportManager`, `MrxPmc`, `MrxGuiSatellite`, `MrxSound`

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
Creates a new per-instance table for the satellite designator using the module's prototype. Initializes various fields such as owner, designation type, validation function, and other parameters.

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
- Listens for custom events related to satellite targetting end and cancellation.

## Notes for modders
- Ensure that `Commence` is called appropriately to start the satellite designator process.
- Customize zoom levels, radius, and cost by using `SetZoomLimits`, `SetRadius`, and `SetCost`.
- Be aware of AA level and fuel requirements when using this support type.
- The mini-game data can be customized by setting `tSectors`.