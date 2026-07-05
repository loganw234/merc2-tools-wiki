---
title: MaterialAnimation_LargeCanopy02
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [material animation, canopy]
verified: true
verified_note: "deeper pass: re-confirmed the 9-line source — no node-hash check, fires on CollapseFireState/CollapseState, and (confirmed) plays the 01 animation name jungle_env_largecanopy01_material_anim; only Event.* is ObjectIsReady; cross-linked sibling drivers"
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

## Module constants & tunables
- **Trigger:** state `"CollapseFireState"` **or** `"CollapseState"` (hashed via `String.GetHash`). No node
  check — unlike [MaterialAnimation_LargeCanopy01](materialanimation_largecanopy01), which also gates on the
  `"Slice00"` node.
- **Animation:** `"jungle_env_largecanopy01_material_anim"` — the `01` name, one-shot (`false`).

{: .note }
> The animation string is literally the `largecanopy01` name even though this is the `02` module. This is
> what the decompiled source contains; it may be intentional asset reuse or an authoring copy-paste — it
> can't be determined from static reading alone. If you clone this file for a new canopy, double-check the
> animation name is the one you intend.

## Notes for modders
- Change the two state strings and/or the animation name to retarget — that's the whole knob set.
- **Sibling drivers:** [MaterialAnimation_LargeCanopy01](materialanimation_largecanopy01) (adds a `"Slice00"`
  node check, fires only on `CollapseFireState`) and
  [MaterialAnimation_TreePlaza02](materialanimation_treeplaza02) (fires on `FireDebrisState`/
  `FireDestroyedState`; plays `global_env_treeplaza02_anim`).