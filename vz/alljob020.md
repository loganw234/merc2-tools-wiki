---
title: AllJob020
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 10
inherits: MrxTaskJobDestroySet
tags: [job]
verified: false
---

# AllJob020

## Overview
An Allied Nation "destroy set" side job over 19 pre-existing targets — but every single target name it
registers is prefixed `AllJob005_`, `AllJob009_`, or `ChiJob006_`, not `AllJob020_`. Despite the
`alljob020.lua` filename, this file introduces no targets of its own; it reads as a later rollup job that
consolidates target sets originally defined for two earlier Allied jobs (`005`, `009`) and, unusually,
reaches across factions to include China's `ChiJob006` destructibles as well.

## Inheritance
- Inherits from: [`MrxTaskJobDestroySet`](../resident/mrxtaskjobdestroyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: none

## Instance pattern
A native `MrxTaskJobDestroySet` subclass. Two module-level VO tables use range-gated entries (a `tRange`
field like `{"[", 1, 10, "]"}` or a single-index `{24}`) to pick a VO line based on which numbered target
(by registration order) triggered it — a different convention than [AllJob002](alljob002)'s flat,
un-ranged VO tables (that file inherits `MrxTaskJobVerifySet` instead).

## Functions
### `LoadAssets(self, tSaveData)`
Registers all 19 targets via `self:_AddTarget{...}` (pristine/defense/destroyed/staging layer names for
each), then calls the base `MrxTaskJobDestroySet.LoadAssets`.

### `Activated(self)`
Calls the base `MrxTaskJobDestroySet.Activated`, wires both VO tables, and starts the job with `_Go`.

### `Cleanup(self)`
Calls the base `MrxTaskJobDestroySet.Cleanup`.

## Events
None registered directly in this file — target destruction tracking is handled inside the native
`MrxTaskJobDestroySet` base class.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Same pattern confirmed on the China side**: [ChiJob020](chijob020) does exactly this — a
  `MrxTaskJobDestroySet` whose registered targets are all `ChiJob005_`/`ChiJob009_`-prefixed rather than
  its own `ChiJob020_` names. Between the two, the `020`-numbered destroy-set jobs in this corpus look
  like a consistent, deliberate "consolidation job" pattern rather than a one-off.
- If you're trying to find which script owns a particular destructible, check the earlier-numbered job
  (`005`/`009`/`ChiJob006`) first — the `020` file only re-registers layer names that were likely
  authored there originally.
