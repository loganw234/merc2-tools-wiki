---
title: MaterialAnimation_LargeCanopy02
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, canopy]
verified: true
verified_note: removed fabricated Event.ObjectStateChange (not in source — OnStateChange is engine-invoked by naming convention, only real Event.* reference is Event.ObjectIsReady); noted the animation name is still "largecanopy01" despite this being the 02 file, and that this file has no node-hash check (unlike largecanopy01).
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
Engine-invoked by naming convention (no `Event.Create` wiring for `OnStateChange` itself in this file).
Unlike `materialanimation_largecanopy01`, this version does **not** check `uiNodeHashName` at all — it
only checks `uiStateHashName == String.GetHash("CollapseFireState") or uiStateHashName ==
String.GetHash("CollapseState")`. If either matches, it registers an `Event.ObjectIsReady` listener to
call `_PlayMaterialAnims` once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified object using its GUID, one-shot (`false` loop flag). The
animation name is **`"jungle_env_largecanopy01_material_anim"`** — literally the `01` name, even though
this is the `02` module. This is what's in the decompiled source; whether that's an authoring copy-paste
or intentional asset reuse can't be determined from static reading alone.

## Events
- Listens for `Event.ObjectIsReady` (registered inside `OnStateChange`) to call `_PlayMaterialAnims` once
  the object is ready, after the object enters "CollapseFireState" or "CollapseState".
- **Correction:** `Event.ObjectStateChange` does not appear anywhere in this file's source — that event
  name was previously listed here in error. `OnStateChange` is invoked directly by the engine via naming
  convention, not through an `Event.Create`/`Event.ObjectStateChange` registration.

## Notes for modders
- Ensure that the state names ("CollapseFireState", "CollapseState") match exactly with those used in the game.
- The animation name "jungle_env_largecanopy01_material_anim" should be verified to ensure it exists and is correctly named in the game assets.
- This module does not require any specific initialization or cleanup beyond what is provided by default.