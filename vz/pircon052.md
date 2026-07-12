---
title: PirCon052
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 6
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# PirCon052

## Overview
PirCon052 is a second outpost-capture contract, structurally identical to [PirCon051](pircon051) — a single capture point at a different Pirate outpost building. Like PirCon051, it's a pure config wrapper: all capture/defend/ownership-flip logic lives in the native `MrxTaskContractOutpost` base class.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
Not a per-instance object module — a single function returning a data table, no `self`-based lifecycle overrides.

## Functions
### `GetOutpostConfig()`
Returns the outpost's configuration table:

| Field | Value |
|---|---|
| `sOutpostBldg` | `"PirJob002_03_Outpost"` |
| `tCapturePts` | `{"PirJob002_03_CapturePt2"}` |
| `sDspShortDesc` | `"[PirCon052.Objectives.001]"` |
| `sStagingLayer` | `"Vz_State_PirJob002_03_Staging"` |
| `sStagingTgLayer` | `"Vz_State_PirCon052_Tg"` |
| `sPristineLayer` | `"Vz_State_PirJob002_03_Pristine"` |
| `sDefenseLayer` | `"Vz_State_PirJob002_03_Defenses"` |
| `sCapturedLayer` | `"Vz_State_PirJob002_03_Captured"` |
| `sCapturedTgLayer` | `"Vz_State_PirCon052c_Tg"` |
| `sRivalFaction` | `"Vza"` |
| `tDangerousBldgs` | `{}` |
| `nStartingHealth` | `3` |
| `nRusherQuota` | `1` |

## Events
None registered directly in this file — handled by the base `MrxTaskContractOutpost` class using this config.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Same `"Vza"` rival-faction value and `PirJob002_03`-vs-`PirCon052` naming mismatch as [PirCon051](pircon051) — see that page's notes; the pattern is consistent enough across both that it looks intentional rather than a one-off typo.
- Nearly identical to PirCon051 apart from the building/capture-point names and layer tags — useful as a second reference point if you're templating your own outpost contract.
