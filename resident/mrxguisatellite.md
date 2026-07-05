---

title: MrxGuiSatellite

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, satellite]

verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- has an Init() setup function but no OnActivate/Create/tInstance anywhere in source)

---



# MrxGuiSatellite



*Module: mrxguisatellite.lua*



## Overview

The `MrxGuiSatellite` module is responsible for managing the satellite GUI overlay in the game. It handles various aspects of the satellite interface, including initializing the overlay, managing minigame states, updating timers and costs, handling user inputs, and providing visual feedback through animations and widgets. This module ensures that the satellite GUI behaves correctly during gameplay, providing players with necessary information and interactive elements.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `MrxFactionManager`, `Pg`, `Player`, `Sound`, `Net`



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: only a one-time `Init()` setup function, no
`OnActivate`/`Create`/`tInstance` registry anywhere in source. This is the one shared satellite overlay,
not something spawned per world object. Key fields:

- `_bUseMinigame`: A boolean indicating whether the minigame is enabled.

- `_nMinigameTime`: The initial time limit for the minigame.

- `_nMinigameTimeIncrease`: The factor by which the minigame time increases.

- `_nMinigameMaxTime`: The maximum time limit for the minigame.

- `_nMoneyCost`: The cost in money to use the satellite.

- `_tDefaultSectorData`: A table containing default sector data.

- `oOverlay`: The GUI overlay instance.

- `bActivated`: Indicates whether the overlay is currently activated.

- `bAdvanced`: Indicates whether advanced mode is enabled.

- `bMinigame`: Indicates whether the minigame is active.

- `fCallback`: Callback function for success events.

- `tData`: Data associated with the callback.

- `oHelpField`: Help field widget.

- `sHelpText`: Help text for the overlay.

- `oFoundWidget`: Widget representing found items.

- `oReadoutWidget`: Widget displaying readout information.

- `oFactionWidget`: Widget showing faction status.

- `oXMeter`: X meter widget.

- `oZMeter`: Z meter widget.

- `oWipeAnimation`: Wipe animation widget.

- `oReticle`: Reticle widget for aiming.

- `bBackgroundVisible`: Indicates whether the background is visible.

- `_nCostPerSecond`: Cost per second during the minigame.

- `_tSectorData`: Current sector data.

- `_fMinigameCallback`: Callback function for minigame events.

- `_tMinigameData`: Data associated with minigame events.

- `bCursorAnimating`: Indicates whether the cursor is animating.

- `_nTolerance`: Tolerance for sector hits.

- `_nTimeLimit`: Current time limit for the minigame.

- `_nCostAccumulator`: Accumulated cost during the minigame.



## Functions



### Init()

Initializes the module state by setting up the default sector data.



### UseMinigame()

Returns whether the minigame is enabled (`_bUseMinigame`).



### HandleSatelliteStateChangeEvent(oOverlay, tEvent)

Handles changes to the satellite's state and updates the overlay accordingly.



### SetActivated(oOverlay, bActivate, bAdvanced, bMinigame)

Sets the activation state of the overlay. If activating, it shows the overlay and initializes the minigame if enabled. If deactivating, it cleans up resources and stops sounds.



### _ActivateStaticEffect(oOverlay)

Activates a static effect on the overlay if it is activated.



### _Cleanup(oOverlay)

Cleans up resources associated with the overlay, such as hiding widgets and stopping animations.



### _HandleInput(oOverlay, tInput)

Handles input events for the overlay. If the appropriate button is pressed and the minigame is active, it begins the minigame.



### Initialize(oOverlay)

Initializes the overlay by setting up its children and custom data fields, including initializing the minigame if enabled.



### SetSuccessCallback(oOverlay, fCallback, tData)

Sets a callback function and associated data for when a success event occurs.



### InitializeHelpField(oField)

Wraps the help field widget.



### SetHelpText(oOverlay, sText)

Sets the help text for the overlay.



### HandleGuidFound(oOverlay, tEvent)

Handles the event where a GUID is found by updating the found widget's position and animation.



### _FinishFoundAnimation(oFound, fCallback, tData)

Finishes the found animation by calling another function to continue the process.



### _FinishFoundAnimation2(oFound, fCallback, tData)

Continues the found animation process by calling another function to finish it.



### _CallFoundCallback(oFound, fCallback, tData)

Calls the callback function with the provided data if it is a valid function.



### HandleReadoutUpdate(oReadout, tEvent)

Updates the readout widget based on the event data.



### HandleFactionUpdate(oFaction, tEvent)

Updates the faction widget's texture and visibility based on the event data.



### HandleXUpdate(oMeter)

Updates the X meter widget with the current camera position.



### HandleZUpdate(oMeter)

Updates the Z meter widget with the current camera position.



### InitMeter(oMeter)

Initializes the meter widget by setting up its children and custom data fields.



