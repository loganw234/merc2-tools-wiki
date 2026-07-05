---
title: MaterialAnimation_TreePlaza02
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, tree plaza]
verified: true
verified_note: "deeper pass: re-confirmed the 9-line source — no node check, fires on FireDebrisState/FireDestroyedState, plays global_env_treeplaza02_anim one-shot; only Event.* is ObjectIsReady; cross-linked the two canopy sibling drivers"
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

## Module constants & tunables
- **Trigger:** state `"FireDebrisState"` **or** `"FireDestroyedState"` (hashed via `String.GetHash`). No
  node check.
- **Animation:** `"global_env_treeplaza02_anim"`, one-shot (loop flag `false`) via
  `Object.PlayMaterialAnimation`.

## Notes for modders
- Change the two fire-state strings and/or the animation name to retarget this driver — those three strings
  are the entire knob set.
- **Sibling drivers** (same one-shot `OnStateChange` → `Event.ObjectIsReady` → `_PlayMaterialAnims` shape):
  [MaterialAnimation_LargeCanopy01](materialanimation_largecanopy01) (checks `"Slice00"` node +
  `CollapseFireState`) and [MaterialAnimation_LargeCanopy02](materialanimation_largecanopy02)
  (`CollapseFireState`/`CollapseState`, no node check).