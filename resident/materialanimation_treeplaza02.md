---
title: MaterialAnimation_TreePlaza02
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, tree plaza]
verified: true
verified_note: removed fabricated Event.ObjectStateChange (not in source, and the old wording was self-contradictory — said OnStateChange listens for the event that invokes it); only real Event.* reference is Event.ObjectIsReady; corrected the two state names checked (FireDebrisState/FireDestroyedState, not the largecanopy modules' CollapseFireState/CollapseState).
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
Engine-invoked by naming convention (no `Event.Create` wiring for `OnStateChange` itself in this file —
same pattern as the `materialanimation_largecanopy01`/`02` sibling modules). Does not check
`uiNodeHashName`. Checks `uiStateHashName == String.GetHash("FireDebrisState") or uiStateHashName ==
String.GetHash("FireDestroyedState")`. If either matches, registers an `Event.ObjectIsReady` listener to
call `_PlayMaterialAnims` once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified object using the `Object.PlayMaterialAnimation` function,
one-shot (`false` loop flag). The animation played is named `"global_env_treeplaza02_anim"`.

## Events
- Listens for `Event.ObjectIsReady` (registered inside `OnStateChange`) to call `_PlayMaterialAnims` once
  the object is ready, after it enters "FireDebrisState" or "FireDestroyedState".
- **Correction:** `Event.ObjectStateChange` does not appear anywhere in this file's source — that event
  name (and the claim that `OnStateChange` "listens for" it) was previously listed here in error.
  `OnStateChange` is invoked directly by the engine via naming convention, not through an
  `Event.Create`/`Event.ObjectStateChange` registration.

## Notes for modders
- Ensure that the object has the correct material animations defined in its asset files.
- The animation name "global_env_treeplaza02_anim" should match the actual animation defined for the object.
- This module does not require any specific initialization or cleanup steps beyond ensuring the object's state changes are properly handled.