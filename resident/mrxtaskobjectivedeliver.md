---

title: MrxTaskObjectiveDeliver

parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1


inherits: MrxTaskObjective

tags: [task, delivery]

verified: true

verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskObjective](mrxtaskobjective) for the general mechanism.

---



# MrxTaskObjectiveDeliver



*Module: mrxtaskobjectivedeliver.lua*



## Overview

The `MrxTaskObjectiveDeliver` module is responsible for managing task objectives related to delivering specific objects or entities to designated destinations. It handles various events such as target delivery, player interactions, and winching operations to ensure that the task requirements are met.



## Inheritance

- Inherits from: `MrxTaskObjective`
- Imports: `MrxUtil`



## Instance pattern

**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields tracked via the config table:

- `sGlobalDiscCount`: A global counter used to generate unique IDs for destination blips.

- `tTargetData`: Table containing data about targets, including their GUIDs and delivery status.

- `nAttachedTargets`: Number of currently attached targets.

- `bDestinationBlipEnabled`: Boolean indicating whether the destination blip is enabled.

- `bTargetBlipsEnabled`: Boolean indicating whether target blips are enabled.

- `tConfig`: Configuration settings for the task objective, including delivery type and criteria.

```



## Functions



### Activated(self)

- **Description**: This function is called when the task objective is activated. It initializes the configuration settings, sets up events for player and target delivery, and creates delivery events based on the type of targets.

- **Parameters**:

  - `self`: The instance of the task objective.



### Cleanup(self)

- **Description**: Cleans up resources used by the task objective, such as removing destination blips and cleaning up target events.

- **Parameters**:

  - `self`: The instance of the task objective.



### _CleanupTargetEvents(self, tTargetData)

- **Description**: Cleans up events associated with a specific target.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `tTargetData`: Table containing data about the target.



### _DeliveryCheck(self, uGuid)

- **Description**: Checks if a target has been delivered based on configuration settings and updates the delivery status accordingly.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the target object.



### _TargetDelivered(self, uGuid)

- **Description**: Marks a target as delivered, cleans up associated events, removes the target from the list, and completes the part of the task.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the target object.



### _OnAttachment(self, sAttachMode, iGuid, bAttached)

- **Description**: Handles attachment status changes for targets. Updates the number of attached targets and destination blip visibility based on the new attachment status.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `sAttachMode`: Mode of attachment (e.g., "follow").

  - `iGuid`: GUID of the target object.

  - `bAttached`: Boolean indicating whether the target is attached.



### _OnStatusChange(self, sStatusType, iGuid)

- **Description**: Handles status changes for targets. Updates the number of attached targets and destination blip visibility based on the new status type.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `sStatusType`: Type of status change (e.g., "destroyed").

  - `iGuid`: GUID of the target object.



### _TargetLeftDestination(self, uGuid)

- **Description**: Handles the event when a target leaves the destination area. Sets up events to monitor when the target returns to the destination.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the target object.



### _TargetAtDestination(self, uGuid)

- **Description**: Handles the event when a target reaches the destination area. Sets up events to monitor when the target leaves the destination and checks if the target has been delivered.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the target object.



### LabelFilterDeliveryCreate(self, tConfig)

- **Description**: Creates an event for label filter delivery. This function is used when the task involves delivering a group of objects based on a label filter.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `tConfig`: Configuration settings for the delivery.



### _FilterTargetAtDestination(self, uGuid)

- **Description**: Handles the event when a target reaches the destination area based on a label filter. Adds the target to the list of targets and sets up events to monitor its status.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the target object.



### _FilterTargetLeftDestination(self, uGuid)

- **Description**: Handles the event when a target leaves the destination area based on a label filter. Cleans up associated events and removes the target from the list.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the target object.



### EnableDestinationBlip(self, bOn)

- **Description**: Enables or disables the destination blip based on the configuration settings. This function is used to visually indicate the delivery location to players.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bOn`: Boolean indicating whether to enable or disable the blip.



### EnableTargetBlips(self, bOn)

- **Description**: Enables or disables blips for all targets based on the configuration settings. This function is used to visually indicate the location of targets to players.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `bOn`: Boolean indicating whether to enable or disable the blips.



### _PlayerDeliveryCreate(self, uGuid)

- **Description**: Creates an event for player delivery. This function is used when the task involves delivering a specific player object.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the player object.



### _HumanDeliveryCreate(self, uGuid)

- **Description**: Handles the creation of events for human delivery. This function is used when the task involves delivering a specific human object.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the human object.



### _HumanDeliveryCheck(self, uGuid)

- **Description**: Checks if a human target has been delivered based on configuration settings and updates the delivery status accordingly.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `uGuid`: GUID of the human object.



### _HumanOnAttachment(self, sAttachMode, iGuid, bAttached)

- **Description**: Handles attachment status changes for human targets. Updates the number of attached targets and destination blip visibility based on the new attachment status.

- **Parameters**:

  - `self`: The instance of the task objective.

  - `sAttachMode`: Mode of attachment (e.g., "follow").

  - `iGuid`: GUID of the human object.

  - `bAttached`: Boolean indicating whether the target is attached.



### _MarkAttachedHuman(self, uGuid, bEnable)

- **Description**: Marks a human target with a visual marker and radar objective.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target object.

  - `bEnable`: A boolean indicating whether to enable or disable the marker.



