---
title: MecJob002
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 6
inherits: MecJob
tags: [job]
verified: false
---

# MecJob002

## Overview
`MecJob002` is the second of 3 thin [`MecJob`](mecjob) subclasses — delivers a damaged vehicle labeled
`"m35"` (displayed as reference image `global_polaroid_cortez`) to the mechanic's garage. The smallest of
the three: unlike [`MecJob001`](mecjob001) it doesn't spawn its own starter vehicle, and unlike
[`MecJob003`](mecjob003) it doesn't override `LoadAssets`/`Cleanup` — it relies entirely on whatever places
the target vehicle in the world and on [`MecJob`](mecjob)'s own layer/cleanup handling.

## Inheritance
- Inherits from: [`MecJob`](mecjob) (→ [`MrxTaskJob`](../resident/mrxtaskjob) →
  [`MrxTaskMission`](../resident/mrxtaskmission) → [`MrxTask`](../resident/mrxtask)) — `MecJob` is a
  locally-defined base class in this same `vz/` corpus, not a native engine class.
- Imports: none

## Instance pattern
Native task-framework subclass (`self`-based) — no state of its own beyond the identity fields it sets on
`self` before deferring to its parent.

## Functions
### `Activated(self)`
Sets `sVehImg`/`sVehLabel`/`sObjText`/`iMinHealth`/`sIntro`/`sWrongVeh`/`sRightVeh` (label `"m35"`,
minimum health `30`) and `sPropVehTemplate = "Monster Truck phase1"` (the damaged-vehicle prop
[`MecJob`](mecjob)'s own `Activated` spawns/respawns), then calls `MecJob.Activated(self)` (super call).

## Events
None registered directly in this file — all event wiring happens in [`MecJob`](mecjob).

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system (the `MrxTaskJob` branch), not
  [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- The `sPropVehTemplate` field is what makes [`MecJob`](mecjob) spawn a visible "damaged vehicle"
  placeholder prop at `mc001.propVehicle` — omit it (as [`MecJob001`](mecjob001) does) if your variant
  doesn't need one.
