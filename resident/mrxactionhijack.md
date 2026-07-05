---

title: MrxActionHijack

parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [action hijack, minigame, animation]

verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- no OnActivate/Create/tInstance/setmetatable anywhere in source; self-prefixed fields belong to one shared, reused state table, not a per-uGuid factory)

---



# MrxActionHijack



*Module: mrxactionhijack.lua*



## Overview

The `MrxActionHijack` module is responsible for managing the action hijack sequence in the game. It handles various aspects such as initializing the hijack, playing animations, managing minigames, and handling success or failure scenarios. This module also manages events related to the hijack process, ensuring smooth transitions and proper cleanup.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `MrxGui`, `MrxGuiManager`, `MrxGuiHudActionHijack`, `MrxSound`, `Hero`, `MrxAchievements`, `MrxMusic`, and `WifFreePlay`



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance`/`setmetatable`
anywhere in source. The `self`-prefixed fields below belong to one shared, reused state table for
whichever hijack sequence is currently in progress, not a fresh factory-built object per vehicle/hijacker.
Key fields:

- `_bIsInHijack`: A boolean indicating whether the hijack action is currently active.

- `_fUnloadCallback`, `_tUnloadCallbackArgs`: Variables to store a callback function and its arguments for unloading purposes.

- `nVehicleAnimBlendTime`: Set to `0.2`.

- `RULESET_TANK`, `RULESET_HELICOPTER`, `RULESET_APC`, `RULESET_SOLANO`: Constants defining different vehicle hijack rulesets.

- `tDifficulty`: A table containing difficulty levels for tap and mash actions, each with three values representing some timing parameters.

- `tRagdoll`: A table defining ragdoll-related settings such as duration, input, and knockdown times.



## Functions



### IsInHijack()



Returns the current state of the hijack action (`_bIsInHijack`).



### SetUnloadCallback(fCallback, tCallbackArgs)



Sets the unload callback function and its arguments. This function is used to define what should happen when the hijack action unloads.



### CheckGoodStart(uVehicleObject, nRuleSet)



Checks if the vehicle hijack can start based on the rule set and vehicle state. Returns `true` if the conditions are met, otherwise logs a message and returns `false`.



### InitializeActionHijack(self)



Initializes the action hijack by setting up various properties, enabling/disabling certain features, and preparing for the hijack to begin. It also handles local player-specific settings like atmosphere changes and camera focus.



### TankPrep(self)



Prepares the tank for hijacking by disabling AI, clearing vehicle controls, disabling physics for the hijacker, and setting turret parameters.



### Begin(self, i)



Begins a specific step in the hijack action. It handles various tasks such as playing animations, handling multi-events, creating timers for explosions and rumble effects, and setting up event listeners for animation completion and driver/hijacker actions.



### _ProcessMultiEventTable(eCharGuid, tMultiTable)

- **Description**: Processes a multi-event table for a given character GUID. Each event in the table can trigger various actions such as controller rumble, camera shake, particle effects, sound playback, music playback, and more.

- **Parameters**:

  - `eCharGuid`: The GUID of the character associated with the events.

  - `tMultiTable`: A table containing multiple event data entries.

- **Behavior**: For each entry in `tMultiTable`, it sets up a timer that triggers after a specified time. When the timer expires, it processes the corresponding event data, which may include:

  - Controller rumble: Triggers a rumble effect on the controller.

  - Camera shake: Shakes the camera for a local player character.

  - Camera parameters: Adjusts camera focus and field of view parameters.

  - Particle effects: Spawns particle effects at specified positions.

  - Detach event: Detaches an object from another.

  - Play single VO: Plays a voice-over cue.

  - Play music: Starts playing special music.

  - Play sound FX: Plays a sound effect.

  - Stop sound FX: Stops a sound effect.

  - Heli kill: Creates explosion and smoke effects for helicopter destruction.

  - Link object: Attaches or detaches an object to/from another based on state.



### ToggleLinkedObject(self, ChildObject, ParentObject, AttachPoint, State)

- **Description**: Toggles the attachment state of a child object to a parent object at a specified attach point. If `State` is true, it attaches the child object; if false and an instance exists, it detaches and removes the child object.

- **Parameters**:

  - `self`: The current instance of the module.

  - `ChildObject`: The name of the child object to be attached or detached.

  - `ParentObject`: The GUID of the parent object.

  - `AttachPoint`: The attach point on the parent object where the child should be attached or detached.

  - `State`: A boolean indicating whether to attach (true) or detach (false).



### PlayReactiveLoop(self)

- **Description**: Plays reactive loop animations for a hijacker, hijackee, and vehicle. It also sets facial expressions if provided and creates an event for the completion of the animation.

- **Parameters**:

  - `self`: The current instance of the module.



### CreateReactiveLoopAnimationCompleteEvent(self)

- **Description**: Creates or recreates an event that triggers when a reactive loop animation completes. This event is used to handle further actions after the animation finishes.

- **Parameters**:

  - `self`: The current instance of the module.



### OnReactiveLoopAnimationComplete(self)

- **Description**: Handles the completion of a reactive loop animation. If a minigame is not done, it recreates the animation complete event to ensure proper handling of subsequent animations.

- **Parameters**:

  - `self`: The current instance of the module.



### Play(self, sHijackerAnimation, sHijackeeAnimation, sVehicleAnimation, sExtraActors, sReactiveLoopFaceStates, sCharactersFaceStates)

- **Description**: Plays animations for a hijacker, hijackee, and vehicle. It also sets facial expressions for characters if provided.

- **Parameters**:

  - `self`: The current instance of the module.

  - `sHijackerAnimation`: The animation name for the hijacker character.

  - `sHijackeeAnimation`: The animation name for the hijackee character.

  - `sVehicleAnimation`: The animation name for the vehicle.

  - `sExtraActors`: Additional actors and their animations (optional).

  - `sReactiveLoopFaceStates`: Facial expressions for reactive loop characters (optional).

  - `sCharactersFaceStates`: Facial expressions for other characters (optional).



### SetMultiFacialExpressions(sCharGuid, tCharTable)

- **Description**: Sets multiple facial expressions for a character based on the provided table of expression data.

- **Parameters**:

  - `sCharGuid`: The GUID of the character whose expressions are to be set.

  - `tCharTable`: A table containing facial expression data with keys as expression names and values as tables with state, weight, duration, and blend information.



### OnMinigameStart(self)

- **Description**: Handles the start of a minigame based on the type of action specified (`press`, `hold`, `tap`, `alternate`).

- **Parameters**:

  - `self`: The instance table containing the current state and configuration for the minigame.

- **Behavior**:

  - Initializes or updates the HUD button motion speed and other parameters based on the minigame type.

  - Deletes any existing minigame event and creates a new one with the appropriate settings.

  - For `tap` and `alternate` actions, sets up additional parameters like scores, difficulty, and success thresholds.

  - Shows the HUD button using `MrxGuiHudActionHijack.ShowButton` with various parameters depending on the minigame type.



### OnMinigameStatus(self, sStatus, n)

- **Description**: Handles updates to the status of a minigame (`success`, `failed`, `update`, `timeout`).

- **Parameters**:

  - `self`: The instance table containing the current state and configuration for the minigame.

  - `sStatus`: A string indicating the current status of the minigame.

  - `n`: An optional parameter that may be used to provide additional context or data related to the status update.

- **Behavior**:

  - Logs the status update using `Debug.Printf`.

  - Updates internal state based on the status (e.g., setting success flags, showing fail UI).

  - Triggers sound cues and animations for success or failure.

  - Calls `HandleTapMinigame` for specific actions (`tap`, `alternate`) to handle player input.



### HandleTapMinigame(self, sStatus, n)

- **Description**: Manages the logic for minigames involving tapping or alternating inputs (`tap`, `alternate`).

- **Parameters**:

  - `self`: The instance table containing the current state and configuration for the minigame.

  - `sStatus`: A string indicating the current status of the minigame.

  - `n`: An optional parameter that may be used to provide additional context or data related to the status update.

- **Behavior**:

  - Updates player and driver scores based on the status.

  - Checks if either the player or driver has reached the success threshold.

  - Triggers animations and sound cues for success or failure.

  - Adjusts difficulty levels and reactive loops as needed.



### OnDriverSimulatedButtonPress(self)

- **Description**: Simulates a button press by the driver in the minigame.

- **Parameters**:

  - `self`: The instance table containing the current state and configuration for the minigame.

- **Behavior**:

  - Logs the simulated button press using `Debug.Printf`.

  - Updates the driver's score to the success threshold.

  - Calls `HandleTapMinigame` to handle the result of the simulated button press.

  - Schedules the next simulated button press using a timer event.



### ActionHijackFinish(uHijacker, uHijackee, uVehicle, bSuccess)

- **Description**: Finalizes an action hijack by posting an event and cleaning up resources.

- **Parameters**:

  - `uHijacker`: The GUID of the player performing the hijack.

  - `uHijackee`: The GUID of the target being hijacked.

  - `uVehicle`: The GUID of the vehicle involved in the hijack.

  - `bSuccess`: A boolean indicating whether the hijack was successful.

- **Behavior**:

  - Logs the completion of the action hijack using `Debug.Printf`.

  - Posts an event with the hijack results.

  - Resets global flags and calls any unload callbacks.

  - Starts a nag sequence if applicable.



### OnAnimationComplete(self)

- **Description**: Handles the completion of an animation during the action hijack process.

- **Parameters**:

  - `self`: The instance table containing the current state and configuration for the minigame.

- **Behavior**:

  - Logs the completion of the animation using `Debug.Printf`.

  - Posts an event indicating the completion of the action hijack.

  - Triggers success or failure animations based on the final outcome.



### DoSuccessAnimation(self)

Handles the success animation sequence for an action hijack. It checks if there is a custom next section and proceeds accordingly. If no more sections are available, it completes the action hijack.



### DoFailureAnimation(self)

Handles the failure animation sequence for an action hijack. It sets up various animations and facial expressions for different characters involved in the hijack. It also manages the ragdoll state and cleanup after a failure.



### OnFailAnimationComplete(self)

Called when the failure animation completes. It handles cleanup, including disabling invincibility, restoring camera settings, and toggling HUD visibility. It also starts a ragdoll minigame if applicable.



### OnRagdollMinigameUpdate(self, sStatus, n)

Handles updates during the ragdoll minigame. This function is currently empty and may be intended for future implementation.



### OnRagdollMinigameDone(self, bSuccess)

Called when the ragdoll minigame completes. It toggles HUD visibility based on whether the player succeeded or failed in the minigame. It also cleans up the event handle for the minigame timer.



### OnRagdollDone(self, bGetUp)

Handles the cleanup after a ragdoll state is completed. It re-enables invincibility for characters involved in the hijack, restores camera settings, and toggles HUD visibility. It also calls any custom completion handlers if defined.



### ChangeAtmosphere(bBegin)

Changes the atmosphere effect to enhance the visual impact of an action hijack. It adjusts bloom settings and ensures that changes are safe to begin or end based on current atmospheric conditions.



### RestoreCamera(self)

Restores camera focus parameters and effects after an action hijack sequence, ensuring a smooth transition back to normal gameplay.



### DisableFacialExpressions(self)

Disables facial expressions for all characters involved in the hijack. This function is used to ensure that no unintended facial animations interfere with the hijack sequence.



### CleanupCommonNonSuccess(self, bFail)

Performs common cleanup tasks after an action hijack fails or completes without success. It disables facial expressions, restores camera settings, and handles ragdoll states based on whether the player succeeded or failed.



### CompleteHijackNonFailure(self, bSuccess)

Handles the completion of an action hijack that did not fail. It re-enables invincibility for characters involved in the hijack, restores camera settings, and toggles HUD visibility. It also handles vehicle animations and cleanup based on whether the player succeeded or failed.



### ActionHijackCancel(self)

- **Description**: Cancels the action hijack process.

- **Process**:

  - Prints debug information.

  - Ends the action hijack sound if the local player is the hijacker.

  - Disables cinematic mode for the hijacker based on their control state.

  - Deletes all events associated with the hijack.

  - If using the Solano ruleset, cancels any contract if available.

  - Calls `CleanupCommonNonSuccess` to clean up common non-success states.

  - Sets the hijacker's state to "Upright" and "Idle".

  - Enables physics for the hijacker.

  - Aborts the vehicle hijack.

  - Completes the hijack as a non-failure.

  - Prints debug information.



### ActionHijackComplete(self)

- **Description**: Completes the action hijack process successfully.

- **Process**:

  - Prints debug information.

  - Adds an achievement count if the local character is the hijacker.

  - Calls `CompleteHijackNonFailure` with success status from the current state.

  - Prints debug information.



### OnDriverDone(self)

- **Description**: Handles the completion of the driver's role in the hijack process.

- **Process**:

  - Prints debug information.

  - Enables AI for the hijackee.

  - Depending on the current state (`bDriverDoneRagdoll`, `bDriverDoneStanding`, `bDriverDoneDead`, etc.):

    - Forces the hijackee to exit the vehicle without snapping.

    - Knocks down or kills the hijackee based on attributes and conditions.

    - Removes the driver from the world if necessary.

  - Prints debug information.



### DeleteAllEvents(self)

- **Description**: Deletes all events associated with the action hijack process.

- **Process**:

  - Prints debug information.

  - Iterates through `self.tEvent` and deletes each event.

  - If there are multi-events, iterates through them and deletes their timers.



### OnAnimationCompleteRemote(self)

- **Description**: Handles the completion of a remote animation.

- **Process**:

  - Prints debug information.



### PushActionHijack(self, newState, bSuccess)

- **Description**: Pushes a new state for the action hijack process.

- **Process**:

  - Prints debug information.

  - If `newState` is 0 and `bSuccess` is true, marks success and completes the hijack.

  - If `newState` is 0 and `bSuccess` is false, marks failure and handles the failure animation.

  - If not `bSuccess`, handles the failure animation if not already done.

  - If `newState` differs from the current state, handles the success animation.



## Events



- **Event.ObjectHibernation**: Listens for this event to wake up and initialize the hijack action when the object leaves hibernation.

- **Event.MinigameStatus**: Handles updates to the status of a minigame (`success`, `failed`, `update`, `timeout`).

- **Event.AnimationComplete**: Triggers when an animation during the hijack process completes, handling success or failure animations and cleanup tasks.

- **Event.DriverSimulatedButtonPress**: Simulates a button press by the driver in the minigame.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `InitializeActionHijack` is called before starting any hijack actions to set up necessary properties and configurations.

   - Properly handle the completion of animations and minigames using `OnAnimationComplete`, `OnMinigameStatus`, and related functions.



2. **Pitfalls**:

   - Be cautious with modifying global flags or state variables, as they can affect multiple instances of the hijack action.

   - Ensure that all events are properly deleted using `DeleteAllEvents` to avoid memory leaks or unintended behavior.



3. **Tunables**:

   - Adjust difficulty levels in `tDifficulty` for different minigames (`tap`, `mash`) to balance player experience.

   - Modify ragdoll settings in `tRagdoll` to control the duration and effects of ragdoll states during hijack failures.



4. **Decompiler artifacts**:

   - Some local variables may appear unused or are assigned but never read, which is a decompiler artifact and should be ignored unless it affects logic.

   - Duplicate table keys in literals (last one wins at runtime) are also decompiler artifacts and do not affect functionality.