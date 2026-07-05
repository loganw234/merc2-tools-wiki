---

title: MrxTaskObjectiveDeliver

parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1


inherits: MrxTaskObjective

tags: [task, delivery]

verified: true

verified_note: deeper pass — REPLACED a fabricated Events section (OnActivate/OnDeactivate/OnDeath/OnUse/OnEnter/Event.PlayerInVehicle none exist) with the real events (ObjectDeath, ObjectProximity, Boundary, HumanStateTransition, ObjectWinched, ObjectInSeat, ScriptEvent); corrected imports (MrxFollow/MrxUtil/MrxTutorialManager); surfaced config tunables (fDist default 5, bStop, bDetach, bUseDestRing, bHumansFollow, vDestLoc/vDestRegion) and NETEVENT_* codes

---



# MrxTaskObjectiveDeliver



*Module: mrxtaskobjectivedeliver.lua*



## Overview

The `MrxTaskObjectiveDeliver` module is responsible for managing task objectives related to delivering specific objects or entities to designated destinations. It handles various events such as target delivery, player interactions, and winching operations to ensure that the task requirements are met.



## Inheritance

- Inherits from: [`MrxTaskObjective`](mrxtaskobjective)
- Imports: [`MrxFollow`](mrxfollow), `MrxUtil`, [`MrxTutorialManager`](mrxtutorialmanager)



## Instance pattern

**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page). Real per-instance fields used here:

- `self._tTargets[uGuid]` — inherited target table, extended with delivery bookkeeping per target
  (`oFollower`, `tEvents`, `bAtDestination`, `bWinched`, `bPlayerInVehicle`, `bIsLabelFilter`, `uMarker`).

- `self._iNumAttached` — count of targets currently "attached" (following/winched/ridden); drives when the
  destination blip turns on.

- `self.uRing` — the [`Marker`](../namespaces/marker) disc drawn around the destination when
  `bUseDestRing` is set; `self.discCount` its slot id.

{: .warning }
> `sGlobalDiscCount = 1` is a **module-level global**, not a per-instance field — it is a shared counter
> (wrapping at `8192`) for destination-ring ids across *all* live deliver objectives. `NETEVENT_EXITVEHICLE`
> / `NETEVENT_UNWINCH` / `NETEVENT_CLEARTUTORIAL` are likewise module globals (`0`/`1`/`5`).



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

All are `Event.Create` / `Event.CreatePersistent`, chosen per target kind. Which fire depends on the target
(player / human / vehicle / object / label filter):

- **`Event.ObjectDeath`** (persistent, on the target filter) → an inline handler or `_OnStatusChange` with
  `"destroyed"` — cancels delivery when the carried target dies.

- **`Event.ObjectProximity`** (`vDestLoc`) / **`Event.Boundary`** (`vDestRegion`) → `_TargetAtDestination`
  / `_TargetLeftDestination` / `_TargetDelivered` — the core "did it reach the drop-off?" test.

- **`Event.HumanStateTransition`** (`"*"` → `"subdued.idle"`) → `_OnStatusChange` `"subdued"` — a followed
  human being knocked out.

- **`Event.ObjectWinched`** (persistent) → `_OnObjectWinched` — track/attach state for winched cargo.

- **`Event.ObjectInSeat`** → `_OnPlayerInVehicle` — whether a player is still in the delivered vehicle.

- **`Event.ScriptEvent`** (`"mpPlayerLeft"`) → re-fires `_OnPlayerInVehicle` when a remote player drops out
  of a target vehicle in co-op.

{: .warning }
> A previous version of this page listed `OnActivate`/`OnDeactivate`/`OnDeath`/`OnUse`/`OnEnter`/`OnExit`/
> `OnStateChange`/`OnPlayerJoined`/`OnPlayerLeft` and `Event.PlayerInVehicle` here. **None of those exist in
> this file** — they were fabricated. The real events are the ones listed above.

`NetEventCallback(nEventType, tArgs)` is the module's custom-net handler (`NETEVENT_EXITVEHICLE`/`UNWINCH`/
`CLEARTUTORIAL`) driving the "[objective.Deliver.*]" tutorial hints via
[`MrxTutorialManager`](mrxtutorialmanager) — not an engine event subscription.

## Notes for modders

- **Destination is `vDestLoc` (a point, default proximity `fDist = 5`) or `vDestRegion` (a boundary
  volume).** Label-filter deliveries (many objects, filtered by label) require a `vDestLoc` — delivering a
  label filter to a *region* is explicitly unsupported (logs `"WARNING: Cannot deliver label filter to
  region"`).

- **Key config toggles** (all via `MrxUtil.SetDefault`): `bStop` (must be stationary to count, default
  `true`), `bDetach` (default = `bStop`), `bXZOnly` (ignore height, default `false`), `bUseDestRing` (draw a
  ground ring at the drop, default on when `bStop` and `vDestLoc`), `bHumansFollow` (escorted humans follow
  the player, default `true`), `bDisplayHelpText` (tutorial nudges like "unwinch"/"exit vehicle", default
  `true`).

- **Delivering different target types takes different paths**: humans get an [`MrxFollow`](mrxfollow)
  escort; vehicles must have the player *out* to count (`_VehicleDeliveryCheck`); winched objects must be
  *un*winched (`_ObjectDeliveryCheck`). Wrong-state deliveries show the matching
  `"[objective.Deliver.vehicleExit]"` / `"[objective.Deliver.winch]"` hint instead of completing.

- Destination blip art reuses the base action icons for the *carried* target and a distinct set for the
  *destination* (`_GetDestinationRadarIcon` → `"objective_deliverable"`, world
  `"HUD_objective_deliverable"`, PDA `"icon_deliverable_1_mc"`/`"_2_mc"`).