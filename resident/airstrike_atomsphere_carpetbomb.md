---
title: AirstrikeAtomsphereCarpetbomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
---

# AirstrikeAtomsphereCarpetbomb

*Module: airstrike_atomsphere_carpetbomb.lua*

## Overview
The `AirstrikeAtomsphereCarpetbomb` module is responsible for initiating a specific atmospheric effect when an airstrike event occurs. It adjusts various atmosphere settings to create a visual and environmental impact, likely simulating the effects of carpet bombing.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (no per-instance table or `uGuid` keying). It does not track any persistent state.

## Functions
### `OnActivate(guid)`
Called when the airstrike event is activated. It sets up a timer to call `_GraphicsAto` after a short delay of 0.1 seconds.

### `_GraphicsAto(guid)`
Adjusts various atmosphere settings and triggers a visual effect using `MrxUtil.ShieldFace`. This function modifies ambient colors, bloom settings, light intensity, and other atmospheric parameters to create the desired visual impact.

## Events
- Listens for `Event.TimerRelative` to call `_GraphicsAto` after a delay of 0.1 seconds when the airstrike event is activated.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to trigger the atmosphere effect.
- Customize the atmospheric settings by modifying the values set in `_GraphicsAto`.
- Be aware that changes to atmosphere settings may affect visual consistency and performance.