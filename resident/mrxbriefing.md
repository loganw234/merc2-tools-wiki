---

title: mrxbriefing

parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [briefing, UI]

verified: true
verified_note: 'deeper pass: added a Module constants section with the full CHEAP_* (1-17, incl. the
  previously-omitted CONFIRM/DECLINE/INTRO 14-16) and NETEVENT_* (0-3) enums, the default camera-effects
  table, and the forced shadow-base-distance; all prior confirmed mechanism detail (Start/_LoadSpiel/
  _FileLoaded/_AcceptOrDeclineMission/_End/_EndBegin/_UnloadSpiel/GetSpielFileName and the fabricated-Events
  correction) re-verified against source. Custom-contract crash/hang findings unchanged — see the
  [Custom Contract deep dive](../deep-dives/custom-contract).'

---



# mrxbriefing



*Module: mrxbriefing.lua*



## Overview

The `mrxbriefing` module is responsible for managing the briefing system in Mercenaries 2. It handles various aspects of the briefing process, including displaying briefings, managing UI elements, loading/unloading assets, and handling player interactions during the briefing sequence. The module also manages camera settings, face animations, and other visual effects to enhance the briefing experience.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxCinematic`, `WifEquipmentData`, `MrxFactionManager`, `MrxGui`, `MrxUtil`, `MrxVoSequence`, and others



## Instance pattern

**Not per-`uGuid` — this is a singleton module table**, confirmed directly: `_THIS` (the `self` passed to
`MrxUtil.SetupLoadingCallback`/`LoadingCallback` throughout this file) turns out to just be
`mrxbriefing.lua`'s own module environment — `tostring(_THIS)` dumps every function and constant the file
itself defines (this engine gives tables a custom `__tostring` that lists their contents). There's exactly
one active briefing session at a time, tracked in module-level fields, not one instance per world object.

- `_oStarter`: The starter object for the briefing currently in progress.

- **`_tBriefings`: not this module's own private table.** `Start()` (below) sets it via
  `_tBriefings = _oStarter:GetOfferedBriefings()` — literally the *same table reference* as the current
  starter's own briefing list (populated by [`MrxStarter`](mrxstarter)'s `AddBriefing`). Reading or writing
  `_tBriefings` here and reading/writing it through the starter are the same operation.

- `_sSelectedMission`: The currently selected mission name.

- `_bNetSafeSpielLoaded`: Indicates whether the spiel (briefing sequence) has been loaded.

- `_ClientMenuBox`: Reference to a client menu box used in the briefing UI.

- `_tFlashObjects`: Table holding references to flash objects used in the briefing UI.

- `_nLoadPending`: A bare module-level counter used by `_UnloadSpiel`, distinct from `_THIS._nLoadPending`
  (the field `MrxUtil.SetupLoadingCallback`/`LoadingCallback` manage when called as
  `MrxUtil.LoadingCallback(_THIS)`) — two separate pieces of pending-load bookkeeping in this file, not
  one, easy to conflate when tracing a hang since they share a naming pattern but not storage.

- `_tAssetLoadTimers`: Table managing timers for asset loading operations.

- `_tLoadedAssets`: Reference count table for loaded assets.

- `_tNetSafeHardpoints`: Table mapping hardpoint names to indices.

- `_tNetSafeShotNames`: Table mapping shot names to indices.

- `_ClientWaitBox`: Reference to a client wait box used during briefing operations.

- `_nBaseShadowDistance`: Base shadow distance setting before it is modified for briefing purposes.



## Module constants

Confirmed from the top and bottom of the source:

**`CHEAP_*` cheap-cinematic types** (the `nType` passed to `_CreateCheapCinematic`/`NetSafePlayCheapCinematic`):
`CHEAP_GREETING = 1`, `CHEAP_SPECIALCASEGREETING = 2`, `CHEAP_STARTINTRO = 3`, `CHEAP_JOBREQUEST = 4`,
`CHEAP_JOBACCEPT = 5`, `CHEAP_JOBDECLINE = 6`, `CHEAP_WAGERBEGINWIN = 7`, `CHEAP_WAGERBEGINLOSE = 8`,
`CHEAP_WAGERWON = 9`, `CHEAP_WAGERLOST = 10`, `CHEAP_WAGERCHICKENSUIT = 11`, `CHEAP_HINT = 12`,
`CHEAP_GOODBYE = 13`, `CHEAP_CONFIRM = 14`, `CHEAP_DECLINE = 15`, `CHEAP_INTRO = 16`, `CHEAP_PMCWAGER = 17`.
(The earlier list under `_CreateCheapCinematic` omitted 14/15/16 — CONFIRM/DECLINE/INTRO are handled in
`NetSafePlayCheapCinematic`, not `_CreateCheapCinematic`.)

**`NETEVENT_*` custom-network-event IDs** (dispatched to `NetEventCallback` via
`Net.SendCustomEvent("MrxBriefing", ...)`): `NETEVENT_ENABLEMARKERS = 0`, `NETEVENT_DISABLEMARKERS = 1`,
`NETEVENT_DISPLAYMENU = 2`, `NETEVENT_HIDEMENU = 3`.

**`_tDefaultCameraEffects`** — the briefing's default depth-of-field / FOV: `DOF` = `{nAngle=0, nStartNear=0,
nEndNear=0.3, nStartFar=4, nEndFar=10, nBlur=0.5}`, `FOV` = `{nAngle=55}`. Shadow base distance is forced to
`2` for the duration of a briefing (`Graphics.SetShadowBaseDistance(2)` in `Start`, restored in `_EndBegin`).

## Functions



### Deinit()

This function calls `_CheckAssets()` to perform any necessary cleanup when the module is being deinitialized.



### SetStarter(oStarter)

Sets the starter object and initializes an event listener for player join events. If the current player is not the local player, it sends a custom network event to display the menu.



### SetBriefingWrapper(tBriefingWrapper)

Sets the briefing wrapper table, which likely contains configuration data for the briefing UI.



### SendPlayerJoinEvents()

Sends a custom network event to display the client menu if the current player is not the local player.



### NetSafeBriefingAssetsLoaded()

Marks briefing assets as loaded and exits the `STATE_WAITFORGAME` state. If there are assets pending unloading, it calls `NetSafeUnloadBriefingAssets()`.



### NetSafeAreBriefingAssetsLoaded()

Returns a boolean indicating whether briefing assets have been loaded.



### NetSafeLoadBriefingAssets(tAssetTable)

Marks briefing assets as not loaded and enters the `STATE_WAITFORGAME` state. It then loads the specified asset table using `LoadTableOfAssets()`.



### NetSafeUnloadBriefingAssets(tAssetTable)

Unloads the specified asset table. If briefing assets are currently loading, it sets a flag to force unload them later; otherwise, it unloads the assets immediately.



### NetSafeShowFlashBriefing(uName)

Displays a flash object with the given name by calling `_ShowFlashObject()`.



### NetSafeRemoveFlashBriefing(uName)

Removes a flash object with the given name by calling `_RemoveFlashObject()`.



### NetSafeIsStarterLoaded()

Returns a boolean indicating whether the starter has been loaded.



### NetSafeStarterLoaded()

Marks the starter as loaded and sets quick fade to true.



### NetSafeSetStarter(starterIndex, tActors, tShopUnlocked)

Sets up the starter with the given index, actors, and shop unlocked data. It performs various operations such as setting actor names, loading the starter, attaching actors to locations, disabling weapons if necessary, and setting up camera settings.



### NetSafeClearStarter()

Clears the starter by unloading it and resetting related configurations.



### NetSafeLoadSpiel(nMissionIndex, tActors)

Loads the spiel (briefing sequence) for the specified mission index. It sets up briefing actors, attaches them to hardpoints, and loads the corresponding spiel file.



### NetSafeIsSpielLoaded()

Returns a boolean indicating whether the spiel has been loaded.



### NetSafeUnloadSpiel(nMissionIndex)

Unloads the spiel by clearing all flash objects and completing any ongoing cinematics.



### NetSafePlayCheapCinematic(nCinematicType, nIntroIndex)

Plays a cheap cinematic of the specified type. It handles different types of cinematics like confirmations, declines, intros, and other custom sequences.



### GetViewedIntros()

Returns the table containing viewed intros.



### LoadTableOfAssets(tAssetTable, fCallback, tCallbackArgs)

Loads assets from the given asset table using `MrxUtil.SetupLoadingCallback()` and `_LoadTableOfAssets()`. It also sets up loading callbacks and increments the load pending counter.



### UnloadTableOfAssets(tAssetTable, fCallback, tCallbackArgs)

Unloads assets from the given asset table in a similar manner to `LoadTableOfAssets()`, but for unloading operations.



### `_UnloadTableOfAssets(sAssetType, tAssets, fCallback, tCallbackData)`

- **Purpose:** Unloads a table of assets with a timeout mechanism.

- **Parameters:**

  - `sAssetType`: Type of the asset (e.g., "soundbank").

  - `tAssets`: Table of assets to unload.

  - `fCallback`: Callback function to call after unloading.

  - `tCallbackData`: Data to pass to the callback function.

- **Process:**

  - Iterates over each asset in `tAssets`.

  - Sets up a timer for each asset to handle potential timeouts.

  - Calls `_ProcessAsset` to unload each asset.

  - Registers an event handler `_AssetUnloaded` to manage unloading and logging.



### `_ProcessAsset(bLoad, sName, sType, fCallback, tCallbackData)`

- **Purpose:** Loads or unloads a specific asset based on the `bLoad` flag.

- **Parameters:**

  - `bLoad`: Boolean indicating whether to load (`true`) or unload (`false`) the asset.

  - `sName`: Name of the asset.

  - `sType`: Type of the asset (e.g., "soundbank").

  - `fCallback`: Callback function to call after processing.

  - `tCallbackData`: Data to pass to the callback function.

- **Process:**

  - Determines the appropriate loading or unloading function based on `sType`.

  - Updates a reference count for the asset in `_tLoadedAssets`.

  - Calls the determined function to load or unload the asset.



### `_CheckAssets()`

- **Purpose:** Checks and logs all currently loaded assets.

- **Process:**

  - Iterates over each entry in `_tLoadedAssets`.

  - Logs the key (asset name) and its reference count.

  - If no assets are loaded, logs a confirmation message.

  - Clears `_tLoadedAssets` after checking.



### `Start()`

- **Purpose:** Initializes the briefing system for the player.

- **Confirmed mechanism:** `_tBriefings = _oStarter:GetOfferedBriefings()` — this is the aliasing described
  under Instance pattern above, not a copy. Immediately after, it loops over every entry and sets
  `tMissionData.tConfig = WifBriefingData[sMissionName] or {}` — this is where every later
  `_GetSelectedBriefingConfig()` call actually gets its answer from; a mission with no
  `WifBriefingData` entry (e.g. a custom mission added via `WifMissionData.tMissionData` directly) ends up
  with `tConfig = {}`, making every `if tConfig.tXxx then` check throughout this file a safe no-op rather
  than an error.

- **Process:**

  - Retrieves offered briefings and mission data from `_oStarter` (see above).

  - Sets up default camera effects and shadow distance.

  - Saves original actor positions and attaches actors to starting locations.

  - Disables weapons for non-boss starters.

  - Cancels any ongoing voice-over (VO) and sets cinematic mode.

  - Displays the appropriate greeting or menu based on the starter type.



### `_Greeting()`

- **Purpose:** Initiates the initial greeting sequence.

- **Process:**

  - Creates a cheap cinematic for the greeting.

  - Processes the cinematic if available, otherwise proceeds to the business card moment.



### `_BusinessCardMoment()`

- **Purpose:** Handles the display of the business card and subsequent job request.

- **Process:**

  - Stops any ongoing cheap cinematic and deletes skip events.

  - Retrieves and displays the starter's card data using `Hud.CardFanfare`.

  - Sets up a callback to handle the job request after displaying the card.



### `_JobRequest()`

- **Purpose:** Initiates the job request sequence.

- **Process:**

  - Creates a cheap cinematic for the job request.

  - Processes the cinematic if available, otherwise proceeds to display the root menu.



### `_HasSpecialCaseGreeting()`

- **Purpose:** Checks if there is a special case greeting available.

- **Returns:** Boolean indicating whether a special case greeting exists.



### `_SpecialCaseGreeting()`

- **Purpose:** Handles the special case greeting sequence.

- **Process:**

  - Creates a cheap cinematic for the special case greeting.

  - Processes the cinematic if available, otherwise fades and displays the root menu.



### `_DisplayRootMenu()`

- **Purpose:** Displays the main briefing menu with options for briefings, shop, transit, hint, and bribe systems.

- **Confirmed behavior — boss starters skip the menu entirely:** `if _oStarter:IsBoss() then
  _BriefingSelected(_tNames[1]); return end` — for a starter where `IsBoss()` is true, this function
  auto-selects and opens whatever ended up first in `_tNames` and never shows the option list at all.
  **`IsBoss()` is just `return self.bBoss`** ([`MrxStarter`](mrxstarter)), and Fiona's real starter data
  (`WifStarterData.PmcBoss`) does not set `bBoss = true` despite the starter ID's name — confirmed live:
  talking to Fiona shows the normal multi-option menu, not an auto-selected briefing, meaning `IsBoss()`
  evaluates false for her. Don't assume a starter ID containing "Boss" implies this branch fires; check the
  actual `WifStarterData` entry's `bBoss` field.

- **Process:**

  - Stops any ongoing cheap cinematic and deletes skip events.

  - Collects and organizes available briefings, intros, and other options into `_tNames`, `_tTitles`, and
    `_tActions` — walks `_tBriefings` with `pairs()`, so a custom mission added via
    [`MrxStarter`](mrxstarter)'s `AddBriefing` shows up here exactly like a real one, in whatever position
    Lua's table iteration happens to put it (not guaranteed stable/first, except for
    `WifMissionData.IsMissionOnCriticalPath` entries, which are forced to index 1).

  - Sends a custom event to display the menu on the client side if it's the server.

  - Uses `MrxGui.DisplayDialogBox` to show the menu.



### `_RootMenuOptionSelected(tNames, tActions, nIndex)`

- **Purpose:** Handles the selection of an option from the root menu.

- **Process:**

  - Retrieves and executes the action associated with the selected index.



### `_BriefingSelected(sName)`

- **Purpose:** Handles the selection of a briefing mission.

- **Process:**

  - Sets the selected mission name.

  - Checks if the mission is already accepted or if it's a contract with active/pending status.

  - If not yet accepted, calls `_Fade(false, _BeginLoad)`, where a local `_BeginLoad()` reads
    `_GetSelectedBriefingConfig()` and then calls `_LoadSpiel()`.

### `_LoadSpiel()`

- **Purpose:** Loads the briefing spiel for the selected mission.

- **Confirmed exact body** (`resident/mrxbriefing.lua:792`):

  ```lua
  function _LoadSpiel()
    if Net.IsServer() then
      local idx = 1
      local tNetBriefingActors = {}
      if _sSelectedMission then
        local tBriefingData = WifBriefingData[_sSelectedMission]
        if tBriefingData then
          local tActors = tBriefingData.tActors
          if tActors then
            for sName, tActorData in pairs(tActors) do
              if sName ~= "Starter" then
                tNetBriefingActors[idx] = GetActorGuid(sName)
                idx = idx + 1
              end
            end
          end
        end
      end
      Net.LoadMissionSpiel(WifMissionData.GetMissionIndexFromId(_sSelectedMission), tNetBriefingActors)
    end
    local sSpielFile = GetSpielFileName(_sSelectedMission)
    dynamic_import(sSpielFile, _FileLoaded)
  end
  ```

- **`dynamic_import` here is a real, confirmed crash risk for a mission with no compiled spiel asset.**
  Calling it with a name that was never a real compiled asset crashes the game outright (`AV READ`,
  confirmed live) — and this is the only place in the accept flow that calls it for the initially selected
  mission. A custom mission with no real spiel file needs to intercept `_LoadSpiel` itself (an ordinary Lua
  function, safe to wrap) and skip straight to `_FileLoaded(nil)`, while still calling the
  `Net.LoadMissionSpiel(...)` native above it with an empty actor list — `_UnloadSpiel` (below) always
  calls the matching `Net.UnloadMissionSpiel` later regardless of how the spiel was loaded, so skipping the
  load half while still hitting the unload half is an easy way to leave that native pair unbalanced. See
  the [Custom Contract deep dive](../deep-dives/custom-contract) for the full worked example.

- **Never wrap `dynamic_import` itself, even just to log around it.** Confirmed by two separate crashes
  with an identical signature: one from a bogus name, and a second from wrapping `dynamic_import`
  transparently (call the original, change nothing) around a call using a real, valid asset name. It's
  sensitive to its immediate caller's Lua environment, not just its arguments.

### \_FileLoaded(tFile)

- **Description**: Handles the loading of briefing files and assets. It sets up loading callbacks, processes sequences, preloads assets, and waits for player characters to unhibernate.

- **Parameters**:

  - `tFile`: The file containing briefing data.

- **Confirmed: `_FileLoaded(nil)` is a safe, deliberate way to skip straight to `_StartSpiel()`.** Every
  asset-preload block in this function is gated on `type(tFile) == "table"`, so passing `nil` skips all of
  them. The one unconditional `MrxUtil.LoadingCallback(_THIS)` call at the end still fires, and since
  `_THIS._nLoadPending` starts at 0 (from the matching `SetupLoadingCallback(_THIS, _StartSpiel)` earlier
  in this function), that single call is enough to immediately invoke `_StartSpiel`. This is the mechanism
  a custom mission with no real spiel asset relies on when it calls `_FileLoaded(nil)` directly instead of
  routing through `dynamic_import`.



### \_StartSpiel()

- **Description**: Starts the briefing process. It initializes camera settings, binds face animations, and plays the appropriate type of briefing (cinematic, cheap cinematic, or placeholder slides).

- **Parameters**: None

- **Confirmed: has a generic placeholder for a mission with no real cinematic configured at all** — its
  `_PlayCinematic` falls back to `MrxCinematic.PlaceholderSequence({ {sCaption = "Mission Briefing:\n\"" ..
  _sSelectedMission .. "\""} }, _CinematicComplete)`. This is what makes a custom mission with no briefing
  assets at all still show *something* playable (a plain caption screen with a Continue prompt) instead of
  erroring — confirmed live.



### \_DisplayConfirmDialog()

- **Description**: Displays a confirmation dialog box for the mission briefing. It handles client-specific behavior and shows the mission description.

- **Parameters**: None



### \_HandleConfirmDialogInput(nIndex)

- **Description**: Handles user input from the confirmation dialog. It processes the selected option (accept, decline, or wager) and calls the appropriate function.

- **Parameters**:

  - `nIndex`: The index of the selected option.

- **Confirmed**: `nIndex == 1` is Accept (if no recommendations pending), `nIndex == 2` is Decline —
  confirmed live via the dialog shown in the [Custom Contract deep dive](../deep-dives/custom-contract).



### \_DisplayRecommendationsDialog()

- **Description**: Displays a recommendations dialog box for mission items. It generates a recommendation string and plays sound cues based on whether all recommended items are in stock.

- **Parameters**: None



### \_HandleRecommendationsDialogInput(sCue, nIndex)

- **Description**: Handles user input from the recommendations dialog. It stops any playing sound cue and processes the selected option (accept or return to confirmation).

- **Parameters**:

  - `sCue`: The sound cue that was played.

  - `nIndex`: The index of the selected option.



### \_AcceptOrDeclineMission(bAccepted)

- **Description**: Accepts or declines a mission based on user input. It updates the mission status, plays confirmation cinematics if applicable, and prepares for the next step.

- **Parameters**:

  - `bAccepted`: A boolean indicating whether the mission was accepted.

- **Confirmed key steps, in order**: reads `tConfig = _GetSelectedBriefingConfig()`; if accepted and
  `WifMissionData.IsMissionAContract` is true, calls `_oStarter:SetPendingContract(
  _sSelectedMission)` — this is what later tells `WifPmcInterior.Exit()` where to teleport the player, so a
  custom contract mission that never set `bContract = true` on its own `WifMissionData` entry silently
  skips this call and the player ends up stranded with nowhere to go after accepting. Also calls
  `_oStarter:SetMissionAccepted(_sSelectedMission, true)` and appends to `_tMissionsToBeAccepted`. Branches
  three ways on `_oStarter:IsBoss()`/`IsPmcStarter()`: the boss/simple-briefing path plays a confirm/decline
  cinematic if configured, then calls `_End()` directly if none is configured (this is the path Fiona's
  `PmcBoss` starter actually takes, since her real config has no such cinematic set for a mission that
  doesn't define one); the non-PMC-starter path goes through a cheap cinematic before `_End()`/
  `_ReturnToRootMenu()`; the final fallback is a plain `_End()` (accepted) or `_ReturnToRootMenu()`
  (declined) with no cinematic at all.



### \_ReturnToRootMenu()

- **Description**: Stops any ongoing cheap cinematic, deletes skip events, unloads the briefing spiel, and fades out to return to the root menu.

- **Parameters**: None



### \_PrepareForRootMenu()

- **Description**: Prepares the game for returning to the root menu. It clears subtitle buffers, sets default camera effects, attaches actors to starting locations, and sets them to default poses.

- **Parameters**: None



### \_DisplayWagerDialog(nValue)

- **Description**: Displays a wager dialog box for missions that require a wager. It formats the message text based on language settings and shows the numeric input box for the wager amount.

- **Parameters**:

  - `nValue`: The initial value of the wager.



### \_DisplayConfirmWagerDialog(nValue)

- **Description**: Displays a confirmation dialog box for the selected wager amount. It prompts the player to confirm their wager before proceeding.

- **Parameters**:

  - `nValue`: The wager amount selected by the player.



### `_DisplayWagerDialog(nValue)`

- **Description**: Displays a dialog box for setting the wager amount. If confirmed, it updates the rewards data and proceeds to confirm the dialog; if canceled, it reopens the wager dialog.

  

### `_DisplayCancelWagerDialog(nValue)`

- **Description**: Displays a confirmation dialog box to cancel the current wager. If confirmed, it proceeds to the confirm dialog; if canceled, it reopens the wager dialog.



### `_Goodbye()`

- **Description**: Ends the briefing process. It hides any client menu, stops any cheap cinematic, deletes skip events, unloads the spiel, and performs various cleanup tasks like detaching actors from hardpoints and restoring them to original positions if necessary. Finally, it fades out and begins the end sequence.



### `_End()`

- **Description**: Ends the briefing process by setting loading screens, stopping cinematic effects, disabling quick fade, and cleaning up various UI elements and player states. It also sends events to the server and client to handle specific tasks like enabling markers and exiting the briefing state.

- **Confirmed exact sequence**: `Net.SetLoadingScreen(true)` → `_StopCheapCinematic()` →
  `_DeleteSkipEvent()` → **`_UnloadSpiel(true)`** (called directly, not deferred — see below, this is the
  step that has to actually finish for the accept flow to continue at all) → client-menu-box cleanup →
  `LTILibName.ChangeShellState(false)` → `MrxState.SetQuickFade(false)` → `_Fade(false, _EndBegin)`.

### `_EndBegin()`

- **Description**: Sets up the final state of the briefing after it has ended. This includes restoring shadow distances, camera effects, face animations, player setup, enabling player markers, suppressing PDA, detaching actors from hardpoints, restoring actor positions if needed, disabling cinematic mode, and setting animation LOD settings. It also handles client-specific tasks like exiting the wait-for-game state.

- **Confirmed**: the non-client branch ends with `_oStarter:End(_tMissionsToBeAccepted,
  _sLastAcceptedMission)` ([`MrxStarter.End`](mrxstarter)), which is what actually calls
  `WifPmcInterior.Exit(1, false)` for a PMC starter to teleport the player back out — the real end of the
  whole accept sequence. Confirmed reached live, end to end, for a custom contract mission with no real
  spiel asset, once `_UnloadSpiel` (below) was fixed to not error for such a mission.



### `_DisplayJobSummary()`

- **Description**: Displays a dialog box with the summary of the selected mission. This includes the mission title, level, and terms. If the player is on the server, it sends an event to enable markers.



### `_DisplayClientMenu()`

- **Description**: Displays the client menu if the starter actor is loaded and not a boss. It checks if the starter has a shop and if the faction price scale is available before showing the shop option in the menu.



### `_CleanupClientMenu()`

- **Description**: Closes the store and the client menu, and resets the client shop availability flag.



### `_DisplayShop()`

- **Description**: Opens the shop interface. It sets up a callback function based on whether the player is on the client or server to handle closing the shop and returning to the root menu.



### `_DisplayHint()`

- **Description**: Displays a cheap cinematic hint and returns to the root menu after processing the cinematic.



### `_DisplayBribes()`

- **Description**: Displays a dialog box with options to bribe various factions. It includes the faction names and a back option. If a faction is selected, it confirms the bribe amount and executes the bribe if confirmed.



### `_ConfirmBribe(nIndex)`

- **Description**: Confirms the bribe by displaying a dialog box asking for confirmation. If confirmed, it deducts the bribe amount from the player's cash and sets the relation with the chosen faction to friendly.



### `_ExecuteBribe(sFactionAbbrev, nBribe, nIndex)`

- **Description**: Executes the bribe transaction by updating the player's cash and setting the faction relation. It then returns to the root menu.



### `_DisplayTransit()`

- **Description**: Opens the transit interface for the player. It sets up a callback function to handle the transit selection and success status.



### `_TransitCallback(nSelectedIndex, bSuccess)`

- **Description**: Handles the result of the transit selection. If successful, it ends the briefing, deducts fuel, and processes the transit interface callback.



### `_WagerBegin(sMissionId, bWagerWin)`

- **Description**: Begins the wager process by setting up the original actor positions, retrieving rewards data, and starting a cheap cinematic based on whether the wager is won or lost.



### `_WagerTransaction()`

- **Description**: Stops the current cheap cinematic and deletes any skip event. It then creates a timer to execute the wager transaction after a short delay.



### `_ExecuteWagerTransaction(bWagerWin, nChoice)`

- **Description**: Executes the wager transaction by displaying the player's cash balance and updating the rewards data. If the player chooses to chicken out, it changes their outfit before completing the transaction.



### `_WagerEnd()`

- **Description**: Ends the wager process by resetting the wager-related variables and returning to the root menu.



### `_PlayIntro(sName)`

- **Description**: Plays an intro cinematic for the selected mission. It fades out and starts the intro if available, otherwise, it returns to the root menu.



### `_StartIntro(sName)`

- **Description**: Starts the intro cinematic by setting up a cheap cinematic with the specified sequence. It handles the completion of the intro by clearing flash objects, updating viewed intros, and returning to the root menu.



### `_UnloadSpiel(bExitingBriefing)`

- **Description**: Unloads the briefing spiel for the selected mission. It performs various cleanup tasks like unloading assets, stopping animations, and resetting face animations. It also handles server-specific tasks like unloading mission data and sending events.

- **Confirmed exact final two statements — a real crash risk for any mission with no real spiel asset**:

  ```lua
  local sSpielFile = GetSpielFileName(_sSelectedMission)
  dynamic_remove(sSpielFile)
  _sSelectedMission = nil
  ```

  `dynamic_remove` is `dynamic_import`'s native counterpart — calling it here always runs, regardless of
  whether anything was ever actually `dynamic_import`'d for this mission (a mission using the
  `_FileLoaded(nil)` bypass above never imported anything, so this is asking the engine to unload a module
  that was never loaded). More importantly, **`GetSpielFileName` itself throws a hard Lua error** for any
  mission ID that doesn't fit the real `<3-letter faction><Con|Job><3-digit number>` shape (see
  `GetSpielFileName` below) — confirmed to be the actual cause of a real, reproducible hang (no crash
  dump, no log output, just a permanently frozen screen) when this function ran for a custom mission ID
  like `"CustomTest001"`. Everything else in this function is a legitimate no-op for a mission with no
  `WifBriefingData` entry (`_GetSelectedBriefingConfig()` returns `{}`, per `Start()` above, so every
  `if tConfig.tXxx then` block here is skipped) — `GetSpielFileName`'s crash is the one real blocker.
  **Fix**: temporarily short-circuit `GetSpielFileName` (and, separately, neutralize `dynamic_remove`) for
  the specific mission ID, only for the duration of this one call — full worked example and diagnostic
  trail in the [Custom Contract deep dive](../deep-dives/custom-contract).

- **`Net.UnloadMissionSpiel(bExitingBriefing)`** (the native call near the top of this function, paired
  with `_LoadSpiel`'s `Net.LoadMissionSpiel`) was independently bracketed and confirmed *not* to be the
  source of the hang above — it returns normally even for a mission that never had a matching
  `dynamic_import`, as long as the load half was still called (see `_LoadSpiel` above).



### _NextCinematicFrame(tCinematic, fCallback, tCallbackArgs)

This function processes the next frame of a cinematic sequence. It takes three arguments:

- `tCinematic`: A table representing the cinematic sequence.

- `fCallback`: A callback function to be called after processing the current frame.

- `tCallbackArgs`: Arguments to pass to the callback function.



The function checks if the cinematic is valid and initializes the frame counter if necessary. It then processes animations, flash objects, camera settings, and other events defined in the current frame. If there are no events or conditions that require stalling, it proceeds to the next frame.



### GetHardpointIndex(sHardpointName)

This function returns the index of a given hardpoint name from the `_tNetSafeHardpoints` table. It takes one argument:

- `sHardpointName`: The name of the hardpoint.



If the hardpoint is found, it returns its index; otherwise, it logs an error message and returns `nil`.



### GetShotNameIndex(sShotName)

This function returns the index of a given shot name from the `_tNetSafeShotNames` table. It takes one argument:

- `sShotName`: The name of the shot.



If the shot is found, it returns its index; otherwise, it logs an error message and returns `nil`.



### _ProcessCameraSettings(tSettings)

This function processes camera settings for a cinematic frame. It takes one argument:

- `tSettings`: A table containing camera settings.



The function converts hardpoint names and shot names to their respective indices, sets the position and look-at targets, and applies other settings such as blend time and hold state. It then calls `NetSafeProcessCameraSettings` to apply these settings to the cameras.



### NetClientProcessCameraSettings(tSettings, tPosition, tLookAt, tShot)

This function updates camera settings with new position, look-at, and shot data. It takes four arguments:

- `tSettings`: A table containing initial camera settings.

- `tPosition`: The new position for the camera.

- `tLookAt`: The new look-at target for the camera.

- `tShot`: The new shot configuration.



The function updates the settings with the new data and calls `NetSafeProcessCameraSettings` to apply these changes.



### NetSafeProcessCameraSettings(tSettings)

This function applies safe camera settings to both primary and secondary player cameras. It takes one argument:

- `tSettings`: A table containing camera settings.



The function retrieves the GUIDs for the primary and secondary players, converts hardpoint indices back to names, and applies various camera settings such as position, look-at, shot configuration, blend time, and hold state. Debug messages are logged for each setting applied.



### _CreateCheapCinematic(nType)

This function creates a cheap cinematic based on the provided type (`nType`). It returns a table representing the cinematic sequence or `nil` if no valid cinematic can be created.



- **Parameters:**

  - `nType`: An integer representing the type of cheap cinematic to create. The types include:

    - `CHEAP_GREETING`

    - `CHEAP_SPECIALCASEGREETING`

    - `CHEAP_STARTINTRO`

    - `CHEAP_JOBREQUEST`

    - `CHEAP_JOBACCEPT`

    - `CHEAP_JOBDECLINE`

    - `CHEAP_WAGERBEGINWIN`

    - `CHEAP_WAGERBEGINLOSE`

    - `CHEAP_WAGERWON`

    - `CHEAP_WAGERLOST`

    - `CHEAP_WAGERCHICKENSUIT`

    - `CHEAP_HINT`

    - `CHEAP_GOODBYE`

    - `CHEAP_PMCWAGER`



- **Returns:**

  - A table representing the cinematic sequence with fields such as `sParticipant1`, `sParticipant2`, `bFadeIn`, and `tSequence`.

  - `nil` if no valid cinematic can be created.



- **Logic:**

  - Depending on the type, it fetches appropriate voice-over cues (`sCue`) and animations (`sAnim`).

  - It constructs a table `tCheapCinematic` with the necessary fields.

  - If the current network context is a server (`Net.IsServer()`), it sets the briefing cheap cinematic using `Net.SetBriefingCheapCinematic(nType)`.

  - Returns the constructed `tCheapCinematic` or `nil` if no valid sequence can be created.



### `_ProcessCheapCinematic(tData, fCallback, tCallbackArgs)`

- **Purpose**: Processes a cheap cinematic sequence based on the provided data.

- **Parameters**:

  - `tData`: A table containing the cinematic data, including participants, camera overrides, and sequence stages.

  - `fCallback`: A callback function to be executed after the cinematic completes.

  - `tCallbackArgs`: Arguments to pass to the callback function.

- **Process**:

  - Initializes variables for participants and fade-in settings.

  - Defines local functions for switching cameras, stopping animations, playing animations, and playing flashes.

  - Retrieves the primary character's name and sets up a voice sequence data table.

  - Sets up a loading callback to handle the cinematic playback.

  - Iterates through the sequence stages, processing each stage based on whether it is a speaker cue or a flash file.

  - Stops animations for participants at the end of the process.



### `_StopCheapCinematic()`

- **Purpose**: Stops a cheap cinematic sequence.

- **Process**:

  - Checks if the current player is the server and sets the briefing cheap cinematic to 0.

  - Stops the voice sequence.

  - Deletes any animation events associated with participants.



### `_ProcessCheapCinematicAsText(tData, fCallback, tCallbackArgs)`

- **Purpose**: Processes a cheap cinematic sequence as text-based dialogue.

- **Parameters**:

  - `tData`: A table containing the cinematic data, including participants and sequence stages.

  - `fCallback`: A callback function to be executed after the cinematic completes.

  - `tCallbackArgs`: Arguments to pass to the callback function.

- **Process**:

  - Sets up camera settings for a close-up shot.

  - Constructs a message text by iterating through the sequence stages and formatting speaker names and cues.

  - Displays the dialogue in a dialog box.



### `_CleanupCinematic(tCinematic)`

- **Purpose**: Cleans up resources used during a cinematic sequence.

- **Parameters**:

  - `tCinematic`: A table containing the cinematic data, including camera effects and frames.

- **Process**:

  - Clears all flash objects.

  - Restores camera settings to default.

  - Deletes any timer events associated with camera effects and frames.



### `_StopClientCheapCinematic()`

- **Purpose**: Stops a cheap cinematic sequence on the client side.

- **Process**:

  - Stops the cheap cinematic.

  - Deletes the skip event.

  - Processes camera settings to release them.

  - Resets various cinematic-related variables.

  - Sets up a timer to restore the default camera shot.



### `_CinematicComplete()`

- **Purpose**: Handles the completion of a cinematic sequence.

- **Process**:

  - Retrieves the selected briefing configuration.

  - Cancels all voice overs if it's a full cinematic.

  - Stops the cheap cinematic if applicable.

  - Deletes the skip event.

  - Processes camera settings to release them.

  - Resets various cinematic-related variables.

  - Sets actors to their default poses.

  - Cleans up the cinematic or clears flash objects based on the configuration.



### `_ShowFlashObject(sName)`

- **Purpose**: Shows a flash object by name.

- **Parameters**:

  - `sName`: The name of the flash object to show.

- **Process**:

  - Retrieves the flash object from the flash objects table.

  - Sets the flash object to visible and plays it.



### `_AddFlashObject(sName, tPosition, fCallback, tCallbackData)`

- **Purpose**: Adds a flash object by name with optional position and callback.

- **Parameters**:

  - `sName`: The name of the flash object to add.

  - `tPosition`: An optional table specifying the position of the flash object.

  - `fCallback`: A callback function to be executed after adding the flash object.

  - `tCallbackData`: Arguments to pass to the callback function.

- **Process**:

  - Checks if the flash object already exists and calls the callback if it does.

  - Creates a new flash widget, sets its properties, and adds it to the GUI.



### `_RemoveFlashObject(sName, iTimer)`

- **Purpose**: Removes a flash object by name and associated timer.

- **Parameters**:

  - `sName`: The name of the flash object to remove.

  - `iTimer`: The index of the associated timer event.

- **Process**:

  - Retrieves the flash object from the flash objects table.

  - Deletes the flash object and its associated timer.



### `_ClearAllFlashObjects()`

- **Purpose**: Clears all flash objects and associated timers.

- **Process**:

  - Iterates through all flash objects, removing each one.

  - Deletes any associated timer events.



### `_SetupPlayers(bOn)`

- **Purpose**: Sets up player states for cinematic playback.

- **Parameters**:

  - `bOn`: A boolean indicating whether to enable or disable cinematic mode for players.

- **Process**:

  - Retrieves all players and iterates through them.

  - Enables or disables cinematic mode, scrubs characters, and sets their state based on the parameter.



### `_BindFaceAnim(bBind, sActor, sFaceFile)`

Binds or unbinds a face animation set to an actor. If `bBind` is true, it binds the face animation; if false, it unbinds it. The function checks for a valid face file and logs errors if necessary.



### `_AttachActorsToHardpoints(tActorsToHardpoints)`

Attaches actors to specified hardpoints on the "HqInterior" object. It disables physics for each actor before attaching them and persists their transform.



### `_DetachActorsFromHardpoints(tActors)`

Detaches actors from the "HqInterior" object, enabling physics for each actor after detaching.



### `_AttachActorsToLocations(tActorsToLocations)`

Attaches actors to specified locations. It first detaches the actors from any previous attachments and then sets their transform to the target location, disabling physics.



### `_AttachActorsToStartingLocations()`

Attaches actors to starting locations based on whether it's a PMC starter or not. It uses different hardpoints or locations accordingly.



### `_SaveActorsOriginalPositions(tActors)`

Saves the original positions and orientations of specified actors for later restoration.



### `_RestoreActorsToOriginalPositions(tActors)`

Restores actors to their saved original positions and orientations, enabling physics after restoring.



### `_SetActorsToDefaultPose(tActors, bBlend)`

Sets actors to a default pose animation. If `bBlend` is false, it sets the animation without blending.



### `GetActorGuid(sActor)`

Retrieves the GUID of an actor based on its name. It handles special cases for "Player1", "Player2", and "Starter".



### `GetSpielFileName(sMissionName)`

Generates the file name for a spiel based on the mission name and the primary character's name.

**Confirmed exact body — throws a hard Lua error for any mission ID that isn't shaped like a real one:**

```lua
function GetSpielFileName(sMissionName)
  local sCharName = MrxUtil.GetPrimaryCharacterName()
  if sMissionName == "ChiCon009" then
    return "Spiel_Job_Chi09_" .. sCharName
  elseif sMissionName == "OilCon020" then
    return "Spiel_Job_Oil00_" .. sCharName
  elseif sMissionName == "OilCon050" then
    return "Spiel_Job_Oil01_" .. sCharName
  end
  local sFaction, bContract, nNumber = MrxUtil.ExplodeMissionName(sMissionName)
  local sMissionType = "Job"
  if bContract then
    sMissionType = "MinorContract"
  end
  return "Spiel_" .. sMissionType .. "_" .. sFaction .. string.format("%02d", nNumber) .. "_" .. sCharName
