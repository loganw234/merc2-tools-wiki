---
title: Paratrooper
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [ai, airborne]
---

# Paratrooper

*Module: paratrooper.lua*

## Overview
The `Paratrooper` module manages the behavior of paratroopers in the game. It handles the transition from a paratrooper to an airborne faction unit when the paratrooper's health drops below 100.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It does not track any specific state fields beyond what is inherited from `Inheritable`.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the paratrooper instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, iArg)`
Sets up an event listener for the `Event.ObjectHealth` event, which triggers when the paratrooper's health drops below 100. This event calls `RemoveChute`.

### `RemoveChute(uGuid, iArg)`
Removes the paratrooper object and spawns a new airborne faction unit at the same position and orientation. The faction is determined by calling `MrxUtil.GetFaction(uGuid)`. The spawned unit's yaw is set to match the original paratrooper.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for `Event.ObjectHealth` to call `RemoveChute` when the paratrooper's health drops below 100.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the paratrooper.
- Customize the faction templates in `tTemplates` if you want to change which airborne units are spawned.
- Be aware that the health threshold for chute removal is hardcoded at 100.