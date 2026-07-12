---
title: ChiJob020
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 11
inherits: MrxTaskJobDestroySet
tags: [job]
verified: false
---

# ChiJob020

## Overview
A China "destroy set" side job over eight pre-existing targets — seven `ChiJob005_A` through `_G`
building targets plus one `ChiJob009_A` target (an oilrig demo object) — none of them `ChiJob020_`-named.
This is the same rollup pattern as Allied Nation's [AllJob020](alljob020): despite the `chijob020.lua`
filename, every target it registers was very likely authored for an earlier-numbered job (`005`, `009`),
not for this one.

## Inheritance
- Inherits from: [`MrxTaskJobDestroySet`](../resident/mrxtaskjobdestroyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxLayerManager`

## Instance pattern
A native `MrxTaskJobDestroySet` subclass. Two module-level VO tables use range-gated entries (a `tRange`
field like `{"[", 1, 2, "]"}` or a single-index `{8}`) to pick a VO line based on which numbered target
(by registration order) triggered it — the same convention [AllJob020](alljob020) uses.

## Functions
### `LoadAssets(self, tSaveData)`
Registers all eight targets via `self:_AddTarget{...}` (pristine/defense/destroyed/staging layer names
for each), marks an additional pristine-tag layer for addition, then calls the base
`MrxTaskJobDestroySet.LoadAssets`.

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

- **Same pattern confirmed on the Allied side**: [AllJob020](alljob020) does exactly this — a
  `MrxTaskJobDestroySet` whose registered targets are all `AllJob005_`/`AllJob009_`/`ChiJob006_`-prefixed
  rather than its own `AllJob020_` names. Between the two, the `020`-numbered destroy-set jobs in this
  corpus look like a consistent, deliberate "consolidation job" pattern rather than a one-off.
- If you're trying to find which script owns a particular destructible, check the earlier-numbered job
  (`005`/`009`) first — this file only re-registers layer names likely authored there originally.
