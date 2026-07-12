---
title: PirJob020
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTaskJobDestroySet
tags: [job]
verified: false
---

# PirJob020

## Overview
PirJob020 is a "destroy this fixed set of targets" side job spanning 10 named objectives, each with its own pristine/defense/destroyed (and sometimes staging) layers. Unusually, none of the internal target names reference "PirJob020" at all — they're drawn from `PirJob007` (5 targets), `PirJob010` (3 targets), and `PirJob011` (3 targets). This reads as a job that collects leftover/scattered destroy-targets originally scoped to three other job numbers into one combined job, rather than a numbering mistake.

## Inheritance
- Inherits from: [`MrxTaskJobDestroySet`](../resident/mrxtaskjobdestroyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskJobDestroySet` subclass. Two module-level (bare global) tables drive shared VO: `_tTargetNearbyVo` and `_tTargetCompleteVo`, each a list of `{vSequence, tRange}` entries mapping a range of completed-target counts to a VO line — e.g. `tRange = {"[", 1, 5, "]"}` covers completions 1 through 5 inclusive, while `tRange = {11}` matches exactly the 11th (final tally, since there are 10 targets plus one on true completion, or a base-class count semantic not fully visible here).

## Functions
### `LoadAssets(self, tSaveData)`
Registers the 10 targets via `self:_AddTarget{...}` — `PirJob007_Objective1/2/3/7/8`, `PirJob010_Target01/02/03`, `PirJob011_Target01/02/03` — each with matching pristine/defense/destroyed layer names, then calls the base `MrxTaskJobDestroySet.LoadAssets`.

### `Activated(self)`
Calls the base `MrxTaskJobDestroySet.Activated`, wires up the shared `_tTargetNearbyVo`/`_tTargetCompleteVo` tables via `self:_SetTargetNearbyVo`/`self:_SetTargetCompleteVo`, and starts the job (`self:_Go()`).

### `Cleanup(self)`
A pure passthrough to `MrxTaskJobDestroySet.Cleanup(self)`.

## Events
None registered directly in this file — target destruction tracking is handled by the base `MrxTaskJobDestroySet` class using the registered targets.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system (jobs included), not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Compare [PirJob012](pirjob012), which calls the same `_SetTargetNearbyVo`/`_SetTargetCompleteVo` pattern but never defines the tables it passes — this file is the complete, correctly-wired version of that pattern and a good template to copy from.
- The `tRange` bracket convention (`{"[", lo, hi, "]"}` for an inclusive range, `{n}` for a single exact value) is worth knowing if you're building similar progress-tiered VO tables for your own destroy-set job.
- The target list spanning `PirJob007`/`010`/`011` object names rather than `PirJob020` is a genuine source fact, not a decompiler artifact — treat this file as an aggregation of those jobs' targets rather than a self-contained "020" mission area.
