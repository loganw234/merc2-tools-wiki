---
title: MrxSupportPickup
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [pickup, support]
verified: true
verified_note: 'deeper pass: corrected Events section (ObjectInSeat is Event.ObjectInSeat not a "custom event"; DesignationCallback is the framework hook), surfaced the tCues per-faction Land/Inc/Leave VO table + tFactionToId map + the pluggable-callback set, noted the 30s auto-return timeout; all functions re-confirmed'
---

# MrxSupportPickup

*Module: mrxsupportpickup.lua*

## Overview
The `MrxSupportPickup` module manages the extraction helicopter support system: it flies an extraction heli
to a designated point, lands it, waits for a prisoner/passenger to board, and returns home. It handles
spawning, landing, destruction, and per-faction voice-over, and exposes a set of **pluggable callbacks** so
mission scripts can hook the heli's lifecycle (spawned / landed / damaged / destroyed / pilot-killed). It
inherits from [`MrxSupport`](mrxsupport). [`MrxSupportData`](mrxsupportdata) wires one instance per faction as
the `Extraction_*` freebies, and [`MrxChiCon001Rescue`](mrxchicon001rescue) subclasses it.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: `MrxSupportManager`, [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke), `MrxUtil`, `MrxTutorialManager`, `MrxVoSequence`, `MrxFactionManager`

Module constants (file scope): `sDeliveryVehicle = "UH1 Transport (PMC) (Driver)"`; `nAltitude = 250`
(declared but unused — spawn height comes from `MrxSupport.GetSpawnHeight()`); `tCues`, a per-faction table
of extraction VO cues split into `Land`/`Inc`/`Leave` sub-lists (`Allied`/`China`/`Guerilla`/`OC` full;
`Pirate`/`PMC` have only `Inc`); and `tFactionToId`, mapping engine faction names to the short IDs used for
`SetFaction` (`Allied`→`All`, `China`→`Chi`, `Guerilla`→`Gur`, `OC`→`Oil`, `Pirate`→`Pir`, `PMC`→`Pmc`,
`VZ`→`Vza`, `Civ`→`Civ`).

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
Confirmed from source. `DesignationCallback` is the [`MrxSupport`](mrxsupport) framework hook (spawns the
heli), not an event. Real subscriptions, all set up in `_WaitCallback` / `_VehicleLanded` and torn down in
`DriverExited`:

- **`Event.ObjectHibernation`** (`"awake"`) — heli wakes → `_WaitCallback`.
- **`Event.ObjectHealth`** — if a heli-damaged callback was registered, fires it once health drops by 25
  (`Object.GetHealth(uHeli) - 25`).
- **`Event.ObjectDeath`** — on the heli (heli-destroyed CB) and on the pilot (via the inherited
  `MrxSupport.SetupPilotKilledEvent`, plus an optional pilot-killed CB).
- **`Event.ObjectInSeat`** — two handles in `_VehicleLanded`: `("Prisoner", uHeli, "Any", "Enter")` →
  `MrxSupport.GoHome` (someone boarded, leave), and `("Human", uHeli, "Driver", "x")` → `DriverExited`
  (cleanup).
- **`Event.TimerRelative`** `{30}` — if nobody boards within 30s, `MrxSupport.GoHome` sends the heli back.

## Notes for modders
- **Pluggable lifecycle callbacks** are the main extension point — register with `SetHeliSpawnedCB`,
  `SetHeliLandedCB`, `SetHeliDamagedCB`, `SetHeliDestroyedCB`, `SetPilotKilledCB` (each takes `fCallback,
  tArgs`). The damaged CB fires on a 25-point health drop, not a percentage.
  {: .note }
  > Two setters have a decompiled-artifact quirk: `SetHeliSpawnedCB` and `SetHeliDamagedCB` store the args
  > table under `self.fHeliSpawnedCBArgs` / `self.fHeliDamagedCBArgs` (an `f` prefix), while `_WaitCallback`
  > reads `self.fHeliDamagedCBArgs` for the damaged case — consistent there — but the *destroyed* and
  > *pilot-killed* paths read `self.tHeliDestroyedCBArgs` / `self.tPilotKilledCBArgs`. If a callback's args
  > arrive empty, check you're setting the field name the read side expects.
- **Auto-return timeout is 30s** after landing (the `Event.TimerRelative {30}` in `_VehicleLanded`).
- **Faction is auto-derived** from the pickup vehicle: `SetPickupVehicle` looks up the vehicle's faction and
  maps it through `tFactionToId` into `SetFaction`, so choosing an Allied extraction heli tags the support
  Allied automatically.
- Extraction VO is per-faction in `tCues` (`Inc` on the way, `Land` on arrival, `Leave` on takeoff).