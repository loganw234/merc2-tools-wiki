---
title: Airstrike_Atmosphere_MOAB
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: spot-checked against source, no changes needed — OnActivate/_GraphicsAto, MrxUtil import and ShieldFace call, and Events section all confirmed accurate
---

# Airstrike_Atmosphere_MOAB

*Module: airstrike_atomsphere_moab.lua*

## Overview
The `Airstrike_Atmosphere_MOAB` module is responsible for setting up atmospheric effects and visual graphics when a MOAB (Massive Ordnance Air Blast) airstrike occurs. It adjusts various atmosphere parameters to create a specific visual and environmental impact.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module with no per-instance pattern. It does not track any persistent state.

## Functions
### `OnActivate(guid)`
Called when the MOAB airstrike object instance is activated. It sets up an event to call `_GraphicsAto` after a short delay of 0.1 seconds.

### `_GraphicsAto(guid)`
Handles the atmospheric and graphical adjustments for the MOAB airstrike. It modifies various atmosphere settings such as ambient colors, bloom effects, light intensity, and other visual parameters. After setting these values, it calls `MrxUtil.ShieldFace` to apply additional visual effects.

## Events
- Listens for `Event.TimerRelative` to call `_GraphicsAto` after a delay of 0.1 seconds when the MOAB airstrike is activated.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to trigger the atmospheric and graphical adjustments.
- Customize the atmosphere settings by modifying the values set in `_GraphicsAto`.
- Be aware that changes to these settings may affect the overall visual experience of the game.