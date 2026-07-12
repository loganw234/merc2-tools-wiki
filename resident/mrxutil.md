---

title: MrxUtil

parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [utility, helper]

verified: true
verified_note: "deeper pass: corrected Imports (source imports MrxCheatBootstrap/MrxGui/MrxGuiShellBootstrap/MrxState/WifPmcInterior/MrxHqManager, not none), documented GetFaction's exact full-name return set and FormatMoney/_tNumbers suffix table, added marker-index lookup tables and objective-RGB constants; TeleportHeroesToLocations indoor-crash caveat and all cross-links re-confirmed"

---



# MrxUtil



*Module: mrxutil.lua*



## Overview

The `MrxUtil` module is a comprehensive utility library providing a wide range of helper functions for various tasks in the game. It includes functionalities for handling tables, managing object spawning and teleportation, processing callbacks, calculating distances, working with factions and markers, and more. This module serves as a foundational resource for other modules to perform common operations efficiently.



## Inheritance

- Inherits from: `none` (base/utility module)

- Imports: [`MrxCheatBootstrap`](mrxcheatbootstrap), [`MrxGui`](mrxgui),
  [`MrxGuiShellBootstrap`](mrxguishellbootstrap), [`MrxState`](mrxstate), `WifPmcInterior`,
  [`MrxHqManager`](mrxhqmanager) (an earlier draft said `none` — the source has all six `import()` lines).



## Instance pattern

This is a stateless manager/utility module without a per-instance pattern. It does not track any persistent state across function calls and relies on global functions and variables for its operations.



## Functions



### CallWithOptionalArgs(fFunction, tArgs)

Calls a given function with optional arguments. If `fFunction` is a function and `tArgs` is a table, it unpacks `tArgs` and passes them to `fFunction`. If `tArgs` is not a table, it calls `fFunction` without any arguments.



### SetDefault(vVar, vDefaultValue)

Sets `vVar` to `vDefaultValue` if `vVar` is `nil`. Returns the value of `vVar`.



### CopyTable(tSrc)

Creates a deep copy of a given table `tSrc`. If an element in `tSrc` is a table, it recursively copies that table.



### MergeIndexedTables(...)

Merges multiple indexed tables into one. It iterates over each table passed as arguments and inserts all elements from these tables into a new table.



### GetTableAsString(tInput, nTabs)

Converts a given table `tInput` to a string representation with optional indentation specified by `nTabs`.



### FormatMoney(n)

Formats a given number `n` as a money string. It uses predefined factors and suffixes to format the number into a string that represents money.



### TeleportSecondaryHeroToPrimaryHero()

Teleports the secondary hero to the position of the primary hero, aligning their yaw and disabling physics for the secondary hero. It also handles camera settings and game state changes.



### PlaceSecondaryPlayer()

Requests a game state change to "waitfortether" for the secondary player. The function does not perform any additional actions beyond this request.



### TeleportHeroesToLocations(tLocations, fCallback, tCallbackArgs, bEnterState, bExitState)

Teleports all heroes to specified locations. If skip mode is enabled, it calls the callback immediately without performing teleportation. It handles network synchronization and player states during teleportation.
This is what [`MrxCheatBootstrap`](mrxcheatbootstrap)'s `_G.DebugTeleport(x, y, z)` calls under the hood
(one location per player, always the same `x, y, z` — no per-player targeting). **Confirmed by live
testing: crashes to desktop if used while inside an interior cell** (e.g. the PMC HQ interior); works fine
outdoors/in the open world. Root cause not confirmed, but "safe outdoors, unsafe indoors" is the operating
rule regardless of cause.



### TeleportHeroesToHardpoints(tHardpoints, fCallback, tCallbackArgs, bEnterState, bExitState)

Teleports all heroes to specified hardpoints on objects. Similar to `TeleportHeroesToLocations`, it handles network synchronization and player states during teleportation.



### _TeleportHeroes(tOperations, fCallback, tCallbackArgs, bEnterState, bExitState)

