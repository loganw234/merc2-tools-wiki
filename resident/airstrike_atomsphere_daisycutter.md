---
title: Airstrike_Atmosphere_Daisycutter
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
---

# Airstrike_Atmosphere_Daisycutter

*Module: airstrike_atomsphere_daisycutter.lua*

## Overview
The `Airstrike_Atmosphere_Daisycutter` module is responsible for setting up the atmospheric effects and visual settings when a daisy cutter airstrike occurs. It adjusts various atmosphere parameters to create a specific visual environment during the airstrike.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables or `uGuid` management).

## Functions
### `OnActivate(guid)`
Called when the daisy cutter airstrike object instance is activated. It sets up a timer to call `_GraphicsAto` after a short delay.

### `_GraphicsAto(guid)`
Handles the atmospheric and visual settings for the daisy cutter airstrike. It configures various atmosphere parameters such as ambient colors, bloom effects, light intensity, and other visual properties. After setting these values, it calls `MrxUtil.ShieldFace(guid)` to apply additional visual effects.

## Events
- Listens for `Event.TimerRelative` to call `_GraphicsAto` after a 0.1-second delay when the object is activated.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to trigger the atmospheric changes.
- Customize the atmosphere settings by modifying the values set in `_GraphicsAto`.
- Be aware of the dependencies on `MrxUtil.ShieldFace`, as it may have additional effects not covered here.