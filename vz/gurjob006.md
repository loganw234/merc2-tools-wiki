---
title: GurJob006
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 10
inherits: MrxTaskJobDestroyType
tags: [job]
verified: false
---

# GurJob006

## Overview
An 8-line Guerilla side job: destroy every object labeled `"OC"` (Oil Company), hero-only. Notably, despite
living in the Guerilla contract/job batch, the label filter targets Oil-Company-owned objects rather than
anything Guerilla-flagged — see the note below.

## Inheritance
- Inherits from: [`MrxTaskJobDestroyType`](../resident/mrxtaskjobdestroytype) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. No module-level state at all — the file is a single function.

## Functions
### `Activated(self)`
Calls `MrxTaskJobDestroyType.Activated(self)`, sets the label filter to `"OC"`, sets hero-only targeting,
and calls `_Go()`. No custom description or VO table override — whatever `MrxTaskJobDestroyType` defaults
to is used as-is.

## Events
None — entirely delegated to the native `MrxTaskJobDestroyType` base.

## Notes for modders
This is the native `MrxTaskJobDestroyType`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The `"OC"` label filter in a Guerilla-batch file isn't a typo to "fix" — file placement in this corpus
  reflects which faction offers the job, not which faction's objects it targets. [OilJob004](oiljob004) is
  the mirror image: an Oil Company job filed under `oiljob*` that targets objects labeled `"Guerilla"`.
