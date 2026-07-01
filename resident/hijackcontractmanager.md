---
title: HijackContractManager
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [contract, hijack]
---

# HijackContractManager

*Module: hijackcontractmanager.lua*

## Overview
The `HijackContractManager` module is responsible for managing active hijack contracts in the game. It provides functions to set an active contract, complete it, and cancel it.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance pattern. It tracks the following key field:
- `_oContract`: The currently active contract object.

## Functions
### `SetActiveContract(oContract)`
Sets the active contract to `oContract`. Logs a debug message indicating that an active contract has been set.

### `CompleteActiveContract()`
Completes the currently active contract by calling its `Complete` method. Logs a debug message indicating that the active contract is being completed.

### `CancelActiveContract()`
Cancels the currently active contract by calling its `Cancel` method. Logs a debug message indicating that the active contract is being canceled.

## Events
- none

## Notes for modders
- Ensure that `SetActiveContract`, `CompleteActiveContract`, and `CancelActiveContract` are called appropriately to manage the lifecycle of hijack contracts.
- The module uses a global variable `_oContract` to track the currently active contract, so be cautious when modifying this variable directly.