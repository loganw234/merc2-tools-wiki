---
title: PursuitCopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, support]
verified: true
verified_note: deeper pass — surfaced the blip constants (tFlash/sTexture/nSize) and the FindLZ geometry/retry tunables as a table, flagged the module-level `self`/tCopters[1] single-copter assumption, corrected the Notes (no local OnDeactivate), and added inheritance/namespace cross-links
---

# PursuitCopter

*Module: pursuitcopter.lua*

## Overview
The `PursuitCopter` module represents a pursuit helicopter that lands near the player and deploys passengers. It is part of the support system in the game, designed to provide reinforcements or additional forces during missions.

## Inheritance
- Inherits from: [`VehicleBlippable`](vehicleblippable) (→ [`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable) → [`Inheritable`](inheritable))
- Imports: [`MrxSupport`](mrxsupport)

## Instance pattern
This is a per-instance object module (keyed by `uGuid`), but `pursuitcopter.lua` itself defines no `Create`
— it inherits one through the chain [`VehicleBlippable`](vehicleblippable) →
[`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable) → [`Inheritable`](inheritable), none of
which override `Create` after `Inheritable`, so `self:Create(uGuid, uRuntimeOwner)`
(called from `FoundPosition`, line 76) resolves all the way to [`Inheritable.Create`](inheritable) — the
standard `setmetatable`/`tInstance[uGuid]` factory described on [Resident Modules](index). Module-level (not
per-instance) state:
- `tCopters`: a table (used as a queue) of GUIDs for copters currently mid-LZ-search.
- `tRetries`: retry counts, keyed by `uGuid`.

{: .note }
> `self` here is a **module-level global** set to `getfenv()` in `Start` (`self = getfenv()`, no `local`),
> not a per-instance handle. `FoundPosition`/`FindLZ`/`AllOut` all read that shared `self`, so this module
> effectively assumes one pursuit copter is being processed at a time — matching the single `tCopters[1]`
> queue-head it always operates on.

## Module constants & tunables
Blip cosmetics (read up the chain by `Blippable.AddObjective`) and the LZ-search geometry:

| Constant / value | Value | Where |
|---|---|---|
| `tFlash` | `{255, 255, 255}` | radar blip flash color |
| `sTexture` | `"temp_radar_icon_helicopter"` | radar blip texture |
| `nSize` | `5` | radar blip size |
| LZ inner / outer radius | `6` / `19` | `FindLZ` (`Ai.TestDropZone`) |
| LZ inner / outer height tolerance | `1` / `2.5` | `FindLZ` |
| LZ max height | `20` | `FindLZ` |
| LZ search radius | `40` | `FindLZ` |
| Retry nudge toward player | `+50` on Y | `FoundPosition` (`Ai.Goal` "MoveTo") |
| Retry limit / delay | `3` attempts, `3`s apart | `FoundPosition` / `FindLZ` |

The LZ geometry is built as a local `oData` table inside `FindLZ` and passed to
[`Ai.TestDropZone`](../namespaces/ai) — adjust it there to change how picky the copter is about where it
lands.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Creates a new per-instance table for the object using the module's prototype and attempts to find a landing zone for the pursuit copter.

### `FoundPosition(bFound, x, y, z)`
A callback function that handles the result of finding a landing zone. If a valid LZ is found, it sets up a landing goal; otherwise, it retries or sends the copter home if too many attempts fail.

Exact retry behavior, read directly from source: **3 attempts**, tracked per-`uGuid` in `tRetries`. Each
failed attempt also nudges the pilot 50 units toward the player (`Ai.Goal({Goal = "MoveTo", ...})`)
before trying again 3 seconds later. On both "no LZ found at all" and "3 retries exhausted," it calls
`MrxSupport.GoHome(self, uGuid)` — the same fallback used elsewhere in the support-delivery system for
"couldn't complete the delivery, send the vehicle away" (see [Support & Airstrikes](cat-support-airstrikes)).

### `AllOut(self, uGuid, nState)`
Handles the outcome of the landing goal. If successful, it deploys passengers; if not, it sends the copter home.

### `FindLZ(uGuid)`
Attempts to find a suitable landing zone for the pursuit copter using AI functions and sets up a callback to handle the result.

## Events
- `Event.ObjectHibernation` (in `OnActivate`) — fires `Start` once the object leaves hibernation.
- `Event.TimerRelative` (in `FindLZ`, on retry) — schedules another `FindLZ` attempt 3 seconds later when
  `Ai.TestDropZone` fails to find a valid landing zone.
- `FoundPosition` and `AllOut` are not `Event.*` registrations themselves — they're passed as bare
  `Callback` fields to `Ai.TestDropZone` and `Ai.Goal`/`Ai.Deploy` respectively, which are native AI
  functions, not the `Event.Create` mechanism.

## Notes for modders
- There is **no local `OnDeactivate`** in this file — lifecycle teardown falls through to the inherited
  [`VehicleBlippable`](vehicleblippable) chain. `OnActivate` is the only engine lifecycle callback defined here.
- Customize the landing-zone pickiness by editing the `oData` geometry in `FindLZ` (inner/outer radius,
  height tolerances, search radius — table above), or the retry limit by changing the `> 3` check in
  `FoundPosition`.
- Because the module keys almost everything off the shared `self`/`tCopters[1]` head rather than per-`uGuid`
  state, two pursuit copters searching for an LZ at the same time can interfere — worth knowing before you
  spawn several at once.