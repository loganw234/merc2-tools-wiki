---
title: SpyHunter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, boost]
verified: true
verified_note: 'deeper pass: re-confirmed all functions + the ObjectInSeat/ScriptEvent/TimerRelative/Button subscriptions and 4 NETEVENT_* codes; added the particle-effect hash names, the jetexhaust node, the jump/cooldown timings (0.8s/5.5s/8s, nJump 0-5 impulses) and Sound.SetVehicleEngineBoost; re-confirmed the DisplayBoost/nBoost dead-code bug; cross-linked ObjectState/Object/Net/Event namespaces.'
---

# SpyHunter

*Module: spyhunter.lua*

## Overview
The `SpyHunter` module manages the behavior of the Spy Hunter vehicle in the game. It handles player entry and exit events, jump mechanics, boost meter display, and network synchronization for particle effects and sound cues.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
No `Create`/`tInstance`/`setmetatable` anywhere in this file — this is a plain module-level utility, not
the `Inheritable`-style per-`uGuid` factory pattern. Per-vehicle state is tracked manually with a table
keyed by `uGuid`, not a real instance object:
- `tEvents`: table of `tEvents[uGuid] = {bReady, eExit, eMPquit, eCoolCheck, eJump, eEnter, eSmokeStop,
  eReset, ...}` — event handles and a `bReady` boost-cooldown flag per vehicle GUID. Initialized in
  `Init()`, torn down in `Deinit()`.
- `gbEnableBoostMeter`: module-level boolean, hardcoded `false` at the top of the file. **No code path in
  this file (or found anywhere else in the decompiled corpus) ever sets it to `true`** — see the
  `DisplayBoost` note below.

## Functions
### `Init()`
Initializes the module by setting up an empty table `tEvents` to store event handlers.

### `Deinit()`
Deinitializes the module by clearing the `tEvents` table.

### `OnActivate(uGuid, args)`
Called when a Spy Hunter instance is activated. It initializes the event table for the instance and sets up initial events.

### `OnDeactivate(uGuid, args)`
Called when a Spy Hunter instance is deactivated. It cleans up all registered events for the instance.

### `OnEnter(uDriver, uGuid)`
Called when a player enters the Spy Hunter vehicle. It sets up events to handle exit and multiplayer player left scenarios, and starts the cool check process.

### `CoolCheck(uGuid)`
Checks if the Spy Hunter is ready for a jump. If it is, it resets the jump; otherwise, it schedules another check in 0.5 seconds.

### `OnExit(uDriver, uGuid)`
Called when a player exits the Spy Hunter vehicle. It stops any ongoing boost effects and sets up an event to handle re-entry.

### `NetEventCallback(eventId, tArgs)`
Handles network events related to boost particle effects and sound cues. It calls appropriate functions based on the event ID.

### `GetDriverGuid(uGuid)`
Retrieves the GUID of the driver controlling the Spy Hunter vehicle.

### `DisplayBoost(uGuid)`
Displays the boost meter on the HUD based on `nBoost`, an undeclared global that is **never assigned
anywhere in this file** (or elsewhere in the decompiled corpus). `DisplayBoost` is only ever called when
`gbEnableBoostMeter` is truthy (from `OnEnter` and `CoolDown`), and since that flag is hardcoded `false`
with no setter anywhere found, this function is effectively dead code. If it were ever reached with
`nBoost` still `nil`, the `nBoost <= 99` comparison on the first line would raise a Lua runtime error
(comparing `nil` with a number). Likely leftover/half-finished feature — confirmed in source, not a
guess: `nBoost` has zero write sites in the file.

### `ResetJump(uGuid)`
Resets the jump mechanics for the Spy Hunter, starting the boost effect and setting up the jump event handler.

### `NetSafeSmokeStop(uGuid)`
Stops the smoke particle effect safely by stopping the emitter.

### `SetupBoost(uGuid)`
Sets up the boost mechanics for the Spy Hunter, including starting the boost effect and sending a network event if active.

### `NetSafeSetupBoost(uGuid)`
Starts the boost particle effect safely by setting up the emitter.

### `OnJump(uGuid)`
Handles the jump mechanics for the Spy Hunter. It applies impulses based on the current jump stage and schedules the next jump or stops the boost if all jumps are completed.

### `StopBoost(uGuid)`
Stops the boost mechanics for the Spy Hunter, including stopping the boost effect and sending a network event if active.

### `NetSafeStopBoost(uGuid)`
Stops the boost particle effect safely by stopping the emitter.

### `NetSafeSmokeStart(uGuid)`
Starts the smoke particle effect safely by setting up the emitter.

