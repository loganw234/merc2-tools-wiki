---
title: MoonPatrol
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, ai]
verified: true
verified_note: deeper pass — re-confirmed the Deactivated/Activated undefined-callback bug, all Event.* references, and the dual table/non-table tEvents handling; added a tunables block surfacing the turbo particle template, exhaust attach points, jump impulse, 1.5s timer, and 10-unit reactivation radius, plus namespace cross-links.
---

# MoonPatrol

*Module: moonpatrol.lua*

## Overview
The `MoonPatrol` module manages the behavior of a moon patrol vehicle in the game. It handles events related to the vehicle's activation, deactivation, and player interaction, including jump mechanics and visual effects.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
No `inherit()` call and no `getfenv():Create()` anywhere in source — despite tracking per-object state,
this **isn't** the `Inheritable`-style per-instance pattern used elsewhere in `Vehicles`. It's a flat
module that manually keys its own state by `uGuid` instead (same style as `alarm.lua`):
- `tEvents[uGuid]`: A table of event handles per vehicle instance, managed by hand rather than via a
  prototype-based instance object.
- `NETEVENT_STARTEMITTERS` and `NETEVENT_STOPEMITTERS`: Constants for network events related to starting and stopping emitters.

## Functions
### `NetEventCallback(eventId, tArgs)`
Handles custom network events. It starts or stops emitters based on the event ID.

### `Init()`
Initializes the module by setting up an empty table for storing event handles.

### `Deinit()`
Deinitializes the module by clearing the event handles table.

### `OnActivate(uGuid, args)`
Called when the vehicle instance is activated. It triggers the `OnExit` function immediately.

### `OnDeath(uGuid)`
Called when the vehicle's underlying object dies. It deactivates the vehicle instance.

### `OnDeactivate(uGuid, args)`
Called when the vehicle instance is deactivated (also called directly by `OnDeath`). Reads
`tEvents[uGuid]`: if it's a table, iterates and deletes every handle in it with `pairs`; otherwise (a
single non-table handle, as `Deactivated` stores) calls `Event.Delete` on it directly. Either way, clears
`tEvents[uGuid]` afterward.

### `OnEnter(uDriver, uGuid)`
Called when a player enters the vehicle's seat. It sets up events to handle player exit and co-op player session changes.

### `OnExit(uDriver, uGuid)`
Called when a player exits the vehicle's seat. It resets jump mechanics and stops emitters. If networking is active, it sends a network event to stop emitters on other clients.

### `StartEmitters(uGuid)`
Starts particle effects for the vehicle's exhaust system.

### `StopEmitters(uGuid)`
Stops particle effects for the vehicle's exhaust system.

### `OnJump(uGuid)`
Handles the jump action. It applies an impulse to the vehicle, starts emitters, and sets up a timer event to wait for landing.

### `WaitForLanding(uGuid)`
Called after the jump duration. It stops emitters and waits for the vehicle to land before resetting jump mechanics.

### `ResetJump(uGuid)`
Resets jump mechanics by setting up an event to handle the player pressing the jump button. **Confirmed
gated to the local player only** — the trigger-press listener is only (re-)armed when
`Vehicle.GetDriver(uGuid) == Player.GetLocalCharacter()`; if a co-op partner is currently driving, this
client never re-arms the jump listener for them.

### `Deactivated(uGuid, tListOfObjects)`
Closes the gate of the vehicle and sets up a proximity event to reactivate it when nearby objects are detected.

**Confirmed in source, likely a bug:** the proximity event's callback is a bare `Activated` — but no function
named `Activated` (as opposed to `OnActivate`) is defined anywhere in this file. Referencing an undefined
global in Lua evaluates to `nil` rather than erroring immediately, so this silently registers the proximity
event with a `nil` callback instead of actually reactivating the vehicle when it fires.

## Events
- Listens for `Event.ObjectInSeat` — registered twice: once in `OnEnter` (driver exits, `"d","xo"`) to
  call `OnExit`, and once in `OnExit` (any character enters, `"d","ei"`) to call `OnEnter` again.
- Listens for `Event.ScriptEvent` with `"mpPlayerLeft"` (registered in `OnEnter`) to detect the current
  driver leaving the co-op session and trigger `OnExit`.
- Listens for `Event.TimerRelative` (registered in `OnJump`) to call `WaitForLanding` 1.5s after a jump.
- Listens for `Event.ObjectIsGrounded` (registered in `WaitForLanding`) to call `ResetJump` once the
  vehicle lands.
- Listens for `Event.Button` (registered in `ResetJump`, local-driver-gated — see below) for an
  `"rtrigger"` `"press"` to call `OnJump`.
- Listens for `Event.ObjectProximity` (registered in `Deactivated`) with a **bare `Activated` callback
  that is never defined anywhere in this file** — see the confirmed bug noted under `Deactivated` above.
- Also uses `Net.SendCustomEvent("moonpatrol", ...)` (in `OnExit`, `OnJump`, `WaitForLanding`) paired with
  the module-level `NetEventCallback(eventId, tArgs)` dispatcher (`NETEVENT_STARTEMITTERS = 0`,
  `NETEVENT_STOPEMITTERS = 1`) to mirror emitter start/stop across the network — this is the engine's
  custom-net-event mechanism, not an `Event.*` constant.

## Module constants & tunables
This module names only two constants (`NETEVENT_STARTEMITTERS = 0`, `NETEVENT_STOPEMITTERS = 1`), but the
interesting knobs are the hard-coded values in the function bodies — the "make it jump higher / change the
exhaust" levers:

| What | Value / string | Where |
|---|---|---|
| Turbo/exhaust particle template | `"global_particle_monstertruck_turbo"` | `StartEmitters`/`StopEmitters` |
| Exhaust emitter attach points | `"hp_fx_exhaust_a"`, `"hp_fx_exhaust_b"` | `StartEmitters`/`StopEmitters` |
| Jump impulse | `Object.ApplyPointImpulse(uGuid, 0, 10*mass, 0.1*mass, 0, 0, 0.15, true)` | `OnJump` — vertical `10*mass`, slight forward `0.1*mass` |
| Airborne wait before landing check | `1.5`s | `OnJump` → `WaitForLanding` (`Event.TimerRelative`) |
| Jump trigger button | `"rtrigger"` `"press"` | `ResetJump` (`Event.Button`) |
| Reactivation proximity radius | `10` units | `Deactivated` (`Event.ObjectProximity`, `"<"`) |

All template/attach-point names are passed through `String.GetHash(...)` before use; the emitter calls go
through the `ObjectState` namespace (`ObjectState.StartEmitter`/`StopEmitter`), and the impulse/mass lookups
use the [`Object`](../namespaces/object) namespace (`Object.ApplyPointImpulse`/`Object.GetMass`).

## Notes for modders
- Ensure that `OnActivate`, `OnDeactivate`, and related functions are called appropriately to manage the vehicle's lifecycle.
- Customize jump mechanics by modifying the impulse values in `OnJump` or the particle template/attach points
  in `StartEmitters`/`StopEmitters` (table above).
- Be aware of network synchronization ([`Net.SendCustomEvent`](../namespaces/net)) when extending this module
  for multiplayer support — emitter start/stop is mirrored to other clients via the module-level
  `NetEventCallback` dispatcher, so a client-only tweak to `StartEmitters` won't automatically replicate.