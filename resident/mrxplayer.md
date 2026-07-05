---
title: MrxPlayer
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [player, character management]
verified: true
verified_note: "deeper pass: replaced the vague Imports 'and others' with the full 19-module list, surfaced the medevac cost (10000) and NETEVENT_ constants (0-4), clarified Events (PlayerJoined/PlayerLeft are Player.Set*Callback engine callbacks not Event subs; the real persistent sub is Event.ObjectDeath on each hero in OnPlayerInit; posts mpPlayerJoin/mpPlayerLeft/MedevacComplete/ClientKill); instance-pattern + functions re-confirmed"
---

# MrxPlayer

*Module: mrxplayer.lua*

## Overview
The `MrxPlayer` module is responsible for managing player characters in the game. It handles various aspects such as player initialization, character creation and destruction, character switching, medical evacuation processes, and network event handling. The module ensures that players can join and leave the game smoothly, manage their characters' equipment, and interact with the game world.

## Inheritance
- Inherits from: none — base/utility module
- Imports (all 19): [`MrxCoop`](mrxcoop), [`MrxGui`](mrxgui), [`MrxGuiManager`](mrxguimanager),
  [`MrxGuiShellBootstrap`](mrxguishellbootstrap), [`MrxPlayState`](mrxplaystate), [`MrxPmc`](mrxpmc),
  [`MrxUtil`](mrxutil), `WifPmcInterior`, [`MrxMissionFlow`](mrxmissionflow), [`MrxState`](mrxstate),
  [`MrxTransit`](mrxtransit), [`MrxActionHijack`](mrxactionhijack), [`MrxHqManager`](mrxhqmanager),
  [`MrxVoSequence`](mrxvosequence), [`Hero`](hero), [`MrxStatsManager`](mrxstatsmanager),
  [`Munitions`](munitions), [`MrxSound`](mrxsound), [`MrxGuiHudMessage`](mrxguihudmessage)

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. `_tPlayerDatabase` is a plain module-level table this module maintains itself (keyed
by player), not a factory-built per-instance object with inherited methods. Key fields:
- `_tCharacterMap`: A table mapping character names to their upgrade templates and costume models.
- `_tPlayerDatabase`: A database of player instances, each containing information about the player's character, position, health, and equipment.
- `_fLocalPlayerJoinedCallback`: A callback function for when the local player joins the game.
- `_tSpawnLocations`: A table of spawn points for players.
- `_bInVehicle`: A boolean indicating if any players are in a vehicle.
- `_nMedEvacCost`: The cost of medical evacuation in PMC currency.

## Functions

### Init()
Initializes the player module by creating player instances for each possible player slot up to the maximum number of players allowed.

### Deinit()
Deinitializes the player module by destroying all player instances and clearing the player database.

### Start()
Registers callbacks for player join and leave events.

### Reset()
Deregisters callbacks for player join and leave events.

### SetLocalPlayerJoinedCallback(fFunc, tArgs)
Sets a callback function to be called when the local player joins. The function is stored along with its arguments and may be immediately invoked if the local player already exists.

### SetSpawnLocations(tSpawnLocations)
Sets the spawn locations for players based on the provided table of spawn points.

### GetTemplateAndModelName(tCharacterConfig)
Retrieves the template and model name for a given character configuration. It checks the index and upgrade level to determine the appropriate template and costume model.

### OnPlayerJoined(iPlayerId, sPlayerName, tCharacterConfig, bLocalPlayer, iLocalId)
Handles the event when a player joins the game. It sets up the player's character, binds them locally or remotely, creates GUI elements if necessary, and triggers various events and callbacks.

### PlayJoinVO()
Plays voice-over messages for both the host and client players joining the game based on their selected characters.

### PlayRandomLeftVO(tVO)
Plays a random voice-over message from the provided table when a player leaves the game.

### OnPlayerLeft(iPlayerId, sPlayerName, bLocalPlayer)
Handles the event when a player leaves the game. It cleans up GUI elements, removes AI subjects, and triggers various events and callbacks.

### RequestPlayerRevive(iPlayerId, uChar, fX, fY, fZ)
Requests to revive a player character. If the player is remote, it sends a network message; otherwise, it revives the character locally and sets their position if provided.

### PlayerDied(iPlayerId, uChar)
Handles the event when a player dies. It checks conditions for reviving the player or canceling ongoing missions based on whether any heroes are still alive.

### _DisplayOnDeathDialogBox()
Displays a dialog box to the player when all heroes have died, offering options to continue or quit.

### _DialogBoxDismissed(nIndex)
Handles the dismissal of the death dialog box. If the player chooses to continue and is in the "vz" level, it moves them to sickbay.

### CanMedEvac()
Checks if medical evacuation is possible based on various conditions such as player health, cinematic mode, transit status, hijack status, interior access, HQ status, locked state, and client/server status.

