---
title: MrxCombatAirPatrol
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, combat]
verified: true
verified_note: 'deeper pass: rewrote Events section (DesignationCallback/Strike are framework hook + Airstrike.Flyby callback, not "custom events") and surfaced the real tunables -- AA "basic" gate, Pilot recruit, red designator, "Airstrike AA Missile" template, 200m flying-target radius, PMC-friendly-fire skip, 0.2s missile stagger; all functions re-confirmed'
---

# MrxCombatAirPatrol

*Module: mrxcombatairpatrol.lua*

## Overview
The `MrxCombatAirPatrol` module is the "combat air patrol" (CAP) airstrike support type: it flies a jet
past the designated point ([`Airstrike.Flyby`](../namespaces/airstrike)), then fires an AA missile at every
enemy aircraft near the player. Unlike the delivery types it drops nothing and lands nothing — the jet is a
one-pass flyby. It inherits from [`MrxSupport`](mrxsupport) and uses
[`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) (red smoke) to mark the target.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support system.
- `sDeliveryVehicle`: The name of the delivery vehicle used for deploying the aircraft.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the deployed aircraft (set in `DesignationCallback`, read in `LaunchMissile`).
- `oDesignator`: a [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) set in `Create` to **red** smoke,
  AA test level `"basic"` (this strike is denied over even light AA), and a `nil` validation function.

`Create` also sets the recruit type to `"Pilot"` (so it's gated on having recruited the jet pilot — see
[`MrxSupportData`](mrxsupportdata)) and copies `sDeliveryVehicle`/`uDeliveryVehicle` from the prototype.
Note this module defines **no** module-level `sDeliveryVehicle` default of its own — the vehicle comes from
whatever the catalog entry set (`[MrxSupportData](mrxsupportdata)` uses `MrxSupport`'s default
`"Support Vehicle (Mig27)"` for `combatairpatrol`, and overrides it to the OV10 for `upcombatairpatrol`).

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the support system. Initializes the designator with specific properties and sets up the owner, recruit, and module name.

### `DesignationCallback(self)`
Called when the target designation is complete. Finds spawn and target points relative to the camera, deploys an aircraft using `Airstrike.Flyby`, and schedules a voice-over announcement for the airstrike.

### `Strike(self)`
Passed as the flyby callback (fires when the jet reaches the target). Collects all flying objects within
`200`m of the *owning player character* (`Pg.FastCollectFlying`), and for each one whose driver isn't
labeled `"pmc"`, schedules a `LaunchMissile` staggered by `0.2 * nCount` seconds. Friendly PMC aircraft are
skipped, so it won't shoot down your own recruits.

### `LaunchMissile(self, uTarget)`
Fires one homing missile at `uTarget`: computes and normalizes the jet→target vector, spawns
`"Airstrike AA Missile"` ordnance via [`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike) with
`"impact"` fuse and the support's owner, then radar-blips the *missile* red (`{255,0,0}`) via the inherited
`MrxSupport.BlipAircraft`.

## Events
Confirmed from source — this module registers **no** persistent `Event.*` subscriptions.

- `DesignationCallback` is the framework hook called by [`MrxSupport`](mrxsupport) once a target is
  designated — not an event this module subscribes to.
- `Strike` is passed to `Airstrike.Flyby(...)` as its completion callback; `LaunchMissile` is scheduled by
  `Strike` via one-shot `Event.TimerRelative` timers (the `0.2 * nCount` stagger). The only other timer is a
  `3`s `Event.TimerRelative` in `DesignationCallback` that plays Misha's incoming-airstrike VO.

## Notes for modders
- **Retargeting knobs** (all in `Strike`/`LaunchMissile`): the `200`m flying-target radius, the
  `not Object.HasLabel(..., "pmc")` friendly-fire skip, the `0.2`s per-missile stagger, and the
  `"Airstrike AA Missile"` ordnance template are the levers for changing what CAP shoots and how fast.
- **AA gate**: the `"basic"` AA test level means CAP is denied near any anti-air, including basic — loosen
  it to `"none"` on the designator if you want it usable under fire.
- The blip is applied to the *missile*, colored red — change the `{255,0,0}` in `LaunchMissile` to recolor.