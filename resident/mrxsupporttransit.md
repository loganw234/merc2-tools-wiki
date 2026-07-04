---
title: MrxSupportTransit
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, transit]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxSupportTransit

*Module: mrxsupporttransit.lua*

## Overview
The `MrxSupportTransit` module is responsible for managing the support transit system in the game. It handles operations such as initiating a transit, managing the heli's behavior during transit, and handling player interactions with the transit interface. The module also manages various events related to vehicle entry, exit, and death.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: 
  - `MrxSupportDesignatorSmoke`
  - `MrxSupportDesignatorFlare`
  - `MrxTransit`
  - `MrxUtil`
  - `MrxState`
  - `WifPmcInterior`
  - `MrxTutorialManager`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `sDeliveryVehicle`: The name of the delivery vehicle, set to `"UH1 Transport (Transit)"`.
- `nAltitude`: The altitude at which the heli operates, set to `250`.
- `tVOOnTheWay`: A table containing VO cues for when the transit is on the way.
- `tVOGoHome`: A table containing VO cues for when the transit goes home.
- `bTransitInterfaceActive`: A boolean flag indicating whether the transit interface is active.

## Functions

### Create(self, uPlayerGuid)
- **Description**: Creates a new support instance with the specified player GUID.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uPlayerGuid`: The unique identifier for the player.
- **Returns**: A new support instance.

### Commence(self, bFireImmediately)
- **Description**: Initiates the support operation. If the player is swimming, it switches to using a flare designator instead of smoke.
- **Parameters**:
  - `self`: The current instance of the module.
  - `bFireImmediately`: A boolean indicating whether to fire immediately.

### DesignationCallback(self)
- **Description**: Handles the designation callback for the support operation. It spawns the heli at the designated target and sets up various events for handling the transit process.
- **Parameters**:
  - `self`: The current instance of the module.

### _WaitCallback(self, uHeli)
- **Description**: A private function that waits for the heli to be spawned and sets up AI goals and events for the transit process.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.

### SetPickupVehicle(self, sVehicleTemplateName)
- **Description**: Sets the pickup vehicle template name and updates the delivery vehicle GUID accordingly.
- **Parameters**:
  - `self`: The current instance of the module.
  - `sVehicleTemplateName`: The name of the vehicle template.

### _VehicleLanded(self, uHeli, uDriver, nState)
- **Description**: Handles the event when the heli lands. It sets up an idle goal for the driver and starts a timeout event if the transit is not in water pickup mode.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uDriver`: The unique identifier for the driver.
  - `nState`: The state of the vehicle.

### _RemoveTimeoutEvent(self, uHeli, uDriver)
- **Description**: Removes the timeout event and sends the heli home if it has landed. It also deletes related events and clears messages.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uDriver`: The unique identifier for the driver.

### _OnHibernate(self, uHeli)
- **Description**: Handles the event when the heli hibernates. It cleans up resources and removes the heli from the game world.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.

### _OpenTransitInterface(self, uHeli, uDriver, uPlayer)
- **Description**: Opens the transit interface when the player boards the heli. It starts a VO sequence and sets up events for handling player exits and game events.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uDriver`: The unique identifier for the driver.
  - `uPlayer`: The unique identifier for the player.

### _PlayerExited(self, uHeli, uDriver, uPlayer)
- **Description**: Handles the event when a player exits the heli. It clears messages and sets up timeout events if necessary.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uDriver`: The unique identifier for the driver.
  - `uPlayer`: The unique identifier for the player.

### _PlayerLeftGame(self, uHeli, uDriver)
- **Description**: Handles the event when a player leaves the game. It opens the transit interface if necessary and sets up timeout events.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uDriver`: The unique identifier for the driver.

### _TransitInterfaceCallback(self, uHeli, nSelectedIndex, bSuccess)
- **Description**: Handles the callback from the transit interface. It sends a clear message event and either starts transit to the selected point or exits all players from the vehicle.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `nSelectedIndex`: The index of the selected transit point.
  - `bSuccess`: A boolean indicating whether the selection was successful.

### TransitInterfaceCallbackBriefing(self, nSelectedIndex)
- **Description**: Handles the briefing callback from the transit interface. It spawns a temporary heli and sets up events for handling the briefing process.
- **Parameters**:
  - `self`: The current instance of the module.
  - `nSelectedIndex`: The index of the selected transit point.

### _WaitCallbackBriefing(self, oSupport, uHeli, uPlayer, nSelectedIndex)
- **Description**: A private function that waits for the briefing heli to be spawned and sets up AI goals and events for handling the briefing process.
- **Parameters**:
  - `self`: The current instance of the module.
  - `oSupport`: The support instance.
  - `uHeli`: The unique identifier for the heli.
  - `uPlayer`: The unique identifier for the player.
  - `nSelectedIndex`: The index of the selected transit point.

