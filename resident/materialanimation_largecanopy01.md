---
title: MaterialAnimation_LargeCanopy01
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, canopy]
---

# MaterialAnimation_LargeCanopy01

*Module: materialanimation_largecanopy01.lua*

## Overview
The `MaterialAnimation_LargeCanopy01` module is responsible for triggering a material animation on a large canopy object when it enters the "CollapseFireState" state. The animation plays once the object is ready.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance tables or fields.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the state of an object changes. If the node hash name is "Slice00" and the state hash name is "CollapseFireState", it registers an event to call `_PlayMaterialAnims` once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified object using the `Object.PlayMaterialAnimation` function. The animation played is "jungle_env_largecanopy01_material_anim".

## Events
- Listens for `Event.ObjectIsReady` to call `_PlayMaterialAnims` when the object is ready after entering the "CollapseFireState" state.

## Notes for modders
- Ensure that the object has the correct node and state names ("Slice00" and "CollapseFireState") for the animation to trigger.
- The material animation name "jungle_env_largecanopy01_material_anim" must be correctly specified in the game's asset files.
- This module does not require any additional setup or configuration beyond ensuring the object is in the correct state.