### MedEvac()
- **Description**: Handles the medical evacuation process for the player. If a mission is currently active, it cancels the mission and stops any voice sequences. Otherwise, it attempts to move the player to sickbay.
- **Parameters**: None
- **Returns**: None

### MoveToSickbay()
- **Description**: Initiates the process of moving players to sickbay. It checks if they are inside a PMC interior and, if not, stops any voice sequences, enters a wait state, and begins the move process.
- **Parameters**: None
- **Returns**: Boolean indicating whether the move process was initiated

### ResetLocalCharacter()
- **Description**: Resets the local player's character by dropping any carried items and resetting weapons if the character is not alive.
- **Parameters**: None
- **Returns**: None

### _MoveToSickbayBegin()
- **Description**: Internal function that handles the initial steps of moving players to sickbay. It stops grappling, exits vehicles, resets characters, and sends network events for client and server sides.
- **Parameters**: None
- **Returns**: None

### _CompleteMove()
- **Description**: Completes the move process by setting player positions, orientations, and ending survival mode. It also triggers a "MedevacComplete" event.
- **Parameters**: None
- **Returns**: None

### _MoveToSickbayEnd()
- **Description**: Internal function that handles the final steps of moving players to sickbay, including deducting medevac costs from the player's PMC balance.
- **Parameters**: None
- **Returns**: None

### GetMedEvacCost()
- **Description**: Returns the flat medevac cost, hard-coded as `return 10000`. This is the amount `_MoveToSickbayEnd`
  deducts via `MrxPmc.AddCashQty(-GetMedEvacCost(), true, "[Generic.Medevacs]")`.
- **Returns**: `10000` (integer, PMC cash). To change the medevac price, override this function.

### ResetWeapons(uCharGuid, sNewWeapon)
- **Description**: Resets the weapons for a given character. It sets the primary weapon to a specified type or defaults to "Pistol", and also sets grenade and C4 as secondary weapons.
- **Parameters**:
  - `uCharGuid`: GUID of the character
  - `sNewWeapon`: Optional string specifying the new primary weapon
- **Returns**: None

### RiseFromYourGrave()
- **Description**: Revives any dead players. It checks if the player is the local or secondary character and revives them accordingly.
- **Parameters**: None
- **Returns**: None

### OnPlayerInit(iPlayerId, uChar)
- **Description**: Initializes event listeners for a player's death. If the player is alive, it sets up an event to handle their death; if not, it retries initialization after 2 seconds.
- **Parameters**:
  - `iPlayerId`: ID of the player
  - `uChar`: GUID of the character
- **Returns**: None

### CreatePlayerCharacter(bLocalPlayer, iPlayerId, sCharacterName, vLocation)
- **Description**: Creates a new player character. It sets the location based on whether it's a local or remote player and initializes the character.
- **Parameters**:
  - `bLocalPlayer`: Boolean indicating if the player is local
  - `iPlayerId`: ID of the player
  - `sCharacterName`: Name of the character to create
  - `vLocation`: Location where the character should be spawned (can be a string or table)
- **Returns**: GUID of the created character

### DestroyPlayerCharacter(iPlayerId)
- **Description**: Destroys an existing player character by detaching it from the player and removing it from the game world.
- **Parameters**:
  - `iPlayerId`: ID of the player
- **Returns**: None

### ChangePlayerCharacter(iPlayerId, sCharacterName, sCharacterModel)
- **Description**: Changes a player's character to a new one. It removes the old character and spawns a new one with the specified name and model.
- **Parameters**:
  - `iPlayerId`: ID of the player
  - `sCharacterName`: Name of the new character
  - `sCharacterModel`: Model of the new character
- **Returns**: GUID of the new character

### GetSelectedCharacter(iPlayerId)
- **Description**: Retrieves the selected character for a given player. It checks if the player has a character and returns its name based on labels.
- **Parameters**:
  - `iPlayerId`: ID of the player
- **Returns**: String representing the selected character's name

### AreAnyHeroesAlive()
- **Description**: Checks if any heroes (players) are currently alive.
- **Parameters**: None
- **Returns**: Boolean indicating if any heroes are alive

### SaveSingleton()
- **Description**: Saves the current state of all players, including their health and equipment. It returns a table containing this data.
- **Parameters**: None
- **Returns**: Table with saved player data

### LoadSingleton(tSaveData)
- **Description**: Loads the saved state of players from a given data table. It restores characters' health and equipment based on the saved data.
- **Parameters**:
  - `tSaveData`: Table containing saved player data
