---
title: HijackContractManager
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [contract, hijack]
verified: true
verified_note: "deeper pass: re-confirmed all 3 functions against the 15-line source; stateless singleton with one _oContract global, zero Event.* references; caller notes for pmccon004.lua retained, no changes needed"
---

# HijackContractManager

*Module: hijackcontractmanager.lua*

## Overview
The `HijackContractManager` module is responsible for managing active hijack contracts in the game. It provides functions to set an active contract, complete it, and cancel it.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Stateless singleton module — no `OnActivate`/`Awake`/`Create`/`setmetatable`, no `uGuid` keying. It holds
exactly one piece of global state, a single active contract (not per-instance, not a table of contracts):
- `_oContract`: the currently active contract object (whatever table was last passed to
  `SetActiveContract`). Only one contract can be tracked at a time — setting a new one silently discards
  the reference to any previous one, with no cleanup call made on it.

## Functions
### `SetActiveContract(oContract)`
Sets `_oContract = oContract`. Logs a debug message. Called externally from
`src/vz/pmccon004.lua:92` (`HijackContractManager.SetActiveContract(self)`), confirming this is used by at
least one mission/contract script in the corpus.

### `CompleteActiveContract()`
Calls `_oContract:Complete()`. Logs a debug message. **No confirmed call site found anywhere in the
decompiled corpus** — can't confirm from static reading alone whether/how this gets invoked (possibly
native/engine-triggered, or simply unused in the shipped content).

### `CancelActiveContract()`
Calls `_oContract:Cancel()`. Logs a debug message. Called externally from
`src/vz/pmccon004.lua:506` (`HijackContractManager.CancelActiveContract()`).

## Events
None — no `Event.*` reference anywhere in this file.

## Notes for modders
- `SetActiveContract`/`CancelActiveContract` are confirmed used by `src/vz/pmccon004.lua`, a
  contract/mission script — that's the concrete example to look at for calling convention.
- `_oContract` must implement `:Complete()` and `:Cancel()` methods for `CompleteActiveContract`/
  `CancelActiveContract` to work; calling either when `_oContract` is `nil` (i.e., before
  `SetActiveContract` has ever run) will error.
- The module only tracks one contract globally — calling `SetActiveContract` again before the current
  contract completes/cancels overwrites `_oContract` with no warning or cleanup of the old reference.