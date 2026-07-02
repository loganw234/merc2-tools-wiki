---
title: DangerousBuilding
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, world entity]
---

# DangerousBuilding

*Module: dangerousbuilding.lua*

## Overview
The `DangerousBuilding` module manages dangerous buildings in the game. It handles the activation, deactivation, and state changes of these buildings, including their radar blips, health monitoring, and attached spawners. The module also supports setting properties such as rarity and reward for these buildings.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxPmc`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tDBs`: A table storing data for each dangerous building instance.
- `nDBCount`: The current count of active dangerous buildings.
- `nMaxDBs`: The maximum number of active dangerous buildings allowed.
- `nDefaultRarity`: The default rarity value for dangerous buildings.
- `nGlobalRarity`: The global rarity value that affects the activation probability.
- `nDefaultCashReward`: The default cash reward for destroying a dangerous building.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Handles the initialization of the dangerous building instance. If the building is occupied, it calls `SetupOccupied`. Otherwise, it rolls a random chance based on rarity and activates a random dangerous building if conditions are met.

### `SetupOccupied(uGuid, bForceOnClient)`
Sets up an occupied dangerous building by adding a grey radar blip and monitoring its health. If the building is permanently occupied, it sends a network event to update the server.

### `TurnOn(uGuid, bRadar, bPermanent, bForceOnClient)`
Activates the dangerous building by turning on attached spawners and changing the radar blip to red active. It also animates the blip size and sends a network event if necessary.

### `OccupiedBuildingSpawnCallback(uGuid)`
Animates the radar blip alpha for an occupied dangerous building when it spawns.

### `TurnOnRandomDB(uGuid, bForceOnClient)`
Activates a random dangerous building by turning on attached spawners with specific settings and sending a network event if necessary.

### `OnDeactivate(uGuid)`
Called when the object instance is deactivated. It removes the dangerous building if it's not permanent and deletes associated events.

### `Delete(oSelf)`
Deletes the dangerous building instance by calling `RemoveDB`.

### `OnDeath(uGuid)`
Handles the death of a dangerous building by removing it and rewarding the player if applicable.

### `ClearProperties(uGuid)`
Clears properties for the specified dangerous building by calling `RemoveDB`.

### `RemoveDB(uGuid, bKilled, bForceOnClient)`
Removes the specified dangerous building, updates radar blips, turns off attached spawners, and sends network events as necessary. If the building is killed, it rewards the player.

### `RemoveAllDBs()`
Removes all active dangerous buildings by calling `RemoveDB` for each one.

### `GetAllDBs()`
Prints debug information about all currently active dangerous buildings.

### `GetRarity(uGuid)`
Returns the rarity value of the specified dangerous building or the global rarity if none is set.

### `SetProperties(uGuid, tProps)`
Sets properties for the specified dangerous building, including density, faction, reward, and spawner settings.

### `_Process(tTable, data)`
Processes and inserts data into a table, converting names to GUIDs if necessary.

### `ConvertToTableOfGuids(tData)`
Converts input data into a table of GUIDs.

### `ProcessProperties(uGuid, tProps)`
Processes properties for the specified dangerous building, updating density, faction, reward, and spawner settings as needed.

### `SetFaction(uGuid, sFaction)`
Sets the faction for the specified dangerous building and updates attached spawners accordingly.

### `SetWakeupFunction(uGuid, fFunction)`
Sets a wakeup function for the specified dangerous building.

### `SetRarity(uGuid, iRarity)`
Sets the rarity value for the specified dangerous building or updates the global rarity if applicable.

### `SetDBFaction(uGuid, sFaction, tProps)`
Updates the faction settings for attached spawners of the specified dangerous building.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for custom event `RemoveDangerousBuilding` to remove buildings when they are deactivated or destroyed.

## Notes for modders
- Ensure that `OnActivate`, `OnDeactivate`, and `OnDeath` are called appropriately to manage the lifecycle of dangerous buildings.
- Use `SetProperties` to customize properties such as density, faction, reward, and spawner settings.
- Be aware that network synchronization (`Net.IsClient()` and `Net.IsServer()`) may affect multiplayer behavior.
- The global rarity (`nGlobalRarity`) affects the activation probability of random dangerous buildings. Adjust it carefully to balance gameplay.