### TransitToPoint(self, uHeli, uPoint)
- **Description**: Starts transit to the specified point. It checks if the distance between the heli and the point is greater than 15 units and then proceeds with the transit process.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uPoint`: The unique identifier for the transit point.

### _StartTransit(self, uHeli, uPoint)
- **Description**: Starts the transit process by setting the position and orientation of the heli and preparing it for transit.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uPoint`: The unique identifier for the transit point.

### _FinishTransit(self, uHeli, uPoint)
- **Description**: Finishes the transit process by setting up AI goals and events for landing the heli at the specified point.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.
  - `uPoint`: The unique identifier for the transit point.

### _FinishTransit2(self, uHeli)
- **Description**: Finishes the transit process by exiting all players from the vehicle and setting up events for handling the end of the transit.
- **Parameters**:
  - `self`: The current instance of the module.
  - `uHeli`: The unique identifier for the heli.

### NetEventCallback(eventId, tArgs)
- **Description**: Handles network events related to entering and exiting vehicles, showing and clearing messages.
- **Parameters**:
  - `eventId`: The ID of the network event.
  - `tArgs`: A table containing arguments for the event.

### AllPlayersExitVehicle(bSendEvent)
- **Description**: Exits all players from their current vehicle. It sends a network event to exit the vehicle and clears messages.
- **Parameters**:
  - `bSendEvent`: A boolean indicating whether to send an exit vehicle event.

### \_Cleanup(self)
This function is responsible for cleaning up various event handlers and resetting a module-level state variable. It deletes several events (`EnterEvent`, `ExitEvent`, `PlayerLeftEvent`, `TimeoutEvent`, `DeathEvent`, `eAbort`) using the `Event.Delete` function to prevent memory leaks or unintended behavior after these events are no longer needed. Additionally, it sets a module-level boolean `bTransitInterfaceActive` to `false` and sends a custom network event `NETEVENT_CLEARMESSAGE` to clear any messages related to support transit.

### \_HandleDeath(self)
This function handles the death of an object associated with the support transit system. It first clears the `DeathEvent` field by setting it to `nil`. Then, it calls the `_Cleanup` function to perform a full cleanup of all event handlers and reset the module-level state.

## Events

- **`OnActivate(uGuid, uRuntimeOwner, iArg)`**: This module listens for this event when a world object instance is spawned/activated. It initializes the support system by creating a new support instance with the specified player GUID.
  
- **`OnDeactivate(uGuid)`**: This module listens for this event when an instance is being torn down (despawned/unloaded). It cleans up resources and removes any associated events.

- **`OnDeath(uGuid)`**: This module listens for this event when the underlying object dies. It handles the death by calling `_HandleDeath`, which performs a full cleanup of all event handlers and resets the module-level state.

- **`OnUse(uGuid, ...)`**: This module listens for this event when the player interacts with or uses the object. It initiates the support operation by calling `Commence`.

- **`OnEnter` / `OnExit`**: These events are used to handle player or trigger volume enter/exit scenarios. They manage various aspects of the transit process, such as opening the transit interface and handling player exits.

- **`OnStateChange`**: This module listens for this event when a tracked state machine field changes. It manages the state transitions related to the support system.

- **`OnPlayerJoined` / `OnPlayerLeft`**: These events are used to handle co-op player session changes. They manage the transit interface and timeout events accordingly.

- **`Event.ObjectHibernation`**: This module listens for this event when an object hibernates. It handles the hibernation by calling `_OnHibernate`, which cleans up resources and removes the heli from the game world.

## Notes for modders

- **Call-order requirements**: Ensure that `OnActivate` is called before any other lifecycle events to properly initialize the support system. The sequence of events like `OnEnter`, `OnExit`, and `OnUse` should be respected to maintain the integrity of the transit process.
  
- **Pitfalls**: Be cautious with network events (`NetEventCallback`) as they can lead to unintended behavior if not handled correctly. Ensure that all players are properly managed during transitions, especially when exiting vehicles.

- **Tunables**: The module-level state variables such as `nAltitude` and the VO cue tables (`tVOOnTheWay`, `tVOGoHome`) can be tuned to adjust the behavior of the support system. For example, changing `nAltitude` will affect the altitude at which the heli operates.

- **Decompiler artifacts**: There are no known decompiler artifacts in this module that require special attention. All functions and variables appear to be correctly interpreted by the decompiler.