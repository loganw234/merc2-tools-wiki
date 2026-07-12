---
title: GurCon052
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 6
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# GurCon052

## Overview
A Guerilla outpost-capture contract, config-only like [GurCon050](gurcon050). Internally named after
`GurJob008_01`. Includes an explicit (empty) `tDangerousBldgs` field that `GurCon050` omits entirely,
suggesting the outpost config schema tolerates optional fields being left out rather than requiring a fixed
shape.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. No lifecycle overrides — only the config getter.

## Functions
### `GetOutpostConfig()`
Returns: outpost building `GurJob008_01_Outpost`, one capture point (`GurJob008_01_CapturePt4`), a short
description key, staging/pristine/defense/captured layer names (plus separate "TG" staging/captured
variants), an empty `tDangerousBldgs = {}`, rival faction `"Vza"`, `nStartingHealth = 4` (one higher than
`GurCon050`/`GurCon053`), `nRusherQuota = 1`.

## Events
None — capture-flow event wiring lives in the native `MrxTaskContractOutpost` base.

## Notes for modders
This is the native `MrxTaskContractOutpost`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- `nStartingHealth` is the one field that visibly differs across this batch's three Guerilla outposts (3,
  4, 3) — the most likely per-outpost balance knob if you're adapting one of these.
