---
title: Treetrunk
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tree, animation]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (2 functions, one Event.ObjectIsReady subscription); surfaced the two trigger state names + the "global_env_treeplaza03_anim" material anim; documented the near-identical relationship to treetrunkpalm (different anim name, no debug line); cross-linked treetrunkpalm/Object/Event namespaces.'
---

# Treetrunk

*Module: treetrunk.lua*

## Overview
The `Treetrunk` module is a small set-dressing script: when a tree trunk enters a fire state
(`"FireDebrisState"` or `"FireDestroyedState"`), it plays a material animation on the trunk to show
the charred/debris look. That's the whole module — two functions, one deferred animation.

This is nearly identical to its sibling [`treetrunkpalm`](treetrunkpalm); the only real differences
are the animation name (`global_env_treeplaza03_anim` here vs. `global_env_treepalm_anim`) and that the
palm version also prints a debug line. See "Module constants" below.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: none. (`String`, `Event`, `Object` are built-in engine namespaces called directly, not
  `import()`ed modules — this file has no `import(...)` or `inherit(...)` calls at all.)

## Instance pattern
This is a stateless utility module. It does not track any per-instance state; instead, it handles global events related to tree trunk states.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Engine lifecycle callback. Compares `uiStateHashName` against `String.GetHash("FireDebrisState")` and
`String.GetHash("FireDestroyedState")` (i.e. it hashes the state *name* strings and compares hashes,
rather than converting the incoming hash to a string). On a match it schedules `_PlayMaterialAnims`
via `Event.ObjectIsReady`. `uiNodeHashName` is unused.

### `_PlayMaterialAnims(uiGuid)`
Calls [`Object.PlayMaterialAnimation(uiGuid, "global_env_treeplaza03_anim", false)`](../namespaces/object)
— the trailing `false` means non-looping (play once).

## Events
- `Event.ObjectIsReady` (in `OnStateChange`, via `Event.Create`) — the only `Event.*` call in this file.
  Used to defer `_PlayMaterialAnims` until the object is ready, after a matching state change is detected.
- `OnStateChange` itself is **not** registered through `Event.Create` in this file — no
  `Event.ObjectStateChange` (or similarly named constant) appears anywhere in the source. It's invoked
  directly by the engine as a naming-convention callback on the world-object script, the same way
  `OnActivate`/`OnDeath` are called on other modules.

## Module constants & tunables
- **Trigger states**: `"FireDebrisState"` and `"FireDestroyedState"` (compared as hashes via
  `String.GetHash`). These are the authored object states that fire the animation.
- **Material animation**: `"global_env_treeplaza03_anim"`, played once (non-looping).

## Notes for modders
- Change the animation by editing the `"global_env_treeplaza03_anim"` string in `_PlayMaterialAnims`;
  change *when* it plays by editing the two state names in `OnStateChange`.
- The animation is deliberately deferred with `Event.ObjectIsReady` — the object may not be ready to
  animate at the instant its state changes, so don't call `Object.PlayMaterialAnimation` directly from
  `OnStateChange`.