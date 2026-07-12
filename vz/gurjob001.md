---
title: GurJob001
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 8
inherits: MrxTaskJobDestroyType
tags: [job]
verified: false
---

# GurJob001

## Overview
A tiny Guerilla side job: destroy every object labeled `"Billboard"` (VZ propaganda billboards, going by
the label), restricted to the hero characters. All of the actual destroy-set/target-discovery logic lives
in the native `MrxTaskJobDestroyType` base; this file only supplies the label filter, hero-only flag, and
completion VO.

## Inheritance
- Inherits from: [`MrxTaskJobDestroyType`](../resident/mrxtaskjobdestroytype) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxVoSequence`

## Instance pattern
A native task-framework subclass. The only module-level state is `_tTargetCompleteVo`, a 3-entry weighted
VO table (`nWeight = 3` on each) handed to the base class.

## Functions
### `Activated(self)`
Calls `MrxTaskJobDestroyType.Activated(self)`, then configures the job: a custom short-description loc key
(`_SetShortDescription`), the `"Billboard"` label filter (`_SetLabelFilter`), hero-only targeting
(`_SetHeroOnly(true)`), the completion VO table (`_SetTargetCompleteVo`), and finally `_Go()` to start the
job running.

## Events
None registered directly in this file — target discovery/tracking/completion events all live in the
native `MrxTaskJobDestroyType` base.

## Notes for modders
This is the native `MrxTaskJobDestroyType`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- About as minimal as a `MrxTaskJobDestroyType` subclass gets: `_SetLabelFilter` + `_SetHeroOnly` + `_Go()`
  is the whole contract with everything else being cosmetic (description/VO). Good starting template if
  you want to see the smallest possible "destroy all objects with label X" job.
