---
title: MaterialAnimation_LargeCanopy01
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, canopy]
verified: true
verified_note: "deeper pass: re-confirmed the 9-line source — checks Slice00 node + CollapseFireState, plays jungle_env_largecanopy01_material_anim once via Object.PlayMaterialAnimation; only Event.* is ObjectIsReady; cross-linked the two sibling drivers and made the trigger a clear tunable"
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

## Module constants & tunables
- **Trigger:** node `"Slice00"` **and** state `"CollapseFireState"` (both hashed via `String.GetHash`).
  This is the only sibling driver that also gates on the node name.
- **Animation:** `"jungle_env_largecanopy01_material_anim"`, played one-shot (loop flag `false`) via
  `Object.PlayMaterialAnimation`.

## Notes for modders
- To retarget this to a different collapse, change the `"Slice00"`/`"CollapseFireState"` trigger and/or the
  animation name — those two strings are the entire knob set.
- **Sibling drivers** (same shape, different trigger/animation):
  [MaterialAnimation_LargeCanopy02](materialanimation_largecanopy02) (no node check; fires on
  `CollapseFireState`/`CollapseState`; reuses this file's `...largecanopy01...` animation name) and
  [MaterialAnimation_TreePlaza02](materialanimation_treeplaza02) (fires on `FireDebrisState`/
  `FireDestroyedState`; plays `global_env_treeplaza02_anim`).