### `DontSmoke(uGuid)`
Stops the smoke particle effect and sends a network event if active.

### `IsCool(uGuid)`
Marks the Spy Hunter as ready for another jump and resets it if there is a driver.

### `CoolDown(uGuid)`
Starts the cooldown process after a boost, including setting up smoke effects and sending network events if active. It also updates the boost meter display if enabled.

## Events
All are real [`Event.Create`](../namespaces/event) subscriptions (stored in `tEvents[uGuid]`):

- **`Event.ObjectInSeat`** — driver enter (`"d","ei"` → `OnEnter`, handle `eEnter`) and exit (`"d","a"`
  → `OnExit`, handle `eExit`).
- **`Event.ScriptEvent`** named **`"mpPlayerLeft"`** (filtered on the driver, handle `eMPquit`) — treats
  an MP player leaving as an exit.
- **`Event.Button`** — the actual boost trigger: while seated and cool, a `"lbutton"` `"press"` (handle
  `eJump`) fires `SetupBoost`. (This was missing from the previous draft's list.)
- **`Event.TimerRelative`** — the readiness poll (`0.5`s `CoolCheck`), the per-stage jump ticks (`0.8`s
  `OnJump`), and the cooldown timers (`5.5`s `DontSmoke`, `8`s `IsCool`).
- **Custom `"spyhunter"` net events** — `NETEVENT_STARTEMITTERS`, `NETEVENT_STOPEMITTERS`,
  `NETEVENT_STARTEMITTERSMOKE`, `NETEVENT_STOPEMITTERSMOKE` dispatched by `NetEventCallback` to the
  `NetSafe*` emitter helpers (visual-only sync).

## Module constants & tunables
- **Net event codes**: `NETEVENT_STARTEMITTERS=0`, `NETEVENT_STOPEMITTERS=1`,
  `NETEVENT_STARTEMITTERSMOKE=2`, `NETEVENT_STOPEMITTERSMOKE=3` (channel `"spyhunter"`).
- **Emitter node**: all effects attach to the vehicle node hash `"hp_fx_jetexhaust"`.
- **Particle effect hashes** ([`ObjectState.StartEmitter`](../namespaces/object)/`StopEmitter`):
  - `"global_particle_fire_jetengine_orange_infinite"` — idle/ready jet flame
  - `"global_particle_fire_jetengine_boost_infinite"` — active boost flame
  - `"global_particle_fire_jetengine_infinite"` — cooldown smoke
- **Timings**: readiness poll `0.5`s; jump stage interval `0.8`s; smoke-stop `5.5`s after boost;
  ready-again (`IsCool`) `8`s after boost.
- **Jump impulse profile** (`OnJump`, `nJump` 0→5, each 0.8s apart, `myMass = Object.GetMass`):
  stage 0 `Object.ApplyPointImpulse(...,50000,...)`; stages 1–2 upward `Object.ApplyImpulse` scaled by
  mass (`6*`/`8*`); stages 3–5 forward-ish (`10*`/`6*`/`4*` mass with slight down). These are the knobs
  for how the Spy Hunter "hops".
- **Engine boost sound**: `Sound.SetVehicleEngineBoost(uGuid, 1/0)` (guarded by a nil-check on the
  function itself).
- **HUD string** (dead-code path): `"[GurCon003.Objectives.Boost]"`.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage Spy Hunter lifecycle.
- `DisplayBoost`/the HUD boost meter is dead code as shipped: `gbEnableBoostMeter` is hardcoded `false`
  and `nBoost` is never assigned. To actually use this feature, you'd need to set `gbEnableBoostMeter =
  true` and assign `nBoost` yourself somewhere before `DisplayBoost` runs.
- Customize jump mechanics by modifying impulse values in `OnJump` (5 stages, `nJump` 0–5, each with its
  own `Object.ApplyImpulse`/`Object.ApplyPointImpulse` call, spaced 0.8s apart via `Event.TimerRelative`).
- Be aware that network synchronization (`Net.SendCustomEvent("spyhunter", ...)`) may affect multiplayer
  behavior — `NetEventCallback` dispatches on 4 numeric event IDs (`NETEVENT_STARTEMITTERS = 0`,
  `NETEVENT_STOPEMITTERS = 1`, `NETEVENT_STARTEMITTERSMOKE = 2`, `NETEVENT_STOPEMITTERSMOKE = 3`) to the
  `NetSafe*` variants, which only touch particle emitters (no gameplay/impulse logic) so remote clients
  see the visual effect without re-simulating the boost itself.