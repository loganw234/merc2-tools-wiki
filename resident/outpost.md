---
title: outpost
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [outpost, support]
verified: true
verified_note: 'deeper pass: corrected the Events section (player-join is Event.ScriptEvent "mpPlayerJoin", not Event.PlayerJoined/PlayerLeft; also documents the real Event.ObjectDeath/TimerRelative subscriptions and the NETEVENT_* codes); surfaced all tunables (nStartingHealth=3, nCaptureTime=10, nStartRange=150, nSpawnTime=20, iCashReward=5000, nRusherQuota=1, faction defaults); flagged the uRunnerGuid typo bug in IssueCommand; cross-linked imports/namespaces.'
---

# outpost

*Module: outpost.lua*

## Overview
The `outpost` module manages the behavior and state of outposts in the game world. It handles various events such as activation, deactivation, health changes, and player interactions. The module also manages support types for different factions and provides functions to update the outpost's health display on the HUD.

## Inheritance
- Inherits from: none — hand-rolled instance registry (see below)
- Imports: [`MrxGui`](mrxgui), [`MrxPmc`](mrxpmc), [`MrxUtil`](mrxutil),
  [`MrxFactionManager`](mrxfactionmanager), [`MrxGuiInterface`](mrxguiinterface),
  [`MrxOutpostManager`](mrxoutpostmanager), [`MrxSupportData`](mrxsupportdata),
  [`MrxVoSequence`](mrxvosequence)

The "Imports: none" on the previous draft was wrong — the source `import()`s eight modules. The
capture/destroy status is reported up to [`MrxOutpostManager`](mrxoutpostmanager)
(`OutpostStatusChange` with `knStatusCaptured`/`knStatusDestroyed`).

## Instance pattern
**Confirmed genuinely accurate** — unlike most other pages that carried this same line, `Outpost` really
does maintain one rich instance object per `uGuid`. It just doesn't get this from the shared
[`Inheritable`](inheritable) base ([`Blippable`](blippable)/[`MrxTask`](mrxtask)'s pattern) — it hand-rolls
the identical idea itself: `Create(oPrototype, tArgs)` builds `oSelf` via
`setmetatable(oSelf, {__index = oPrototype})`, then explicitly registers it with
`_tOutposts[oSelf.uGuid] = oSelf` (and `nil`s it back out on destruction). `Find(uGuid)` is the confirmed
lookup function: `return uGuid and _tOutposts[uGuid]`. It tracks the following key fields:
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
- **Description**: Gives one AI soldier a high-priority `Ai.Goal` "MoveTo" the capture point, plays a
  rusher VO, sets a 20s `Event.TimerRelative` timeout (`RusherFailed`) and an `Event.ObjectDeath`
  watchdog (`RescindRusherCommand`), marks the rusher on the radar, and increments
  `nAttackers`/`nDefenders`.
- **Arguments**: `oSelf`; `uRusher` (soldier GUID); `sCapturePt` (capture-point name); `bAttacker`.
- {: .warning } **Confirmed bug**: the line `Ai.SetPriorityTarget(uRunnerGuid)` reads an undefined
  global `uRunnerGuid` (the rusher variable is `uRusher`). It resolves to `nil` at runtime, so this
  call is effectively a no-op / mis-fire. Left as-is in the decompiled source.

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
All real subscriptions are created in `Create`/`Activate`/`IssueCommand` (server-side only —
everything is gated behind `Net.IsClient()` returns):

- **`Event.ObjectDeath`** (`Create`, handle `tEvents.OnDeath`) — the outpost object dying calls
  `OnDeath` → `Destroyed`.
- **`Event.ScriptEvent`** named **`"mpPlayerJoin"`** (`Event.CreatePersistent`, handle
  `tEvents.OnJoin`) — filtered to server + non-local joiner; calls `SendPlayerJoinEvents` to push the
  current health display to the new client. (The previous draft's `Event.PlayerJoined`/`Event.PlayerLeft`
  were fabricated — those names do not appear in the source.)
- **`Event.TimerRelative`** at 1s (`Activate`, persistent, handle `tEvents.OnTimer`) — the `TimerTick`
  heartbeat that drives capture/defense logic. Also used for the 20s per-rusher timeout in
  `IssueCommand`.
- **`Event.ObjectDeath`** per rusher (`IssueCommand`) — cleans up a rusher's command if it dies.

Health-display sync uses the `"Outpost"` custom-event channel with `NETEVENT_UPDATEHEALTHDISPLAY = 0`
and `NETEVENT_CLEARHEALTHDISPLAY = 1` (see `NetEventCallback`).

## Module constants & tunables
Module-level globals set at the top of the file (all directly editable to retune outposts):

| Constant | Value | Meaning |
|----------|-------|---------|
| `nStartingHealth` | `3` | "X" pips shown in the objective tray; number of successful rushes to flip the outpost. |
| `nCaptureTime` | `10` | (declared; capture pacing.) |
| `nStartRange` | `150` | (declared; engagement range.) |
| `nSpawnTime` | `20` | Seconds-per-cycle applied to the outpost's spawners via `Ai.TweakAttachedSpawnersInGroup`. |
| `iCashReward` | `5000` | (declared cash reward.) |
| `nRusherQuota` | `1` | Max simultaneous rushers per side (`IsRusherQuotaMet`). |
| `sDefenders` / `sAttackers` | `"VZ"` / `"OC"` | Default defending / attacking faction codes. |

- `tDefaultSupport` maps each faction to its freebie support (`SoldierDelivery_AL/PR/CH/GR/OC`), added
  via [`MrxSupportData.AddFreebie`](mrxsupportdata) while an outpost is active (ref-counted through
  `_tSupportRefCount`).
- Rusher radar markers use per-faction textures from `MrxFactionManager.GetMarkerTexture` plus a
  minimap-icon lookup (`MiniMap_Icon_Faction_PMC/GR/OC/PR/AN/CH/VZ`).
- `PlayerRusherVO` holds large per-faction/gender tables of "advance"/"attack building" barks played at
  `MrxVoSequence.knPriorityFreeplay`.

## Notes for modders
- **Retune difficulty** via `nStartingHealth` (pips to capture) and `nRusherQuota` (how many soldiers
  push at once). `nSpawnTime` controls how fast the outpost's attached spawners refill.
- Health math (`HealthChange`): an **attacker** reaching the capture point applies `nDelta = -1`, a
  **defender** applies `+1`, clamped to `[0, nStartingHealth]`. Hitting 0 triggers `Captured`
  (attacker win → `SetDBFaction(sAttackers)`); the outpost object dying triggers `Destroyed`.
- Hook outcomes with the instance callbacks `fCapturedCallback` / `fDestroyedCallback` /
  `fUpdatedCallback` (each with its `t*CallbackData`), invoked via
  [`MrxUtil.CallWithOptionalArgs`](mrxutil) — this is the intended integration point for missions.
- This is **server-authoritative**: nearly every function early-returns on `Net.IsClient()`. Clients
  only receive the health-display via the custom-event channel. See [`Net`](../namespaces/net).
- Manage instances only through `Create`/`Find`/`Delete`; don't touch `_tOutposts` directly.
- Two confirmed source quirks: the `uRunnerGuid` typo in `IssueCommand` (above), and empty
  `if not bRushers then end` / `if not tMunitions[nStock] then end`-style no-op branches left by the
  decompiler.