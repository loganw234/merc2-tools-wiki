---

title: MrxTaskObjective

parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1


inherits: MrxTask

tags: [task, objective]

verified: true

verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTask](mrxtask) for the general mechanism.

---



# MrxTaskObjective



*Module: mrxtaskobjective.lua*



## Overview

The `MrxTaskObjective` module is responsible for managing task objectives within the game. It handles the activation, completion, and cancellation of tasks, as well as managing target tracking, display settings, and message handling. This module ensures that players are informed about their progress through various in-game interfaces such as the PDA and radar.



## Inheritance

- Inherits from: `MrxTask`
- Imports: `MrxUtil`



## Instance pattern

**Not per-`uGuid` — inherits [`MrxTask`](mrxtask)'s class-factory pattern** (see that page for the general
mechanism), identified by name/lineage rather than a world-object GUID. Key fields tracked via the config
table:

- `_tEvents`: A table for managing event callbacks.

- `_tTargets`: A table tracking target objects and their statuses.

- `_nCompleted`: The number of completed parts of the task.

- `_nCancelled`: The number of cancelled parts of the task.

- `_nQuota`: The required number of completions to meet the quota.

- `_nTotal`: The total number of targets or parts in the task.

- `_bDspBlpRdr`, `_bDspBlpPda`, `_bDspBlpWld`: Flags for enabling/disabling radar, PDA, and world blip displays.

- `_bDspMsgAdd`, `_bDspMsgUpd`, `_bDspMsgCpl`, `_bDspMsgCcl`: Flags for enabling/disabling add, update, complete, and cancel message displays.

- `_bDspDescPda`: Flag for enabling/disabling PDA description displays.

- `_knMarkerYClampDistance`: A constant used for clamping the Y-axis position of markers or blips.



## Functions



### Activated(self)

- **Description**: Initializes the task objective when it is activated.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Resets various counters and flags (`_tEvents`, `_tTargets`, `_nCompleted`, `_nCancelled`, `_nQuota`, `_nTotal`).

  - Retrieves configuration settings from `GetConfig()`.

  - Sets up target filtering based on configuration (`uTgtObjFilter`, `bTrackOnActivate`, `sTgtLabelFilter`, `vTgtInclude`, `vTgtExclude`).

  - Initializes the display settings and refreshes all target displays.

  - Creates initial notes and messages for the objective.



### _InitialNotesComplete(self)

- **Description**: Handles the completion of initial notes or messages.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Processes callback tables (`tOnInitialNotesComplete`).

  - Calls optional arguments (`fOnInitialNotesComplete`).



### Complete(self)

- **Description**: Marks the task objective as completed.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Checks if the task is already completed and logs a failure message if so.

  - Logs the completion of the task.

  - Cleans up resources and sets the state to completed.

  - Refreshes the PDA display for the mission ancestor.

  - Issues state change callbacks.



### Cancel(self)

- **Description**: Marks the task objective as cancelled.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Checks if the task is already cancelled and logs a failure message if so.

  - Logs the cancellation of the task.

  - Cleans up resources and sets the state to cancelled.

  - Refreshes the PDA display for the mission ancestor.

  - Issues state change callbacks.



### Cleanup(self)

- **Description**: Cleans up resources associated with the task objective.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Stops any voice sequences if they are still running.

  - Clears target filters and event tables.

  - Removes all target status and GUI information.



### _ClearEventTable(tEvents)

- **Description**: Recursively deletes events in a table.

- **Parameters**:

  - `tEvents`: The table containing event handles.

- **Behavior**:

  - Iterates through the table, deleting each event handle using `Event.Delete`.



### CompletePart(self, ...)

- **Description**: Marks a part of the task objective as completed.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `...`: Additional arguments passed to the function.

- **Behavior**:

  - Increments the completion counter (`_nCompleted`).

  - Processes callback tables and optional arguments for part completion.

  - Adjusts the timer if configured (`nAddTime`).

  - Determines if all parts are complete and sets the message type accordingly.

  - Prints an objective message based on the configuration.

  - Updates the mission PDA display.

  - Completes the task if all parts are completed.



