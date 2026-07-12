---
title: OilJob004
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 10
inherits: MrxTaskJobDestroyType
tags: [job]
verified: false
---

# OilJob004

## Overview
A 9-line Oil Company side job: destroy every object labeled `"Guerilla"`, hero-only. The mirror image of
[GurJob006](gurjob006) — a job filed under one faction's batch that targets a different faction's objects.

## Inheritance
- Inherits from: [`MrxTaskJobDestroyType`](../resident/mrxtaskjobdestroytype) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. No module-level state — the file is a single function.

## Functions
### `Activated(self)`
Calls `MrxTaskJobDestroyType.Activated(self)`, sets the label filter to `"Guerilla"`, sets hero-only
targeting, and calls `_Go()`. No custom description or VO table override.

## Events
None — entirely delegated to the native `MrxTaskJobDestroyType` base.

## Notes for modders
This is the native `MrxTaskJobDestroyType`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- See [GurJob006](gurjob006)'s notes: file placement (which faction's `*job*` series a file lives in)
  reflects who offers the job, not which faction's objects the `_SetLabelFilter` targets. These two files
  are a matched pair confirming that's a deliberate pattern, not a one-off.
