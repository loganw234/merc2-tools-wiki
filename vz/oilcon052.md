---
title: OilCon052
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# OilCon052

## Overview
An Oil Company outpost-capture contract, config-only (internally `OilJob005`) — the third of this batch's
three near-identical Oil Company outposts, differing from [OilCon051](oilcon051) only in which building/
capture point it names.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. No lifecycle overrides — only the config getter.

## Functions
### `GetOutpostConfig()`
Returns: outpost building `OilJob005_Outpost`, one capture point (`OilJob005_CapturePt2`), a short
description key, staging/pristine/defense/captured layer names (plus "TG" variants), an empty
`tDangerousBldgs = {}`, rival faction `"Vza"`, `nStartingHealth = 3`, `nRusherQuota = 1`.

## Events
None — all capture-flow event wiring lives in the native `MrxTaskContractOutpost` base.

## Notes for modders
This is the native `MrxTaskContractOutpost`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- Field-for-field identical shape to [OilCon051](oilcon051) apart from the named building/capture point —
  the rival faction (`"Vza"`) and starting health (3) are consistent across every Oil Company outpost in
  this batch, unlike the Guerilla outposts where `nStartingHealth` varies (3/4/3).
