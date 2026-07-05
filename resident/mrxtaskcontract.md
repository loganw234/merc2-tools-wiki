---
title: Mrxtaskcontract
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: Mrxtaskmission
tags: [task, contract]
verified: true
verified_note: deeper pass — removed a fabricated "ActionHijack" instance field (it is MrxActionHijack.IsInHijack(), a module call); corrected imports ("none" -> the 14 real imports); rewrote the Events section (the listed OnPlayerJoined/Activated/Complete/Cancel/Cleanup are lifecycle methods, NOT event subscriptions — the only real event is MrxFactionManager.CreateAttitudeChangeEvent); surfaced the faction-music codes, reward-type branch, and the multi-stage Complete/Cancel unload chain
---

# Mrxtaskcontract

*Module: mrxtaskcontract.lua*

## Overview
`MrxTaskContract` is the concrete "playable contract mission" on top of
[`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask). It owns the whole run: entering mission play state
and contract music on `Activated`, a checkpoint/retry save system, a faction-goes-hostile auto-fail, and the
elaborate end-of-mission **fanfare** (reward ledger on complete, retry/sickbay handling on cancel). It
overrides `IsContract()` to return `true` — the flag [`MrxTaskObjective`](mrxtaskobjective) and
[`MrxTaskMission`](mrxtaskmission) check to distinguish contracts from other mission types.

## Inheritance
- Inherits from: [`MrxTaskMission`](mrxtaskmission)
- Imports: [`MrxFactionManager`](mrxfactionmanager), [`MrxGui`](mrxgui), [`MrxHqManager`](mrxhqmanager),
  `MrxPlayer`, [`MrxPlayState`](mrxplaystate), `WifPmcInterior`, [`MrxSoundCategories`](mrxsoundcategories),
  [`MrxActionHijack`](mrxactionhijack), [`MrxMusic`](mrxmusic), [`MrxState`](mrxstate),
  [`MrxStatsManager`](mrxstatsmanager), [`MrxParkingLotManager`](mrxparkinglotmanager),
  [`MrxGuiInterface`](mrxguiinterface)

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskMission`](mrxtaskmission)'s class-factory pattern** (itself inherited
from [`MrxTask`](mrxtask); see that page). Real per-instance fields:
- `self._tContractState` — a save-persisted flag table (`_SetFlag`/`_GetFlag`), seeded in `PreLoadAssets`
  from save data.
- `self._bEndSequenceInProgress` — guards the multi-stage `Complete`/`Cancel` fanfare from re-entering.
- `self._bCancelByMedEvac` — whether cancellation should route the player to the sickbay.
- `self._uFactionAttitudeChanged` — handle for the faction-goes-hostile attitude event.
- `self._sCancelMsg`, `self._nContractReward`, `self._nBonus1`, `self._nBonus2`, `self.bRetry` — cancel
  message / reward-ledger values set via the `_Set*` helpers.

{: .note }
> A previous version listed an `ActionHijack` boolean field — **that does not exist**. Hijack state is read
> from the [`MrxActionHijack`](mrxactionhijack) module (`MrxActionHijack.IsInHijack()`), not stored on the
> contract.

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
Handles the completion of the contract mission. Sets `_bEndSequenceInProgress` (re-entry guard), unlocks the
player's seat movement, then — if `MrxActionHijack.IsInHijack()` (and the mission isn't `PmcCon004`) — defers
to `MrxActionHijack.SetUnloadCallback(self.Complete1, …)`; otherwise calls `Complete1` directly. Also calls
`Pg.ContractCompleted()`.

### Complete1(self)
Continues the completion process by handling unloading callbacks for HQ or PMC interiors, then proceeds to `Complete2`.

### Complete2(self)
Finalizes the contract completion by checking if the task is already completed, sending custom network events if necessary, logging the completion message, setting the mission state to completed, and playing a fanfare with ledger items for rewards.

### Cancel(self)
Handles the cancellation of the contract mission. Sets `_bEndSequenceInProgress`, unlocks seat movement,
then routes through HQ/PMC-interior unload callbacks (`MrxHqManager`/`WifPmcInterior.SetUnloadCallback`) if
inside one, else calls `Cancel2` directly; clears the player's GPS and calls `Pg.ContractCancelled()`.

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
The only real engine event this module creates is a **faction-attitude event** (not `Event.Create`):
- **`MrxFactionManager.CreateAttitudeChangeEvent`** — in `Activated`, when the contract faction's attitude
  is mutable, watching for it turning `"Hostile"` toward the PMC; the callback sets the cancel message
  `"[Fanfare.Cancel.FactionHostile]"` and `Cancel()`s the contract. The handle is stored in
  `self._uFactionAttitudeChanged` and `Event.Delete`d in `Cleanup`.

`NetEventCallback(nEventType)` handles the custom-net `NETEVENT_CLIENTPAUSE = 0` (pauses the client's
fanfare queue) — a custom net message, not an event subscription.

{: .warning }
> `OnPlayerJoined` / `OnPlayerLeft` / `AssetsLoaded` / `Activated` / `Complete` / `Cancel` / `Cleanup` are
> **methods** (engine lifecycle hooks the framework calls directly, or overrides of
> [`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask)) — **not** event subscriptions. A previous version
> of this page listed them under Events; that was incorrect. `OnPlayerJoined`/`OnPlayerLeft` here are just
> `Debug.Printf` stubs called from `Activated`'s remote-player loop.

## Notes for modders
- **Reward/fanfare type is decided by config**: `bPlayerVisibleMission` → `"mission"`,
  `tRewards.nWager`/`nWagerPercent` → `"wager"` (disables saving while active), otherwise `"contract"`. The
  contract ledger sums `_nContractReward` (or `tRewards.nCash`) + `_nBonus1`/`_nBonus2` and writes it back to
  `tRewards.nCashOverride`.
- **Contract entry music** is chosen from `sFactionId` via `MrxMusic.EnterContractMusic` with the code map
  `All→"an"`, `Chi→"ch"`, `Gur→"gr"`, `Oil→"oc"`, `Pmc`/`Vza→"pmc"`.
- **Completion/cancellation is a staged chain**, not a single call: `Complete → Complete1 → Complete2` and
  `Cancel → Cancel2 → _DialogBoxDismissed`, each stage waiting on hijack/HQ/interior *unload* callbacks
  before showing the fanfare. Overriding `Complete`/`Cancel` naively will break this — hook the config
  callbacks instead.
- **Retry vs. sickbay:** a non-wager cancel with a `sStarter` is retryable (`Pg.LoadGame("retry")`); an
  unretryable one cancels the parent and, if no hero survives, `MrxPlayer.MoveToSickbay()`.
- **`_Checkpoint`** (called from `Activated`) is the contract's autosave/retry-point mechanism — it saves a
  `"retry"` slot and optionally shows `"[Generic.CheckpointReached]"`.
- Use the `_Set*` helpers (`_SetContractReward`, `_SetPlayer1Bonus`, `_SetPlayer2Bonus`, `_SetCancelMessage`,
  `_SetFlag`) to influence the end-of-contract ledger and persisted state rather than poking fields directly.