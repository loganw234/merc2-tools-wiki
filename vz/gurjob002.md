---
title: GurJob002
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTaskJobVerifySet
tags: [job]
verified: false
---

# GurJob002

## Overview
A Guerilla "verify a set of targets" side job spanning two differently-numbered location series —
`GurJob002_01`–`05` and `GurJob012_01`–`05`, ten targets total under one job. Reads as a "call in tips on
enemy positions across two areas that happen to share a job design" job type.

## Inheritance
- Inherits from: [`MrxTaskJobVerifySet`](../resident/mrxtaskjobverifyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. Module-level `_tTargetNearbyVo` (one line) and `_tTargetCompleteVo` (two
lines) VO tables are handed to the base class in `Activated`.

## Functions
### `LoadAssets(self, tSaveData)`
Registers all ten targets via `self:_AddTarget{...}`, two loops of five (`string.format("%02d", i)` for
`i = 1, 5`) — first the `GurJob002_NN` series, then the `GurJob012_NN` series — each with its own
defense/staging/pristine layer names, then calls `MrxTaskJobVerifySet.LoadAssets(self, tSaveData)`.

### `Activated(self)`
Calls `MrxTaskJobVerifySet.Activated(self)`, sets the faction id to `"Gur"` (`_SetFactionId`), sets the two
VO tables, and calls `_Go()`.

## Events
None registered directly in this file — target discovery/verification events live in the native
`MrxTaskJobVerifySet` base.

## Notes for modders
This is the native `MrxTaskJobVerifySet`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- Every `MrxTaskJobVerifySet` subclass in this batch calls `_SetFactionId` in `Activated`; neither
  `MrxTaskJobDestroySet` subclass in this batch does. If you're writing a new job against one of these two
  base classes, that's a useful structural cue for which one expects an explicit faction id.
- The two-series target list (`_AddTarget` called in a loop, twice, against different name prefixes) is a
  handy pattern for a single job that logically spans two separate in-world areas.
