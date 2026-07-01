---
title: Repairpad
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, repair]
---

# Repairpad

*Module: repairpad.lua*

## Overview
The `Repairpad` module manages the activation and deactivation of repair pads in the game world. It handles events related to the pad's lifecycle, such as when it is activated, deactivated, or destroyed. The module also controls the visual state of the repair pad by toggling its front light.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxTutorialManager`

## Instance pattern
This is a stateless manager/utility module with no per-instance tables. It tracks events associated with each repair pad using the `tEvents` table, keyed by `uGuid`.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the repair pad instance is activated. Sets up an event to call `Awake` once the object leaves hibernation.

### `OnDeactivate(uGuid)`
Called when the repair pad instance is deactivated. Deletes all associated events and clears the entry in the `tEvents` table.

### `OnDeath(uGuid)`
Called when the repair pad's underlying object dies. Turns off the front light and calls `OnDeactivate`.

### `SetupActivationEvents(uGuid)`
Sets up activation events for the repair pad, including turning on the front light.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the repair pad leaves hibernation.
- Listens for custom event `HideMarker` to remove objectives for hidden objects (not explicitly shown in this file).

## Notes for modders
- Ensure that `OnActivate`, `OnDeactivate`, and `OnDeath` are called appropriately to manage the repair pad's lifecycle.
- The front light of the repair pad can be controlled using `Vehicle.SetParts`.
- Be aware of any custom events like `HideMarker` that might affect the repair pad's behavior.