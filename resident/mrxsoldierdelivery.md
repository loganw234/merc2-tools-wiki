---
title: MrxSoldierDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, delivery]
verified: true
verified_note: 'deeper pass: rewrote Events section (DesignationCallback/_WaitCallback/AllOut/FollowTheLeader are framework hook + Ai.Goal/Ai.Deploy callbacks, not "custom events"; real subscription is Event.ObjectHibernation) and surfaced constants -- default vehicle "UH1 Transport (GR) (Full)", nAltitude 50, the CheckForSoldiers <8-in-80m landing gate, Follow AI ranges; all functions re-confirmed'
---

# MrxSoldierDelivery

*Module: mrxsoldierdelivery.lua*

## Overview
The `MrxSoldierDelivery` module is responsible for delivering troop reinforcements: it flies in a
transport helicopter full of soldiers, lands at the designated zone, deploys the passengers, and orders them
to follow the player. It inherits from [`MrxSupport`](mrxsupport). [`MrxSupportData`](mrxsupportdata) wires
one instance per faction as a mission freebie (`SoldierDelivery_AL/CH/GR/OC/PR`), each with its own
transport template and HQ landing zone.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: `MrxSupportManager`, [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke), `MrxUtil`

Module constants (file scope): `sDeliveryVehicle = "UH1 Transport (GR) (Full)"`, `nAltitude = 50`,
`sModuleName = "MrxSoldierDelivery"`, `oFinalDestination = "01_pmc_hq_lz_playerone"`, and `tVOOnTheWay` (a
per-faction table of "reinforcements incoming" cues, keyed `Pmc`/`Allied`/`China`/`Pirate`/`Guerilla`/`OC`).

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oTarget`: The target for the delivery.
- `sDeliveryVehicle`: The template name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `oFinalDestination`: The final destination point for the soldiers.
- `oUpdateEvent`: An event handle for periodic updates.
- `oDesignator`: The designator object used to mark the landing zone.
- `sModuleName`: The name of the module.
- `bSupportComplete`: Indicates whether the support operation is complete.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the delivery operation using the module's prototype. Initializes the delivery vehicle and sets up the designator with validation functions.

### `DesignationCallback(self)`
A passthrough function that calls `_DesignatorCallback`.

### `SetDeliveryVehicle(self, sVehicleTemplateName)`
Sets the template name of the delivery vehicle and updates its GUID.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point for the soldiers.

### `_DesignatorCallback(self)`
Handles the callback when the designator is set. Spawns the delivery vehicle at a calculated position and sets it to land at the designated target.

### `_WaitCallback(self, uHeli, nTargetX, nTargetY, nTargetZ)`
Called after the helicopter is spawned. Plays a voice-over cue and sets up the landing goal for the helicopter.

### `AllOut(self, uHeli, uDriver, nState)`
Handles the outcome of the landing operation. If successful, deploys the soldiers to follow the player; if not, aborts the mission.

### `FollowTheLeader(self, tRiders, uHeli, uDriver)`
Sets up the AI roles for the delivered soldiers to follow the player character.

### `CheckForSoldiers(fCallback, nX, nY, nZ, self)`
The designator's validation function. Collects friendly soldiers of the delivery vehicle's faction within
`80`m (`Pg.FastCollectHumans`); if fewer than `8` are already there it defers to
`MrxSupportDesignator.ValidateLandingZone`, otherwise it denies with `"toomanysoldiers" .. sFaction` (which
[`MrxSupport.DenialMessage`](mrxsupport) maps to the per-faction "too many soldiers" message). This caps how
densely you can stack reinforcements in one spot.

## Events
Confirmed from source — the only real subscription is one `Event.ObjectHibernation`. The functions below
are the framework hook plus `Ai.Goal`/`Ai.Deploy` completion callbacks, **not** subscribed-to events:

- **`Event.ObjectHibernation`** (`"awake"`) — in `_DesignatorCallback`, waits for the spawned heli to wake,
  then runs `_WaitCallback`.
- `DesignationCallback` → `_DesignatorCallback` is the [`MrxSupport`](mrxsupport) designation hook.
- `_WaitCallback` issues a `HeliLand` `Ai.Goal` whose `Callback` is `AllOut`; `AllOut` issues an `Ai.Deploy`
  whose `Callback` is `FollowTheLeader`. These run when the AI orders finish, chained by callback, not by
  event.

Damage-abort during the flight comes from the inherited `MrxSupport.SetupDamageEvent` (heli below 60%
health).

## Notes for modders
- **Landing-zone density gate**: `CheckForSoldiers` denies the drop if ≥8 friendly soldiers of the delivery
  faction are already within 80m. Loosen the `8`/`80` if you want denser reinforcement stacking.
- **Follow behavior**: `FollowTheLeader` sets each survivor to `Role = "Follow"` on the owning player with
  `MinDistance = 10`, `MoveDistance = 12`, `MaxDistance = 50`, `medPri` — the knobs for how tightly troops
  trail you.
- **`SetDeliveryVehicle`/`SetFinalDestination`** choose the transport and where it returns; the catalog sets
  a `(Full)` transport template (soldiers ride pre-loaded) per faction.
- Customize the incoming-VO by editing the `tVOOnTheWay` table.