---
title: MrxSupportManager
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [support, economy]
---

# MrxSupportManager

*Module: mrxsupportmanager.lua*

## Overview
The `MrxSupportManager` module is responsible for managing the designation queues and recruit cooldowns in the game. It handles the validation of drop zones, checks fuel availability, and manages the state of recruits to ensure they are available for use.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSupport`, `MrxPmc`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tRecruitStates`: A table that stores the availability state of each recruit.
- `_tRecruitTimers`: A table that stores the timer objects for each recruit's cooldown period.
- `_nDefaultCooldownTime`: The default cooldown time for recruits.

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
Completes the designation process for a support type by checking recruit availability and fuel requirements, then starts the recruit cooldown.

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
- Listens for `Event.ObjectHibernation` to call `FinishOnActivate` when a designator leaves hibernation.
- Listens for custom network events `NETEVENT_RECRUITSTATE` and `NETEVENT_STARTTIMER` to update recruit states and timers.

## Notes for modders
- Ensure that `OnActivate`, `OnDeactivate`, and `OnDesignate` are called appropriately to manage the designation lifecycle.
- Customize recruit availability and cooldown times by modifying `_tRecruitStates` and `_nDefaultCooldownTime`.
- Be aware of network synchronization (`Net.SendCustomEvent`) when extending or modifying this module.