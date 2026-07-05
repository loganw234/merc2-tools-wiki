---
title: AirstrikeAtomsphereTactNuke
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: spot-checked against source, no changes needed — OnActivate/_GraphicsAto (0.15s delay, correctly noted), MrxUtil import and ShieldFace call, and Events section all confirmed accurate
---

# AirstrikeAtomsphereTactNuke

*Module: airstrike_atomsphere_tactnuke.lua*

## Overview
The `AirstrikeAtomsphereTactNuke` module is responsible for handling the atmospheric effects triggered by a tactical nuke airstrike. It adjusts various atmosphere settings to create visual and lighting effects that simulate the impact of such an attack.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any persistent state.

## Functions
### `OnActivate(guid)`
Called when the object instance is activated. It sets up a timer to call `_GraphicsAto` after 0.15 seconds with the provided `guid`.

### `_GraphicsAto(guid)`
Handles the atmospheric effects for the tactical nuke airstrike. It modifies various atmosphere settings such as ambient colors, bloom parameters, light intensity, and other visual properties. After setting these values, it calls `MrxUtil.ShieldFace` to apply additional effects.

## Events
- Listens for `Event.TimerRelative` to trigger `_GraphicsAto` after a short delay.

## Notes for modders
- Ensure that `OnActivate` is called appropriately when the tactical nuke airstrike is initiated.
- Customize the atmospheric effects by modifying the values set in `_GraphicsAto`.
- Be aware that changes to atmosphere settings may affect visual consistency across different game scenarios.