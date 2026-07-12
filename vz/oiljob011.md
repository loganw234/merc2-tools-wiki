---
title: OilJob011
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 12
inherits: MrxTaskJobVerifySet
tags: [job]
verified: false
---

# OilJob011

## Overview
An Oil Company "verify a set of targets" side job spanning two location series —
`OilJob011_Target_01`–`05` and `OilJob012_Target_01`–`05`, ten targets total under one job. Structurally the
Oil Company counterpart to [GurJob002](gurjob002).

## Inheritance
- Inherits from: [`MrxTaskJobVerifySet`](../resident/mrxtaskjobverifyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. Module-level `_tTargetNearbyVo` (5 entries) and `_tTargetCompleteVo`
(6 entries, gated by `tRange` on remaining-target count) are handed to the base class in `Activated`.

## Functions
### `LoadAssets(self, tSaveData)`
Registers the five `OilJob011_Target_0N` targets individually, then the five `OilJob012_Target_NN` targets
in a `for i = 1, 5` loop using `string.format("%02d", i)` — the same two-series shape as
[GurJob002](gurjob002), just built with a literal block for the first five instead of a loop for both.
Note the `OilJob012` targets' staging/pristine layer names are built from an `"OilJob011_"` prefix rather
than `"OilJob012_"` (e.g. `vz_State_OilJob011_01_staging` for an `OilJob012_Target_01` target) — likely a
copy-paste artifact from writing the second loop off the first block, though harmless as long as those
layers actually exist under that name. Calls `MrxTaskJobVerifySet.LoadAssets(self, tSaveData)` last.

### `Activated(self)`
Calls `MrxTaskJobVerifySet.Activated(self)`, sets the faction id to `"Oil"` (`_SetFactionId`), sets both VO
tables, and calls `_Go()`.

## Events
None registered directly in this file — target discovery/verification events live in the native
`MrxTaskJobVerifySet` base.

## Notes for modders
This is the native `MrxTaskJobVerifySet`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- Confirms the pattern noted on [GurJob002](gurjob002): every `MrxTaskJobVerifySet` subclass in this batch
  calls `_SetFactionId` in `Activated` (here, `"Oil"`), while `MrxTaskJobDestroySet` subclasses
  ([GurJob020](gurjob020), [OilJob008](oiljob008)) never do.
