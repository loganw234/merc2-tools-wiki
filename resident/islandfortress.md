---
title: IslandFortress
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, fortress]
verified: true
verified_note: removed speculative Event.ObjectHibernation claim (file has no OnActivate at all, confirmed); clarified OnStateChange is an engine-invoked hook not an Event.Create registration; all 6 functions and 2 real Event.* constants confirmed
---

# IslandFortress

*Module: islandfortress.lua*

## Overview
The `IslandFortress` module manages the collapse and destruction of an island fortress. It uses a flood-fill algorithm to propagate damage through connected nodes based on an adjacency table.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
Stateless manager/utility module — no `OnActivate` at all in this file (confirmed by grep: only
`OnDeactivate` exists, not `OnActivate`/`Awake`/`Create`/`setmetatable`/`tInstance`). Per-fortress state is
tracked with plain `uGuid`-keyed globals, initialized in `Init()`/cleared in `Deinit()`:
- `tFortressNodes`: `uGuid -> {sNodeName -> (true | timer-event-handle)}` — tracks which nodes on a given
  fortress have already been damaged/killed, and any pending propagation timer for each.
- `tAdjacencyTable`: a fixed table, keyed by node-name hash string (e.g. `"0x024BE2A6"`), of adjacent node
  name lists — hardcoded with 14 entries covering the fortress's node graph. Shared across all fortress
  instances (not per-`uGuid`).

## Functions
### `Init()`
Initializes the module by setting up the adjacency table with predefined node connections.

### `Deinit()`
Cleans up the module by clearing the `tFortressNodes` and `tAdjacencyTable`.

### `OnDeactivate(uGuid, args)`
Called when a fortress instance is deactivated. It logs a debug message, kills the object if it's alive, deletes any pending events, and removes the fortress from the `tFortressNodes` table.

### `OnStateChange(uGuid, uiNodeHashName, uiStateHashName)`
Engine-invoked lifecycle hook (same naming convention as [`Fueltank`](fueltank)'s `OnStateChange`, and
several other resident files — not something this file registers via `Event.Create`). If the node hash
string is `"0xCF37044A"` and the state hash string is `"0x694683EB"`, it initializes `tFortressNodes[uGuid]`
to a fresh empty table, picks one of `{"Slice2B", "Slice2C"}` at random via `Math.randi`, and starts the
collapse by calling `KillNode` on that starting node. Any other hash combination is silently ignored (no
`else`).

### `KillNode(uGuid, sNodeName)`
Damages a specified node and schedules its neighbors for damage after a random delay (0.3–1.0 seconds). It logs a debug message, checks if the node is already damaged, applies damage if necessary, and sets up a timer to call `KillNodeSet` on adjacent nodes.

### `KillNodeSet(uGuid, tTable)`
Iterates over a list of node names and calls `KillNode` on each one.

## Events
- `OnStateChange(uGuid, uiNodeHashName, uiStateHashName)` is an engine-invoked callback, not an
  `Event.Create` registration — there is no `OnActivate` in this file at all, so no
  `Event.ObjectHibernation` wiring exists here (the previous version of this page speculated one might
  exist "not explicitly shown"; that doesn't check out — there's nothing to show).
- `Event.TimerRelative` — the only real `Event.Create` call in this file, used in `KillNode` to schedule
  `KillNodeSet` on adjacent nodes after a random 0.3–1.0s delay.

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately to manage fortress lifecycle.
- Customize the adjacency table to change how nodes are connected.
- Use `OnStateChange` to trigger the collapse process by setting the appropriate state hashes.
- Be aware of the random delay in node damage propagation, which can affect the collapse speed.