end
```

[`MrxUtil.ExplodeMissionName`](mrxutil) expects the real mission-ID convention — 3-letter faction +
`"Con"`/`"Job"` + 3-digit number, e.g. `"PmcCon031"`. Feed it anything else (e.g. a custom mission ID like
`"CustomTest001"`) and its number parse (`tonumber(string.sub(sMissionName, 7, 9))`) comes back `nil`,
which makes the `string.format("%02d", nNumber)` above throw a hard Lua error. This is a real,
confirmed-live crash/hang source — see `_UnloadSpiel` above, the one place in the accept flow that calls
this function for a mission whose `_LoadSpiel` bypassed `dynamic_import` (and therefore never called this
function earlier, where the problem would have surfaced sooner and been easier to trace).



### `GetAnimSet(vSet, sActor)`

Retrieves an animation set for an actor. If the set is a table, it selects the set based on the primary character's name.



### `_GetGreeting()`

Determines the greeting message and animation based on the attitude between the starter's faction and PMC. It also considers whether it's an initial or subsequent greeting.



### `_GetJobRequest()`

Retrieves a random job request cue for the primary character.



### `_GetSpielResponse(bAccepted)`

Retrieves a random spiel response cue based on whether the job was accepted or declined.



### `_GetGoodbye()`

Retrieves a random goodbye cue from the briefing wrapper, if available.



### `_GetGenericTalkBodyAnim(sSpeakerName)`

Generates a generic talk body animation for a speaker. It selects an animation based on the speaker's name and gender.



### `_GetGenericIdleBodyAnim(sSpeakerName)`

Generates a generic idle body animation for a speaker. It selects an animation based on the speaker's name and gender.



### `_GetSelectedBriefingConfig()`

Retrieves the briefing configuration for the selected mission, if available.

**Confirmed exact body**:

```lua
function _GetSelectedBriefingConfig()
  if not (_tBriefings and _sSelectedMission) or not _tBriefings[_sSelectedMission] then
    return nil
  end
  return _tBriefings[_sSelectedMission].tConfig
