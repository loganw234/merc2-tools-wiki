---
title: GurCon053
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# GurCon053

## Overview
A Guerilla outpost-capture contract (internally `GurJob008_02`), notable for being one of only two outpost
files in this batch with a custom `Activated` override on top of the config. It cross-references
[OilCon050](oilcon050) via `WifMissionFlow`: whichever of the two contracts activates first plays the "you
found this outpost first" VO intro, and the other silently skips its own intro — the two files describe the
same physical outpost from two different factions' contract numbering.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxVoSequence`, `WifMissionFlow`

## Instance pattern
A native task-framework subclass. No per-instance state fields beyond what the base class tracks; the
override just adds one proximity event and a VO branch.

## Functions
### `GetOutpostConfig()`
Returns: outpost building `GurJob008_02_Outpost`, one capture point (`GurJob008_02_CapturePt3`),
staging/pristine/defense/captured layer names (plus "TG" variants), rival faction `"Vza"`,
`nStartingHealth = 3`, `nRusherQuota = 1`. No `sDspShortDesc` field here, unlike
[GurCon050](gurcon050)/[GurCon052](gurcon052) — another example of the config schema's optional fields
varying instance to instance.

### `Activated(self)`
Calls `MrxTaskContractOutpost.Activated(self)`, then checks `WifMissionFlow.HasKey("OilCon050")`. If that
key is **not** set (i.e. the player hasn't already discovered the outpost via the Oil Company side), it
arms a 100-unit proximity trigger (`NearOutpost`) and plays the "pre-oil" Fiona intro
(`GurCon053_FionaVO_Activate_PreOil`). If the key **is** set, it plays a different, shorter "post-oil" VO
line instead (`GurCon053_FionaVO_Activate_PostOil`) and skips the proximity trigger entirely.

### `GurCon053_FionaVO_Activate_PreOil(self)` / `NearOutpost(self)` / `GurCon053_FionaVO_Activate_PostOil(self)`
The three VO branches described above — a three-line "first discovery" sequence, a one-line "getting
close" bark, and a one-line "already seen it from the other side" bark.

## Events
`Event.ObjectProximity` — the 100-unit `NearOutpost` trigger, only armed on the "first discovery" path.

## Notes for modders
This is the native `MrxTaskContractOutpost`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- If you're adapting this pattern for a mod, `WifMissionFlow.HasKey(...)` is the mechanism to check
  whether a *different* contract has already been activated/completed — useful for any pair of contracts
  that share a physical location or narrative beat and shouldn't both play their "first time" introduction.
