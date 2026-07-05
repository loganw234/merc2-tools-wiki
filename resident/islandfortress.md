---
title: IslandFortress
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, fortress]
verified: true
verified_note: "deeper pass: re-confirmed all 5 functions; corrected the propagation delay to its two real ranges (0.3-0.5s when a node still has health, 0.7-1.0s when already dead); surfaced the trigger hash pair, starting-node set, and 15-entry adjacency table; OnStateChange is an engine hook, sole Event.* is TimerRelative"
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
- `tAdjacencyTable`: a fixed table, keyed by node-name **hash** string (e.g. `"0x024BE2A6"`), of adjacent
  node-**name** lists (e.g. `{"Slice2A", "Slice2C"}`) — hardcoded with 15 entries covering the fortress's
  node graph, forming a mostly-linear `Slice2A…Slice2O` chain that branches to `Slice4A` at two points.
  Shared across all fortress instances (not per-`uGuid`). Note the keys are node-name **hashes** while the
  values are node **names**; `KillNode` bridges the two via `String.GetHash(sNodeName)` →
  `Sys.GuidToString(...)`.

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
Damages one node and schedules its neighbors. If the node was already visited (`tNodeList[sNodeName]` is
set), it returns immediately (prevents re-processing). Otherwise, if the node still has health
(`Object.GetNodeHealth > 0`) it deals 1 damage via `ObjectState.SendDamage(uGuid, uNodeNameHash, 1)` and
picks a **0.3–0.5 s** delay; if the node was already dead it picks a **0.7–1.0 s** delay. It then looks up
the node's neighbors in `tAdjacencyTable` and, if any exist, schedules `KillNodeSet` on them after that
delay (storing the timer handle in `tNodeList[sNodeName]`); if the node has no adjacency entry it stores
`true` instead (marks it visited, terminal).

### `KillNodeSet(uGuid, tTable)`
Iterates over a list of node names and calls `KillNode` on each one.

## Events
- `OnStateChange(uGuid, uiNodeHashName, uiStateHashName)` is an engine-invoked callback, not an
  `Event.Create` registration — there is no `OnActivate` in this file at all, so no
  `Event.ObjectHibernation` wiring exists here (the previous version of this page speculated one might
  exist "not explicitly shown"; that doesn't check out — there's nothing to show).
- `Event.TimerRelative` — the only real `Event.Create` call in this file, used in `KillNode` to schedule
  `KillNodeSet` on adjacent nodes after a random delay (0.3–0.5 s for a node still being damaged, 0.7–1.0 s
  for one already dead).

## Module constants & tunables
- **Collapse trigger:** the state change only fires when the node hash is `"0xCF37044A"` and the state hash
  is `"0x694683EB"` (compared via `Sys.GuidToString`). Any other pair is ignored.
- **Starting node:** `{"Slice2B", "Slice2C"}` — one is chosen at random (`Math.randi`) as the collapse seed.
- **Propagation delays:** `Math.randf(0.3, 0.5)` (damaging a live node) and `Math.randf(0.7, 1)` (node
  already dead) — the two knobs that set how fast the collapse ripples outward.
- **Damage amount:** `1` per `ObjectState.SendDamage` call.
- **Node graph:** the 15-entry `tAdjacencyTable` in `Init` defines which nodes propagate to which.

## Notes for modders
- **Change the collapse shape/speed:** edit `tAdjacencyTable` (topology) and the two `Math.randf` ranges in
  `KillNode` (pacing). The starting node set and the trigger hash pair are the other collapse levers.
- **Trigger from a mission:** drive the fortress into the `"0xCF37044A"`/`"0x694683EB"` node/state so the
  engine calls `OnStateChange` — that's what kicks off `KillNode`.
- `OnStateChange` is engine-invoked, not something you register; there is no `OnActivate` in this file, so
  don't expect hibernation wiring here.