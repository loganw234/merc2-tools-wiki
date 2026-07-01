---
title: Treetrunkpalm
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tree, animation]
---

# Treetrunkpalm

*Module: treetrunkpalm.lua*

## Overview
The `Treetrunkpalm` module is responsible for playing material animations on palm tree trunks when they transition to specific fire-related states. It listens for state changes and triggers animations that simulate debris or destruction effects.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless utility module with no per-instance pattern. It does not track any persistent state.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the object's state changes. If the new state is either "FireDebrisState" or "FireDestroyedState", it schedules `_PlayMaterialAnims` to be called once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the palm tree trunk with the GUID `uiGuid`. The animation played is named "global_env_treepalm_anim". It also logs a debug message indicating that the animation is being played.

## Events
- Listens for `Event.ObjectStateChange` to call `_PlayMaterialAnims` when the object transitions to "FireDebrisState" or "FireDestroyedState".

## Notes for modders
- Ensure that `OnStateChange` is called appropriately to manage state transitions and trigger animations.
- Customize the animation name by modifying the argument passed to `Object.PlayMaterialAnimation`.
- Be aware of the specific state names ("FireDebrisState", "FireDestroyedState") as they are used to determine when to play the animation.