### CancelPart(self, ...)

- **Description**: Marks a part of the task objective as cancelled.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `...`: Additional arguments passed to the function.

- **Behavior**:

  - Increments the cancellation counter (`_nCancelled`).

  - Processes callback tables and optional arguments for part cancellation.

  - Updates the mission PDA display.

  - Determines if the quota can no longer be met and cancels the task if necessary.



### IsQuotaMet(self)

- **Description**: Checks if the completion quota has been met.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Returns**:

  - A boolean indicating whether the quota has been met (`_nCompleted == _nQuota`).



### IsLiveConfigureable(self, sConfigKey)

- **Description**: Checks if a configuration key can be live-configured.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `sConfigKey`: The configuration key to check.

- **Returns**:

  - A boolean indicating whether the key is valid for live configuration.



### ReinterpretConfig(self)

- **Description**: Reinterprets the configuration settings for the task objective.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Sets display settings from the configuration.

  - Updates target statuses and refreshes all target displays.



### _SetupTargets(self)

- **Description**: Sets up targets for the task objective based on the filter.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Retrieves included objects from the target filter.

  - Determines the total number of targets and sets the quota accordingly.



### RemoveTarget(self, uGuid)

- **Description**: Removes a target from the task objective.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: The GUID of the target to remove.

- **Behavior**:

  - Adds the target to the filter with exclusion and sets its status to false.



### _SetTargetStatus(self, uGuid, bOn, sType)

- **Description**: Sets the status of a target.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: The GUID of the target.

  - `bOn`: A boolean indicating whether the target is active.

  - `sType`: An optional type string for the target.

- **Behavior**:

  - Updates the status and type of the target in `_tTargets`.

  - Refreshes the display for the target.



### _SetAllTargetStatus(self, bOn)

- **Description**: Sets the status of all targets.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bOn`: A boolean indicating whether the targets are active.

- **Behavior**:

  - Iterates through all targets and sets their status using `_SetTargetStatus`.



### GetTargetObjectFilter(self)

- **Description**: Retrieves the target object filter for the task objective.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Returns**:

  - The GUID of the target object filter.



### _SetDisplaySettingsFromConfig(self)

- **Description**: Sets display settings from the configuration.

- **Parameters**:

  - `self`: The instance of the task objective.

- **Behavior**:

  - Retrieves and processes display-related configuration settings.

  - Toggles blip and message displays based on the configuration.



### _ToggleBlipDisplay(self, bOn)

- **Description**: Toggles the display of blips for the task objective.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bOn`: A boolean indicating whether to enable or disable blip displays.

- **Behavior**:

  - Sets default values for radar, PDA, and world blip displays based on the toggle state.



### _SetBlipDisplay(self, tConfig)

- **Description**: Sets blip display settings from a configuration table.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `tConfig`: A table containing blip display configuration settings.

- **Behavior**:

  - Updates blip display settings (`_bDspBlpRdr`, `_bDspBlpPda`, `_bDspBlpWld`) based on the configuration.



### _ToggleMsgDisplay(self, bOn)

- **Description**: Toggles the display of messages for the task objective.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bOn`: A boolean indicating whether to enable or disable message displays.

- **Behavior**:

  - Sets default values for add, update, complete, and cancel message displays based on the toggle state.



### _SetMsgDisplay(self, tConfig)

- **Description**: Sets message display settings from a configuration table.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `tConfig`: A table containing message display configuration settings.

- **Behavior**:

  - Updates message display settings (`_bDspMsgAdd`, `_bDspMsgUpd`, `_bDspMsgCpl`, `_bDspMsgCcl`) based on the configuration.



### _SetDescPdaDisplay(self, bDspDescPda)

- **Description**: Sets the PDA description display setting.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bDspDescPda`: A boolean indicating whether to enable or disable PDA description displays.

