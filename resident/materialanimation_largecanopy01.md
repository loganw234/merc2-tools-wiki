---
title: MaterialAnimation_LargeCanopy01
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, canopy]
verified: true
verified_note: spot-checked against source, no changes needed — Events section already correctly lists only Event.ObjectIsReady (no fabricated Event.ObjectStateChange, unlike the largecanopy02/treeplaza02 sibling pages).
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
Engine-invoked by naming convention (there's no `Event.Create`/`Event.*` wiring for it in this file — the
engine calls it directly when an object's animation-graph node changes state). Checks
`uiNodeHashName == String.GetHash("Slice00")` **and** `uiStateHashName == String.GetHash("CollapseFireState")`
— both must match. If so, registers an `Event.ObjectIsReady` listener to call `_PlayMaterialAnims` once
the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified object using the `Object.PlayMaterialAnimation` function. The
animation played is `"jungle_env_largecanopy01_material_anim"`, with the loop flag set to `false`
(one-shot, not looping).

## Events
- Listens for `Event.ObjectIsReady` (registered inside `OnStateChange`) to call `_PlayMaterialAnims` once
  the object is ready, after the "Slice00" node enters "CollapseFireState".
- `OnStateChange` itself is not registered via `Event.Create` in this file — it's called directly by the
  engine using the `OnStateChange` name convention (same as the sibling `materialanimation_*` modules).

## Notes for modders
- Ensure that the object has the correct node and state names ("Slice00" and "CollapseFireState") for the animation to trigger.
- The material animation name "jungle_env_largecanopy01_material_anim" must be correctly specified in the game's asset files.
- This module does not require any additional setup or configuration beyond ensuring the object is in the correct state.