---
title: MrxSupportCopterDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, delivery, helicopter]
verified: true
verified_note: 'deeper pass: corrected Events section (DesignationCallback is the MrxSupport framework hook, not an event; real subscriptions are ObjectHibernation/ObjectInSeat + a persistent 3s CheckEwan timer), noted _WaitCallback is a dead empty stub, confirmed this is the Heli-type catalog delivery for ~21 flyable helicopters; all functions re-confirmed'
---

# MrxSupportCopterDelivery

*Module: mrxsupportcopterdelivery.lua*

## Overview
The `MrxSupportCopterDelivery` module delivers a **flyable helicopter** to the player's designated point:
Ewan flies the ordered heli in, lands it, exits, walks off and fades out, leaving the vehicle for the player
to take. It inherits from [`MrxSupport`](mrxsupport). This is the delivery type behind every `Heli`-category
catalog item in [`MrxSupportData`](mrxsupportdata) (~21 helicopters) — the catalog just calls
`SetDeliveryVehicle("<template> (Ewan)")` on each.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: `MrxSupportManager`, [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke), `MrxUtil`, `MrxVoSequence`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oTarget`: The target location for the delivery.
- `sDeliveryVehicle`: The type of vehicle to be delivered (helicopter).
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sFinalDestination`: The final destination point after landing.
- `oDesignator`: The designator object used for marking the drop zone.
- `uOwnerGuid`: The GUID of the owner of the support operation.
- `DamageEvent`: Event handle for damage detection on the helicopter.
- `LandGoal`: AI goal for landing the helicopter.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the helicopter delivery operation. Initializes the designator with blue smoke and sets the recruit to "Copter".

### `DesignationCallback(self)`
Called when the designator is used. Spawns the helicopter at a calculated position near the camera, sets its orientation towards the target, and starts a voice sequence.

### `_WaitCallback(self, uHeli)`
An empty stub — defined but with no body, and not referenced anywhere in this file (the actual "heli is
awake" work is done by `_HeliReady`). Dead code left over from the shared delivery pattern.

### `_HeliReady(self, uHeli)`
Called when the helicopter is spawned and ready. Adds it to the disposer, sets up damage detection, and creates an AI goal for landing the helicopter at the designated target.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point after the helicopter lands.

### `_VehicleLanded(self, uHeli, uDriver, nState)`
Called when the helicopter lands. Handles the outcome of the landing (success or failure), refunds costs if necessary, and sets up the AI behavior for Ewan to exit the vehicle and fade out.

### `ExitedVehicle(self, uDriver)`
Called when Ewan exits the vehicle. Starts a voice sequence, creates an event to remove Ewan after hibernation, and makes the recruit available again in the support manager.

### `CheckEwan(self, uDriver)`
Checks if Ewan is still visible. If not, removes him and deletes associated events.

## Events
Confirmed from source. `DesignationCallback` is **not** an event — it's the [`MrxSupport`](mrxsupport)
framework hook (called once the target is designated), and it's where the heli is spawned (server-only, via
`Net.IsClient()` guard).

- **`Event.ObjectHibernation`** — `"awake"` (heli ready → `_HeliReady`) and, in `ExitedVehicle`,
  `"Hibernated"` on the driver → `Object.Remove`.
- **`Event.ObjectInSeat`** (`"D","X"`) — fires `ExitedVehicle` when Ewan leaves the driver seat.
- **`Event.ObjectDelete`** (on the driver) — frees the `"Copter"` recruit via
  `MrxSupportManager.MakeRecruitAvailable`.
- **`Event.CreatePersistent(Event.TimerRelative, {3}, CheckEwan, ...)`** — a 3-second repeating check that
  removes Ewan if he's no longer visible (stored as `self.Timer`, cleaned up in `CheckEwan`).

Damage handling during the flight comes from the inherited `MrxSupport.SetupDamageEvent` (`self.DamageEvent`).

## Notes for modders
- **On failed landing (`nState == 0`) the cost is refunded** — `_VehicleLanded` calls `self:RefundCosts()`
  and sends the heli home, so a denied delivery doesn't cost the player. Worth knowing if you rework the
  landing gate.
- **Recruit gating**: `Create` sets recruit `"Copter"`; the delivery frees it again on `Event.ObjectDelete`
  of Ewan. If Ewan gets stuck, the `CheckEwan` 3s timer is the cleanup safety net.
- Customize Ewan's delivery/exit VO via the `tVo` table in `ExitedVehicle`.
- **`_WaitCallback` is dead** (empty stub) — don't wire logic into it expecting it to run.