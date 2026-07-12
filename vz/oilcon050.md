---
title: OilCon050
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# OilCon050

## Overview
An Oil Company outpost-capture contract (internally `OilJob001`) with a custom `Activated` override that
cross-references [GurCon053](gurcon053) via `WifMissionFlow` — the two files describe the same physical
outpost from the two factions' contract numbering, and whichever activates first gets the "first discovery"
VO while the other is skipped.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxVoSequence`, `WifMissionFlow`

## Instance pattern
A native task-framework subclass. No per-instance state beyond the one proximity event the override arms.

## Functions
### `GetOutpostConfig()`
Returns: outpost building `OilJob001_Outpost`, one capture point (`OilJob001_CapturePt1`),
staging/pristine/defense/captured layer names (plus "TG" variants), rival faction `"Vza"`,
`nStartingHealth = 3`, `nRusherQuota = 1`. No `sDspShortDesc` field.

### `Activated(self)` / `OilCon050_FionaVO_Activate(self)` / `NearOutpost(self)`
Calls `MrxTaskContractOutpost.Activated(self)`, then checks `WifMissionFlow.HasKey("GurCon053")`. If that
key is **not** set, it arms a 100-unit proximity trigger (`NearOutpost`) and plays a three-line "first
discovery" VO sequence. If the key **is** set (the Guerilla side already found this outpost), the whole
block is skipped — unlike [GurCon053](gurcon053)'s mirror check, there's no separate "already seen it"
short VO line here; this side just says nothing.

## Events
`Event.ObjectProximity` — the 100-unit `NearOutpost` trigger, only armed when this contract wins the race
to activate first.

## Notes for modders
This is the native `MrxTaskContractOutpost`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- See [GurCon053](gurcon053)'s notes for the general pattern — `WifMissionFlow.HasKey(...)` checking a
  *different* contract's id is the mechanism for two contracts sharing one physical location to avoid both
  playing a "first time here" introduction.
