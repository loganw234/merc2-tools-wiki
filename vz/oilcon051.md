---
title: OilCon051
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 8
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# OilCon051

## Overview
An Oil Company outpost-capture contract, config-only (internally `OilJob002`) — no custom `Activated`
override, unlike its sibling [OilCon050](oilcon050).

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native task-framework subclass. No lifecycle overrides — only the config getter.

## Functions
### `GetOutpostConfig()`
Returns: outpost building `OilJob002_Outpost`, one capture point (`OilJob002_CapturePt5`), a short
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
- A clean minimal-config reference: compare against [OilCon052](oilcon052) (nearly identical shape, one
  capture point and one rival faction, no custom logic) if you're templating a new outpost contract.
