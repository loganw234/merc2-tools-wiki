---
title: MrxHARMStrike
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: "deeper pass: documented the AA-suppression targeting (ObjectFilter AA (Medium)/200-unit collect), the two sound cues, F117 jet + Vehicle AT Missile; corrected Events (LaunchMissile is a timer callback, not an event); flagged the truncated Object.Get artifact"
---

# MrxHARMStrike

*Module: mrxharmstrike.lua*

## Overview
`MrxHARMStrike` is an anti-air-suppression strike (HARM = High-speed Anti-Radiation Missile). The player beacons a spot; an F117 flies in and salvos guided missiles at nearby **medium AA** vehicles around the player. It inherits from [`MrxSupport`](mrxsupport) and designates with [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(oSelf, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who initiated the support.
- `uJet`: The GUID of the aircraft used for the strike.
- `oDesignator`: An instance of `MrxSupportDesignatorBeacon` used for target designation.

## Functions
### `Create(oSelf, uPlayerGuid)`
Creates a new per-instance table for the HARM strike support system. Initializes the designator beacon, sets the owner and recruit, and assigns the module name.

### `DesignationCallback(oSelf)`
Runs on beacon-designation complete. Computes a spawn point behind the camera and an approach path (offsets `nTargetXOffset = 0`, `nTargetZOffset = 200`), flies an F117 in with [`Airstrike.Flyby`](../namespaces/airstrike) (`"Support Vehicle (F117)"`, speed 80, callback `Strike`, jet stored in `oSelf.uJet`), then plays two [`Sound.CueSound`](../namespaces/sound) cues: `"vo_allies_a_Yes01"` (confirmation VO) and `"veh_b52_flyby"` (flyby engine sound).

### `Strike(oSelf)`
Runs when the jet arrives. Builds an [`ObjectFilter`](../namespaces/object) with filter `"AA (Medium)"` and a relation of `"<" , 0` to the hero (i.e. hostile), then `Pg.FastCollectGroundVehicles` within **200 units** of the player. For each collected vehicle that has a driver, schedules `LaunchMissile` with [`Event.TimerRelative`](../namespaces/event) staggered `0.4 * nCount` seconds apart.

### `BombExplodes(uBomb)`
Impact callback. Only `Debug.Printf("Direct Hit!")` — no gameplay effect (the damage is on the ordnance template). Note it calls `Object.GetPos` (not `GetPosition`); the result is unused.

### `LaunchMissile(oSelf, uTarget)`
Launches one homing `"Vehicle AT Missile"` from the jet toward `uTarget` via [`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike) at speed scale 30, `"impact"` detonation, callback `BombExplodes`.

{: .warning }
> `LaunchMissile` contains a truncated decompiled line — `local nPX, nPY, nPZ = Object.Get` — that is incomplete and non-functional (an artifact of the decompile, not a real call). It has no effect because those locals are never used, but don't copy it into a mod.

## Events
No event subscriptions. `DesignationCallback` is the beacon's completion callback (via [`MrxSupport:Commence`](mrxsupport)), `Strike` is the flyby-arrival callback, and `LaunchMissile` is fired by [`Event.TimerRelative`](../namespaces/event) timers — none of these are `Event.Create` subscriptions.

## Module constants & tunables
All inline (no module-level `local`s):
- Jet: `"Support Vehicle (F117)"`; flyby speed 80.
- Missile: `"Vehicle AT Missile"` (homing); `nSpeedScale = 30`.
- Target search: filter `"AA (Medium)"`, radius **200** units, one missile per driver-crewed target, `0.4s` between launches.
- Approach offsets: `nTargetXOffset = 0`, `nTargetZOffset = 200`.
- Designator AA level is set to `"advanced"` in `Create` (this strike is blocked by advanced AA).

## Notes for modders
- The `"AA (Medium)"` filter is the whole point — this strike only engages medium AA. Change the filter string in `Strike` (a plain global) to target something else, or widen the 200-unit radius for a bigger sweep.
- Swap `"Vehicle AT Missile"` for another [Airstrike template](../namespaces/airstrike#confirmed-ordnance-template-name-strings) in `LaunchMissile` to change the payload.
- The two `Sound.CueSound` strings (`"vo_allies_a_Yes01"`, `"veh_b52_flyby"`) are the audio hooks if you want to reskin the callout.