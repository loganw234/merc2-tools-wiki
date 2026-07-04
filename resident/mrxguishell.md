---

title: mrxguishell

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, shell]

verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- no OnActivate/Create/tInstance anywhere in source)

---



# mrxguishell



*Module: mrxguishell.lua*



## Overview

The `mrxguishell` module is responsible for managing the GUI shell in the game. It handles various user interactions, such as opening dialogs for mission selection and installation options, managing server lists, and handling events related to the Flash interface. The module also manages the attract mode and initializes the shell widget with necessary properties and event handlers.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxSound`, `MrxMultiPageMenu`



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is the one shared front-end shell, not something spawned per world object. Key
fields:

- `_nTimeToAttractMode`: Time in seconds before the attract mode is enabled.

- `_bWaitForDelay`: A flag to indicate whether a delay is active.

- `_SkipButton`: The button used to skip to a mission.

- `tMissions`: A list of mission names that can be selected from the menu.

- `Joystick`: A table mapping joystick buttons to their corresponding actions.

- `tControlMap`: A mapping of joystick buttons to control descriptions.

```



## Functions



### _ClearPressSpaceDelay(data)

- **Description**: Clears the wait for delay flag, allowing the legal screen to be skipped.

- **Parameters**:

  - `data`: The data associated with the event.



### OpenSkipToMissionDialog(oShell)

- **Description**: Opens a dialog to select a starting mission. It pauses the movie and resets the multi-page menu, then adds options for each mission and additional settings like briefings.

- **Parameters**:

  - `oShell`: The shell widget that manages the UI.



### MissionSelected(sMission, oShell)

- **Description**: Handles the selection of a mission or briefing option. It updates the system settings based on the selected option and opens the skip to mission dialog again if briefings are toggled.

- **Parameters**:

  - `sMission`: The name of the selected mission or "EnableBriefings" for toggling briefings.

  - `oShell`: The shell widget that manages the UI.



### OpenInstallDialog(oShell)

- **Description**: Opens a dialog to choose an installation option (install to HDD, use existing install, or use source media).

- **Parameters**:

  - `oShell`: The shell widget that manages the UI.



### InstallCallback(iOption, oShell)

- **Description**: Handles the callback for the selected installation option. It calls the appropriate function based on the selected option and resumes the movie.

- **Parameters**:

  - `iOption`: The index of the selected installation option.

  - `oShell`: The shell widget that manages the UI.



### GetShellGfxFilename()

- **Description**: Returns the filename for the shell graphics file.

- **Returns**: A string representing the filename.



### ResetStartButtonState()

- **Description**: Resets the start button state by clearing the custom data associated with the "Shell" widget.

- **Parameters**: None.



### HandleResetStartButton(oShell)

- **Description**: Handles the reset of the start button state by setting it to nil in the custom data.

- **Parameters**:

  - `oShell`: The shell widget that manages the UI.



### HandleGameStateChangeEvent(oWidget, sStateName, sStateAction)

- **Description**: Handles changes in game state. If the state name is "Shell" and the action is "Enter", it opens the widget.

- **Parameters**:

  - `oWidget`: The widget associated with the event.

  - `sStateName`: The name of the current state.

  - `sStateAction`: The action performed on the state.



### ExitLoad()

- **Description**: Handles the exit load process. If E3 HUD mode is active, it requests a pause and sends an imposter shell event. Otherwise, it fades to black.

- **Parameters**: None.



### HandleInitializationEvent(oWidget, tUnused)

- **Description**: Initializes the shell widget by setting its properties, adding child widgets (movie and flash), and registering various event handlers.

- **Parameters**:

  - `oWidget`: The widget being initialized.

  - `tUnused`: Unused parameters.



### MakeFullscreen(oWidget)

- **Description**: Sets the widget to fullscreen mode.

- **Parameters**:

  - `oWidget`: The widget to be set to fullscreen.



### HandleInput(oWidget, tEvent)

- **Description**: Handles input events. It checks for specific button presses and opens dialogs or performs actions based on those inputs.

- **Parameters**:

  - `oWidget`: The widget associated with the event.

  - `tEvent`: The input event data.



### HandleUpdate(oWidget, nDeltaTime)

- **Description**: Updates the shell widget's state. It checks if the flash is loaded and sets the loading flag to false if it is. It also manages the attract mode timer.

- **Parameters**:

  - `oWidget`: The widget being updated.

  - `nDeltaTime`: The time elapsed since the last update.



### HandleAttractModeEnable(oWidget, tEvent)

- **Description**: Handles enabling or disabling the attract mode based on the event data.

- **Parameters**:

  - `oWidget`: The widget associated with the event.

  - `tEvent`: The event data containing the enable flag.



### HandleServerAdd(oWidget, tEvent)

- **Description**: Adds a server to the list of servers. It updates the server lists and calls an action script callback to add the server in the flash widget.