### _ObjectDeliveryCreate(self, uGuid)

- **Description**: Sets up event listeners and initializes delivery state for an object.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target object.



### _ObjectDeliveryCheck(self, uGuid)

- **Description**: Checks if an object is ready for delivery based on winch status.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target object.

- **Returns**: A boolean indicating whether the object is ready for delivery.



### _VehicleDeliveryCreate(self, uGuid)

- **Description**: Sets up event listeners and initializes delivery state for a vehicle.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target vehicle.



### _VehicleDeliveryCheck(self, uGuid)

- **Description**: Checks if a vehicle is ready for delivery based on player presence and winch status.

- **Parameters**:

  - `self`: The instance of the module.

  - `uGuid`: The unique identifier of the target vehicle.

- **Returns**: A boolean indicating whether the vehicle is ready for delivery.



### _OnObjectWinched(self, uObject, uWincher, sState)

- **Description**: Handles the event when an object is winched.

- **Parameters**:

  - `self`: The instance of the module.

  - `uObject`: The unique identifier of the object being winched.

  - `uWincher`: The unique identifier of the wincher.

  - `sState`: A string indicating the state of the winching ("attach" or "detach").



### _OnPlayerInVehicle(self, uPlayerChar, uVehicle, sSeatType, uSeat, sAction)

- **Description**: Handles the event when a player enters or exits a vehicle.

- **Parameters**:

  - `self`: The instance of the module.

  - `uPlayerChar`: The unique identifier of the player character.

  - `uVehicle`: The unique identifier of the vehicle.

  - `sSeatType`: A string indicating the type of seat.

  - `uSeat`: The unique identifier of the seat.

  - `sAction`: A string indicating the action ("enter" or "exit").



### _GetShortDescription()

- **Description**: Returns a short description of the objective.

- **Returns**: A string representing the short description.



### GetInlineIcon(self)

- **Description**: Retrieves the inline icon for the objective based on its configuration.

- **Parameters**:

  - `self`: The instance of the module.

- **Returns**: A string representing the inline icon.



### _GetTargetRadarIcon()

- **Description**: Returns the radar icon for a target.

- **Returns**: A string representing the radar icon.



### _GetTargetPdaIcon(bOptional)

- **Description**: Retrieves the PDA icon for a target based on its optional status.

- **Parameters**:

  - `bOptional`: A boolean indicating whether the target is optional.

- **Returns**: A string representing the PDA icon.



### _GetTargetGameSpaceIcon()

- **Description**: Returns the game space icon for a target.

- **Returns**: A string representing the game space icon.



### _GetDestinationRadarIcon()

- **Description**: Returns the radar icon for a destination.

- **Returns**: A string representing the radar icon.



### _GetDestinationPdaIcon(bOptional)

- **Description**: Retrieves the PDA icon for a destination based on its optional status.

- **Parameters**:

  - `bOptional`: A boolean indicating whether the destination is optional.

- **Returns**: A string representing the PDA icon.



### _GetDestinationGameSpaceIcon()

- **Description**: Returns the game space icon for a destination.

- **Returns**: A string representing the game space icon.



### _IsValidTarget(uGuid)

- **Description**: Checks if a given target is valid based on its GUID.

- **Parameters**:

  - `uGuid`: The unique identifier of the target object.

- **Returns**: A boolean indicating whether the target is valid.



### NetEventCallback(nEventType, tArgs)

- **Description**: Handles network events related to delivery objectives.

- **Parameters**:

  - `nEventType`: An integer representing the type of event.

  - `tArgs`: A table containing arguments for the event.



## Events



- **`OnActivate(uGuid, uRuntimeOwner, iArg)`**: This module listens for this event to initialize the task objective when it is activated.

- **`OnDeactivate(uGuid)`**: This module listens for this event to clean up resources and deactivate the task objective.

- **`OnDeath(uGuid)`**: This module listens for this event to handle the death of a target object, which may trigger cleanup or status updates.

- **`OnUse(uGuid, ...)`**: This module listens for this event if there are specific interactions with the task objective that need handling.

- **`OnEnter` / `OnExit`**: These events are not explicitly mentioned but could be used to handle player or trigger volume enter/exit related to the delivery task.

- **`OnStateChange`**: This module listens for state changes in targets, such as attachment status or winch state, to update delivery status accordingly.

- **`OnPlayerJoined` / `OnPlayerLeft`**: These events are not explicitly mentioned but could be used to handle player session changes affecting the delivery task.

- **`Event.ObjectWinched`**: This module listens for this event to handle when an object is winched, which may affect its delivery status.

- **`Event.PlayerInVehicle`**: This module listens for this event to handle when a player enters or exits a vehicle, which may affect vehicle delivery checks.



## Notes for modders



1. **Call-order requirements**: Ensure that the `Activated` function is called before any other functions to properly initialize the task objective.

2. **Pitfalls**: Be cautious with enabling and disabling blips as it can affect player visibility of targets and destinations. Always ensure that cleanup functions are called when deactivating or deleting the task objective to avoid memory leaks or resource conflicts.

3. **Tunables**: The module uses configuration settings for various behaviors, such as delivery checks and blip visibility. Modifying these settings can change how the task behaves in-game.

4. **Decompiler artifacts**: There are no known decompiler artifacts affecting the functionality of this module. All functions and variables appear to be used correctly within the context of the script.