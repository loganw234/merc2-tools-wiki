---
title: LivingWorldProp
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [inventory, weapon]
---

# LivingWorldProp

*Module: livingworldprop.lua*

## Overview
The `LivingWorldProp` module is designed to handle interactions with living world props that can be used by players. Specifically, it provides functionality to drop weapons when a player interacts with these props.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless utility module (no `Create`/instance pattern). It does not track any per-instance state.

## Functions
### `UnUse(objectGuid, holdersGuid)`
Called when a player interacts with a living world prop. This function drops the weapon associated with the prop by calling `Human.Inventory.DropWeapon(holdersGuid, objectGuid)`.

## Events
- Listens for: none — this module does not subscribe to any engine events directly.

## Notes for modders
- Ensure that `UnUse` is called appropriately when a player interacts with a living world prop to drop the associated weapon.
- This module does not require any specific initialization or cleanup beyond ensuring that `UnUse` is triggered correctly.