---
title: MrxSupportPickup
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [pickup, support]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxSupportPickup

*Module: mrxsupportpickup.lua*

## Overview
The `MrxSupportPickup` module manages the extraction helicopter support system in the game. It handles the spawning, landing, and destruction of the extraction heli, as well as managing voice-over cues for different factions. The module also supports pluggable callbacks for various events related to the heli's lifecycle.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `MrxUtil`, `MrxTutorialManager`, `MrxVoSequence`, `MrxFactionManager`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oTarget`: The target for extraction.
- `sDeliveryVehicle`: The template name of the delivery vehicle (extraction helicopter).
- `uDeliveryVehicle`: The GUID of the spawned extraction helicopter.
- `sFinalDestination`: The final destination point for the extraction.
- `oDesignator`: The designator object used to mark the extraction target.
- `fHeliDestroyedCB`, `tHeliDestroyedCBArgs`: Callback and arguments for when the heli is destroyed.
- `fPilotKilledCB`, `tPilotKilledCBArgs`: Callback and arguments for when the pilot is killed.
- `fHeliLandedCB`, `tHeliLandedCBArgs`: Callback and arguments for when the heli lands.
- `fHeliSpawnedCB`, `tHeliSpawnedCBArgs`: Callback and arguments for when the heli spawns.
- `fHeliDamagedCB`, `tHeliDamagedCBArgs`: Callback and arguments for when the heli is damaged.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new instance of the extraction support system. Initializes the delivery vehicle, sets up the designator, and assigns the owner GUID.

### `DesignationCallback(self)`
Handles the callback when the target is designated. Spawns the extraction helicopter at the designated location, sets its orientation, and plays a voice-over cue based on the faction.

### `SetHeliDestroyedCB(self, fCallback, tArgs)`
Sets a callback function to be called when the heli is destroyed. The callback receives the arguments specified in `tArgs`.

### `SetPilotKilledCB(self, fCallback, tArgs)`
Sets a callback function to be called when the pilot is killed. The callback receives the arguments specified in `tArgs`.

### `SetHeliLandedCB(self, fCallback, tArgs)`
Sets a callback function to be called when the heli lands successfully. The callback receives the arguments specified in `tArgs`.

### `SetHeliSpawnedCB(self, fCallback, tArgs)`
Sets a callback function to be called when the heli spawns. The callback receives the arguments specified in `tArgs`.

### `SetHeliDamagedCB(self, fCallback, tArgs)`
Sets a callback function to be called when the heli is damaged. The callback receives the arguments specified in `tArgs`.

### `_WaitCallback(self, uHeli)`
Handles the callback after the heli has spawned and waits for it to land or be destroyed. Sets up damage and death events for the heli and pilot.

### `SetPickupVehicle(self, sVehicleTemplateName)`
Sets a new vehicle template name for the extraction helicopter. Updates the delivery vehicle GUID and faction ID accordingly.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point for the extraction. This is used to determine where the heli should return after completing its mission.

### `_VehicleLanded(self, uHeli, uDriver, nState)`
Handles the callback when the heli lands. Sets up idle roles for the driver and pilot, starts a timeout event, and plays a voice-over cue if the landing was successful.

### `DriverExited(self, uGuid, uDriver)`
Handles the callback when the driver exits the helicopter. Cleans up any events and callbacks associated with the heli and pilot.

## Events
- Listens for `Event.ObjectHibernation` to call `_WaitCallback` after the heli leaves hibernation.
- Listens for custom event `ObjectInSeat` to handle the exit of the driver from the helicopter.
- Listens for `Event.ObjectDeath` to handle the destruction of the heli or pilot.

## Notes for modders
- Ensure that callbacks are set up correctly using `SetHeliDestroyedCB`, `SetPilotKilledCB`, etc., to handle specific events in the extraction process.
- Customize the delivery vehicle and final destination by calling `SetPickupVehicle` and `SetFinalDestination`.
- Be aware of faction-specific voice-over cues, which can be modified or extended for different factions.
- The module uses pluggable callbacks, allowing modders to extend or override default behavior.