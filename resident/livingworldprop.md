---
title: LivingWorldProp
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [inventory, weapon]
verified: true
verified_note: "deeper pass: re-confirmed the 3-line source — the sole function UnUse drops the prop weapon via Human.Inventory.DropWeapon(holdersGuid, objectGuid); replaced vacuous Notes bullets with the one real gotcha (arg order) and the override lever"
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
Called when a player stops using/interacting with a living world prop (the engine-invoked counterpart to
a `Use` handler — no `Use` is defined in this file). Drops the weapon associated with the prop by
calling `Human.Inventory.DropWeapon(holdersGuid, objectGuid)`. This is the only function in the file.

## Events
- Listens for: none — this module does not subscribe to any engine events directly.

## Notes for modders
- **Override lever:** `UnUse` is a plain (non-`local`) global, so a mod can redefine it to do something
  other than drop the weapon when the player releases the prop. The whole module is this one behavior.
- **Argument order gotcha:** `Human.Inventory.DropWeapon(holdersGuid, objectGuid)` — the *holder* (the
  human) comes first, the *prop object* second, which is the reverse of the `(objectGuid, holdersGuid)`
  order the engine passes into `UnUse`. Keep that straight if you reuse the call.
- `UnUse` is the engine's release-counterpart to a `Use` handler; no `Use` is defined here, and the module
  subscribes to no events.