---
title: MrxSupportDesignator
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [support, economy]
---

# MrxSupportDesignator

*Module: mrxsupportdesignator.lua*

## Overview
The `MrxSupportDesignator` module is a base class for support designators in the game. It handles the designation of drop zones and landing zones for various types of cargo and delivery vehicles. This module is crucial for managing the logistics of air strikes and supply drops.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The GUID of the player or entity that owns the designator.
- `bDesignationComplete`: A boolean indicating whether the designation process is complete.
- `sDesignationType`: The type of designation being used.
- `sAATestLevel`: The AA test level for the designation.
- `fValidationFunction`: A function to validate the drop zone.
- `tCallbackList`: A list of callbacks to be called when designation is complete.
- `tVOCues`: A table for voice-over cues related to designation.
- `nX`, `nY`, `nZ`: The coordinates of the designated location.
- `uGuid`: The GUID of the designator object.
- `oParentSupport`: The parent support object that owns this designator.

## Functions
### `GetTarget(self)`
Returns the target coordinates and GUID once the designation is complete. Returns `nil` if the designation is not complete.

### `RemoveBeacon(self)`
Removes a beacon associated with the designator if it exists.

### `Create(self, oNewDesignator)`
Creates a new instance of the designator by copying properties from an existing one. If no new designator is provided, it creates a default instance.

### `SetOwner(self, uPlayerGuid)`
Sets the owner of the designator to the specified player GUID.

### `AddCompleteCallback(self, fCallback, tCallbackData)`
Adds a callback function to be called when the designation is complete. The callback data can be passed as an optional table.

### `RemoveCompleteCallback(self, fCallback)`
Removes a previously added callback function from the list of callbacks.

### `SetCompleteCallback(self, fCallback, tCallbackData)`
Sets a callback function and its associated data to be called when the designation is complete. The callback must be a function, and the data must be a table if provided.

### `SetDesignationType(self, sTemplateName)`
Sets the type of designation template to use for the designator. The template name should be a string or `nil`.

### `SetValidationFunction(self, fFunction)`
Sets the validation function to be used for validating the drop zone. The function must be a function or `nil`.

### `SetTargetValidationRequired(self, bRequireValidation)`
Sets whether target validation is required before completing the designation.

### `SetAATestLevel(self, sAATestLevel)`
Sets the AA test level for the designation.

### `SetTargetLocation(self, nX, nY, nZ)`
Sets the target location coordinates for the designator. The coordinates must be numbers.

### `OnDeny(self, uGuid)`
Called when the designation is denied. Currently does nothing.

### `SetParentSupport(self, oSupport)`
Sets the parent support object that owns this designator.

### `GetParentSupport(self)`
Returns the parent support object that owns this designator.

### `Configure(self, tOptions)`
Configures the designator with options provided in a table. If an option is not present in the table, it retains its current value.

### `Commence(self, bFireImmediately)`
Starts the designation process by equipping the designator and setting the reserve ammo for the weapon. Returns the GUID of the equipped weapon or `false` if the owner is invalid.

### `GetType(self)`
Returns the type of the designator, which is "none" in this base class.

## Events
- Listens for custom events related to designation completion and validation.

## Notes for modders
- Ensure that the designator's owner is set correctly using `SetOwner`.
- Use `AddCompleteCallback` and `RemoveCompleteCallback` to manage callbacks for when the designation is complete.
- Customize the designator by setting various parameters such as type, validation function, and target location using the provided setter functions.
- Be aware that the designator's behavior can be influenced by the parent support object set with `SetParentSupport`.
- The module uses predefined templates (`_cargoTemplateData` and `_heliTemplateData`) for validating drop zones. These templates can be extended or modified as needed.