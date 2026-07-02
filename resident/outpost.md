---
title: outpost
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [outpost, support]
---

# outpost

*Module: outpost.lua*

## Overview
The `outpost` module manages the behavior and state of outposts in the game world. It handles various events such as activation, deactivation, health changes, and player interactions. The module also manages support types for different factions and provides functions to update the outpost's health display on the HUD.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tOutposts`: A table that maps outpost GUIDs to their respective outpost instances.
- `_tSupportRefCount`: A table tracking the reference count of support types for different factions.
- `tDefaultSupport`: A table mapping faction names to default support types.
- `sDefenders` and `sAttackers`: Strings representing the factions defending and attacking the outpost, respectively.
- `nCaptureTime`, `nStartRange`, `nSpawnTime`, `iCashReward`, `nStartingHealth`, `nRusherQuota`: Constants defining various parameters for the outpost's behavior.
- `tDBSpawners`: A table listing spawner names associated with the outpost.
- Callback functions and their data tables (`fCapturedCallback`, `tCapturedCallbackData`, `fDestroyedCallback`, `tDestroyedCallbackData`, `fUpdatedCallback`, `tUpdatedCallbackData`): Used to handle specific events related to the outpost.

## Functions

### Find(uGuid)
- **Description**: Retrieves an outpost instance by its GUID.
- **Arguments**:
  - `uGuid`: The unique identifier of the outpost.

### Create(oPrototype, tArgs)
- **Description**: Creates a new outpost instance and initializes it with provided arguments.
- **Arguments**:
  - `oPrototype`: The prototype table for the outpost class.
  - `tArgs`: A table containing initialization arguments for the outpost.

### Delete(oSelf)
- **Description**: Deletes an outpost instance, cleaning up its events and references.
- **Arguments**:
  - `oSelf`: The outpost instance to be deleted.

### OnDeath(oSelf)
- **Description**: Handles the death event of an outpost instance.
- **Arguments**:
  - `oSelf`: The outpost instance that died.

### Activate(oSelf)
- **Description**: Activates an outpost instance, setting up its initial state and events.
- **Arguments**:
  - `oSelf`: The outpost instance to activate.

### Deactivate(oSelf)
- **Description**: Deactivates an outpost instance, cleaning up its resources and events.
- **Arguments**:
  - `oSelf`: The outpost instance to deactivate.

### TimerTick(oSelf)
- **Description**: Handles the timer tick event for an outpost instance, managing health changes and calls for attackers/defenders.
- **Arguments**:
  - `oSelf`: The outpost instance whose timer ticked.

### Captured(oSelf)
- **Description**: Marks an outpost as captured by attackers, updates its status, and triggers any associated callbacks.
- **Arguments**:
  - `oSelf`: The outpost instance that was captured.

### Destroyed(oSelf)
- **Description**: Marks an outpost as destroyed, updates its status, and triggers any associated callbacks.
- **Arguments**:
  - `oSelf`: The outpost instance that was destroyed.

### UpdateHealthDisplay(oSelf)
- **Description**: Updates the health display for an active outpost instance.
- **Arguments**:
  - `oSelf`: The outpost instance whose health needs to be displayed.

### ClearHealthDisplay(oSelf)
- **Description**: Clears the health display for an outpost instance.
- **Arguments**:
  - `oSelf`: The outpost instance whose health display should be cleared.

### UpdateHealthDisplayHelper(nStartingHealth, nCurrentHealth)
- **Description**: Helper function to update the health display on the HUD.
- **Arguments**:
  - `nStartingHealth`: The starting health of the outpost.
  - `nCurrentHealth`: The current health of the outpost.

### ClearHealthDisplayHelper()
- **Description**: Helper function to clear the health display on the HUD.

### NetEventCallback(nEventId, tArgs)
- **Description**: Handles network events related to the outpost's health display.
- **Arguments**:
  - `nEventId`: The ID of the network event.
  - `tArgs`: A table containing arguments for the event.

### SendPlayerJoinEvents(oSelf)
- **Description**: Sends player join events to update the health display for an active outpost instance.
- **Arguments**:
  - `oSelf`: The outpost instance whose health needs to be updated on player join.

### TweakDBs(oSelf, sState)
- **Description**: Adjusts the tweak database settings for spawners associated with the outpost.
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `sState`: The state to set for the spawners ("on" or "off").

### SetDBFaction(oSelf, sFaction)
- **Description**: Sets the faction for spawners associated with the outpost.
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `sFaction`: The faction to set.

### CallForAttackers(oSelf)
- **Description**: Calls for attackers to rush the capture point of the outpost.
- **Arguments**:
  - `oSelf`: The outpost instance.

### CallForDefenders(oSelf)
- **Description**: Calls for defenders to rush the capture point of the outpost.
- **Arguments**:
  - `oSelf`: The outpost instance.

### CallForRushers(oSelf, bAttackers)
- **Description**: Calls for rushers (either attackers or defenders) to rush the capture point of the outpost.
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `bAttackers`: A boolean indicating whether the rushers are attackers.

