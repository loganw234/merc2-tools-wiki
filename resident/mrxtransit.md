---
title: MrxTransit
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [transit, landing zone]
verified: true
verified_note: "deeper pass: surfaced _nTransitFuelCost=20, the ACHIEVEMENT_BURN_THE_SKY grant in SetLocationEnabled, zone-6-is-fake and the per-faction attitude wiring in Reset, and FinishTransit's 0.75s timer; cross-linked imports; UnlockAllLandingZones still confirmed by live testing"
---

# MrxTransit

*Module: mrxtransit.lua*

## Overview
The `MrxTransit` module manages the transit system in the game, including handling player fast-travel to different landing zones. It provides functions for opening the transit interface, initiating a transit, and managing the state of various landing zones.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxGui`](mrxgui), [`MrxSupportTransit`](mrxsupporttransit), [`MrxUnlockFanfare`](mrxunlockfanfare),
  [`MrxFactionManager`](mrxfactionmanager), [`MrxUtil`](mrxutil), [`MrxSound`](mrxsound),
  [`MrxAchievements`](mrxachievements), [`MrxState`](mrxstate), [`MrxStatsManager`](mrxstatsmanager)

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_tLandingZones`: A table (indexed by numeric zone id) of per-zone data — each entry carries
  `uLocation1`/`uLocation2` (spawn points), `sName`, `sFactionAbbrev`, and the flags `bEnabled`,
  `bSuppressed`, `bIsNuked`, `bFake`, `bHasPlayedFanfare`. Built by `Reset` from `Pg.GetAllLandingZones`.
- `_bInitialized`: Indicates whether the transit system has been initialized (`Reset` sets it).
- `_bEnabled`: Indicates whether the transit system is enabled.
- `_nTransitFuelCost`: **Module-level constant `20`** — the fuel cost per fast-travel (read via
  `GetTransitFuelCost`). Change this one number to make transit cheaper/free.
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
Sets a specific landing zone as enabled and assigns it to the given faction. Plays an unlock fanfare
(`MrxUnlockFanfare.AddUnlockedItem`, type `"landingzone"`) unless `bSuppressFanfare` is set or it already
fired. Skips zones flagged `bFake`, and marks the zone `bSuppressed` if the faction isn't at least Neutral
with PMC. After enabling, if the count of unlocked zones has reached the count of unlockable zones, grants
achievement `"ACHIEVEMENT_BURN_THE_SKY"` to the primary player.

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
Initializes `_tLandingZones` from `Pg.GetAllLandingZones(1)`/`(2)` (bails if the API is missing, already
initialized, or returns no zones). Flags zone index `6` as `bFake` (excluded from the unlockable set), then
registers a persistent attitude-change event per faction (via
`MrxFactionManager.CreatePersistentAttitudeChangeEvent`) so zones auto-enable/suppress as that faction's
attitude toward PMC crosses Neutral. Sets `_bInitialized = true`.

### `SaveSingleton()`
Saves the current state of the transit system, including enabled status and landing zone data.

### `LoadSingleton(tSaveData)`
Loads the saved state of the transit system from the provided `tSaveData` table.

### `UnlockAllLandingZones()`
Unlocks all landing zones by enabling them for the PMC faction. **Confirmed working by live testing** —
see [`MrxCheatBootstrap`](mrxcheatbootstrap)'s "Unlock every landing zone" row:
`import("MrxTransit"); MrxTransit.UnlockAllLandingZones()`. Runs silently — no on-screen confirmation, check
the map/travel menu to see the effect.

### `GetTransitFuelCost()`
Returns the fuel cost per fast-travel.

### `IsInTransit()`
Checks if a transit is currently in progress.

### `StartTransit(fEnterCallback, fExitCallback, tCallbackData)`
Starts a transit process by entering the waiting-for-streaming state and sending a custom network event.

### `FinishTransit(fCallback, tCallbackArgs)`
Finishes the transit process. Waits `0.75` seconds (`Event.TimerRelative`, one-shot) before clearing
`_bInTransit`, exiting `MrxState.STATE_WAITFORSTREAMING`, and invoking the callback via
`MrxUtil.CallWithOptionalArgs`.

### `NetEventCallback(nEventType, tArgs)`
Handles network events related to the transit system. It processes events for enabling/disabling the system and starting a transit.

## Events
- Listens for custom event `NETEVENT_CLIENTTRANSIT` to handle client-side changes in the transit system's enabled status.
- Listens for custom event `NETEVENT_STARTTRANSIT` to start a transit process.

## Notes for modders
- **`UnlockAllLandingZones()` is the fastest way to open every fast-travel destination** — confirmed
  working, one line, see above.
- **Fuel cost is the constant `_nTransitFuelCost = 20`** (returned by `GetTransitFuelCost`, applied to the
  support-menu item in `SetSystemEnabled`). Set it to `0` for free fast-travel.
- **Zone index `6` is hardcoded as fake** in `Reset` (`bFake = true`) and is excluded from the unlockable
  count — don't expect it to appear as a real destination.
- Use `Transit(nLocation)` to initiate fast-travel to a specific landing zone by numeric ID; `GetName(nId)`
  gives you the display name if you need to enumerate options first.
- Customize landing zone properties by modifying `_tLandingZones` data directly, the same "it's just a
  plain Lua table" pattern documented on [`MrxSupportData`](mrxsupportdata#overriding-catalog-values-from-your-own-mod).
- Be aware of network synchronization when enabling/disabling the transit system in multiplayer scenarios —
  `NETEVENT_CLIENTTRANSIT`/`NETEVENT_STARTTRANSIT` sync state to other players; see the
  [full `NETEVENT_` catalog](../deep-dives/networking#the-full-netevent_-catalog).