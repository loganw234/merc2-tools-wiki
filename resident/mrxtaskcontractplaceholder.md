---
title: MrxTaskContractPlaceholder
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskContract
tags: [task, contract]
verified: true
verified_note: 'deeper pass: confirmed the entire 11-line source — Activated calls MrxTaskContract.Activated
  then MrxCinematic.PlaceholderSequence with a single hardcoded caption and self.Complete as the callback;
  cross-linked MrxCinematic; removed the vacuous OnActivate note (engine-called, not a modder lever).'
---

# MrxTaskContractPlaceholder

*Module: mrxtaskcontractplaceholder.lua*

## Overview
The `MrxTaskContractPlaceholder` module is a stub implementation of a task contract. It provides a placeholder sequence to indicate that the contract is not yet implemented, and automatically completes upon activation.

## Inheritance
- Inherits from: `MrxTaskContract`
- Imports: `MrxCinematic`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskContract`](mrxtaskcontract)'s class-factory pattern** (itself
inherited from [`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general
mechanism), identified by name/lineage rather than a world-object GUID. It does not track any additional
state beyond what is inherited from `MrxTaskContract`.

## Functions
### `Activated(self)`
The only function in the file. Calls `MrxTaskContract.Activated(self)` (all the real contract-start work is
inherited — see [`MrxTaskContract`](mrxtaskcontract)), then plays a single-caption placeholder via
[`MrxCinematic.PlaceholderSequence`](mrxcinematic):

```lua
MrxCinematic.PlaceholderSequence(
  {{ sCaption = "This contract is not yet implemented." }},
  self.Complete, {self})
```

The caption string is hardcoded (not localized), and `self.Complete` — the inherited
[`MrxTaskContract.Complete`](mrxtaskcontract) — is the sequence's completion callback, so dismissing the
placeholder immediately completes the contract (running the normal fanfare/reward flow).

## Events
None. No `Event.*` calls; no lifecycle callbacks beyond the inherited `Activated`.

## Notes for modders
- This is a genuine stub — it's how the game fills a contract slot whose real implementation doesn't exist
  yet. Point a mission's `sModuleName` at a real subclass ([`MrxTaskContractOutpost`](mrxtaskcontractoutpost),
  or one built on [`MrxTaskContract`](mrxtaskcontract)) to give it actual objectives.
- If you want a placeholder that *doesn't* auto-complete (e.g. to keep a slot occupied without paying out),
  pass a different callback than `self.Complete` — but note the completion runs the base contract's full
  reward/fanfare path, so an unfinished stub still grants its configured rewards.