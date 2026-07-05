---
title: MrxUtilShell
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: "deeper pass: re-confirmed both functions verbatim; flagged real dependency gap — ProcessCallbackTable calls MergeIndexedTables, which is NOT defined in this trimmed module (only in full MrxUtil), so the both-tables branch errors here unless that global is present"
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
Processes a table of callbacks (`tCallbacks`). Each entry is a two-element array: `[1]` the callback
function, `[2]` an optional argument table. When both the entry's own args **and** `tAdditionalArgs` are
tables it merges them (see the warning below); when only one is a table it passes that one; then it invokes
the callback through `CallWithOptionalArgs`.

{: .warning }
> The merge branch calls `MergeIndexedTables(...)`, but **that function is not defined in this trimmed
> module** — it lives only in the full [`MrxUtil`](mrxutil). If `mrxutil_shell` is loaded on its own and you
> pass both a per-callback arg table *and* a `tAdditionalArgs` table, this line raises an
> "attempt to call global 'MergeIndexedTables' (a nil value)" error. Only the single-table and no-table
> paths are safe standalone. (`CallWithOptionalArgs` here is self-contained and works fine on its own.)

## Events
- none

## Notes for modders
- This is the **shell/front-end build's** cut-down copy of two [`MrxUtil`](mrxutil) helpers (identical
  bodies), so front-end/menu scripts can call them without pulling in the full gameplay `MrxUtil`.
- `CallWithOptionalArgs(fFunction, tArgs)` is the safe, standalone one: pass a function plus an optional arg
  **table**; a non-table `tArgs` means "call with no args". It silently no-ops if `fFunction` isn't a
  function.
- Prefer the full [`MrxUtil`](mrxutil) in-game — it has the complete helper set (spawning, distance, faction,
  markers) and defines `MergeIndexedTables`, avoiding the gotcha above.