---
title: MrxMunitionsPickup
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [pickup, transit]
verified: true
verified_note: 'deeper pass: rewrote Events section (real Event.ScriptEvent/ObjectDeath/ObjectHibernation subscriptions, not "custom events"), flagged bPickupInProgress/tImmediatePickupData as module-level globals not per-instance state, added the green-smoke designator + Copter recruit constants; all functions re-confirmed'
---

# MrxMunitionsPickup

*Module: mrxmunitionspickup.lua*

## Overview
The `MrxMunitionsPickup` module is responsible for handling the pickup of tagged munitions by a heli. It inherits from `MrxSupport` and manages the spawning, targeting, and retrieval of munitions by a designated vehicle. The module also handles voice-over sequences and faction infraction logic when munitions are picked up.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `Munitions`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oTarget`: The target for the pickup operation.
- `sDeliveryVehicle`: The name of the vehicle template used for delivery.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `oUpdateEvent`: An event handle for periodic updates.
- `oDesignator`: a [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) set to **green** smoke, AA test
  level `"none"`, and a `nil` validation function (any target accepted). Recruit type is `"Copter"`.
- `oFinalDestination`: The final destination point for the pickup operation.
- Per-designation event handles: `oNoMunitionsScriptEvent`, `oMunitionsKilledEvent`,
  `oMunitionsSleepEvent`, `oUntagScriptEvent` — created in `_WaitCallback`/`PickMunitionsTarget`, deleted in
  `Pickup`/`ImmediatePickup`.

{: .warning }
> **`bPickupInProgress` and `tImmediatePickupData` are module-level globals, not per-`self` fields.** Both
> are declared at file scope and read/written by bare name (not through `self`), so they are shared across
> every munitions-pickup object. `tImmediatePickupData` even caches a `self` reference so the free-function
> `ImmediatePickup()` (which takes no arguments) can reach back into the active pickup. This works only
> because at most one munitions pickup is ever in flight — it is not safe for concurrent pickups.

## Functions
### `Create(self, uOwnerGuid)`
Creates a new per-instance table for the object using the module's prototype. Initializes the delivery vehicle and designator settings.

### `DesignationCallback(self)`
A callback function that handles designation events.

### `SetDeliveryVehicle(self, sVehicleTemplateName)`
Sets the delivery vehicle template name and updates the GUID accordingly.

### `SetFinalDestination(self, oFinalDestination)`
Sets the final destination point for the pickup operation.

### `_DesignatorCallback(self)`
Handles the designator callback logic, spawning the delivery vehicle at the designated target position and setting its orientation.

### `_WaitCallback(self, uHeli)`
Called after the heli wakes up. Starts a voice-over sequence, sets up damage event handling, and begins picking up munitions.

### `PickMunitionsTarget(self, uHeli)`
Detaches cargo from the winch, gets tagged munitions, and sets up events to handle various scenarios (e.g., no munitions, untagged munitions).

### `ImmediatePickup()`
A free function (no `self` parameter) that force-completes an in-progress pickup: it no-ops unless
`bPickupInProgress` and there's still a tagged munition, then calls `Munitions.PickupAllMunitions()`,
deletes the four per-pickup events via the cached `tImmediatePickupData.self`, fades out the heli (and any
winched target), frees the `"Copter"` recruit, and resets the module globals. Reaches its target object
entirely through the module-level `tImmediatePickupData` table — see the warning above.

### `Pickup(self, uHeli, uDriver, pu, nState)`
Handles the actual pickup of munitions. Updates faction infraction, picks up all tagged munitions, and returns the heli to its home position.

## Events
Confirmed from source — all one-shot registrations tied to a specific pickup. `DesignationCallback` is
**not** an event; it's the framework hook called by [`MrxSupport`](mrxsupport) and it just forwards to the
plain function `_DesignatorCallback`.

- **`Event.ObjectHibernation`** (`"awake"`) — waits for the spawned heli to wake, then runs `_WaitCallback`.
- **`Event.ScriptEvent`** `"NoMunitions"` — if the game posts this, calls `MrxSupport.Abort(self, uHeli,
  "NoMunitions")`.
- **`Event.ScriptEvent`** `"UntagMunitions"` (filtered to the current target `self.pu`) — if the target is
  un-tagged mid-run, re-picks a new target via `PickMunitionsTarget`.
- **`Event.ObjectDeath`** (on `self.pu`) and **`Event.ObjectHibernation`** (`"hibernated"`, on `self.pu`) —
  if the current target munition dies or sleeps, re-run `PickMunitionsTarget`.

Damage abort comes from the inherited `MrxSupport.SetupDamageEvent` (aborts if the heli drops below 60%
health — see [`MrxSupport`](mrxsupport)).

## Notes for modders
- **`SetDeliveryVehicle`/`SetFinalDestination`** configure the heli and where it returns; the module-level
  default vehicle is `"UH1 Transport (PMC) (Driver)"`.
- **This is a mission/freebie support type, not a purchasable catalog entry** — [`MrxSupportData`](mrxsupportdata)
  wires two `tFreebieData` instances of it (`GurCon001_Munitions`, `MunitionsPickup`), each with a fixed
  delivery vehicle + faction HQ landing zone.
- **Faction infraction**: `Pickup` adds `+5` infraction (via `Ai.AddInfraction`) against the picked-up
  munition's faction, for each local player character — grabbing another faction's dropped ordnance is a
  hostile act.
- Customize the "on the way" VO by editing the `tVO` table in `_WaitCallback`.
- **`bPickupInProgress`/`tImmediatePickupData` are shared module globals** (see the Instance-pattern
  warning) — don't build logic that assumes two pickups can run at once.