- **Returns**: None
- **Not previously documented:** the actual equipment restore is a nested function, `_RestoreEquipment(uGuid, tSavedEquipment)`, defined *inside* `LoadSingleton`'s own loop body without `local` — like a couple of other modules on this wiki, that means it's technically redefined as a global every time `LoadSingleton` runs, though it's only ever called from directly within that same loop. It rebuilds a flat weapon list from the saved per-slot data, calls `Human.Inventory.SetAllWeapons`, then re-reads the equipped weapons back out and re-applies each one's saved reserve ammo once it's no longer hibernating (`Event.Create(Event.ObjectHibernation, {uEquipment, "a"}, Weapon.SetReserveAmmo, ...)`).

### IsInVehicle(sFilter)
- **Description**: Checks if any players are in a vehicle that matches a specified filter. If no filter is provided, it defaults to checking for any vehicle.
- **Parameters**:
  - `sFilter`: Optional string specifying the type of vehicle to check
- **Returns**: Integer count of players in vehicles matching the filter or false if none are found

### SetCharacterMap(tNewCharacterMap)
- **Description**: Sets a new character map. The character map is used to manage different characters.
- **Parameters**:
  - `tNewCharacterMap`: Table representing the new character map
- **Returns**: Boolean indicating success

### KilledByPlayer(uGuid)
- **Description**: Sends a network event when a player kills another player, identified by their GUID.
- **Parameters**:
  - `uGuid`: GUID of the killed player
- **Returns**: None

### NetEventCallback(nEventType, tArgs)
- **Description**: Handles various network events. It processes different types of events such as client selecting medivac, host selecting medivac, client done streaming, client kill, and client out-of-boundary death.
- **Parameters**:
  - `nEventType`: Integer representing the type of event
  - `tArgs`: Table containing arguments for the event
- **Returns**: None

## Events

**Player join/leave are not `Event.*` subscriptions** — `Start()` registers them as engine callbacks
(`Player.SetPlayerJoinedCallback(OnPlayerJoined)` / `Player.SetPlayerLeftCallback(OnPlayerLeft)`), and `Reset()`
removes them. Don't look for `Event.Create(Event.PlayerJoined, ...)`; it isn't there.

Real `Event.*` usage:
- **`Event.CreatePersistent(Event.ObjectDeath, {uChar}, PlayerDied, {iPlayerId, uChar})`** — set up per hero in
  `OnPlayerInit`; this is how the module reacts to a player character dying.
- **`Event.Create(Event.ObjectHibernation, {..., "awake"/"a"}, ...)`** — deferred outfit set (`OnPlayerJoined`),
  ammo restore (`LoadSingleton`), i.e. "run once the object is streamed in".
- **`Event.Create(Event.GameStateChange, {"WaitForStreaming", "exit"}, ...)`** and short `Event.TimerRelative`
  timers drive the medevac / revive-nag flow (`_evReviveNag` at 30 s, `_evCancelTimer` at 60 s).

Events **posted** (other modules subscribe): `mpPlayerJoin`, `mpPlayerLeft` (the same `mpPlayerJoin` that
[`MrxFactionManager`](mrxfactionmanager) listens for to sync a joiner), `MedevacComplete`, and `ClientKill`.

## Network events
`NetEventCallback` handles a small integer catalog (module-level constants): `NETEVENT_CLIENTSELECTMEDEVAC = 0`,
`NETEVENT_CLIENTDONESTREAMING = 1`, `NETEVENT_HOST_SELECT_MEDEVAC = 2`, `NETEVENT_CLIENTKILL = 3`,
`NETEVENT_CLIENT_OUT_BOUNDARY_DEATH = 4`. Sent via `Net.SendCustomEvent("MrxPlayer", <id>, ...)`.

## Notes for modders
- **Medevac price** is the hard-coded `return 10000` in [`GetMedEvacCost`](#getmedevaccost); override it to
  change the cost. It's charged through [`MrxPmc.AddCashQty`](mrxpmc) with reason `"[Generic.Medevacs]"`.
- **`CanMedEvac()` is a gate you can read** before offering a medevac UI — it returns `false` if anyone is
  dead/in a cinematic, in transit ([`MrxTransit`](mrxtransit)), mid-hijack
  ([`MrxActionHijack`](mrxactionhijack)), the PMC interior is locked or you're inside it, you're in an HQ
  ([`MrxHqManager`](mrxhqmanager)), [`MrxState`](mrxstate) is locked, or you're a network client.
- **Default respawn loadout** is set by `ResetWeapons`: primary `"Pistol"` (unless `sNewWeapon` is passed),
  plus `"Grenade"` and `"C4"` — change these three template names to reskin the revive kit.
- **`_tCharacterMap`** holds the three heroes' upgrade templates and costume model lists (Mattias/Chris/Jen);
  `SetCharacterMap` swaps the whole table. Costume/upgrade indices from `tCharacterConfig` index into it via
  `GetTemplateAndModelName`.
- Decompiler note: `_RestoreEquipment` is defined without `local` **inside** `LoadSingleton`'s loop, so it leaks
  as a global each load; harmless because it's only called from that same loop.