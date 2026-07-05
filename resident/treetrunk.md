---
title: Treetrunk
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tree, animation]
verified: true
verified_note: removed fabricated Event.ObjectStateChange claim (file only references Event.ObjectIsReady; OnStateChange is engine-invoked by naming convention) and corrected the Inheritance/Imports line (String/Object are engine namespaces, not imported modules)
---

# Treetrunk

*Module: treetrunk.lua*

## Overview
The `Treetrunk` module is responsible for handling the state changes of tree trunks in the game. Specifically, it triggers animations when a tree trunk transitions into a "FireDebrisState" or "FireDestroyedState". This helps in visually representing the destruction and debris left after a fire.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: none. (`String`, `Event`, `Object` are built-in engine namespaces called directly, not
  `import()`ed modules — this file has no `import(...)` or `inherit(...)` calls at all.)

## Instance pattern
This is a stateless utility module. It does not track any per-instance state; instead, it handles global events related to tree trunk states.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the state of an object changes. If the new state is either "FireDebrisState" or "FireDestroyedState", it schedules `_PlayMaterialAnims` to be called once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified tree trunk object (`uiGuid`). The animation used is "global_env_treeplaza03_anim".

## Events
- `Event.ObjectIsReady` (in `OnStateChange`, via `Event.Create`) — the only `Event.*` call in this file.
  Used to defer `_PlayMaterialAnims` until the object is ready, after a matching state change is detected.
- `OnStateChange` itself is **not** registered through `Event.Create` in this file — no
  `Event.ObjectStateChange` (or similarly named constant) appears anywhere in the source. It's invoked
  directly by the engine as a naming-convention callback on the world-object script, the same way
  `OnActivate`/`OnDeath` are called on other modules.

## Notes for modders
- Ensure that the tree trunk's state transitions are correctly handled in your game logic.
- Customize the animation by changing the animation name in `_PlayMaterialAnims`.
- Be aware of any potential performance impacts from frequent state changes and animations.