- **Parameters**:

  - `oWidget`: The widget associated with the event.

  - `tEvent`: The event data containing server information.



### HandleServerRemove(oWidget, tEvent)

- **Description**: Removes a server from the list of servers. It updates the server lists and calls an action script callback to remove the server in the flash widget.

- **Parameters**:

  - `oWidget`: The widget associated with the event.

  - `tEvent`: The event data containing the key of the server to be removed.



### HandleServerUpdate(oWidget, tEvent)

- **Description**: Handles updates to the server list in the GUI shell. If the server exists in `tServerList`, it updates its fields with new data from `tEvent`. If not, it calls `HandleServerAdd` to add the new server.

- **Parameters**:

  - `oWidget`: The widget containing the server list.

  - `tEvent`: An event table containing server details like `uKey`, `sName`, `nStatus`, etc.



### _RepopulateServerList(oWidget)

- **Description**: Repopulates the server list in the GUI shell by removing and re-adding servers from `tServerOrderList`.

- **Parameters**:

  - `oWidget`: The widget containing the server list.



### _OpenShell(oWidget)

- **Description**: Opens the GUI shell, sets up the Flash interface, and handles various initialization tasks like setting viewports, enabling child widgets, and playing sound effects.

- **Parameters**:

  - `oWidget`: The widget representing the GUI shell.



### CompleteFlashSetup(oFlash)

- **Description**: Completes the setup of the Flash interface by setting event handlers for various actions and sending build number information to the Flash player.

- **Parameters**:

  - `oFlash`: The Flash object being set up.



### _CloseShell(oWidget, bRetainShellSwf)

- **Description**: Closes the GUI shell, stops any ongoing movies, and handles cleanup tasks like pausing or unloading the Flash interface.

- **Parameters**:

  - `oWidget`: The widget representing the GUI shell.

  - `bRetainShellSwf`: A boolean indicating whether to retain the SWF file after closing.



### _NewGame(fCallback, tData)

- **Description**: Starts a new game based on the current network state (either singleplayer or multiplayer). It sets up the selected character and starts the appropriate server.

- **Parameters**:

  - `fCallback`: A callback function.

  - `tData`: Data related to the new game.



### _NewGameFlashCallback(oFlash, sCharacter)

- **Description**: Handles the "newGame" event from the Flash interface by setting the selected character and starting a new game.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sCharacter`: The name of the character to select.



### _EnterLobbyFlashCallback(oFlash, sUnused)

- **Description**: Handles entering the lobby by resetting server list data and starting the network lobby process.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sUnused`: Unused parameter (likely a placeholder).



### _ExitLobbyFlashCallback(oFlash, sUnused)

- **Description**: Handles exiting the lobby by resetting server list data and stopping the network if not in online mode.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sUnused`: Unused parameter (likely a placeholder).



### _EnterFriendsLobbyFlashCallback(oFlash, sUnused)

- **Description**: Handles entering the friends lobby by resetting server list data and starting the network friends lobby process.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sUnused`: Unused parameter (likely a placeholder).



### _ExitFriendsLobbyFlashCallback(oFlash, sUnused)

- **Description**: Handles exiting the friends lobby by resetting server list data and stopping the network if not in online mode.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sUnused`: Unused parameter (likely a placeholder).



### _JoinGameFlashCallback(oFlash, sNumber)

- **Description**: Handles joining a game by connecting to the server specified by `sNumber`.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sNumber`: The identifier of the server to join.



### _JoinFriendsGameFlashCallback(oFlash, sName)

- **Description**: Handles joining a friends game by connecting to the server specified by `sName`.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sName`: The name of the server to join.



### _QuickmatchFlashCallback()

- **Description**: Handles the "quickmatch" event from the Flash interface.

- **Parameters**: None.



### _OptimatchFlashCallback()

- **Description**: Handles the "optimatch" event from the Flash interface.

- **Parameters**: None.



### _QuickmatchJoinGameFlashCallback(oFlash, sServerName)

- **Description**: Handles joining a quickmatch game by connecting to the server specified by `sServerName`.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sServerName`: The name of the server to join.



### _OptimatchJoinGameFlashCallback(oFlash, sServerName)

- **Description**: Handles joining an optimatch game by connecting to the server specified by `sServerName`.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sServerName`: The name of the server to join.



### _HandleMovieStartFlashCommand(oFlash, sMovieName)

- **Description**: Handles starting a movie by setting and playing the specified movie in the Flash interface.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sMovieName`: The name of the movie to start.



### _HandleMovieStopFlashCommand(oFlash, sMovieName)

- **Description**: Handles stopping a movie by stopping the specified movie in the Flash interface.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sMovieName`: The name of the movie to stop.



### _LTIStartNewGame(oFlash, sUnused)

- **Description**: Handles starting a new game from the LTI (Learning Tools Interoperability) interface by setting the selected character and starting a new game.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sUnused`: Unused parameter (likely a placeholder).



