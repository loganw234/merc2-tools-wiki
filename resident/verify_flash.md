---
title: VerifyFlash
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [graphics, atmosphere]
verified: true
verified_note: spot-checked against source (28-line file, single OnActivate with no branching) — page already accurate; corrected parameter count to the actual 23 calls (10 SetColorValue + 13 SetValue) and tightened a vague closing note
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
Called when the module is activated. Takes no arguments (no `uGuid` — this isn't a world-object script).
Runs `Graphics.Atmosphere.Begin()`, then a fixed, unconditional sequence of 23
`Graphics.Atmosphere.SetColorValue`/`SetValue` calls (10 `SetColorValue` calls — 7 ambient-cube/ambient
values plus `uiGradient0_Color2`, `uiGradient1_Color1`, `uiRimColor` — and 13 `SetValue` calls covering
atmosphere-force/limit, bloom, light intensity, and time-restore), then `Graphics.Atmosphere.End()`. No
branching, no loops, no other functions called — every value is a literal constant.

## Events
- Listens for none — this module does not subscribe to or fire any engine events.

## Notes for modders
- This module directly modifies atmospheric settings when activated. Ensure that it is called at the appropriate time to achieve the desired visual effect.
- Be cautious with modifying atmospheric parameters, as they can significantly affect the game's visuals and performance.
- All 23 parameter values are hardcoded literals in `OnActivate` — there's no config table or external
  input to override, so customizing this module means editing the literal arguments directly.