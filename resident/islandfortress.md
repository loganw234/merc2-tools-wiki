---
title: IslandFortress
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, fortress]
---

# IslandFortress

*Module: islandfortress.lua*

## Overview
The `IslandFortress` module manages the collapse and destruction of an island fortress. It uses a flood-fill algorithm to propagate damage through connected nodes based on an adjacency table.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `tFortressNodes`: A table mapping fortress GUIDs to their node lists.
- `tAdjacencyTable`: A table defining adjacency relationships between nodes.

## Functions
### `Init()`
Initializes the module by setting up the adjacency table with predefined node connections.

### `Deinit()`
Cleans up the module by clearing the `tFortressNodes` and `tAdjacencyTable`.

### `OnDeactivate(uGuid, args)`
Called when a fortress instance is deactivated. It logs a debug message, kills the object if it's alive, deletes any pending events, and removes the fortress from the `tFortressNodes` table.

### `OnStateChange(uGuid, uiNodeHashName, uiStateHashName)`
Handles state changes for fortress nodes. If the node hash is "0xCF37044A" and the state hash is "0x694683EB", it initializes a new node list and starts the collapse by calling `KillNode` on a random starting node.

### `KillNode(uGuid, sNodeName)`
Damages a specified node and schedules its neighbors for damage after a random delay (0.3–1.0 seconds). It logs a debug message, checks if the node is already damaged, applies damage if necessary, and sets up a timer to call `KillNodeSet` on adjacent nodes.

### `KillNodeSet(uGuid, tTable)`
Iterates over a list of node names and calls `KillNode` on each one.

## Events
- Listens for `Event.ObjectHibernation` (not explicitly shown in the provided code).
- Listens for custom event `OnStateChange` to handle state changes and start the collapse process.
- Creates `Event.TimerRelative` events to schedule node damage propagation.

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately to manage fortress lifecycle.
- Customize the adjacency table to change how nodes are connected.
- Use `OnStateChange` to trigger the collapse process by setting the appropriate state hashes.
- Be aware of the random delay in node damage propagation, which can affect the collapse speed.