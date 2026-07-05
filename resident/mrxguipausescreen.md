---

title: MrxGuiPauseScreen

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, pause]

verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- has an Init() setup function but no OnActivate/Create/tInstance anywhere in source)

---



# MrxGuiPauseScreen



*Module: mrxguipausescreen.lua*



## Overview

The `MrxGuiPauseScreen` module is responsible for managing the pause screen in the game. It handles opening and closing the pause menu, initializing control maps, and managing various user interactions such as saving, quitting, and adjusting settings through the LTI (Library Template Interface) library. The module ensures that the pause screen behaves correctly, interacts with other GUI elements, and responds to player inputs.



## Inheritance

- Inherits from: none — base/utility module
- Imports: none



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: only a one-time `Init()` setup function, no
`OnActivate`/`Create`/`tInstance` registry anywhere in source. This is the one shared pause screen, not
something spawned per world object. Key fields:

- **`Joystick`**: A table defining constants for joystick button mappings.

- **`tControlMap`**: A boolean flag initialized to `false`, likely used to track the initialization state of the control map.



## Functions



### Init()

Initializes the control map with different configurations for various vehicle types and human controls. Each entry in the table maps a joystick button constant to a string representing the corresponding action or menu item.



### OpenPauseScreen(oPauseMenu)

Opens the pause screen by checking if there is an active system dialog box or if the pause menu is already active. If not, it loads the pause screen flash file and sets up the necessary event handlers and UI elements.



### _FinishPauseOpen(oPauseMenu)

Finishes loading the pause screen by setting various properties such as visibility, control focus, and Flash event handlers. It also updates the HUD state, control bindings, and other settings based on the current game state.



### ClosePauseScreen(oPauseMenu)

Closes the pause screen by releasing control focus, pausing the flash file, and resetting UI elements. It also restores the HUD state and exits the pause sound state.



### SetUserSaveEnabled(oPause, bEnable)

Enables or disables user save functionality in the pause menu based on the provided boolean flag `bEnable`.



### HandleStateChangeEvent(oWidget, sStateName, sStateAction)

- **Description**: Handles state change events for the pause screen widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `sStateName`: The name of the state that changed.

  - `sStateAction`: The action associated with the state change (e.g., "Enter", "Exit").

- **Behavior**: 

  - If the widget is an imposter or if the state name is not "Pause", it returns early.

  - If the state action is "Enter", it opens the pause screen.

  - If the state action is "Exit", it closes the pause screen.

  - Finally, it calls `MrxGuiBase.ChangeScreenResolution()`.



### HandleInitializationEvent(oWidget, tUnused)

- **Description**: Handles initialization events for the pause screen widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Sets the widget to use immortal events.

  - Retrieves and stores the menu child widget in the custom data.

  - Sets the first child widget to fullscreen.

  - Closes the pause screen.

  - Removes and then adds the `GuiStateChangeEvent` handler for the widget.

  - Initializes an empty table for HUD states.



### _Initialize(oPauseMenu)

- **Description**: Initializes the pause menu widget.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

- **Behavior**:

  - Sets the pause menu to use immortal events.

  - Marks the pause menu as active.

  - Creates and adds a background image widget to the pause menu.

  - Creates and adds a map flash widget to the pause menu.

  - Initializes various properties for the map flash widget.

  - Assigns methods `Open`, `Close`, and `SetUserSaveEnabled` to the pause menu.

  - Sets up event handlers for controller input.

  - Loads the "pause_graphic" asset.

  - Closes the pause menu.



### _FinishLoad(oPauseMenu)

- **Description**: Finishes loading the pause menu widget.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

- **Behavior**:

  - Marks the pause menu as having a flash and not loading.

  - Sets up event handlers for various actions in the map flash widget.

  - Pauses the map flash.



### _HandleToggleEvent(oPauseMenu, tUnused)

- **Description**: Handles toggle events for the pause menu.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

  - `tUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Toggles the active state of the pause menu. If active, it closes; otherwise, it opens.



### _HandleInput(oPauseMenu, tInput)

- **Description**: Handles input events for the pause menu.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

  - `tInput`: Input data.

- **Behavior**:

  - Passes the input event to the map flash widget's event handler.



### _HandleCloseEvent(oMapFlash)

- **Description**: Handles close events for the map flash widget.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

- **Behavior**:

  - If the pause menu is active, requests the game state to return to "ingame" and closes the pause menu.



### _HandleQuitEvent(oMapFlash)

- **Description**: Handles quit events for the map flash widget.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

- **Behavior**:

  - Requests the game state to unload and quits the game. Then, closes the pause menu.



### _ConfirmMedEvacEvent(oMapFlash)

- **Description**: Confirms a medical evacuation event.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

- **Behavior**:

  - Formats the cost of medical evacuation and displays a confirmation message with options to proceed or cancel.



### _HandleMedEvacEvent(oMapFlash, sButton)

- **Description**: Handles the response to the medical evacuation confirmation.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

  - `sButton`: The button pressed in the confirmation message ("1" for yes, other values for no).

- **Behavior**:

  - If the "yes" button is pressed, performs a medical evacuation and requests the game state to return to "ingame".



### HandleImposterInitializationEvent(oWidget, tEvent)

- **Description**: Handles initialization events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tEvent`: Event data.