Handles the main logic of teleporting heroes based on operations defined in `tOperations`. It manages game state changes and streaming completion.



### _CompleteTeleportHeroes(tOperations, fCallback, tCallbackArgs, bEnterState, bExitState)

Completes the teleportation process for heroes. It handles exiting player modes, reviving characters if necessary, and setting positions and orientations.



### _TeleportStreamingComplete(tOperations, fCallback, tCallbackArgs, bExitState)

Marks streaming as complete for teleport operations and calls `_TeleportComplete` to finalize the teleportation process.



### _TeleportHero(tOperations, i, bExitState, fCallback, tCallbackArgs)

Performs the actual teleportation of a hero based on the operation defined in `tOperations`. It handles setting positions, orientations, and enabling/disabling physics.



### _TeleportComplete(tOperations, fCallback, tCallbackArgs, bExitState)

Finalizes the teleportation process by enabling physics for heroes, resetting camera settings, and calling the callback function.



### EnterBestAvailableSeat(uCharacterGuid, uVehicleGuid, uAvoidSeatGuid, bImmediate)

- **Description**: Attempts to seat a character in the best available seat of a vehicle.

- **Parameters**:

  - `uCharacterGuid`: The GUID of the character to be seated.

  - `uVehicleGuid`: The GUID of the vehicle where the character should be seated.

  - `uAvoidSeatGuid`: The GUID of the seat to avoid (optional).

  - `bImmediate`: A boolean indicating whether the seating should be immediate or not.

- **Returns**: A boolean indicating whether the character successfully entered the vehicle.



### ProcessCallbackTable(tCallbacks, tAdditionalArgs)

- **Description**: Processes a table of callbacks, merging additional arguments and calling each callback with the appropriate arguments.

- **Parameters**:

  - `tCallbacks`: A table containing callback functions and their arguments.

  - `tAdditionalArgs`: Additional arguments to be merged with the callback arguments (optional).



### FindSpawnPointOutOfView(iPathGuid, fRadius, iPrimaryPt)

- **Description**: Finds a spawn point on a path that is out of view from a specified primary point.

- **Parameters**:

  - `iPathGuid`: The GUID of the path where the spawn point should be found.

  - `fRadius`: The radius around the primary point to search for a spawn point.

  - `iPrimaryPt`: The primary point (optional, defaults to the primary character).

- **Returns**: The GUID of the found spawn point.



### SpawnObject(sTemplate, sLocation, sName)

- **Description**: Spawns an object at a specified location with a given name.

- **Parameters**:

  - `sTemplate`: The template name of the object to be spawned.

  - `sLocation`: The location where the object should be spawned (can be a string or GUID).

  - `sName`: The name to assign to the spawned object (optional).

- **Returns**: The GUID of the spawned object.



### SpawnActor(sTemplate, sName, vAnchorObject, sAnchorHardpoint, nYaw, bLink, bHighDetail, fCallback, tData)

- **Description**: Spawns an actor with specific properties and sets up a callback for when the actor is ready.

- **Parameters**:

  - `sTemplate`: The template name of the actor to be spawned.

  - `sName`: The name to assign to the spawned actor (optional).

  - `vAnchorObject`: The object to anchor the actor to (can be a string or GUID).

  - `sAnchorHardpoint`: The hardpoint on the anchor object to attach to (optional).

  - `nYaw`: The yaw angle for the actor (optional).

  - `bLink`: A boolean indicating whether the actor should be linked to the anchor object (optional).

  - `bHighDetail`: A boolean indicating whether the actor should be high detail (optional).

  - `fCallback`: A callback function to call when the actor is ready (optional).

  - `tData`: Additional data to pass to the callback function (optional).

- **Returns**: The GUID of the spawned actor.



### _SpawnActorComplete(uGuid, sName, bInanimate, fCallback, tData)

- **Description**: A helper function called when an actor is fully loaded and ready for use.

