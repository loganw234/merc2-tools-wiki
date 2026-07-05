---
title: MrxArtillery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, artillery]
verified: true
verified_note: "deeper pass: added ordnance/spread/timing constants (Artillery Shell, nWidth=25, 12 shells over 8s), the recruit/delivery-vehicle default (Fiona), Airstrike.SpawnOrdnance call shape, cross-links; all functions re-confirmed against source"
---

# MrxArtillery

*Module: mrxartillery.lua*

## Overview
`MrxArtillery` is a player-called artillery strike. The player drops a [beacon](mrxsupportdesignatorbeacon) to mark a spot, then this module rains a burst of ordnance down onto it. It inherits from [`MrxSupport`](mrxsupport) (which owns the cost/cooldown/network plumbing) and uses [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon) for target designation and [`MrxVoSequence`](mrxvosequence) for the "incoming!" voice-over.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon), [`MrxVoSequence`](mrxvosequence)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oDesignator`: The designator beacon used for target designation.
- `uOwner`: The GUID of the player who owns this support.
- `sRecruit`: The recruit name associated with this support.
- `sDeliveryVehicle`: The delivery vehicle used for artillery deployment.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sAmmo`: The type of ammunition used (e.g., "Artillery Shell").
- `nWidth`: The width parameter affecting the spread of missiles.
- `tVO`: Table of voice-over sequences.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new instance of `MrxArtillery` and initializes it with the given player GUID. Sets up the designator beacon, owner, recruit, delivery vehicle, and module name.

### `DesignationCallback(self)`
Runs once the beacon designation completes (the base [`MrxSupport`](mrxsupport) wires this up as the designator's complete-callback). Reads the beacon target, then hardcodes the shot pattern: `self.sAmmo = "Artillery Shell"`, `self.nWidth = 25`, `nShells = 12`, `nTime = 8`. It schedules all 12 shells with [`Event.TimerRelative`](../namespaces/event) at `3 + i * (nTime / nShells)` seconds each, and — inside the same loop — also schedules the beacon's own removal at `3.5 + nTime` seconds (only when `uBeacon and Player.IsLocal(self.uOwner)`). Finally it picks a faction-based VO table from the *delivery vehicle's* labels (Allied / China / Guerilla, else a Fiona line) and plays it via [`MrxVoSequence.Start`](mrxvosequence).

### `TriggerFallingMissile(self)`
Fires one shell. Re-reads the target (preferring the live beacon position via `Object.GetPosition(uBeacon)` if the beacon still exists, so shells track a beacon that moved), bails if there's no target, then jitters X and Z by `±self.nWidth` and spawns the round with [`Airstrike.SpawnOrdnance`](../namespaces/airstrike):
```lua
Airstrike.SpawnOrdnance(self.sAmmo, nTargetX, nTargetY + 200, nTargetZ, 0, -100, 0, "impact", 1, self.uOwner)
```
It spawns 200 units above the mark with a downward velocity of `-100` and `"impact"` detonation — a shell falling from the sky, not a horizontal projectile.

{: .note }
> The spread math `math.randf() * self.nWidth - math.randf() * self.nWidth` is applied to X and Z but **not** Y, so `nWidth` widens the impact footprint on the ground, not the drop height.

## Events
This module subscribes to **no** engine events directly. `DesignationCallback` is invoked as the beacon's completion callback (registered in [`MrxSupport:Commence`](mrxsupport)), not via `Event.Create`. The only real scheduling here is [`Event.TimerRelative`](../namespaces/event) for the 12 shell timers and the beacon-removal timer.

## Module constants & tunables
Not module-level constants — these are set inline in `DesignationCallback`, so the clean override point is the whole function (or reassign `self.sAmmo` / `self.nWidth` on the live instance before it fires — see [Airstrike](../namespaces/airstrike)):
- Ordnance template: `"Artillery Shell"` (one of the confirmed [Airstrike](../namespaces/airstrike#confirmed-ordnance-template-name-strings) template strings).
- `nWidth = 25` — ground spread radius per shell.
- `nShells = 12`, `nTime = 8` — twelve rounds walked in over ~8 seconds (first at ~3.67s, last at ~11s).
- Recruit `"Fiona"` and delivery vehicle default `"Fiona"` (set in `Create`; `uDeliveryVehicle` is looked up from the name only for its faction labels in the VO branch).

## Notes for modders
- To change what falls, swap `"Artillery Shell"` for another [Airstrike template string](../namespaces/airstrike#confirmed-ordnance-template-name-strings) — `DesignationCallback` and `TriggerFallingMissile` are plain (non-`local`) globals, so both are overridable from an `OnLoad` script.
- Increase `nShells` / decrease `nWidth` for a tighter, heavier barrage; the timer expression spreads them evenly, so raising `nShells` alone shortens the gap between rounds.
- The VO branch keys off the **delivery vehicle's** faction labels, not the player's — a quirk to be aware of if you repoint `sDeliveryVehicle`.