---
title: Treetrunk
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tree, animation]
---

# Treetrunk

*Module: treetrunk.lua*

## Overview
The `Treetrunk` module is responsible for handling the state changes of tree trunks in the game. Specifically, it triggers animations when a tree trunk transitions into a "FireDebrisState" or "FireDestroyedState". This helps in visually representing the destruction and debris left after a fire.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `String`, `Event`, `Object`

## Instance pattern
This is a stateless utility module. It does not track any per-instance state; instead, it handles global events related to tree trunk states.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the state of an object changes. If the new state is either "FireDebrisState" or "FireDestroyedState", it schedules `_PlayMaterialAnims` to be called once the object is ready.

### `_PlayMaterialAnims(uiGuid)`
Plays a material animation on the specified tree trunk object (`uiGuid`). The animation used is "global_env_treeplaza03_anim".

## Events
- Listens for `Event.ObjectStateChange` to trigger animations when a tree trunk's state changes to "FireDebrisState" or "FireDestroyedState".
- Fires `Event.ObjectIsReady` to ensure the object is ready before playing the animation.

## Notes for modders
- Ensure that the tree trunk's state transitions are correctly handled in your game logic.
- Customize the animation by changing the animation name in `_PlayMaterialAnims`.
- Be aware of any potential performance impacts from frequent state changes and animations.