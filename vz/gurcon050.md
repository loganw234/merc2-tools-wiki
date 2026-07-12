---
title: GurCon050
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# GurCon050

## Overview
A Guerilla outpost-capture contract. Entirely config — no custom logic beyond the outpost data the native
`MrxTaskContractOutpost` base reads. Internally the outpost's building/capture-point names use a different
numbering scheme (`GurJob003`) than this file's own name (`GurCon050`), which is worth knowing if you're
trying to map a contract file to its in-world assets by name.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. No lifecycle overrides at all — the only function is the config getter.

## Functions
### `GetOutpostConfig()`
Returns the outpost's static configuration table: outpost building `GurJob003_Outpost`, one capture point
(`GurJob003_CapturePt1`), a short description key, staging/pristine/defense/captured layer names (plus a
separate "TG" — trigger-group? — layer variant for staging and captured states), rival faction `"Vza"`,
`nStartingHealth = 3`, `nRusherQuota = 1`.

## Events
None — all capture-flow event wiring lives in the native `MrxTaskContractOutpost` base, not in this file.

## Notes for modders
This is the native `MrxTaskContractOutpost`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The easiest way to see the full shape of an outpost config table with every field populated: compare
  this file against [GurCon052](gurcon052) and [GurCon053](gurcon053) — the same schema, slightly
  different field sets (e.g. `tDangerousBldgs` appears on some, not this one).
