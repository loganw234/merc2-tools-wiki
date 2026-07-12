---
title: MecJob003
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 7
inherits: MecJob
tags: [job]
verified: false
---

# MecJob003

## Overview
`MecJob003` is the third of 3 thin [`MecJob`](mecjob) subclasses — delivers a damaged vehicle labeled
`"amx30"` (displayed as reference image `global_polaroid_calderone`) to the mechanic's garage. Like
[`MecJob002`](mecjob002) it uses a `sPropVehTemplate` placeholder prop, but it's the only one of the three
that adds its own extra layer (`Vz_State_MecJob003`) and its own `Cleanup` override to mark that layer for
removal again afterward.

## Inheritance
- Inherits from: [`MecJob`](mecjob) (→ [`MrxTaskJob`](../resident/mrxtaskjob) →
  [`MrxTaskMission`](../resident/mrxtaskmission) → [`MrxTask`](../resident/mrxtask)) — `MecJob` is a
  locally-defined base class in this same `vz/` corpus, not a native engine class.
- Imports: none

## Instance pattern
Native task-framework subclass (`self`-based) — no state of its own beyond the identity fields it sets on
`self` before deferring to its parent.

## Functions
### `LoadAssets(self, tSaveData)`
Overrides [`MecJob`](mecjob)'s `LoadAssets` to add an extra layer, `Vz_State_MecJob003`, alongside the
usual `vz_state_gua_upperclass_pristine`/`Vz_State_MecJob` pair, before calling `AssetsLoaded`.

### `Activated(self)`
Sets `sVehImg`/`sVehLabel`/`sObjText`/`iMinHealth`/`sIntro`/`sWrongVeh`/`sRightVeh` (label `"amx30"`,
minimum health `30`) and `sPropVehTemplate = "Monster Truck phase2"`, then calls `MecJob.Activated(self)`
(super call).

### `Cleanup(self)`
Marks `Vz_State_MecJob003` for removal (undoing the extra layer from `LoadAssets`), then calls
`MecJob.Cleanup(self)` (super call).

## Events
None registered directly in this file — all event wiring happens in [`MecJob`](mecjob).

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system (the `MrxTaskJob` branch), not
  [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- If you add your own extra layer in a `LoadAssets` override like this one, remember to mirror it with a
  `Cleanup` override that marks it for removal — [`MecJob002`](mecjob002) needs neither because it adds no
  extra layer of its own.