### WipeUpdate(oWipe, nDeltaTime)

Updates the wipe animation based on the delta time.



### LoopToHigh(oReticle, nTime)

Animates the reticle to a high point and then loops to a low point.



### LoopToLow(oReticle, nTime)

Animates the reticle to a low point and then loops to a high point.



### HandleBackgroundMessage(oOverlay, tEvent)

Handles background message events by updating the overlay's background visibility and alpha.



### _ShowBackground(oBackground, bShow, fAlpha)

Shows or hides the background widget based on the provided parameters.



### _InitializeMinigame(oOverlay, bUse)

Initializes the minigame if enabled by setting up its children and custom data fields.



### _OpenMinigame(oOverlay, bUse)

- **Description**: Initializes or deactivates the satellite minigame overlay.

- **Parameters**:

  - `oOverlay`: The GUI overlay containing the minigame.

  - `bUse`: A boolean indicating whether to activate (`true`) or deactivate (`false`) the minigame.

- **Behavior**:

  - If `bUse` is `true`, sets up the minigame by initializing colors, animations, and event handlers. It also resets cost and time counters and creates widgets based on sector data.

  - If `bUse` is `false`, simply hides the minigame.



### _CostUpdate(oCost, nDeltaTime)

- **Description**: Updates the cost display in the satellite minigame.

- **Parameters**:

  - `oCost`: The GUI element representing the cost.

  - `nDeltaTime`: The time elapsed since the last update.

- **Behavior**:

  - Increments the cost based on a per-second rate and updates the text of the cost display.



### _TimeUpdate(oTime, nDeltaTime)

- **Description**: Updates the timer display in the satellite minigame.

- **Parameters**:

  - `oTime`: The GUI element representing the timer.

  - `nDeltaTime`: The time elapsed since the last update.

- **Behavior**:

  - Increments the timer and formats it as minutes, seconds, and milliseconds. Updates the text of the timer display accordingly.



### _CleanupMinigame(oOverlay, bUse)

- **Description**: Cleans up resources and resets the satellite minigame overlay.

- **Parameters**:

  - `oOverlay`: The GUI overlay containing the minigame.

  - `bUse`: A boolean indicating whether to perform cleanup (`true`) or not (`false`).

- **Behavior**:

  - If `bUse` is `true`, releases control focus, updates player cash if applicable, and animates various elements back to their base states. It also resets sector data and event handlers.



### _ResetMinigame(oMinigame)

- **Description**: Resets the state of the satellite minigame.

- **Parameters**:

  - `oMinigame`: The minigame instance to reset.

- **Behavior**:

  - Resets sectors, makes child widgets visible, and sets up default sector data.



### BeginMinigame(oOverlay)

- **Description**: Begins the satellite minigame by setting up initial states and animations.

- **Parameters**:

  - `oOverlay`: The GUI overlay containing the minigame.

- **Behavior**:

  - Shows the minigame, hides the reticle, resets sectors, and sets up animations for opening widgets. It also posts an event to indicate the start of the minigame.



### _FinishBeginMinigame(oMinigame)

- **Description**: Finalizes the setup of the satellite minigame after initial animations.

- **Parameters**:

  - `oMinigame`: The minigame instance being set up.

- **Behavior**:

  - Completes animations, sets up event handlers for user input and updates, and starts the cursor animation cycle.



### _MinigameCycleEnd(oCursor, oMinigame, nTime)

- **Description**: Handles the end of a cursor animation cycle in the satellite minigame.

- **Parameters**:

  - `oCursor`: The GUI element representing the cursor.

  - `oMinigame`: The minigame instance.

  - `nTime`: The duration of the current cycle.

- **Behavior**:

  - Adjusts the tolerance for sector hits, restarts the cursor animation with an increased time limit, and posts events for timing success or failure.



### _HandleMinigameUpdate(oMinigame, fDeltaTime)

- **Description**: Handles updates to the satellite minigame during gameplay.

- **Parameters**:

  - `oMinigame`: The minigame instance being updated.

  - `fDeltaTime`: The time elapsed since the last update.

- **Behavior**:

  - Updates the cursor rotation, checks for collisions with sectors, and updates sector colors. It also positions the button based on the current sector and handles player input to complete or reset the minigame.



### _CompleteMinigame(oMinigame)

- **Description**: Completes the satellite minigame by setting up final animations and states.

- **Parameters**:

  - `oMinigame`: The minigame instance being completed.

- **Behavior**:

  - Hides the cursor, resets sectors, posts an event for targetting success, and sets up a callback to remove the targeting mode.



### _FinishCompleteMinigame(oUnused, oMinigame)

- **Description**: Finalizes the completion of the satellite minigame by releasing control focus and exiting the PDAMapMode.

- **Parameters**:

  - `oUnused`: Unused parameter (likely a placeholder).

  - `oMinigame`: The minigame instance being completed.

