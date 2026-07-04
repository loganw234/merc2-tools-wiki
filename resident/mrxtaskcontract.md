---
title: Mrxtaskcontract
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: Mrxtaskmission
tags: [task, contract]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskMission](mrxtaskmission) for the general mechanism.
---

# Mrxtaskcontract

*Module: mrxtaskcontract.lua*

## Overview
The `Mrxtaskcontract` module is responsible for managing contract missions within the game. It handles various lifecycle events such as activation, completion, and cancellation of contracts. The module also manages player states, checkpoint creation, and network event handling specific to contract missions.

## Inheritance
- Inherits from: `MrxTaskMission`
- Imports: `none`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskMission`](mrxtaskmission)'s class-factory pattern** (itself inherited
from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage rather than
a world-object GUID. Key fields tracked via the config table:
- `_tContractState`: A table used to store contract-specific state data. It is initialized from saved data or set to an empty table if no saved data is available.
- `_bCancelByMedEvac`: A flag indicating whether the cancellation should be handled by moving to sickbay or medevac.
- `ActionHijack`: A boolean flag used in hijack scenarios.
- Other fields related to mission state, player bonuses, and contract rewards.

## Functions

### OnPlayerJoined(self, iPlayerId, uPlayerGuid, uCharacterGuid)
Called when a player joins the game session. Logs the player's ID and GUIDs.

### OnPlayerLeft(self, iPlayerId, uPlayerGuid, uCharacterGuid)
Called when a player leaves the game session. Logs the player's ID and GUIDs.

### PreLoadAssets(self)
Loads saved data for the contract state. If no saved data is available, initializes `_tContractState` as an empty table.

### AssetsLoaded(self)
Handles the loading of assets after they are fully loaded by the network. Adds a global exit callback for `Activated` and issues any necessary asset-loaded callbacks.

### Activated(self)
Activates the contract mission. Sets up various game states, such as setting the current mission, enabling or disabling PDA display, initializing retry locations, entering contract music, setting player health, creating a checkpoint, handling faction attitude changes, and marking the last vehicle in the parking lot manager.

### Complete(self)
Handles the completion of the contract mission. Starts the end sequence by setting `ActionHijack` to false and pausing if inside a hijack scenario. Delegates further completion logic to `Complete1`.

### Complete1(self)
Continues the completion process by handling unloading callbacks for HQ or PMC interiors, then proceeds to `Complete2`.

### Complete2(self)
Finalizes the contract completion by checking if the task is already completed, sending custom network events if necessary, logging the completion message, setting the mission state to completed, and playing a fanfare with ledger items for rewards.

### Cancel(self)
Handles the cancellation of the contract mission. Starts the end sequence by setting `ActionHijack` to false and pausing if inside a hijack scenario. Delegates further cancellation logic to `Cancel2`.

### Cancel2(self)
Finalizes the contract cancellation by checking if the task is already cancelled, logging the cancellation message, setting the mission state to cancelled, playing a fanfare with appropriate messages, and handling retry or sickbay/medevac scenarios.

### Cleanup(self)
Cleans up after the end sequence of the contract. Resets various states, stops voice sequences, resets faction infraction multipliers, clears PDA display, and re-enables pause menu save options if applicable.

### _DialogBoxDismissed(self, bRetry)
Handles the dismissal of a dialog box during cancellation or completion. Cleans up the task, issues state change callbacks, and either retries the mission or handles failure scenarios like moving to sickbay or medevac.

### _GetMissionType()
Returns the type of the mission, which is `MrxTaskMission._knContract`.

### IsContract()
Returns `true` indicating that this is a contract mission.

### SetCancelByMedEvac(self, bSet)
Sets a flag `_bCancelByMedEvac` to indicate whether the cancellation should be handled by moving to sickbay or medevac.

### _SetFlag(self, sFlagName, vFlagValue)
Sets a flag in `_tContractState` with the given name and value. If no value is provided, it defaults to `1`.

### _GetFlag(self, sFlagName)
Retrieves the value of a flag from `_tContractState` by its name.

### _Checkpoint(tSpawnLocations, bNoAutosave, bHideMessages)
Creates a checkpoint for retrying the mission. Enables checkpoint save mode, sets retry locations if provided, saves the game state, and optionally performs an autosave and displays messages.

### SaveInstance(self, bDefaultState)
Saves the instance of the contract task. If `bDefaultState` is true, it clears the contract-specific state; otherwise, it includes the current contract state in the saved data.

### _SetCancelMessage(self, sCancelMsg)
Sets a custom cancellation message for the contract.

### _SetContractReward(self, nContractReward)
Sets the contract reward amount.

### _SetPlayer1Bonus(self, nBonus1)
Sets the bonus for player 1.

### _SetPlayer2Bonus(self, nBonus2)
Sets the bonus for player 2.

### _SetPlayersInvincible(bSet)
This function sets the invincibility state for both primary and secondary players. It takes a boolean `bSet` as an argument, which determines whether the players should be set to invincible (`true`) or not (`false`). The function uses `Player.GetPrimaryCharacter()` and `Player.GetSecondaryCharacter()` to get the GUIDs of the primary and secondary player characters, respectively. If a valid GUID is obtained, it calls `Object.SetInvincible(uGuid, bSet, "Fanfare")` to set the invincibility state.

### NetEventCallback(nEventType)
This function handles network events. It takes an integer `nEventType` as an argument, which represents the type of event received. If the event type matches `NETEVENT_CLIENTPAUSE`, it performs the following actions:
- Calls `MrxGuiInterface.HudInterface.FanfareQueue.ClientPause(true)` to pause the client.
- Calls `MrxGuiInterface.HudInterface.FanfareQueue.ClientSetPending(false)` to set the pending state to false.

## Events
- **`OnPlayerJoined(uPlayerGuid, uCharacterGuid)`**: Triggered when a player joins the game session. Logs the player's ID and GUIDs.
- **`OnPlayerLeft(uPlayerGuid, uCharacterGuid)`**: Triggered when a player leaves the game session. Logs the player's ID and GUIDs.
- **`AssetsLoaded()`**: Triggered after assets are fully loaded by the network. Adds a global exit callback for `Activated` and issues any necessary asset-loaded callbacks.
- **`Activated()`**: Triggered to activate the contract mission. Sets up various game states, such as setting the current mission, enabling or disabling PDA display, initializing retry locations, entering contract music, setting player health, creating a checkpoint, handling faction attitude changes, and marking the last vehicle in the parking lot manager.
- **`Complete()`**: Triggered to handle the completion of the contract mission. Starts the end sequence by setting `ActionHijack` to false and pausing if inside a hijack scenario. Delegates further completion logic to `Complete1`.
- **`Cancel()`**: Triggered to handle the cancellation of the contract mission. Starts the end sequence by setting `ActionHijack` to false and pausing if inside a hijack scenario. Delegates further cancellation logic to `Cancel2`.
- **`Cleanup()`**: Triggered after the end sequence of the contract. Resets various states, stops voice sequences, resets faction infraction multipliers, clears PDA display, and re-enables pause menu save options if applicable.
- **`NetEventCallback(nEventType)`**: Triggered by network events. Handles specific event types like `NETEVENT_CLIENTPAUSE`.

## Notes for modders
- **Call-order requirements**: Ensure that lifecycle functions such as `OnPlayerJoined`, `OnPlayerLeft`, `PreLoadAssets`, and `Activated` are called in the correct order to maintain proper game state.
- **Pitfalls**: Be cautious with setting player invincibility using `_SetPlayersInvincible(bSet)`. Misuse can lead to unintended consequences, such as players being invincible during critical moments.
- **Tunables**: Adjustments to contract rewards and bonuses should be made through functions like `_SetContractReward(nContractReward)` and `_SetPlayer1Bonus(nBonus1)`.
- **Decompiler artifacts**: Some unused locals or redundant operator groupings may appear in the decompiled code. These are artifacts of the decompilation process and do not affect the functionality of the module.