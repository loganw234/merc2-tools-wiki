---
title: MaterialAnimation_LargeCanopy02
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, canopy]
---

# MaterialAnimation_LargeCanopy02

*Module: materialanimation_largecanopy02.lua*

## Overview
The `MaterialAnimation_LargeCanopy02` module is responsible for playing material animations on large canopy objects when they enter specific states, such as "CollapseFireState" or "CollapseState". It triggers the animation by listening to state changes and then executing the appropriate animation sequence.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state; it operates based on global events and object states.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the state of an object changes. If the new state is either "CollapseFireState" or "CollapseState", it schedules the `_PlayMaterialAnims` function to be called once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified object using its GUID. The animation played is named "jungle_env_largecanopy01_material_anim".

## Events
- Listens for `Event.ObjectStateChange` to call `_PlayMaterialAnims` when the object enters "CollapseFireState" or "CollapseState".

## Notes for modders
- Ensure that the state names ("CollapseFireState", "CollapseState") match exactly with those used in the game.
- The animation name "jungle_env_largecanopy01_material_anim" should be verified to ensure it exists and is correctly named in the game assets.
- This module does not require any specific initialization or cleanup beyond what is provided by default.