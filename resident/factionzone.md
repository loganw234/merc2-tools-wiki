---
title: FactionZone
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [faction, radar]
---

# FactionZone

*Module: factionzone.lua*

## Overview
The `FactionZone` module adds a colored line region to the radar and PDA map for specific faction zones. It also sends `TrespassStateChange` GUI events when players enter or exit these zones.

## Inheritance
- Inherits from: `Inheritable`
- Imports: `MrxGui`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uFaction`: The GUID of the faction associated with the zone.
- `sFaction`: The short name of the faction.
- `bActive`: Indicates whether the zone's visual and event triggers are active.
- `bTrespassing`: Tracks if a player is currently trespassing in the zone.

## Functions
### `Init()`
Initializes the module by setting up an association map that links faction names to their short identifiers.

### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It creates a new per-instance table for the object using the module's prototype.

### `Create(oPrototype, uGuid, uRuntimeOwner)`
Creates a new per-instance table for the object using the module's prototype. It sets up the faction association and enables the zone if it isn't already active.

### `Delete(oSelf)`
Tears down the per-instance table by disabling the zone and calling the base class's `Delete`.

### `BoundaryCallback(oSelf, uObjectGuid, uBoundaryGuid, sAction)`
A callback function that handles boundary events (enter/exit) for the faction zone. It sends `TrespassStateChange` GUI events to update the player's UI.

### `Enable(oSelf)`
Enables the faction zone by adding a colored line region to both the radar and PDA map. It also sets up a persistent boundary event listener.

### `Disable(oSelf)`
Disables the faction zone by removing the line regions from the radar and PDA map. It also deletes the boundary event listener and sends a final `TrespassStateChange` event if necessary.

## Events
- Listens for `Event.Boundary` to call `BoundaryCallback` when players enter or exit the faction zone.
- Sends `TrespassStateChange` GUI events on enter/exit.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the faction zone.
- Customize the faction association by modifying the `_tAssociationMap` in the `Init` function.
- Be aware that enabling/disabling the zone affects both radar and PDA map visualizations.