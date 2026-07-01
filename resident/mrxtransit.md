---
title: MrxTransit
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [transit, landing zone]
---

# MrxTransit

*Module: mrxtransit.lua*

## Overview
The `MrxTransit` module manages the transit system in the game, including handling player fast-travel to different landing zones. It provides functions for opening the transit interface, initiating a transit, and managing the state of various landing zones.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui`, `MrxSupportTransit`, `MrxUnlockFanfare`, `MrxFactionManager`, `MrxUtil`, `MrxSound`, `MrxAchievements`, `MrxState`, `MrxStatsManager`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_tLandingZones`: A table containing data for each landing zone.
- `_bInitialized`: Indicates whether the transit system has been initialized.
- `_bEnabled`: Indicates whether the transit system is enabled.
- `_nTransitFuelCost`: The fuel cost per fast-travel.
- `_bInTransit`: Indicates whether a transit is currently in progress.

## Functions
### `OpenInterface(uPlayerGuid, fCallback, tCallbackData)`
Opens the transit interface for the specified player. It checks if the system is initialized and enabled, then gathers data on available landing zones and opens the interface using `MrxGui`.

### `_InterfaceCallback(sNumber, bSuccess, fCallback, tCallbackData, oPda)`
Handles the callback from the transit interface. Closes the PDA interface and calls the provided callback function with the selected zone number and success status.

### `Transit(nLocation)`
Initiates a fast-travel to the specified landing zone. It checks if the system is initialized and enabled, verifies the location's availability, and then teleports players to the destination using `MrxUtil.TeleportHeroesToLocations`.

### `GetTransitPoint(nLocation)`
Returns the transit point (location) for the specified landing zone.

### `GetName(nId, bAppendIcon)`
Retrieves the name of a landing zone. Optionally appends an inline icon based on the faction associated with the zone.

### `GetUnlockedLocations()`
Returns a table of all unlocked landing zones.

### `GetUnlockableLocations()`
Returns a table of all unlockable landing zones (excluding those flagged as fake).

### `GetNumValidLocations()`
Returns the number of valid, enabled, and not suppressed landing zones.

### `EnableFactionLocations(sFactionAbbrev, bAllow)`
Enables or disables all landing zones associated with the specified faction based on the `bAllow` parameter.

### `SetLocationEnabled(nLocation, sFactionAbbrev, bSuppressFanfare)`
Sets a specific landing zone as enabled and assigns it to the given faction. Optionally suppresses the fanfare if `bSuppressFanfare` is true.

### `_GetTableSizeSlow(t)`
A helper function that returns the size of a table by counting its elements.

### `SuppressLocation(nLocation, bSuppress)`
Suppresses or unsuppresses a specific landing zone based on the `bSuppress` parameter.

### `IsLocationEnabled(nLocation)`
Checks if a specific landing zone is enabled.

### `SetLocationIsNuked(nLocation, bIsNuked)`
Sets whether a specific landing zone has been nuked.

### `IsSystemEnabled()`
Returns whether the transit system is enabled.

### `SetSystemEnabled(bEnable, bAnimate, bHidden)`
Enables or disables the transit system. Optionally animates the change and hides the interface based on the provided parameters.

### `IsSystemInitialized()`
Returns whether the transit system has been initialized.

### `Reset()`
Resets the transit system by initializing it with data from `Pg.GetAllLandingZones`.

### `SaveSingleton()`
Saves the current state of the transit system, including enabled status and landing zone data.

### `LoadSingleton(tSaveData)`
Loads the saved state of the transit system from the provided `tSaveData` table.

### `UnlockAllLandingZones()`
Unlocks all landing zones by enabling them for the PMC faction.

### `GetTransitFuelCost()`
Returns the fuel cost per fast-travel.

### `IsInTransit()`
Checks if a transit is currently in progress.

### `StartTransit(fEnterCallback, fExitCallback, tCallbackData)`
Starts a transit process by entering the waiting-for-streaming state and sending a custom network event.

### `FinishTransit(fCallback, tCallbackArgs)`
Finishes the transit process by exiting the waiting-for-streaming state and calling the provided callback function.

### `NetEventCallback(nEventType, tArgs)`
Handles network events related to the transit system. It processes events for enabling/disabling the system and starting a transit.

## Events
- Listens for custom event `NETEVENT_CLIENTTRANSIT` to handle client-side changes in the transit system's enabled status.
- Listens for custom event `NETEVENT_STARTTRANSIT` to start a transit process.

## Notes for modders
- Ensure that the transit system is properly initialized and enabled before attempting to use its functions.
- Use `Transit(nLocation)` to initiate fast-travel to a specific landing zone.
- Customize landing zone properties by modifying `_tLandingZones` data.
- Be aware of network synchronization when enabling/disabling the transit system in multiplayer scenarios.