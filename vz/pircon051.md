---
title: PirCon051
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTaskContractOutpost
tags: [contract]
verified: false
---

# PirCon051

## Overview
PirCon051 is an outpost-capture contract: the player must clear and hold a single capture point at a Pirate outpost building. It's a pure config wrapper around the native `MrxTaskContractOutpost` base class — all mission-specific behavior (capturing, defending, faction ownership flip) lives in the base class; this file only supplies the outpost's layer names, capture point, and a couple of tunables.

## Inheritance
- Inherits from: [`MrxTaskContractOutpost`](../resident/mrxtaskcontractoutpost) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
Not a per-instance object module — this file defines exactly one function, `GetOutpostConfig`, which returns a plain data table read by the base class. There's no `self`-based lifecycle override here at all.

## Functions
### `GetOutpostConfig()`
Returns the outpost's configuration table:

| Field | Value |
|---|---|
| `sOutpostBldg` | `"PirJob002_02_Outpost"` |
| `tCapturePts` | `{"PirJob002_02_CapturePt1"}` |
| `sDspShortDesc` | `"[PirCon051.Objectives.001]"` |
| `sStagingLayer` | `"Vz_State_PirJob002_02_Staging"` |
| `sStagingTgLayer` | `"Vz_State_PirCon051_Tg"` |
| `sPristineLayer` | `"Vz_State_PirJob002_02_Pristine"` |
| `sDefenseLayer` | `"Vz_State_PirJob002_02_Defenses"` |
| `sCapturedLayer` | `"Vz_State_PirJob002_02_Captured"` |
| `sCapturedTgLayer` | `"Vz_State_PirCon051c_Tg"` |
| `sRivalFaction` | `"Vza"` |
| `tDangerousBldgs` | `{}` |
| `nStartingHealth` | `3` |
| `nRusherQuota` | `1` |

## Events
None registered directly in this file — the base `MrxTaskContractOutpost` class handles capture-point events using this config.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- The rival faction here is `"Vza"`, not the more common `"VZ"` seen elsewhere in this batch — likely a specific sub-faction or army-affiliated alias; not confirmed from source alone.
- Note that the outpost/staging/pristine/defense/captured layer names all reference `PirJob002_02`, not `PirCon051` — the underlying world asset naming and this contract's own filename numbering don't match. This is a naming quirk of the source, not a functional issue.
- If you're building your own outpost-style contract, `GetOutpostConfig()`'s field list here is a minimal, complete template.
