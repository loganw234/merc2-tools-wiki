---
title: MrxSupportTransit
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, transit]
verified: true
verified_note: 'deeper pass: rewrote the Events section (the old one listed ~9 On* lifecycle callbacks -- OnActivate/OnDeactivate/OnDeath/OnUse/OnEnter/OnExit/OnStateChange/OnPlayerJoined/OnPlayerLeft -- none of which exist in source; this is a class-factory module with only real Event.* subscriptions), pruned the matching "ensure OnActivate is called" boilerplate, and surfaced the NETEVENT_* constants + bUnrestrictedByFuel + timeout tunables'
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
- `sDeliveryVehicle`: The name of the delivery vehicle, module-level default `"UH1 Transport (Transit)"`.
- `bUnrestrictedByFuel`: set `true` in `Create` — this is the only support type in the category that
  bypasses the fuel check in [`MrxSupportManager.CompleteDesignation`](mrxsupportmanager) (calling for a
  ride home is free).
- `bWaterPickup`: set per-designation in `DesignationCallback` (true if the owning character is swimming) —
  switches the heli from a `HeliLand` goal to a `MoveTo` hover-pickup and skips the seat-enter/exit events.
- Per-designation event handles: `EnterEvent`/`ExitEvent`/`PlayerLeftEvent`/`TimeoutEvent`/`DeathEvent`/
  `HibernateEvent`/`eAbort`/`uIdleGoal` — all created in `_WaitCallback`/`_VehicleLanded` and torn down by
  `_Cleanup`.

{: .warning }
> **`bTransitInterfaceActive` is a module-level global, not per-instance state.** It's declared at file
> scope (`bTransitInterfaceActive = false`) and read/written directly by name — never through `self` — so
> a single flag is shared across every transit object. In practice only one transit is ever in flight, but
> don't assume it's isolated per delivery.

Module constants (file scope): `nAltitude = 250` (unused in this file — spawn height actually comes from
`MrxSupport.GetSpawnHeight()`); `tVOOnTheWay`/`tVOGoHome` (local Ewan freeplay-support cue lists);
the net-event ID constants `NETEVENT_ENTERVEHICLE = 0`, `NETEVENT_EXITVEHICLE = 1`,
`NETEVENT_SHOWMESSAGE = 2`, `NETEVENT_CLEARMESSAGE = 3`.

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

Confirmed directly from source. **There are no `On*` engine-lifecycle callbacks in this file** (an earlier
version of this page listed `OnActivate`/`OnDeactivate`/`OnDeath`/`OnUse`/`OnEnter`/`OnExit`/`OnStateChange`/
`OnPlayerJoined`/`OnPlayerLeft` — none of those functions exist here). Like the rest of the category this is
a [`MrxSupport`](mrxsupport) class-factory object; everything is a one-shot `Event.Create`/
`Event.CreatePersistent` tied to a specific in-flight heli, set up in `_WaitCallback` and cleared in
`_Cleanup`:

- **`Event.ObjectHibernation`** — waits for the spawned heli to wake (`DesignationCallback` →
  `_WaitCallback`); and a `"hibernated"` handle firing `_OnHibernate` to clean up + remove the heli.
- **`Event.ObjectInSeat`** (persistent) — two handles, `"a"/"e"` (any seat, enter → `_OpenTransitInterface`)
  and `"a"/"x"` (any seat, exit → `_PlayerExited`), on the landed heli.
- **`Event.ObjectDeath`** — on the heli, firing `_HandleDeath` (which calls `_Cleanup`).
- **`Event.TimerRelative`** — the auto-return timeouts (`45`s after landing in `_VehicleLanded`; `10`s after
  the last player exits) and short VO/return delays.
- **`Event.ScriptEvent`** `"mpPlayerLeft"` (persistent) — co-op teardown, firing `_PlayerLeftGame`.

`NetEventCallback(eventId, tArgs)` is the receiver for this module's own `Net.SendCustomEvent(
"MrxSupportTransit", ...)` traffic (dispatched by module name, not via `Event.*`), handling the four
`NETEVENT_*` IDs listed above — enter/exit the secondary player's vehicle and show/clear the client transit
tutorial message.

## Notes for modders

- **Free rides**: `bUnrestrictedByFuel = true` is set in `Create`, so transit ignores the fuel gate that
  every other support type respects — see [`MrxSupportManager.CompleteDesignation`](mrxsupportmanager).
- **Water pickup vs. land**: if the owning character is swimming when they designate, `bWaterPickup` flips
  the whole sequence to a hovering `MoveTo` pickup (no landing, no seat events) — test both paths if you
  change the spawn/land logic.
- **Timeouts to tune**: the heli waits `45`s on the ground after landing before auto-returning
  (`_VehicleLanded`), or `10`s after the last player leaves it (`_PlayerExited`/`_PlayerLeftGame`). Both are
  plain `Event.TimerRelative` literals.
- **`bTransitInterfaceActive` is a shared module global**, not per-`self` — see the warning in Instance
  pattern before relying on it in a multi-transit scenario.
- **`nAltitude = 250` is dead here** — spawn height comes from `MrxSupport.GetSpawnHeight()` (250 with a
  co-op secondary character present, else 50), not this constant.