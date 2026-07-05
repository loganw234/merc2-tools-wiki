---
title: AirstrikeAtomsphereClusterbomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: spot-checked against source, no changes needed — OnActivate/_GraphicsAto, no imports, and Events section all confirmed accurate
---

# AirstrikeAtomsphereClusterbomb

*Module: airstrike_atomsphere_clusterbomb.lua*

## Overview
The `AirstrikeAtomsphereClusterbomb` module is responsible for modifying the atmospheric and visual effects of the game world when an airstrike with cluster bombs occurs. It adjusts various atmosphere settings to create a specific visual impact.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless utility module (no `Create`/instance pattern). It does not track any per-instance state.

## Functions
### `OnActivate(guid)`
Called when the airstrike object instance is activated. It sets up an event to call `_GraphicsAto` after a short delay of 0.1 seconds.

### `_GraphicsAto(guid)`
Modifies the atmospheric settings to create a specific visual effect for the cluster bomb airstrike. This function adjusts various atmosphere parameters such as ambient colors, bloom effects, and light intensity.

## Events
- Listens for `Event.TimerRelative` to call `_GraphicsAto` after a delay of 0.1 seconds.

## Notes for modders
- Ensure that `OnActivate` is called appropriately when the airstrike object is activated.
- Customize the atmospheric effects by modifying the parameters set in `_GraphicsAto`.
- Be aware that these changes will affect the visual atmosphere globally during the airstrike event.