- **Parameters**:

  - `uGuid`: The GUID of the actor.

  - `sName`: The name of the actor.

  - `bInanimate`: A boolean indicating whether the actor is inanimate (optional).

  - `fCallback`: A callback function to call when the actor is ready (optional).

  - `tData`: Additional data to pass to the callback function (optional).



### SetupLoadingCallback(self, fCallback, tCallbackData)

- **Description**: Sets up a loading callback for an object.

- **Parameters**:

  - `self`: The object instance.

  - `fCallback`: The callback function to call when loading is complete.

  - `tCallbackData`: Additional data to pass to the callback function (optional).

- **Confirmed exact body**: `self._nLoadPending = 0; self._fLoadCallback = fCallback; self._tLoadData =
  tCallbackData`. Called with no `fCallback` (e.g. `SetupLoadingCallback(_THIS)`) leaves
  `self._fLoadCallback = nil`, which just means `LoadingCallback` below logs `"No load callback!"` instead
  of calling anything once the counter hits zero — a legitimate, harmless way to reuse this counter
  mechanism purely for its pending-count bookkeeping without wanting a callback fired.

### CleanupLoadingCallback(self)

- **Description**: Cleans up a loading callback for an object by removing it from the object's state.

- **Parameters**:

  - `self`: The object instance.



### LoadingCallback(self)

- **Description**: Calls the loading callback if all pending loads are complete.

- **Parameters**:

  - `self`: The object instance.

