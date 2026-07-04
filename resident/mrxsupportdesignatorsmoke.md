---
title: MrxSupportDesignatorSmoke
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxSupportDesignatorSmoke

*Module: mrxsupportdesignatorsmoke.lua*

## Overview
The `MrxSupportDesignatorSmoke` module is responsible for handling the functionality of smoke support designators in the game. It inherits from `MrxSupportDesignator` and provides specific behavior for creating, managing, and removing smoke markers on the battlefield.

## Inheritance
- Inherits from: `MrxSupportDesignator`
- Imports: none

## Instance pattern
**Same class-factory pattern as `MrxSupportDesignator`, not per-`uGuid`** — `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no
`tInstance` registry. It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignateOnDeath`: Whether to designate on death.
- `bDesignationComplete`: Indicates if the designation is complete.
- `sDesignationType`: The type of designation, set to "Smoke Designator".
- `fValidationFunction`: Function used for validation, set to `MrxSupportDesignator.ValidateGroundDropZone`.
- `tCallbackList`: List of callbacks for designation completion.
- `sSmokeHash`: Hash value for the smoke color.
- `sDenialSmokeTemplate`: Template for denial smoke.
- `sAATestLevel`: Anti-air test level, set to "basic".
- `nX`, `nY`, `nZ`: Position coordinates of the designator.
- `uGuid`: Unique identifier for the instance.

## Functions
### `Init()`
Initializes by loading the asset "global_weapon_m34wp".

### `Deinit()`
Unloads the asset "global_weapon_m34wp".

### `Create(self, oNewDesignator)`
Creates a new designator object with default values and sets up its properties. It initializes fields such as `sDesignationType`, `fValidationFunction`, and adds a completion callback.

### `NetEventCallback(nEventType, tArgs)`
Handles network events. Specifically, it processes the `NETEVENT_SMOKEACTIVATE` event by calling `NetSafeDesignationCompleteCallback`.

### `DesignationCompleteCallback(self)`
Called when the designation is complete. It starts an emitter for the smoke, disables physics for the object, sends a custom network event to activate the smoke, and schedules its removal after 10 seconds.

### `NetSafeDesignationCompleteCallback(sTemplateHashName, nx, ny, nz, sBeaconId)`
Spawns a smoke object at the specified position using the given template hash name. It also schedules the removal of this smoke object after 10 seconds.

### `NetSafeRemoveSmoke(sBeaconId)`
Removes a smoke object based on its beacon ID.

### `RemoveSmoke(self)`
Removes the designator object if it has a valid GUID.

### `OnDeny(self, uGuid)`
Handles denial by removing the object and spawning a denial smoke template at its position.

### `SetSmokeColor(self, sColor)`
Sets the smoke color based on the provided string. It updates both the `sSmokeHash` and `sDenialSmokeTemplate` fields accordingly.

### `GetType(self)`
Returns the type of designator, which is "smoke".

## Events
- Listens for `NETEVENT_SMOKEACTIVATE` to call `NetSafeDesignationCompleteCallback`.
- Listens for custom event `Event.TimerRelative` to remove smoke after 10 seconds.

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately to manage asset loading.
- Use `SetSmokeColor` to change the color of the smoke designator.
- Customize behavior by modifying fields like `sDesignationType` or adding additional callbacks in `tCallbackList`.
- Be aware that the smoke automatically removes after 10 seconds, and denial results in a different visual effect.