---
title: ChiJob002
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTaskJobVerifySet
tags: [job]
verified: false
---

# ChiJob002

## Overview
A China "verify" side job spanning ten targets across two location clusters — five
`ChiJob002_Target_0X` sites and five `ChiJob010_Target_0X` sites — each with its own defense/pristine/
staging layer set and (for most targets) a proximity VO line. Structurally identical to Allied Nation's
[AllJob002](alljob002) (same base class, same two-cluster-of-five shape), minus that file's jeep-assault
trigger.

## Inheritance
- Inherits from: [`MrxTaskJobVerifySet`](../resident/mrxtaskjobverifyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxVoSequence`

## Instance pattern
A native `MrxTaskJobVerifySet` subclass. A single module-level VO table, `_tTargetCompleteVo` (5 entries,
all populated — no empty-table padding, unlike [AllJob002](alljob002)'s trailing empty slots).

## Functions
### `LoadAssets(self, tSaveData)`
Registers all ten targets via `self:_AddTarget{...}` (layer names and, where present, a
`vNearVoSequence`), marks an additional pristine-tag layer for addition, then calls the base
`MrxTaskJobVerifySet.LoadAssets`.

### `Activated(self)`
Calls the base `MrxTaskJobVerifySet.Activated`, sets the faction ID to `"Chi"`, wires the completion VO
table, and starts the job with `_Go`.

### `Cleanup(self)`
Calls the base `MrxTaskJobVerifySet.Cleanup`.

## Events
None registered directly in this file — target proximity/verification tracking is handled inside the
native `MrxTaskJobVerifySet` base class.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Structural sibling**: [AllJob002](alljob002) is the Allied-faction counterpart with the same base
  class and target-cluster shape, plus a jeep-assault trigger this file doesn't have.
- Job numbering pairs across factions: this file (`002`) corresponds to [AllJob002](alljob002), the same
  way [ChiJob003](chijob003) pairs with [AllJob003](alljob003) and [ChiJob020](chijob020) pairs with
  [AllJob020](alljob020).
