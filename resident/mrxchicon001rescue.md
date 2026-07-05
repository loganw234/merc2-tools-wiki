---
title: MrxChiCon001Rescue
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportPickup
tags: [support, rescue]
verified: true
verified_note: 'deeper pass: rewrote Events section (real Event.TimerRelative/ObjectInSeat subscriptions; DesignationCallback/_WaitCallback/_VehicleLanded are framework hook + Ai callbacks, not "custom events"), documented the 60m prisoner-collect radius, ValidateLandingZone validation, and that it overrides its parent DesignationCallback rather than reusing it; all functions re-confirmed'
---

# MrxChiCon001Rescue

*Module: mrxchicon001rescue.lua*

## Overview
The `MrxChiCon001Rescue` module is a mission-specific rescue-copter support: it flies a heli to a designated
landing zone, lands, and extracts any **prisoners** within 60m (ordering them to board), then flies them
home. It subclasses [`MrxSupportPickup`](mrxsupportpickup) but **overrides** its parent's
`DesignationCallback`/`_WaitCallback`/`_VehicleLanded` with rescue-specific versions (prisoner collection
instead of the parent's generic pickup). It's added to the support menu by its own `AddSupport`, not through
the [`MrxSupportData`](mrxsupportdata) catalog.

## Inheritance
- Inherits from: [`MrxSupportPickup`](mrxsupportpickup)
- Imports: `MrxChiCon001Rescue`, `MrxVoSequence`

## Instance pattern
**Same class-factory pattern as [`MrxSupportPickup`](mrxsupportpickup)/[`MrxSupport`](mrxsupport), not
per-`uGuid`** — `Create(oSelf, uOwnerGuid)` builds a new table via `setmetatable`/`__index`, exactly like
its parent chain. No `OnActivate`/`Awake`, no `tInstance` registry. It tracks the following key fields:
- `oTarget`: The target for the rescue operation.
- `sDeliveryVehicle`: The name of the delivery vehicle (rescue helicopter).
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `oDesignator`: The designator object used to mark the landing zone.

## Functions
### `Create(oSelf, uOwnerGuid)`
Creates a new per-instance table for the rescue support pickup. Initializes the target, sets up the delivery vehicle, and configures the designator with validation functions.

### `AddSupport()`
Adds the rescue copter option to the player's support menu. Iterates through all players and adds an item to their "Support Menu" widget.

### `RemoveSupport()`
Removes the rescue copter option from the player's support menu. Iterates through all players and removes the "Rescue Copter" item from their "Support Menu" widget.

### `DesignationCallback(oSelf)`
Handles the designation callback when a landing zone is marked. Spawns the rescue helicopter at the designated location, sets its orientation, plays a voice sequence, and waits for it to land.

### `_WaitCallback(oSelf, uHeli)`
A helper function that creates an AI goal for the helicopter to land at the designated target location.

### `_VehicleLanded(oSelf, uHeli, uDriver, nState)`
Runs when the `HeliLand` order completes. On failure (`nState == 0`) it denies (`abortnodrop`) and sends the
heli home. On success it idles the driver, collects `"Prisoner"` humans within `60`m
(`Pg.FastCollectHumans`), and for each orders `Role = "Idle"` then an `Enter`/`Passenger` `Ai.Goal` into the
heli. It then registers an `Event.ObjectInSeat` (`"Prisoner", uHeli, "Any", "Enter"`) that calls
[`MrxSupport`](mrxsupport)`.GoHome` once a prisoner is aboard.

## Events
Confirmed from source — `DesignationCallback`, `_WaitCallback`, and `_VehicleLanded` are the framework hook
and `Ai.Goal` callbacks, not events:

- **`Event.TimerRelative`** `{2}` — in `DesignationCallback`, a 2-second delay after spawn/VO before
  `_WaitCallback` issues the landing order.
- **`Event.ObjectInSeat`** (`"Prisoner", uHeli, "Any", "Enter"`) — in `_VehicleLanded`, sends the heli home
  when a prisoner boards.

The designator uses `MrxSupportDesignator.ValidateLandingZone` (set in `Create`), so the target must be a
valid landing spot. Note `DesignationCallback` uses the module-level `nAltitude` inherited from
[`MrxSupportPickup`](mrxsupportpickup) for its spawn-height fallback.

## Notes for modders
- **`AddSupport`/`RemoveSupport`** add/remove the "Rescue Copter" menu item for all players — this module is
  wired in by mission script, not by the catalog.
- **Extraction radius is `60`m** and it targets the `"Prisoner"` label specifically (in `_VehicleLanded`) —
  change either to alter who gets rescued.
- Change the rescue heli via `sDeliveryVehicle` (set on the prototype before `Create`), and the incoming VO
  is the hardcoded `"Ewan-None-Freeplay-Support-28"` cue in `DesignationCallback`.