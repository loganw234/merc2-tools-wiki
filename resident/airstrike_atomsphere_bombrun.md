---
title: AirstrikeAtomsphereBombrun
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: spot-checked against source, no changes needed — OnActivate/_GraphicsAto, no imports, and Events section all confirmed accurate
---

# AirstrikeAtomsphereBombrun

*Module: airstrike_atomsphere_bombrun.lua*

## Overview
The `AirstrikeAtomsphereBombrun` module is responsible for adjusting the atmospheric and visual effects during an airstrike event. It sets various atmosphere parameters to create a specific visual environment, likely enhancing the dramatic impact of the airstrike.

## Inheritance
- Inherits from: `none`
- Imports: `none`

## Instance pattern
This is a stateless utility module (no per-instance pattern). It does not track any persistent state and operates solely through its top-level functions.

## Functions
### `OnActivate(guid)`
Called when the airstrike event is activated. It schedules a timer to call `_GraphicsAto` after a short delay of 0.1 seconds.

### `_GraphicsAto(guid)`
Adjusts various atmospheric settings to create the desired visual effect for the airstrike. This function sets parameters such as ambient colors, bloom effects, light intensity, and other visual properties through the `Graphics.Atmosphere` API.

## Events
- Listens for `Event.TimerRelative` to call `_GraphicsAto` after a delay of 0.1 seconds when the airstrike event is activated.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to trigger the atmospheric adjustments.
- Customize the visual effects by modifying the parameters set in `_GraphicsAto`.
- Be aware that these changes will affect the entire atmosphere during the airstrike event.