### GetCapturePoint(oSelf)
- **Description**: Retrieves the capture point for the outpost.
- **Arguments**:
  - `oSelf`: The outpost instance.

### IssueCommand(oSelf, uRusher, sCapturePt, bAttacker)
- **Description**: Issues a command to a rusher to move to the capture point and attack or defend.
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `uRusher`: The GUID of the rusher.
  - `sCapturePt`: The name of the capture point.
  - `bAttacker`: A boolean indicating whether the rusher is an attacker.

### RusherGoalFulfilled(oSelf, uRusher, nState)
- **Description**: Handles the fulfillment of a rusher's goal (moving to the capture point).
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `uRusher`: The GUID of the rusher.
  - `nState`: The state of the goal (0 for failure, non-zero for success).

### CancelCallForAttackers(oSelf)
- **Description**: Cancels all calls for attackers rushing the capture point.
- **Arguments**:
  - `oSelf`: The outpost instance.

### CancelCallForDefenders(oSelf)
- **Description**: Cancels all calls for defenders rushing the capture point.
- **Arguments**:
  - `oSelf`: The outpost instance.

### CancelCallForRushers(oSelf, bAttackers)
- **Description**: Cancels all calls for rushers (either attackers or defenders) rushing the capture point.
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `bAttackers`: A boolean indicating whether the rushers are attackers.

### RusherFailed(oSelf, uRusher)
- **Description**: Handles the failure of a rusher's goal (moving to the capture point).
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `uRusher`: The GUID of the rusher.

### RescindRusherCommand(oSelf, uRusher)
- **Description**: Removes a rusher's command and cleans up associated events.
- **Arguments**:
  - `oSelf`: The outpost instance.
  - `uRusher`: The GUID of the rusher.

### MarkRusher(oSelf, uRusher, bEnable)
- **Description**: Marks a rusher with a blip on the minimap and radar. If `bEnable` is true, it adds the marker and updates the radar; if false, it removes them.
- **Parameters**:
  - `oSelf`: The instance of the outpost.
  - `uRusher`: The GUID of the rusher to mark.
  - `bEnable`: A boolean indicating whether to enable or disable the marker.

### IsRusherQuotaMet(oSelf, bAttackers)
- **Description**: Checks if the quota for attackers or defenders has been met.
- **Parameters**:
  - `oSelf`: The instance of the outpost.
  - `bAttackers`: A boolean indicating whether to check the attacker quota (true) or defender quota (false).
- **Returns**: A boolean indicating whether the quota is met.

### HealthChange(oSelf, nDelta)
- **Description**: Changes the health of the outpost by a specified delta. Updates the health display and calls an optional callback if the health changes.
- **Parameters**:
  - `oSelf`: The instance of the outpost.
  - `nDelta`: The amount to change the health by (positive or negative).
- **Returns**: A boolean indicating whether the health was successfully changed.

### IdleAllRushers(oSelf, bKilled)
- **Description**: Sets all rushers in the vicinity to an idle state. If `bKilled` is true, it may perform additional actions related to killing.
- **Parameters**:
  - `oSelf`: The instance of the outpost.
  - `bKilled`: A boolean indicating whether the rushers were killed.

### GetFactionSupportName(sFaction)
- **Description**: Retrieves the name of a faction's support based on the faction abbreviation.
- **Parameters**:
  - `sFaction`: The faction abbreviation.
- **Returns**: The name of the faction's support.

### PlayerRusherVO(uRusher)
- **Description**: Plays a voice-over for a player rusher based on their faction and gender. Selects a random voice-over cue from predefined lists.
- **Parameters**:
  - `uRusher`: The GUID of the rusher to play the voice-over for.

## Events
This module subscribes to and fires several engine events related to outpost behavior:

- **`Event.ObjectDeath`**: Listens for the death event of an outpost instance and calls `OnDeath`.
- **`Event.TimerRelative`**: Handles timer tick events to manage health changes and call for attackers/defenders via `TimerTick`.
- **`Event.PlayerJoined` / `Event.PlayerLeft`**: Updates the health display on player join or leave via `SendPlayerJoinEvents`.

## Notes for modders
- **Call-order requirements**: Ensure that `Activate` is called after creating an outpost instance to properly set up its initial state and events. Similarly, `Deactivate` should be called before deleting an outpost instance to clean up resources.
- **Pitfalls**: Be cautious with modifying the `_tOutposts` table directly, as it holds active outpost instances. Always use the provided functions like `Find`, `Create`, and `Delete` to manage outpost instances safely.
- **Tunables**: The constants `nCaptureTime`, `nStartRange`, `nSpawnTime`, `iCashReward`, `nStartingHealth`, and `nRusherQuota` can be adjusted to change the behavior of outposts. Modifying these values may affect gameplay balance.
- **Decompiler artifacts**: There are no known decompiler artifacts in this module that require special attention. All functions and variables appear to have intended purposes within the context of outpost management.