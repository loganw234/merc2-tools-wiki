---
title: Airstrike_Atmosphere_FuelAirBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
---

# Airstrike_Atmosphere_FuelAirBomb

*Module: airstrike_atomsphere_fuelairbomb.lua*

## Overview
The `Airstrike_Atmosphere_FuelAirBomb` module is responsible for handling the atmospheric effects triggered by a fuel air bomb airstrike. It sets up a timer to apply specific atmosphere changes and triggers a shield face effect.

## Inheritance
- Inherits from: `none`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless utility module (no per-instance table or `uGuid` management).

## Functions
### `OnActivate(guid)`
Called when the object instance is activated. It sets up a timer to call `_GraphicsAto` after 1.75 seconds.

### `_GraphicsAto(guid)`
Applies various atmospheric changes and triggers a shield face effect for the given GUID. It modifies atmosphere settings such as ambient colors, bloom effects, light intensity, and other visual parameters.

## Events
- Listens for `Event.TimerRelative` to call `_GraphicsAto` after 1.75 seconds.

## Notes for modders
- Ensure that `OnActivate` is called appropriately when the airstrike effect should be triggered.
- Customize atmosphere settings by modifying the values set in `_GraphicsAto`.
- Be aware of the shield face effect triggered by `MrxUtil.ShieldFace(guid)`, which may have additional effects on the player or environment.