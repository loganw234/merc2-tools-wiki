---
title: MrxUtilShell
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
---

# MrxUtilShell

*Module: mrxutil_shell.lua*

## Overview
The `MrxUtilShell` module provides utility functions for calling functions with optional arguments and processing callback tables. It is a trimmed-down version of the full `MrxUtil` library, focusing on specific helper functionalities.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module (no per-instance table). It does not track any persistent state.

## Functions
### `CallWithOptionalArgs(fFunction, tArgs)`
Calls the provided function `fFunction` with arguments unpacked from the table `tArgs`. If `tArgs` is not a table, it calls `fFunction` without arguments. This function is used to handle functions that may or may not require arguments.

### `ProcessCallbackTable(tCallbacks, tAdditionalArgs)`
Processes a table of callbacks (`tCallbacks`). Each callback in the table is expected to be a two-element array where the first element is the callback function and the second element is an optional argument table. This function merges any additional arguments provided (`tAdditionalArgs`) with the callback's own arguments and calls the callback function with the merged arguments.

## Events
- none

## Notes for modders
- `CallWithOptionalArgs` is useful for calling functions that may or may not require arguments, simplifying function call logic.
- `ProcessCallbackTable` helps in executing multiple callbacks with optional arguments, making it easier to manage callback-driven systems.
- This module is a trimmed-down version of the full `MrxUtil` library, focusing on specific helper functionalities.