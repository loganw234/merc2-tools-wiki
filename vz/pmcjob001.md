---
title: PmcJob001
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 13
inherits: MrxTaskJobCollectType
tags: [job]
verified: false
---

# PmcJob001

## Overview
PmcJob001 is a "collect this type of item" side job: gather 100 `"SpareParts"`-labeled pickups scattered around the map. Like [PirJob001](pirjob001), it's a minimal config wrapper around a native job base class — all of the actual pickup tracking lives in `MrxTaskJobCollectType`.

## Inheritance
- Inherits from: [`MrxTaskJobCollectType`](../resident/mrxtaskjobcollecttype) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskJobCollectType` subclass — `self`-based lifecycle override, no module-level state.

## Functions
### `Activated(self)`
Calls the base `MrxTaskJobCollectType.Activated`, then configures the job: `self:_SetShortDescription("[PmcJob001.Objectives]")`, `self:_SetCollectName("[PmcJob001.Title]")`, `self:_SetLabelFilter("SpareParts")`, `self:_SetQuota(100)`, and `self:_Go()` to start it running. A `Debug.Printf` call at the top logs when this fires.

### `Cleanup(self)`
A pure passthrough to `MrxTaskJobCollectType.Cleanup(self)`.

## Events
None registered directly in this file — pickup collection tracking is entirely handled by the base `MrxTaskJobCollectType` class.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system (jobs included), not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- A clean, minimal reference if you're studying the `MrxTaskJobCollectType` config surface (`_SetShortDescription`, `_SetCollectName`, `_SetLabelFilter`, `_SetQuota`, `_Go`).
- The 100-item quota against a `"SpareParts"` label filter is the only thing distinguishing this job from any other collect-type job — swap the label and quota to retarget it.