- **Confirmed exact body**:

  ```lua
  function LoadingCallback(self)
    if self._nLoadPending ~= nil then
      self._nLoadPending = self._nLoadPending - 1
      if self._nLoadPending > 0 then
        return
      end
    end
    local fCallback = self._fLoadCallback
    local tData = self._tLoadData
    self._nLoadPending = nil
    self._fLoadCallback = nil
    self._tLoadData = nil
    if fCallback then
      CallWithOptionalArgs(fCallback, tData)
    else
      Debug.Printf("No load callback!")
    end
  end
  ```

  Decrements first, fires (or logs the harmless "No load callback!" message) once the count reaches `<= 0`
  — a `self` whose `_nLoadPending` was set to `0` by `SetupLoadingCallback` fires on the very first
  `LoadingCallback(self)` call, useful for skipping straight to a completion callback with no real asset
  loading in between (e.g. [`mrxbriefing.lua`'s `_FileLoaded(nil)`](mrxbriefing), confirmed live).



### GetPrimaryCharacterName()

- **Description**: Retrieves the name of the primary character based on their identity.

- **Returns**: The name of the primary character.



### ExplodeMissionName(sMissionName)

- **Description**: Extracts faction, mission type, and number from a mission name string.

- **Parameters**:

  - `sMissionName`: The mission name string to be exploded.

- **Returns**: A tuple containing the faction, mission type (boolean), and mission number.

- **Confirmed exact body — expects a specific ID shape, silently returns `nil` for the number if it
  doesn't fit, no error of its own**:

  ```lua
  function ExplodeMissionName(sMissionName)
    local sFaction = string.sub(sMissionName, 1, 3)
    local sMissionType = string.sub(sMissionName, 4, 6)
    local sMissionNum = string.sub(sMissionName, 7, 9)
    local bMissionType
    if sMissionType == "Con" then
      bMissionType = true
    elseif sMissionType == "Job" then
      bMissionType = false
    end
    local nMissionNum = tonumber(sMissionNum)
    return sFaction, bMissionType, nMissionNum
  end
  ```

  Expects the real convention: 3-letter faction + `"Con"`/`"Job"` + 3-digit number, e.g. `"PmcCon031"`. Feed
  it a mission ID that doesn't fit (e.g. a custom mission like `"CustomTest001"`) and `nMissionNum` comes
  back `nil` — this function itself doesn't error, but at least one real caller does:
  [`mrxbriefing.lua`'s `GetSpielFileName`](mrxbriefing) immediately does
  `string.format("%02d", nMissionNum)` on the result, which throws a hard Lua error on `nil`. Confirmed
  live to be the root cause of a real, reproducible hang while building a custom contract with a
  non-conforming mission ID — see the [Custom Contract deep dive](../deep-dives/custom-contract). Also used
  by `WifMissionData.Init()` to auto-set every real mission's `bContract` field from `bMissionType`.



### GetDistanceToObject(uObjectA, nX, nY, nZ, bIgnoreY)

- **Description**: Calculates the distance from an object to a specified position.

- **Parameters**:

  - `uObjectA`: The GUID of the object.

  - `nX`, `nY`, `nZ`: The coordinates of the position.

  - `bIgnoreY`: A boolean indicating whether to ignore the Y coordinate (optional).

- **Returns**: The distance from the object to the specified position.



### GetDistanceBetween(uObjectA, uObjectB, bIgnoreY)

- **Description**: Calculates the distance between two objects.

- **Parameters**:

  - `uObjectA`, `uObjectB`: The GUIDs of the two objects.

  - `bIgnoreY`: A boolean indicating whether to ignore the Y coordinate (optional).

- **Returns**: The distance between the two objects.



### TestDistanceToAllPlayers(uObject, nDistance, bIgnoreY)

- **Description**: Tests if any player is within a specified distance of an object.

- **Parameters**:

  - `uObject`: The GUID of the object to test against.

  - `nDistance`: The distance to check.

  - `bIgnoreY`: A boolean indicating whether to ignore the Y coordinate (optional).

- **Returns**: True if no players are within the specified distance, false otherwise.



### GetDistantLocations(tLocations, nDistance, bIgnoreY)

- **Description**: Filters a list of locations to remove those that are within a specified distance of any player.

- **Parameters**:

  - `tLocations`: A table of objects to test.

  - `nDistance`: The distance to check.

  - `bIgnoreY`: A boolean indicating whether to ignore the Y coordinate (optional).

- **Returns**: A table of objects that are outside the specified distance from all players.



### GetCharacterIdentity(uChar)

- **Description**: Retrieves the identity label of a character (e.g. which hero — used as a key into
  faction/outfit data elsewhere in the codebase).

- **Parameters**:

  - `uChar`: The GUID of the character.

- **Returns**: The identity label of the character. Used by `ConsoleCheatsMenu.lua`'s "Unlock All Costumes"
  option (see [OnKey Scripts](../sample-scripts-onkey)) to find which hero's outfit list
  ([`WifPmcInterior._tOutfits[sHero]`](../vz/wifpmcinterior)) to unlock everything into.



### EnableHeroWeapons(bEnable)

- **Description**: Enables or disables weapons for the primary and secondary characters.

- **Parameters**:

  - `bEnable`: A boolean indicating whether to enable or disable weapons.



### GetRandomTableElement(t)

- **Description**: Retrieves a random element from a table.

- **Parameters**:

  - `t`: The table from which to retrieve the random element.

- **Returns**: A random element from the table.



### GetFaction(uGuid)

- **Description**: Retrieves the faction label of an object.

- **Parameters**:

  - `uGuid`: The GUID of the object.

- **Returns**: The object's faction as a **full-name string** by testing `Object.HasLabel(uGuid, ...)`
  against the fixed list `{"VZ", "Allied", "China", "Guerilla", "OC", "Pirate", "PMC", "Civ"}` (returns the
  first matching label, or `nil` if none). Pass the result to
  [`MrxFactionManager.GetFactionAbbrev`](mrxfactionmanager) to get the short abbreviation
  (`"All"`/`"Chi"`/`"Gur"`/etc.) used everywhere else on this wiki. Used exactly this way by
  [`VehicleBlippable`](vehicleblippable)'s `Create` to look up a vehicle's faction for its attitude-change
  blip-recolor event.



### SetBoundaryEffect(bOutBoundary, fOpacity)

- **Description**: Sets the boundary effect opacity for the local player's satellite overlay.

- **Parameters**:

  - `bOutBoundary`: A boolean indicating whether to set the out-of-boundary effect (not used in this function).

  - `fOpacity`: The opacity value to set.



### DisplayHealthBar(self, uGuid, nOldHealth, bOptional, nOffset)

- **Description**: Displays a health bar for an object on the HUD.

- **Parameters**:

  - `self`: The object instance.

  - `uGuid`: The GUID of the object.

  - `nOldHealth`: The previous health value (optional).

  - `bOptional`: A boolean indicating whether the health bar is optional (optional).

  - `nOffset`: An offset value for the health bar slot (optional).



### StopHealthBar(uGuid)

- **Description**: Stops displaying a health bar for an object on the HUD.

- **Parameters**:

  - `uGuid`: The GUID of the object.



### GetPrimaryObjectiveRgb()

- **Description**: Retrieves the RGB values for the primary objective color.

- **Returns**: The RGB values (255, 200, 0).



### GetSecondaryObjectiveRgb()

- **Description**: Retrieves the RGB values for the secondary objective color. Used by
  [`Blippable`](blippable)'s `AddObjective` as the default marker color fallback when a `tMarker` config
  doesn't specify its own `tColor`/`tFlash`.

- **Returns**: The RGB values (51, 204, 153).



### GetInlineIconIndexByName(sName)

- **Description**: Retrieves the index of an inline icon by its name.

- **Parameters**:

  - `sName`: The name of the inline icon.

- **Returns**: The index of the inline icon.



### GetInlineIconNameByIndex(iIdx)

- **Description**: Retrieves the name of an inline icon by its index.

- **Parameters**:

  - `iIdx`: The index of the inline icon.

- **Returns**: The name of the inline icon.



### _SearchMarkerTable(tTable, sName)

This function searches through a given table `tTable` for an entry with the name `sName`. If found, it returns the index of the entry; otherwise, it returns 0.



### MarkerGetNameByIndex_World(iIdx)

This function retrieves the marker name from the `tObjWorldMarkers` table at the specified index `iIdx`.



### MarkerGetIndexByName_World(sName)

This function searches for a marker name in the `tObjWorldMarkers` table. If found, it returns the index; otherwise, it logs an error message and returns 0.



### MarkerGetNameByIndex_Pda(iIdx)

This function retrieves the marker name from the `tObjPdaMarker` table at the specified index `iIdx`.



### MarkerGetIndexByName_Pda(sName)

This function searches for a marker name in the `tObjPdaMarker` table. If found, it returns the index; otherwise, it logs an error message and returns 0.



### MarkerGetNameByIndex_Radar(iIdx)

This function retrieves the marker name from the `tObjRadarMaker` table at the specified index `iIdx`.



### MarkerGetIndexByName_Radar(sName)

This function searches for a marker name in the `tObjRadarMaker` table. If found, it returns the index; otherwise, it logs an error message and returns 0.



### ExitAllPlayerModes(uPlayer)

This function requests to cancel the PDA map mode for the specified player `uPlayer`. It also sets cinematic and satellite scan modes to false for the same player.



### Init()

This function initializes a table `_tNumbers` with specific numeric keys mapped to string values. This table is likely used for some internal purpose within the module.



### ShieldFace(guid)

This function retrieves the position of an object with the specified `guid`. If the object exists and is within 150 units of any player character, it triggers a "shieldface" action on that character.



### GetNumberOfDigits(nNum)

This function calculates and returns the number of digits in the given number `nNum`.



### IsInside()

This function checks if the current location is inside either a PMC interior or an HQ managed area by calling [`WifPmcInterior.IsInside()`](../vz/wifpmcinterior) and `MrxHqManager.IsInside()`, respectively.



### ClearVehiclesNearPoint(uPoint, uExceptVeh)

This function removes all vehicles (ground and helicopters) within a specified radius of the point `uPoint`, except for the vehicle with GUID `uExceptVeh`. If `uPoint` is a string, it converts it to a GUID using `Pg.GetGuidByName()`. It logs the number of ground vehicles and helicopters found before removing them.



## Module constants & tables
These module-level tables back the `Marker*` / `GetInlineIcon*` / `FormatMoney` helpers — handy if you're
reverse-engineering marker or money strings:
- `tInlineIcons` — 12 objective inline-icon tags (`"[objaction]"`, `"[objdestroy]"`, `"[objverify]"`, …); the
  1-based index into this list is what `GetInlineIconIndexByName`/`...NameByIndex` translate.
- `tObjWorldMarkers`, `tObjPdaMarker`, `tObjRadarMaker` — ordered name lists for HUD/PDA/radar marker icons;
  the `MarkerGetIndexByName_*`/`MarkerGetNameByIndex_*` pairs convert between the string name and the numeric
  index sent over the network. A miss logs `"Could not find marker <name> in <World/Pda/Radar> table"`.
- `_tNumbers` (built in `Init`) — money magnitude → localized suffix hash used by `FormatMoney`
  (`1e3 → "[0xe00c096a]"`, `1e6 → "[0xcd15e5e8]"`, `1e9 → "[0x4cf9c95f]"`, `1e12`, `1e15`). `FormatMoney`
  clamps its input to `[0, 1e15]`.
- Objective colors are hard-coded: `GetPrimaryObjectiveRgb()` → `255, 200, 0` (amber);
  `GetSecondaryObjectiveRgb()` → `51, 204, 153` (teal-green).

## Events

`MrxUtil` **subscribes to nothing at load time** — it has no top-level `Event.Create`/`CreatePersistent`. It
does, however, create *transient* events from inside its functions as part of doing their work, so it isn't
purely event-free:
- Teleport flow: `Event.GameStateChange` (`"waitfortether"`) and short `Event.TimerRelative` timers in
  `TeleportSecondaryHeroToPrimaryHero`/`_CompleteTeleportHeroes`/`_TeleportComplete`; `Event.Player`
  (`"Human"`,`"Enter"`) after a forced vehicle exit.
- `SpawnActor` waits on `Event.ObjectHibernation` (`"awake"`) before running `_SpawnActorComplete`.
- `DisplayHealthBar` creates `Event.ObjectHealth` (`"<"`) and `Event.TimerRelative` events via `self:_CreateEvent`
  (so `self` must be an event-capable instance); `StopHealthBar` deletes them.

These are per-call, self-cleaning subscriptions, not module lifecycle hooks.

## Notes for modders

- **`TeleportHeroesToLocations` crashes indoors — confirmed by live testing.** See the callout on that
  function above before using it (directly or via `_G.DebugTeleport` on
  [`MrxCheatBootstrap`](mrxcheatbootstrap)) anywhere you're not certain the player is outdoors.
- **`GetFaction` + [`MrxFactionManager.GetFactionAbbrev`](mrxfactionmanager)** is the standard two-step path
  from "I have a `uGuid`" to "I have a short faction abbreviation" — used this way by
  [`VehicleBlippable`](vehicleblippable) and worth reusing rather than re-deriving.
- `SetDefault(vVar, vDefaultValue)` returns `vDefaultValue` only when `vVar` is `nil` — note it takes the
  value by copy, so `SetDefault(x, 5)` does **not** mutate `x` in the caller; use the return value
  (`x = SetDefault(x, 5)`), which is how the rest of this file uses it.
- `SpawnObject(sTemplate, sLocation, sName)` and `SpawnActor(...)` are the standard spawn helpers other
  modules (e.g. [`MrxPmc`](mrxpmc)'s fuel tanks) call — `sLocation` may be a spawn-point **name string** or a
  `uGuid`; it's resolved via `Pg.GetGuidByName`. `SpawnActor` disables AI/physics on the result unless the
  name is exactly `"HqInterior"`.