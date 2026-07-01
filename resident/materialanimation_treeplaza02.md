---
title: MaterialAnimation_TreePlaza02
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, tree plaza]
---

# MaterialAnimation_TreePlaza02

*Module: materialanimation_treeplaza02.lua*

## Overview
The `MaterialAnimation_TreePlaza02` module is responsible for triggering material animations on a specific object in the game world. It listens for state changes related to fire debris and destruction, and plays a material animation when these states are detected.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module with no per-instance pattern. It does not track any specific object state.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the state of an object changes. If the new state is either "FireDebrisState" or "FireDestroyedState", it schedules the `_PlayMaterialAnims` function to be called once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified object using the `Object.PlayMaterialAnimation` function. The animation played is named "global_env_treeplaza02_anim".

## Events
- Listens for `Event.ObjectStateChange` to call `OnStateChange` when an object's state changes.

## Notes for modders
- Ensure that the object has the correct material animations defined in its asset files.
- The animation name "global_env_treeplaza02_anim" should match the actual animation defined for the object.
- This module does not require any specific initialization or cleanup steps beyond ensuring the object's state changes are properly handled.