---
title: MrxStarterManager
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, manager]
---

# MrxStarterManager

*Module: mrxstartermanager.lua*

## Overview
The `MrxStarterManager` module is responsible for managing game starters, which are likely key mission or support elements in the game. It handles the creation, activation, deactivation, and destruction of these starters, as well as their associated briefings and fanfare displays.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxFactionManager`, `MrxHqManager`, `MrxStarter`, `MrxSupportData`, `WifStarterData`

## Instance pattern
This is a stateless manager utility module. It tracks the following key fields:
- `_tStarters`: A table that holds all active starters, indexed by their names.

## Functions
### `Init()`
Initializes the module by setting up a persistent faction attitude change event listener. This event triggers a refresh of briefing room displays for all starters when the PMC faction's attitude changes. It also initializes support data by setting recruited statuses for heli pilot, mechanic, and jet pilot to false.

### `GetStarter(sName)`
Retrieves an active starter by its name from the `_tStarters` table.

### `GetStarters()`
Returns the entire `_tStarters` table containing all active starters.

### `RequestStarter(sName, bFanfareDisplayed)`
Requests a starter by its name. If the starter already exists, it returns the existing instance; otherwise, it creates a new one using `CreateStarter`.

### `CreateStarter(sName, bFanfareDisplayed)`
Creates a new starter instance for the given name and fanfare display status. It retrieves starter data from `WifStarterData`, initializes the starter with this data, activates it, and adds it to the `_tStarters` table. If the starter is associated with PMC recruitment, it updates the corresponding support data.

### `DestroyStarter(sName)`
Destroys a starter by its name by deactivating it and removing it from the `_tStarters` table.

### `DestroyAllStarters()`
Deactivates and removes all starters from the `_tStarters` table.

### `GetStarterIndexFromName(sStarterName)`
Retrieves the index of a starter by its name from the `WifStarterData._sStarters` list. Logs a warning if the starter name is not found.

### `GetStarterNameFromIndex(nStarterIndex)`
Retrieves the name of a starter by its index from the `WifStarterData._sStarters` list. Logs a warning if the starter index is not found.

### `SaveSingleton()`
Saves the state of all active starters, including whether fanfare and card displays have been shown, as well as their intros and old briefings.

### `LoadSingleton(tSaveData)`
Loads the saved state of starters from the provided save data. It recreates each starter with its saved status and updates its internal state accordingly.

## Events
- Listens for faction attitude change events to refresh briefing room displays for all starters.

## Notes for modders
- Ensure that starters are requested and destroyed appropriately using `RequestStarter` and `DestroyStarter`.
- Use `SaveSingleton` and `LoadSingleton` to manage the persistent state of starters.
- Be aware of the dependencies on imported modules like `MrxFactionManager`, `MrxSupportData`, and `WifStarterData`.