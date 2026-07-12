---
title: OilJob008
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 11
inherits: MrxTaskJobDestroySet
tags: [job]
verified: false
---

# OilJob008

## Overview
An Oil Company destroy-set side job spanning 11 targets across several differently-prefixed location
series. Two of the eleven targets reuse *other* jobs' layer names for their own defense/pristine/destroyed
state — a cross-faction layer-sharing quirk worth knowing if you're tracing which layers a given contract
or job actually touches.

## Inheritance
- Inherits from: [`MrxTaskJobDestroySet`](../resident/mrxtaskjobdestroyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. Module-level `_tTargetNearbyVo` (8 entries — several lines repeated
two or three times, which biases random selection toward them by simple duplication rather than an
explicit weight field) and `_tTargetCompleteVo` (4 entries, gated by `tRange` on remaining-target count).

## Functions
### `LoadAssets(self, tSaveData)`
Registers 11 targets via `self:_AddTarget{...}`: `OilJob008b_Pristine_Objective 1`,
`_maracaibo_bld_corner32x32B 0x0009b1e1` (a raw object name rather than a job-prefixed alias), five
`_OilJob008a_Pristine_Objective N` placeholders (4 through 8), and `OilJob008_D`/`E`/`F`/`G`/`H`/`J`. Two
of these — objectives 4 and 5 — use layer names from **other** jobs' numbering
(`Vz_State_PirJob002_01_*` and `Vz_State_GurJob005_*` respectively) instead of an `OilJob008`-prefixed set,
suggesting those two targets are physically located in/near those other jobs' zones and share their layer
plumbing rather than defining dedicated layers of their own. Calls
`MrxTaskJobDestroySet.LoadAssets(self, tSaveData)` last.

### `Activated(self)` / `Cleanup(self)`
`Activated` calls the base `Activated`, sets both VO tables, and calls `_Go()` — no per-target spawner
tuning here, unlike [GurJob020](gurjob020)'s `ActivateBuilding` calls. `Cleanup` is a pure passthrough to
`MrxTaskJobDestroySet.Cleanup(self)`.

## Events
None registered directly in this file — target discovery/completion events live in the native
`MrxTaskJobDestroySet` base.

## Notes for modders
This is the native `MrxTaskJobDestroySet`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- If you're chasing down every layer a mission touches, remember cross-job layer reuse (like the two
  targets here borrowing Pirate/Guerilla job layer names) is possible — don't assume a job's layers are
  always prefixed with its own name.
