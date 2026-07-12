---
title: AllCon050
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# AllCon050

## Overview
An Allied Nation outpost-capture side contract wrapping the `AllJob001_01` outpost location. All
mission-specific data lives in the config table returned by `GetOutpostConfig` (capture point, layer
names, starting health, rival faction); `Activated` only adds an introductory VO line on top of the base
`MrxTaskContractOutpost` behavior.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskContractOutpost` subclass — no instance state of its own beyond what the base class
tracks. This file is entirely config plus a one-line VO hook.

## Functions
### `GetOutpostConfig()`
Returns the outpost's static configuration: `sOutpostBldg = "AllJob001_01_Outpost"`, its single capture
point (`AllJob001_01_CapturePt1`), the staging/pristine/defense/captured layer names, `sRivalFaction =
"Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1`.

### `Activated(self)`
Calls the base `MrxTaskContractOutpost.Activated`, then plays an introductory VO exchange
(`Fiona-In-Mission-Contract-All050-02` plus a per-hero follow-up line).

## Events
None registered directly in this file — outpost capture/defense event wiring lives in the native
`MrxTaskContractOutpost` base class, not shown here.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- This file calls `MrxVoSequence.Start(...)` without a local `import("MrxVoSequence")` — presumably
  already present in the global namespace by the time this loads (imports are process-wide once any
  previously loaded script has run them). The same pattern appears in every `MrxTaskContractOutpost`
  file in this batch.
- `sRivalFaction = "Vza"` and `nStartingHealth = 6`/`nRusherQuota = 1` are identical across every outpost
  file in this batch — likely shared defaults for this whole class of side contract, worth checking before
  assuming they're unique to this outpost.
- The outpost's own location prefab is named `AllJob001_01`, distinct from this contract script's own
  `AllCon050` name — the "job" location and the "contract" wrapper that activates it are numbered
  independently.
