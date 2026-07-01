---
title: VerifyFlash
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [graphics, atmosphere]
---

# VerifyFlash

*Module: verify_flash.lua*

## Overview
The `VerifyFlash` module is responsible for setting up and configuring the atmospheric effects in the game. It adjusts various parameters related to lighting, bloom, and ambient colors to create a specific visual effect.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module (no `uGuid`). It does not track any per-instance state.

## Functions
### `OnActivate()`
Called when the module is activated. It sets up various atmospheric parameters to configure the visual effects in the game, including ambient colors, bloom settings, and light intensity.

## Events
- Listens for none — this module does not subscribe to or fire any engine events.

## Notes for modders
- This module directly modifies atmospheric settings when activated. Ensure that it is called at the appropriate time to achieve the desired visual effect.
- Be cautious with modifying atmospheric parameters, as they can significantly affect the game's visuals and performance.
- The decompiler output does not show any unused or redundant assignments, indicating that all code is necessary for the intended functionality.