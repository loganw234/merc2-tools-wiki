---
title: MrxSupportManager
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, economy]
verified: true
verified_note: 'deeper pass: re-confirmed the singleton pattern and OnActivate reactive handler; surfaced the cooldown constants (_nDefaultCooldownTime 12, SupportTimer default 10, the special-cased Copter -1 = indefinite hold), documented the NETEVENT_RECRUITSTATE/STARTTIMER net-sync and the fuel gate in CompleteDesignation, and pruned the vacuous "ensure OnActivate is called" note'
---

# MrxSupportManager

*Module: mrxsupportmanager.lua*

## Overview
The `MrxSupportManager` module is responsible for managing the designation queues and recruit cooldowns in the game. It handles the validation of drop zones, checks fuel availability, and manages the state of recruits to ensure they are available for use.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSupport`, `MrxPmc`

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: no `Create`/`tInstance` registry anywhere in
source — `CurrentlyEquippedSupport`/`SupportQueue` are plain module-level tables this manager maintains
itself, keyed by player/character guid as simple lookup keys, not a factory-built per-instance object with
inherited methods. Key fields:
- `_tRecruitStates`: recruit-hash → available (`true`/`false`). `false` while a recruit's cooldown timer runs.
- `_tRecruitTimers`: recruit-hash → `SupportTimer` object driving that recruit's cooldown.
- `_nDefaultCooldownTime = 12`: default cooldown (seconds) applied by `StartRecruitCooldown` when no explicit
  time is passed. `SupportTimer`'s own default `nTotalTime` is `10`.
- `CurrentlyEquippedSupport` / `SupportQueue` / `ValidationQueue`: module-level tables keyed by
  player/character GUID (see Instance-pattern note).

## Functions
### `CurrentlyEquippedSupport:AddSupport(oSupport)`
Adds a support object to the currently equipped support list for a character.

### `SupportQueue:Add(uPlayerGuid, oSupport, uDesignatorGuid)`
Adds a designator GUID to the support queue for a player and support type.

### `SupportQueue:GetSupport(uPlayerGuid, uDesignatorGuid)`
Retrieves the support type associated with a player and designator GUID from the support queue.

### `ValidationQueue:Add(uPlayerGuid, oSupport, uDesignatorGuid, nX, nY, nZ)`
Adds a validation request to the validation queue for a player, support type, and designator GUID at a specified position.

### `ValidationQueue:_Process()`
Processes the first item in the validation queue by calling the validation function.

### `_ValidationQueueCallback(bSuccess, nX, nY, nZ)`
A callback function that processes the result of a validation request.

### `ValidationQueue:_Callback(bSuccess, nX, nY, nZ)`
Handles the result of a validation request and either completes the designation or denies it.

### `CompleteDesignation(oSupport, uDesignatorGuid, uPlayerGuid)`
Completes the designation process: checks recruit availability and the fuel requirement
(`oSupport:GetFuelCost() > MrxPmc.GetFuelQty()` denies unless `oSupport.bUnrestrictedByFuel` is set — that
flag is how [`MrxSupportTransit`](mrxsupporttransit) makes rides free), then starts the recruit cooldown and
fires the designator's `CompleteDesignation`. **The `"Copter"` recruit is special-cased**: it gets
`StartRecruitCooldown("Copter", -1)`, i.e. held unavailable **indefinitely** (a negative time starts no
timer) until something explicitly calls `MakeRecruitAvailable("Copter")` — which the delivery modules do when
their heli despawns.

### `OnActivate(uDesignatorGuid, uPlayerGuid)`
Called when a designator is activated. It sets up an event to call `FinishOnActivate` once the object leaves hibernation.

### `FinishOnActivate(uDesignatorGuid)`
Finishes the activation process by adding the support type to the support queue for the player.

### `OnInitialize(uDesignatorGuid, uPlayerGuid)`
Initializes a designator by calling `OnActivate`.

### `OnDesignate(uDesignatorGuid, uPlayerGuid, uTargetGuid, bSuccess, bDeactivation)`
Handles the designation event for a designator. It processes the target and validates the drop zone if necessary.

### `OnDeactivate(uDesignatorGuid, uPlayerGuid, uTargetGuid, bSuccess, bDeactivation)`
Handles the deactivation event for a designator by calling `OnDesignate`.

### `OnTimer(uDesignatorGuid, uPlayerGuid, uTargetGuid, bSuccess, bDeactivation)`
Handles the timer event for a designator by calling `OnDesignate`.

### `OnDeath(uDesignatorGuid, uPlayerGuid)`
Called when a designator dies. Currently does nothing.

### `IsRecruitAvailable(sRecruit)`
Checks if a recruit is available by looking up its state in `_tRecruitStates`.

### `StartRecruitCooldown(sRecruit, nTime)`
Starts the cooldown period for a recruit by setting its state to unavailable and creating a timer.

### `RegisterRecruit(sRecruit)`
Registers a recruit by initializing its state to available and creating a timer object.

### `MakeRecruitAvailable(sRecruit)`
Marks a recruit as available by updating its state in `_tRecruitStates`.

### `GetRecruitTimes(sRecruit)`
Retrieves the elapsed time and total time for a recruit's cooldown period.

### `NetEventCallback(nType, tArgs)`
Handles network events related to recruit states and timers.

### `SupportTimer:Create()`
Creates a new support timer object.

### `SupportTimer:Delete()`
Deletes a support timer by stopping it.

### `SupportTimer:GetElapsedTime()`
Returns the elapsed time for the timer.

### `SupportTimer:GetTotalTime()`
Returns the total time for the timer.

### `SupportTimer:SetTotalTime(nTotalTime)`
Sets the total time for the timer.

### `SupportTimer:Reset()`
Resets the elapsed time of the timer to zero.

### `SupportTimer:SetCallback(fCallback, tCallbackData)`
Sets the callback function and data for the timer.

### `SupportTimer:Start()`
Starts the timer by creating a persistent event.

### `SupportTimer:Stop()`
Stops the timer by deleting the persistent event.

### `SupportTimer:_EventCallback(nDeltaTime)`
Updates the elapsed time of the timer and calls the callback if the timer has completed.

### `Init()`
Initializes the recruit states and timers tables.

## Events
- **`Event.ObjectHibernation`** (`"awake"`) — the one real `Event.*` subscription, set up in `OnActivate`;
  calls `FinishOnActivate` once the designator wakes.
- `OnActivate`/`OnInitialize`/`OnDesignate`/`OnDeactivate`/`OnTimer`/`OnDeath` are **engine designator
  callbacks** the engine invokes by name, not `Event.*` subscriptions this module registers.
- **Net sync**: recruit availability is broadcast with `Net.SendCustomEvent("MrxSupportManager", ...)` using
  IDs `NETEVENT_RECRUITSTATE = 0` and `NETEVENT_STARTTIMER = 1`; `NetEventCallback` is the receiver that
  applies remote recruit-state/timer changes.

## Notes for modders
- **Cooldown knobs**: `_nDefaultCooldownTime = 12` is the default recruit cooldown; pass an explicit time to
  `StartRecruitCooldown(sRecruit, nTime)` to override, or `-1` to hold a recruit indefinitely (as
  `CompleteDesignation` does for `"Copter"`). `SupportTimer` ticks on the GUI game timer, so cooldowns are in
  real seconds.
- **Fuel gate**: set `bUnrestrictedByFuel = true` on a support object to bypass the fuel check in
  `CompleteDesignation` (see [`MrxSupportTransit`](mrxsupporttransit)).
- **Recruit availability drives the store**: `IsRecruitAvailable`/`MakeRecruitAvailable` are what gray out or
  re-enable support items — `MakeRecruitAvailable` also posts a `"RecruitAvailable"` event that
  [`MrxSupport`](mrxsupport)'s `SetupDamageEvent` listens for.