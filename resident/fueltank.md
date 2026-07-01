---
title: Fueltank
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [fuel, fx]
---

# Fueltank

*Module: fueltank.lua*

## Overview
The `Fueltank` module manages the visual effects associated with a fuel tank object. Specifically, it handles starting and stopping flame and smoke emitters when certain state changes occur.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any specific state fields.

## Functions
### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Called when the state of an object changes. If the new state hash matches `"0x7687DF41"`, it starts a flame emitter and schedules a timer to start a smoke emitter after a random interval between 12 and 20 seconds.

### `_StartSmoke(uiGuid, uiNodeHashName, fxName)`
A helper function that stops the current flame emitter and starts a smoke emitter for the object.

## Events
- Listens for `Event.StateChange` to call `OnStateChange` when an object's state changes.
- Creates a `Event.TimerRelative` event to call `_StartSmoke` after a random delay.

## Notes for modders
- Ensure that `OnStateChange` is called appropriately to manage the visual effects of the fuel tank.
- Customize the flame and smoke emitters by modifying the associated effect names in the code.
- Be aware that the random timer interval affects when the smoke emitter starts.