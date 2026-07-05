---
title: Treetrunkpalm
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tree, animation]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (2 functions, one Event.ObjectIsReady subscription); surfaced the two trigger state names + the "global_env_treepalm_anim" material anim and the leftover Debug.Printf; documented that this is treetrunk.lua with a different anim name; cross-linked treetrunk/Object/Event namespaces.'
---

# Treetrunkpalm

*Module: treetrunkpalm.lua*

## Overview
The `Treetrunkpalm` module plays a material animation on a **palm** tree trunk when it enters a fire
state (`"FireDebrisState"` or `"FireDestroyedState"`), giving it the charred/debris look. Two
functions, one deferred animation.

It is functionally the same script as [`treetrunk`](treetrunk) — the palm version just uses a
different animation name (`global_env_treepalm_anim` vs. `global_env_treeplaza03_anim`) and adds a
leftover `Debug.Printf`. If you're editing both, keep them in sync.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless utility module with no per-instance pattern. It does not track any persistent state.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Engine lifecycle callback. Compares `uiStateHashName` against `String.GetHash("FireDebrisState")` and
`String.GetHash("FireDestroyedState")` (it hashes the state *name* strings and compares hashes). On a
match it schedules `_PlayMaterialAnims` via `Event.ObjectIsReady`. `uiNodeHashName` is unused.

### `_PlayMaterialAnims(uiGuid)`
Calls [`Object.PlayMaterialAnimation(uiGuid, "global_env_treepalm_anim", false)`](../namespaces/object)
(non-looping), then prints a debug line (`"im playing the palm material anim"`) — engine-log noise, no
gameplay effect. This debug print is the only code difference from [`treetrunk`](treetrunk).

## Events
- `Event.ObjectIsReady` (in `OnStateChange`, via `Event.Create`) — the only `Event.*` call in this file.
  Schedules `_PlayMaterialAnims` to run once the object reports ready, after a matching state change is
  detected.
- `OnStateChange` itself is **not** registered through `Event.Create` in this file — no
  `Event.ObjectStateChange` (or similarly named constant) appears anywhere in the source. It's invoked
  directly by the engine as a naming-convention callback on the world-object script, the same way
  `OnActivate`/`OnDeath` are called on other modules.

## Module constants & tunables
- **Trigger states**: `"FireDebrisState"` and `"FireDestroyedState"` (compared as hashes via
  `String.GetHash`).
- **Material animation**: `"global_env_treepalm_anim"`, played once (non-looping).

## Notes for modders
- Change the animation by editing the `"global_env_treepalm_anim"` string; change *when* it plays by
  editing the two state names in `OnStateChange`.
- The animation is deferred with `Event.ObjectIsReady` — don't move it inline into `OnStateChange`, the
  object may not be ready to animate the instant its state flips.
- The `Debug.Printf` here is harmless leftover; it only writes to the log. See the sibling
  [`treetrunk`](treetrunk) for the non-palm variant.