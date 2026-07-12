---
title: AllCon053
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# AllCon053

## Overview
An Allied Nation outpost-capture side contract wrapping the `AllJob001_04` outpost location. Same shape
as [AllCon050](allcon050)/[AllCon052](allcon052): a static config table plus a one-line VO hook on
activation.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskContractOutpost` subclass — no instance state of its own; entirely config plus a
one-line VO hook.

## Functions
### `GetOutpostConfig()`
Returns the outpost's static configuration: `sOutpostBldg = "AllJob001_04_Outpost"`, its single capture
point (`AllJob001_04_CapturePt1`), the staging/pristine/defense/captured layer names, `sRivalFaction =
"Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1`.

### `Activated(self)`
Calls the base `MrxTaskContractOutpost.Activated`, then plays a single introductory VO line
(`Fiona-In-Mission-Contract-All053-01`).

## Events
None registered directly in this file — outpost capture/defense event wiring lives in the native
`MrxTaskContractOutpost` base class, not shown here.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- Calls `MrxVoSequence.Start(...)` without a local `import("MrxVoSequence")` — see
  [AllCon050](allcon050)'s notes for why that's presumably not an error.
- `sRivalFaction = "Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1` match every other outpost file in this
  batch — shared defaults for this class of side contract rather than anything unique to this outpost.
- The outpost's own location prefab is named `AllJob001_04`, distinct from this contract script's own
  `AllCon053` name.