end
```

Returns `nil` (not `{}`) if the selected mission was never added to `_tBriefings` at all — but for any
mission actually reachable through the normal menu flow, `Start()` (above) already guaranteed
`_tBriefings[sMissionName].tConfig` is set to at least `{}`, so in practice this reliably returns a table,
never `nil`, once a real briefing session is underway.



### `_CreateSkipEvent(fCallback, tCallbackArgs)`

Creates a persistent button event to skip something. It sets up a timer to create the event after a delay.



### `_DeleteSkipEvent()`

Deletes any existing skip events and their associated timers.



### `_ProcessCameraEffects(tData, tCameraEffects)`

Processes camera effects by creating timed events for each effect in the `tCameraEffects` table.



### `_SetCameraEffects(nPlayerCam, sCamEffectState, nDuration, nAngle, nStartNear, nEndNear, nStartFar, nEndFar, nBlur)`

Sets various camera effects such as depth of field and field of view. It restores or sets these effects based on the `sCamEffectState`.



### `_SetDefaultCameraEffects()`

Sets default camera effects for the player's camera.



### `_Fade(bIn, fCallback, tData)`

Fades in or out the game state. It calls a callback function after entering or exiting the wait-for-game state.



### `NetEventCallback(nEventType)`

Handles network events related to enabling/disabling markers and displaying/hiding menus.



## Events

**Corrected — none of `OnActivate`/`OnDeactivate`/`OnDeath`/`OnUse`/`OnEnter`/`OnExit`/`OnStateChange`/
`OnPlayerJoined`/`OnPlayerLeft`/`Init`/`Create`/`Delete` exist anywhere in this file** (a previous pass of
this page listed generic per-`uGuid` object lifecycle boilerplate that doesn't apply — this is a singleton
module, see Instance pattern above, not a spawned world object with its own activation lifecycle). The
real lifecycle is driven by direct calls, not engine object events:

- **`SetStarter(oStarter)` → `Start()`** is how a briefing session actually begins, called by whatever
  starts the interaction with an NPC starter (not shown in this file).
- **`NetEventCallback(nEventType)`** is this file's one real network event handler — enabling/disabling
  markers and showing/hiding the client-side menu box, dispatched through the engine's custom-event
  mechanism (see the [Custom Networked Events deep dive](../deep-dives/networking)), not a `uGuid`-scoped
  object event.
- The `NetSafe*` functions (`NetSafeLoadSpiel`, `NetSafeSetStarter`, etc.) are the client-side halves of
  actions the server initiates via native `Net.*` calls (e.g. `_LoadSpiel`'s `Net.LoadMissionSpiel(...)`
  pairs with `NetSafeLoadSpiel` here) — callback-by-convention, not a subscribed event either.



## Notes for modders

- **Call-order requirements**: Ensure that `SetStarter` is called before starting the briefing process. The sequence of loading assets, setting up actors, and playing cinematics should be followed in a specific order to avoid visual or logical errors.

- **Pitfalls**: Be cautious with network events (`NetSafeBriefingAssetsLoaded`, `NetSafeLoadBriefingAssets`, etc.) as they can lead to race conditions if not handled properly. Ensure that assets are fully loaded before proceeding with briefing sequences.

- **Tunables**: The module uses several boolean flags and counters (e.g., `_bLoadingBriefingAssets`, `_nLoadPending`) to manage the loading state of briefing assets. Modders should be aware of these flags and ensure they are reset or updated correctly after asset operations.

- **Decompiler artifacts**: There are some unused local variables in functions like `_ProcessAsset` and `_UnloadTableOfAssets`. These can be safely ignored as they do not affect the functionality of the module. Additionally, there are slight operator precedence groupings that do not change behavior but look redundant; these should also be disregarded.

- **A custom mission with no compiled spiel asset is possible, but two functions in this file will crash
  or hang if not handled** — confirmed by building a real one end to end. `_LoadSpiel` calls
  `dynamic_import` on a name that was never compiled (crashes outright); `_UnloadSpiel` calls
  `GetSpielFileName` unconditionally, which throws a Lua error for any mission ID that doesn't fit the real
  `<3-letter faction><Con|Job><3-digit number>` naming convention. Both are wrappable/interceptable since
  they're ordinary Lua functions in this file — the crash risk is specifically in `dynamic_import`/
  `dynamic_remove` themselves (see below), not in wrapping the functions that call them. Full worked
  example: the [Custom Contract deep dive](../deep-dives/custom-contract).

- **Never wrap `dynamic_import` (or its counterpart `dynamic_remove`) — not even transparently.** Confirmed
  by two separate real crashes with an identical signature: calling `dynamic_import` with a name that was
  never a real compiled asset, and merely interposing a passthrough wrapper around a call using a real,
  valid asset name. Both natives appear sensitive to their immediate caller's Lua environment, not just
  their arguments.

- **Never write `return fOriginal(...)` when wrapping any function in this file (or anywhere in this
  codebase).** That phrasing compiles as a Lua tail call, which collapses the stack frame and breaks this
  engine's `getfenv(n)`-based module system — confirmed to produce a real runtime error
  (`: no function environment for tail call at level 2`) that broke an already-shipped mission's own
  briefing flow once a hook used this phrasing. Call the original as a plain statement, or capture its
  result in a local and `return` that on a separate line if the return value is actually used (as with
  `GetSpielFileName`).