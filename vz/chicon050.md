---
title: ChiCon050
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 6
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# ChiCon050

## Overview
A China outpost-capture side contract wrapping the `ChiJob001_01` outpost location. All mission-specific
data lives in the config table returned by `GetOutpostConfig` (capture point, layer names, starting
health, rival faction); `Activated` only adds a single introductory VO line on top of the base
`MrxTaskContractOutpost` behavior.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskContractOutpost` subclass — no instance state of its own; entirely config plus a
one-line VO hook.

## Functions
### `GetOutpostConfig()`
Returns the outpost's static configuration: `sOutpostBldg = "ChiJob001_01_Outpost"`, its single capture
point (`ChiJob001_01_CapturePt3`), the staging/pristine/defense/captured layer names, `sRivalFaction =
"Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1`.

### `Activated(self)`
Calls the base `MrxTaskContractOutpost.Activated`, then plays a single introductory VO line
(`Fiona-In-Mission-Contract-Chi050-01`).

## Events
None registered directly in this file — outpost capture/defense event wiring lives in the native
`MrxTaskContractOutpost` base class, not shown here.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- Calls `MrxVoSequence.Start(...)` without a local `import("MrxVoSequence")` — presumably already present
  in the global namespace by the time this loads (imports are process-wide once any previously loaded
  script has run them). The same pattern appears in every `MrxTaskContractOutpost` file in this batch,
  Allied and China alike.
- `sRivalFaction = "Vza"`, `nStartingHealth = 6`, `nRusherQuota = 1` match every other outpost file in
  this batch (Allied and China) — shared defaults for this class of side contract.
- The outpost's own location prefab is named `ChiJob001_01`, distinct from this contract script's own
  `ChiCon050` name.