- **Behavior**:

  - Sets the first child widget to fullscreen.

  - Hides the widget and disables input reception.

  - Disables all child widgets.



### HandleImposterStateChangeEvent(oWidget, sStateName, sStateAction)

- **Description**: Handles state change events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `sStateName`: The name of the state that changed.

  - `sStateAction`: The action associated with the state change (e.g., "Enter", "Exit").

- **Behavior**:

  - If the widget is not an imposter or if the state name is not "Pause", it returns early.

  - If the state action is "Enter", it shows the widget and enables input reception, also enabling all child widgets.

  - If the state action is "Exit", it hides the widget and disables input reception, also disabling all child widgets. It then sends an imposter shell event.



### HandleImposterInputEvent(oWidget, tEvent)

- **Description**: Handles input events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tEvent`: Event data.

- **Behavior**:

  - If the widget is receiving input and a specific button press is detected, requests the game state to return to "ingame".



### HandleImposterEvent(oWidget, tEvent)

- **Description**: Handles general events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tEvent`: Event data.

- **Behavior**:

  - Sets the enabled state of the imposter based on the event's `bOn` flag.



### _LTIFscommand(oFlash, sFuncName)

- **Description**: Handles function calls from the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sFuncName`: The name of the function to call in the LTI library.

- **Behavior**:

  - Calls the corresponding function in the LTI library based on the provided function name.



### _LTIEnter(oFlash, iNumber)

- **Description**: Handles enter events for the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific enter event to handle.

- **Behavior**:

  - Calls the corresponding function in the LTI library based on the provided number.



### _LTIVideo(oFlash, iNumber)

- **Description**: Handles video-related events for the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific video event to handle.

- **Behavior**:

  - Calls the corresponding function in the LTI library based on the provided number.



### _LTIVideoSetGamma(oFlash, fNumber)

- **Description**: Sets the gamma value for video settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `fNumber`: The gamma value to set.

- **Behavior**:

  - Calls the corresponding function in the LTI library to set the gamma value.



### _LTIVideoAdvanceEnter(oFlash, sUnused)

- **Description**: Handles advance enter events for video settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle advance enter.



### _LTIVideoSwitchOpt1(oFlash, iNumber)

- **Description**: Switches video options using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific option to switch.

- **Behavior**:

  - Calls the corresponding function in the LTI library to switch the specified option.



### _LTIVideoAdvanceDefault(oFlash, sUnused)

- **Description**: Handles advance default events for video settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle advance default.



### _LTIInputGeneralEnter(oFlash, sUnused)

- **Description**: Handles enter events for general input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle enter.



### _LTIInputGeneralInvertMouse(oFlash, iNumber)

- **Description**: Inverts mouse settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating whether to invert the mouse (1 for yes, other values for no).

- **Behavior**:

  - Calls the corresponding function in the LTI library to invert the mouse based on the provided number.



### _LTIInputGeneralMouseSense(oFlash, fNumber)

- **Description**: Sets mouse sensitivity using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `fNumber`: The mouse sensitivity value to set.

- **Behavior**:

  - Calls the corresponding function in the LTI library to set the mouse sensitivity.



### _LTIInputGeneralJoySense(oFlash, fNumber)

- **Description**: Sets joystick sensitivity using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `fNumber`: The joystick sensitivity value to set.

- **Behavior**:

  - Calls the corresponding function in the LTI library to set the joystick sensitivity.



### _LTIInputGeneralRumble(oFlash, bBoolean)

- **Description**: Enables or disables rumble feedback using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `bBoolean`: A boolean indicating whether to enable (true) or disable (false) rumble.

- **Behavior**:

  - Calls the corresponding function in the LTI library to set rumble feedback.



### _LTIInputKMEnter(oFlash, sUnused)

- **Description**: Handles enter events for keyboard and mouse input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle enter.



### _LTIInputKMChangeInput(oFlash, iNumber)

- **Description**: Changes input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific input setting to change.

- **Behavior**:

  - Calls the corresponding function in the LTI library to change the specified input setting.



### _LTIInputKMApplyChanges(oFlash, sUnused)

- **Description**: Applies changes to keyboard and mouse input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to apply changes.



### _LTIInputKMDefault(oFlash, sUnused)

- **Description**: Resets keyboard and mouse input settings to default using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to reset to default.



### _LTIInputKMCancelInput(oFlash, sUnused)

- **Description**: Cancels input changes using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to cancel input changes.



### _LTIOverBoundResponse(oFlash, iNumber)

- **Description**: Handles over-bound responses using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific over-bound response to handle.

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle the specified over-bound response.



### _LTIInputKMExit(oFlash, sUnused)

- **Description**: Handles exit events for keyboard and mouse input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle exit.



### _LTIInputJoystickEnter(oFlash, sUnused)

- **Description**: Handles enter events for joystick input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle enter.



### _LTIInputJoystickChangePrimary(oFlash, iNumber)

- **Description**: Changes primary joystick settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific primary setting to change.

- **Behavior**:

  - Calls the corresponding function in the LTI library to change the specified primary setting.



### _LTIInputJoystickChangeInput(oFlash, iNumber)

- **Description**: Changes joystick input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific input setting to change.

- **Behavior**:

  - Calls the corresponding function in the LTI library to change the specified input setting.



### _LTIInputJoystickApplyChanges(oFlash, sUnused)

- **Description**: Applies changes to joystick input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to apply changes.



### _LTIInputJoystickCancel(oFlash, sUnused)

- **Description**: Cancels joystick input changes using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to cancel input changes.



### _LTIInputJoystickDefault(oFlash, sUnused)

- **Description**: Resets joystick input settings to default using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to reset to default.



### _LTIInputJoystickExit(oFlash, sUnused)

- **Description**: Handles exit events for joystick input settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `sUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle exit.



