---
title: AllJob002
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 8
inherits: MrxTaskJobVerifySet
tags: [job]
verified: false
---

# AllJob002

## Overview
An Allied Nation "verify" side job spanning ten targets across two location clusters — five
`AllJob002_0X_Target` sites and five `AllJob010_0X_Target` sites — each with its own defense/staging/
pristine/verified layer set and (for most targets) a proximity VO line. It also arms a one-shot "jeep
assault": entering a marked region sends an AI-driven jeep down a preset path for atmosphere.

## Inheritance
- Inherits from: [`MrxTaskJobVerifySet`](../resident/mrxtaskjobverifyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxVoSequence`

## Instance pattern
A native `MrxTaskJobVerifySet` subclass. Two module-level VO tables drive feedback:
`_tTargetNearbyVo` (3 entries) and `_tTargetCompleteVo` (7 entries, the last 3 left as empty `{}`
placeholders) — presumably indexed by target/completion order, with the trailing empty slots meaning "no
VO" once the scripted lines run out.

## Functions
### `LoadAssets(self, tSaveData)`
Registers all ten targets via `self:_AddTarget{...}` (layer names and, where present, a
`vNearVoSequence`), then calls the base `MrxTaskJobVerifySet.LoadAssets`.

### `Activated(self)`
Calls the base `MrxTaskJobVerifySet.Activated`, arms the jeep-assault trigger, sets the faction ID to
`"All"`, wires both VO tables, and starts the job with `_Go`.

### `JeepRegionActivate(self)`
Arms a boundary-enter trigger on `Region_AllJob002_04_TriggerJeep` that fires `JeepAssault`.

### `JeepAssault(self)`
Sends `AllJob002_04_Jeep01`'s driver down `Path_AllJob002_Jeep01` (one-way, high priority).

### `Cleanup(self)`
Calls the base `MrxTaskJobVerifySet.Cleanup`.

## Events
- `Event.Boundary` — entering `Region_AllJob002_04_TriggerJeep` fires `JeepAssault`.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- The `_AddTarget`/`_SetFactionId`/`_SetTargetNearbyVo`/`_SetTargetCompleteVo`/`_Go` sequence in
  `LoadAssets`/`Activated` is the general recipe for building a verify-set job on this base class — see
  [ChiJob002](chijob002) for the structurally identical China-faction counterpart (same base class, same
  two-cluster-of-five-targets shape).
- Job numbering pairs across factions: this file (`002`) corresponds to [ChiJob002](chijob002), the same
  way [AllJob003](alljob003) pairs with [ChiJob003](chijob003) and [AllJob020](alljob020) pairs with
  [ChiJob020](chijob020).