- **Behavior**:

  - Releases control focus, posts an event for removing the satellite targeting mode, and requests to exit the PDAMapMode.



### _RemoveSatelliteTargettingMode(oMinigame)

- **Description**: Removes the satellite targetting mode by invoking a callback with collected data.

- **Parameters**:

  - `oMinigame`: The minigame instance being removed.

- **Behavior**:

  - Collects player target data and invokes a callback function if available.



### _HandleMinigameInput(oMinigame, tInput)

- **Description**: Handles user input during the satellite minigame.

- **Parameters**:

  - `oMinigame`: The minigame instance handling input.

  - `tInput`: A table containing input data.

- **Behavior**:

  - Checks for specific button presses and handles sector hits by updating sector states, animations, and posting events. It also checks if all sectors have been hit to complete the minigame.



### _SetMinigameCallback(oOverlay, fCallback, tData)

- **Description**: Sets a callback function and associated data for the satellite minigame.

- **Parameters**:

  - `oOverlay`: The GUI overlay containing the minigame.

  - `fCallback`: The callback function to be invoked upon completion.

  - `tData`: A table of data to pass to the callback.



### _SetMinigameSectors(oOverlay, tSectors)

- **Description**: Sets sector data for the satellite minigame.

- **Parameters**:

  - `oOverlay`: The GUI overlay containing the minigame.

  - `tSectors`: A table of sector data to be set.



### _SetMinigameCost(oOverlay, nCost)

- **Description**: Sets the cost per second for the satellite minigame.

- **Parameters**:

  - `oOverlay`: The GUI overlay containing the minigame.

  - `nCost`: The cost per second to be set.



### SetSectorData(oMinigame, tData)

- **Description**: Validates and sets sector data for the satellite minigame.

- **Parameters**:

  - `oMinigame`: The minigame instance setting sector data.

  - `tData`: A table of sector data to be validated and set.



### _InitializeDefaultSectors(oMinigame)

Initializes the default sectors for a given minigame. It sets the sector data from `_tDefaultSectorData` to the minigame's custom data and then creates widgets based on this sector data.



### _CreateWidgetsFromSectorData(oMinigame)

Creates or updates the widgets representing the sectors in the minigame. It iterates through the existing sector widgets, resetting their state and removing them if necessary. Then, it processes each sector data entry to either update an existing widget or create a new one with appropriate properties and animation points.



### _CollideWithSectors(oMinigame, nAngle, nTolerance)

Detects collision between a given angle and the sectors in the minigame. It checks each sector's range (adjusted for negative angles) to see if the provided angle falls within it, considering an optional tolerance. Returns the index of the colliding sector or `nil` if no collision is detected.



### _DetectCollision(nAngle, nLow, nHigh)

A helper function that determines if a given angle falls within a specified range (`nLow` to `nHigh`). It handles cases where the range spans across 0 degrees by adjusting angles accordingly.



### _ResetSectors(oMinigame)

Resets all sectors in the minigame. It clears the hit state for each sector and resets their color and visibility.



### _HaveAllSectorsBeenHit(oMinigame)

Checks if all sectors in the minigame have been hit. It iterates through the sector data to see if any sector's `bHit` flag is still `nil`. Returns `true` if all sectors have been hit, otherwise returns `false`.



## Events

- **Event.SatelliteStateChange**: Triggered when the satellite's state changes. The module handles this event by updating the overlay accordingly.

- **Event.MinigameUpdate**: Triggered during gameplay to update the minigame. The module handles this event by checking for collisions with sectors, updating sector colors, and handling player input.

- **Event.MinigameCycleEnd**: Triggered at the end of a cursor animation cycle in the minigame. The module adjusts the tolerance for sector hits, restarts the cursor animation, and posts events for timing success or failure.

- **Event.MinigameComplete**: Triggered when the minigame is completed. The module hides the cursor, resets sectors, posts an event for targetting success, and sets up a callback to remove the targeting mode.

- **Event.PlayerInput**: Triggered by player input during gameplay. The module handles this event by checking for specific button presses and handling sector hits.



## Notes for modders

- **Call-order requirements**: Ensure that `Init()` is called before any other functions to properly initialize the module state.

- **Pitfalls**: Be cautious when modifying the minigame's cost or time settings, as incorrect values can lead to unexpected behavior. Always validate sector data using `SetSectorData` to ensure proper functionality.

- **Tunables**: The following tunable variables can be adjusted for different gameplay experiences:

  - `_nMinigameTime`: Initial time limit for the minigame.

  - `_nMinigameTimeIncrease`: Factor by which the minigame time increases.

  - `_nMinigameMaxTime`: Maximum time limit for the minigame.

  - `_nMoneyCost`: Cost in money to use the satellite.

- **Decompiler artifacts**: There are no known decompiler artifacts in this module. All functions and variables appear to be correctly named and used according to their intended purpose.