### _LTIJoystickOverBoundResponse(oFlash, iNumber)

- **Description**: Handles over-bound responses for joystick settings using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific over-bound response to handle.

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle the specified over-bound response.



### _LTIPauseItemChanged(oFlash, iNumber)

- **Description**: Handles changes to pause menu items using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific pause menu item changed.

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle the specified change.



### _LTICamera(oFlash, iNumber)

- **Description**: Handles camera-related events using the LTI library.

- **Parameters**:

  - `oFlash`: The flash widget instance.

  - `iNumber`: A number indicating which specific camera event to handle.

- **Behavior**:

  - Calls the corresponding function in the LTI library to handle the specified camera event.



## Events



- **`GuiStateChangeEvent`**: Listens for state change events on GUI widgets and triggers actions like opening or closing the pause screen based on the state name and action.

- **`InitializationEvent`**: Handles initialization events for the pause screen widget, setting up necessary properties and event handlers.

- **`ToggleEvent`**: Toggles the active state of the pause menu, either opening or closing it based on its current state.

- **`InputEvent`**: Passes input events to the map flash widget's event handler.

- **`CloseEvent`**: Handles close events for the map flash widget, returning the game state to "ingame" and closing the pause menu.

- **`QuitEvent`**: Handles quit events for the map flash widget, unloading the game and closing the pause menu.

- **`MedEvacEvent`**: Confirms and handles medical evacuation requests, displaying a confirmation message and performing the evacuation if confirmed.

- **`ImposterInitializationEvent`**: Initializes imposter widgets by setting properties like fullscreen and disabling input reception.

- **`ImposterStateChangeEvent`**: Handles state change events for imposter widgets, showing or hiding them based on the state action.

- **`ImposterInputEvent`**: Handles input events for imposter widgets, detecting specific button presses to return the game state to "ingame".

- **`ImposterEvent`**: Sets the enabled state of imposter widgets based on event data.

- **`LTI*Events`**: Various LTI library-related events that handle different settings and actions within the pause menu, such as video settings, input settings, and camera controls.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `Init()` is called before any other functions to properly initialize the control map and set up necessary properties.

   - The sequence of events (e.g., `OpenPauseScreen`, `_FinishPauseOpen`, `ClosePauseScreen`) should be respected to maintain proper UI behavior.



2. **Pitfalls**:

   - Modifying the control map or LTI settings directly can lead to unexpected behavior if not handled correctly.

   - Ensure that all event handlers are properly registered and unregistered to avoid memory leaks or unintended side effects.



3. **Tunables**:

   - The joystick button mappings in `Joystick` can be adjusted to change the pause menu's input controls.

   - Video settings, input sensitivity, and other options within the LTI library can be modified through their respective functions.



4. **Decompiler artifacts**:

   - Unused local variables or redundant operator groupings are decompiler artifacts and should not be interpreted as intentional logic in the code.