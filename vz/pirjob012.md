---
title: PirJob012
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 8
inherits: MrxTaskJobVerifySet
tags: [job]
verified: false
---

# PirJob012

## Overview
PirJob012 is a "verify" (capture/subdue/confirm) side job against a fixed set of 10 named targets scattered around the map, each with its own defense/pristine/staging layers and a "you're getting near this one" VO cue. It's a thin config layer over the native `MrxTaskJobVerifySet` class: this file just registers the 10 targets and a couple of job-wide settings.

## Inheritance
- Inherits from: [`MrxTaskJobVerifySet`](../resident/mrxtaskjobverifyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxVoSequence`

## Instance pattern
A native `MrxTaskJobVerifySet` subclass — `self`-based lifecycle overrides, no per-instance state beyond what `_AddTarget` registers on the base class.

## Functions
### `LoadAssets(self, tSaveData)`
Registers 10 targets (`PirJob012_Target_01` through `_10`) via `self:_AddTarget{...}`, each with its own `sDefenseLayer`/`sPristineLayer`/`sStagingLayer` and a `vNearVoSequence` VO cue played when the player approaches that specific target, then calls the base `MrxTaskJobVerifySet.LoadAssets`.

### `Activated(self)`
Calls the base `MrxTaskJobVerifySet.Activated`, sets the faction id to `"Pir"`, calls `self:_SetTargetNearbyVo(_tTargetNearbyVo)` / `self:_SetTargetCompleteVo(_tTargetCompleteVo)`, and starts the job (`self:_Go()`).

### `Cleanup(self)`
A pure passthrough to `MrxTaskJobVerifySet.Cleanup(self)`.

## Events
None registered directly in this file — target proximity/verification tracking is handled by the base `MrxTaskJobVerifySet` class using the registered targets.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system (jobs included), not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- **Notable source gap:** `Activated` passes `_tTargetNearbyVo` and `_tTargetCompleteVo` to the base class, but neither table is ever defined anywhere in this file — both read as `nil` unless the base class supplies its own default. Compare [PirJob020](pirjob020), which defines both tables explicitly at file scope with range-based VO selection; this file relies solely on each target's own per-target `vNearVoSequence` field instead (there's no per-target "on complete" VO field in this file's target list). Whether the two `_SetTarget*Vo` calls here are harmless no-ops or silently dropping intended overall-progress VO lines can't be confirmed from source alone.
- If you're adding your own verify-set job, PirJob020's fully-populated `_tTargetNearbyVo`/`_tTargetCompleteVo` tables are the more complete reference to copy from.
