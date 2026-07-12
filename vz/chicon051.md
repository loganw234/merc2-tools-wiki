---
title: ChiCon051
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# ChiCon051

## Overview
A China outpost-capture side contract wrapping the `ChiJob001_02` outpost location. Same shape as
[ChiCon050](chicon050)/[ChiCon053](chicon053): a static config table plus a one-line VO hook (here, a
short banter exchange) on activation.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskContractOutpost` subclass — no instance state of its own; entirely config plus a
one-line VO hook.

## Functions
### `GetOutpostConfig()`
Returns the outpost's static configuration: `sOutpostBldg = "ChiJob001_02_Outpost"`, its single capture
point (`ChiJob001_02_CapturePt2`), the staging/pristine/defense/captured layer names, `sRivalFaction =
"Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1`.

### `Activated(self)`
Calls the base `MrxTaskContractOutpost.Activated`, then plays an introductory VO exchange
(`Fiona-In-Mission-Contract-Chi051-01` plus a per-hero follow-up line).

## Events
None registered directly in this file — outpost capture/defense event wiring lives in the native
`MrxTaskContractOutpost` base class, not shown here.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- Calls `MrxVoSequence.Start(...)` without a local `import("MrxVoSequence")` — see
  [ChiCon050](chicon050)'s notes for why that's presumably not an error.
- `sRivalFaction = "Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1` match every other outpost file in
  this batch.
- The outpost's own location prefab is named `ChiJob001_02`, distinct from this contract script's own
  `ChiCon051` name.