### _ExitGameFlashCallback(oFlash, sUnused)

- **Description**: Handles exiting the game by requesting the "Exiting" game state and closing the GUI shell.

- **Parameters**:

  - `oFlash`: The Flash object that triggered the event.

  - `sUnused`: Unused parameter (likely a placeholder).



### `_LTIFscommand(oFlash, sFuncName)`

Handles various function calls based on the `sFuncName` parameter. It maps specific function names to corresponding functions in the `LTILibName` library.



### `_LTIEnter(oFlash, iNumber)`

Executes different actions based on the `iNumber` parameter. It maps numbers to specific functions in the `LTILibName` library related to entering various settings or profiles.



### `_LTIVideo(oFlash, iNumber)`

Handles video-related settings changes based on the `iNumber` parameter. It maps numbers to corresponding functions in the `LTILibName` library for video settings.



### `_LTIVideoSetGamma(oFlash, fNumber)`

Sets the gamma value for video settings using the `fNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIVideoGetViewDistance(oFlash, iNumber)`

Gets the view distance setting based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIVideoSwitchOpt1(oFlash, iNumber)`

Switches video option 1 based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIVideoAdvanceDefault(oFlash, sUnused)`

Advances to the default video settings by calling a function in the `LTILibName` library.



### `_LTIInputGeneralOptions(oFlash, sString)`

Handles general input options based on the `sString` parameter by calling a function in the `LTILibName` library.



### `_LTIInputKM(oFlash, iNumber)`

Manages keyboard and mouse input settings changes based on the `iNumber` parameter. It maps numbers to corresponding functions in the `LTILibName` library for input settings.



### `_LTIInputKMChangeInput(oFlash, iNumber)`

Changes keyboard and mouse input settings based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIOverBoundResponse(oFlash, iNumber)`

Handles responses when input values are out of bounds based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIInputJoystick(oFlash, iNumber)`

Manages joystick input settings changes based on the `iNumber` parameter. It maps numbers to corresponding functions in the `LTILibName` library for joystick settings.



### `_LTIInputJoystickChangePrimary(oFlash, iNumber)`

Changes the primary joystick setting based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIInputJoystickChangeInput(oFlash, iNumber)`

Changes joystick input settings based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIJoystickOverBoundResponse(oFlash, iNumber)`

Handles responses when joystick values are out of bounds based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIProfileExit(oFlash, sUnused)`

Exits the current profile settings by calling a function in the `LTILibName` library.



### `_LTICamera(oFlash, iNumber)`

Handles camera-related settings changes based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIChoseOnline(oFlash, iNumber)`

Handles online options selection based on the `iNumber` parameter by calling a function in the `LTILibName` library.



### `_LTIPauseItemChanged(oFlash, iNumber)`

Handles changes to pause menu items based on the `iNumber` parameter by calling a function in the `LTILibName` library.



## Events



- **Event.ObjectHibernation**: Listens for this event and calls `Awake` when the object leaves hibernation.

- **Event.Input.ButtonPress**: Listens for button press events and handles them via `HandleInput`.

- **Event.TimerRelative**: Listens for timer events to manage attract mode timing in `HandleUpdate`.

- **Event.Server.Add**: Listens for server addition events and updates the server list in `HandleServerAdd`.

- **Event.Server.Remove**: Listens for server removal events and updates the server list in `HandleServerRemove`.

- **Event.Server.Update**: Listens for server update events and handles them via `HandleServerUpdate`.

- **Event.GameState.Change**: Listens for game state change events to open the widget when entering the "Shell" state.

- **Event.Flash.Command**: Listens for various Flash commands and handles them through specific callback functions like `_NewGameFlashCallback`, `_JoinGameFlashCallback`, etc.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `HandleInitializationEvent` is called during the initialization of the shell widget to set up necessary properties and event handlers.

   - The sequence of events such as server addition, removal, and updates should be handled in the order they are received to maintain consistency in the GUI.



2. **Pitfalls**:

   - Modifying the `tMissions` table directly can affect the mission selection menu. Ensure that any changes do not disrupt the intended flow of the game.

   - The `_SkipButton` constant is used to skip legal screens. Changing its value might interfere with player navigation, so proceed with caution.



3. **Tunables**:

   - `_nTimeToAttractMode`: Adjusting this value can change how long the attract mode remains active before enabling. Be mindful of user experience when making changes.

   - `_bWaitForDelay`: This flag controls whether a delay is active before allowing the legal screen to be skipped. Modifying it might affect the timing of certain UI elements.



4. **Decompiler artifacts**:

   - Unused local variables or redundant operator groupings in the code are decompiler artifacts and should not be interpreted as intentional logic.

   - Duplicate table keys in literals (where the last one wins) are a known behavior of Lua, so ensure that only the intended key-value pairs are used.