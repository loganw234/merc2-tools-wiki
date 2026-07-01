---
title: ParadropLocation
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, mission]
---

# ParadropLocation

*Module: paradroplocation.lua*

## Overview
The `ParadropLocation` module is responsible for triggering a paradrop plane when activated. It determines the faction of the activating object and initiates an airstrike with a predefined template that flies over the location, dropping paratroopers.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state and operates solely through its top-level functions.

## Functions
### `OnActivate(uGuid)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Determines the position and faction of the activating object. If valid, it initiates an airstrike with a paradrop template that flies over the location, dropping paratroopers. After triggering the airstrike, it removes the activating object from the world.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to trigger the paradrop.
- Customize the faction templates in `tTemplates` if you want to change the aircraft used for different factions.
- Be aware that this module removes the activating object after triggering the airstrike, so ensure it does not interfere with other mission logic.