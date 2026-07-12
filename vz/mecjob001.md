---
title: MecJob001
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 5
inherits: MecJob
tags: [job]
verified: false
---

# MecJob001

## Overview
`MecJob001` is the first of 3 thin [`MecJob`](mecjob) subclasses — a side job asking the player to deliver
a damaged vehicle labeled `"rtr"` (displayed as reference image `global_polaroid_belmont`) to the
mechanic's garage. All of the actual delivery/garage/VO logic lives in [`MecJob`](mecjob); this file only
supplies the job-specific identity fields and spawns a starter vehicle for the player to find.

## Inheritance
- Inherits from: [`MecJob`](mecjob) (→ [`MrxTaskJob`](../resident/mrxtaskjob) →
  [`MrxTaskMission`](../resident/mrxtaskmission) → [`MrxTask`](../resident/mrxtask)) — `MecJob` is a
  locally-defined base class in this same `vz/` corpus, not a native engine class.
- Imports: [`MrxUtil`](../resident/mrxutil)

## Instance pattern
Native task-framework subclass (`self`-based) — no state of its own beyond the identity fields it sets on
`self` before deferring to its parent. See [`MecJob`](mecjob) for what those fields drive.

## Functions
### `Activated(self)`
Sets `sVehImg`/`sVehLabel`/`sObjText`/`iMinHealth`/`sIntro`/`sWrongVeh`/`sRightVeh` (label `"rtr"`,
minimum health `30`), then calls `MecJob.Activated(self)` (super call), and finally spawns an
"RTR (crappy)" vehicle at a random one of 3 named spawn points (`mecjob001.rtrspawn1/2/3`) via
[`MrxUtil.SpawnObject`](../resident/mrxutil).

## Events
None registered directly in this file — all event wiring happens in [`MecJob`](mecjob).

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system (the `MrxTaskJob` branch), not
  [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- To make a variant of this job, copy this file's shape rather than [`MecJob`](mecjob) itself — see
  [`MecJob002`](mecjob002)/[`MecJob003`](mecjob003) for how little a concrete job actually needs to define.