- **Behavior**:

  - Updates the PDA description display setting (`_bDspDescPda`) based on the configuration.



### _SetTargetDisplay(self, uGuid, bOn, bPulsate)

- **Description**: Sets the display status of a target.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: The GUID of the target.

  - `bOn`: A boolean indicating whether to enable or disable the target display.

  - `bPulsate`: A boolean indicating whether to pulsate the radar blip for the target.

- **Behavior**:

  - Updates the suppress display flag for the target in `_tTargets`.

  - Refreshes the display for the target.

  - Pulsates the radar blip if enabled.



### _SetAllTargetsDisplay(self, bOn)

- **Description**: Sets the display status of all targets.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bOn`: A boolean indicating whether to enable or disable the target displays.

- **Behavior**:

  - Iterates through all targets and sets their display status using `_SetTargetDisplay`.



### _RefreshTargetDisplay(self, uGuid)

- **Purpose**: Refreshes the display of a target for an objective.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target.

- **Returns**: A boolean indicating whether the display was refreshed.



### _BuildRadarBlipConfig(self, uGuid)

- **Purpose**: Builds the configuration for a radar blip associated with a target.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target.

- **Returns**: A table containing the configuration for the radar blip.



### _BuildPdaBlipConfig(self, uGuid)

- **Purpose**: Builds the configuration for a PDA (Personal Digital Assistant) blip associated with a target.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target.

- **Returns**: A table containing the configuration for the PDA blip.



### _compare(a, b)

- **Purpose**: Compares two values to determine their order.

- **Parameters**:

  - `a`: The first value to compare.

  - `b`: The second value to compare.

- **Returns**: A boolean indicating whether `a` is less than `b`.



### _RefreshAllTargetDisplay(self)

- **Purpose**: Refreshes the display of all targets for an objective.

- **Parameters**:

  - `self`: The instance of the module.



### RefreshPdaDisplay(self)

- **Purpose**: Refreshes the PDA display for all relevant targets.

- **Parameters**:

  - `self`: The instance of the module.



### PulsateRadarBlips(self, nDuration)

- **Purpose**: Makes radar blips pulsate for a specified duration.

- **Parameters**:

  - `self`: The instance of the module.

  - `nDuration`: The duration in seconds for which the blips should pulse.



### PulsateRadarBlip(uGuid, nDuration)

- **Purpose**: Makes a specific radar blip pulsate for a specified duration.

- **Parameters**:

  - `uGuid`: The unique identifier of the target.

  - `nDuration`: The duration in seconds for which the blip should pulse.



### EnableTracking(self, bEnable)

- **Purpose**: Enables or disables tracking for all targets associated with an objective.

- **Parameters**:

  - `self`: The instance of the module.

  - `bEnable`: A boolean indicating whether to enable or disable tracking.



### _PrintObjectiveMessage(self, sMsgType, fCallback, tCallbackArgs)

- **Purpose**: Prints a message related to an objective.

- **Parameters**:

  - `self`: The instance of the module.

  - `sMsgType`: The type of message (e.g., "add", "upd").

  - `fCallback`: A callback function to be executed after printing the message.

  - `tCallbackArgs`: Arguments to pass to the callback function.



### GetDisplayDescription(self)

- **Purpose**: Retrieves the display description for an objective.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: A boolean indicating whether the description should be displayed.



### GetDescription(self, bPrependInlineIcon)

- **Purpose**: Retrieves the full description for an objective, optionally prepending an inline icon.

- **Parameters**:

  - `self`: The instance of the module.

  - `bPrependInlineIcon`: A boolean indicating whether to prepend an inline icon.

- **Returns**: A string containing the description.



### GetObjectiveDescription(sObjDesc, nCompleted, nQuota, sMsgType)

- **Purpose**: Constructs a detailed objective description based on progress and type of message.

- **Parameters**:

  - `sObjDesc`: The base description of the objective.

  - `nCompleted`: The number of completed tasks.

  - `nQuota`: The total quota for the task.

  - `sMsgType`: The type of message (e.g., "add", "upd").

- **Returns**: A string containing the detailed description.



### GetShortDescription(self)

- **Purpose**: Retrieves the short description for an objective.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: A string containing the short description.



### GetProgressQuota(self)

- **Purpose**: Retrieves the progress quota for an objective.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: An integer representing the progress quota.



### GetProgressCompleted(self)

- **Purpose**: Retrieves the number of completed tasks for an objective.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: An integer representing the number of completed tasks.



### GetMissionAncestor(self)

- **Purpose**: Retrieves the ancestor mission associated with an objective.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: The ancestor mission object if found, otherwise `nil`.



### _UpdateMissionInPda(self)

- **Purpose**: Updates the PDA display for the mission associated with an objective.

- **Parameters**:

  - `self`: The instance of the module.



### _GetShortDescription()

- **Purpose**: Retrieves a default short description for an objective.

- **Returns**: A string containing the default short description ("NULL").



### _GetTargetBlipColor(bOptional)

- **Purpose**: Retrieves the color for a target blip based on whether it is optional or not.

- **Parameters**:

  - `bOptional`: A boolean indicating whether the target is optional.

- **Returns**: A table containing RGB values for the blip color.



### _GetJust2DCheckNeeded()

- **Purpose**: Determines if a just 2D check is needed.

- **Returns**: A boolean indicating whether a just 2D check is required (always `false`).



### GetInlineIcon(self)

- **Purpose**: Retrieves an inline icon for an objective based on its configuration.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: A string containing the inline icon.



### _GetTargetRadarIcon()

- **Purpose**: Retrieves the radar icon for a target.

- **Returns**: A string containing the radar icon (always `nil`).



### _GetTargetPdaIcon(bOptional)

- **Purpose**: Retrieves the PDA icon for a target based on whether it is optional or not.

- **Parameters**:

  - `bOptional`: A boolean indicating whether the target is optional.

- **Returns**: A string containing the PDA icon.



### _GetTargetGameSpaceIcon()

- **Purpose**: Retrieves the game space icon for a target.

- **Returns**: A string containing the game space icon (always `nil`).



### _IsValidTarget(uGuid)

- **Purpose**: Determines if a target is valid.

- **Parameters**:

  - `uGuid`: The unique identifier of the target.

- **Returns**: A boolean indicating whether the target is valid (always `true`).



### DisplayTextInSatelliteMode(tObjectives, uGuid)

- **Purpose**: Displays text in satellite mode for a specific target.

- **Parameters**:

  - `tObjectives`: A table containing objectives.

  - `uGuid`: The unique identifier of the target.

- **Returns**: A string containing the text to display.



## Events



- **`Event.ObjectHibernation`**: Listens for when the object leaves hibernation and calls `Awake`.

- **`Event.ObjectDeath`**: Listens for when the object dies and calls `OnDeactivate`.

- **`Event.PlayerJoined` / `Event.PlayerLeft`**: Listens for changes in co-op player sessions.

- **`Event.TimerRelative`**: Used for timing events such as pulsating radar blips.



## Notes for modders



- **Call-order requirements**: Ensure that `Activated` is called before any other functions to properly initialize the task objective. The sequence of calling `Complete`, `Cancel`, and `Cleanup` should be maintained to ensure proper resource management.

  

- **Pitfalls**: Be cautious when modifying `_tEvents` or `_tTargets` directly, as incorrect manipulation can lead to unexpected behavior. Always use provided functions like `_SetTargetStatus` and `_ClearEventTable` to manage these tables.



- **Tunables**: Configuration settings such as `uTgtObjFilter`, `bTrackOnActivate`, `sTgtLabelFilter`, `vTgtInclude`, `vTgtExclude`, and display settings can be adjusted through the configuration system. Ensure that any changes are compatible with the game's logic.



- **Decompiler artifacts**: The function `_compare` is a decompiler artifact and does not have any intentional behavior in this context. It appears to be a placeholder or an unused local variable.