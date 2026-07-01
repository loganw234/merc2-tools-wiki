---
title: Heavymg
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [weapon, event]
---

# Heavymg

*Module: heavymg.lua*

## Overview
The `Heavymg` module is responsible for handling the removal of heavy machine gun (HMG) objects when they are dropped by a human player. It listens for specific weapon events and triggers the appropriate actions to despawn the HMG.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (no per-instance table). It does not track any persistent state.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the HMG object instance is activated. It sets up an event listener for the `Human Drop` weapon event to trigger the removal of the HMG.

### `OnDeactivate(uGuid)`
Called when the HMG object instance is deactivated. It cleans up by deleting the event listener associated with the HMG.

## Events
- Listens for `Event.WeaponEvent` with specific parameters (`"Human"`, `"Drop"`) to call `Object.Remove` and despawn the HMG.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the event listener.
- This module does not have any public API functions other than those required by the engine's lifecycle hooks.
- The decompiler did not introduce any artifacts in this script.