---
title: VerifyFlash
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [graphics, atmosphere]
verified: true
verified_note: "deeper pass: re-counted the 23 Atmosphere calls (10 SetColorValue + 13 SetValue) between Begin()/End() and confirmed each parameter name/value literal against source; cross-linked the Graphics namespace; page was already accurate"
---

# VerifyFlash

*Module: verify_flash.lua*

## Overview
The `VerifyFlash` module sets a fixed atmosphere/post-process preset — flat grey ambient lighting plus a
specific bloom configuration — via the engine [`Graphics`](../namespaces/graphics)`.Atmosphere` API. The
name suggests it's a QA/verify look (uniform 128-grey ambient makes lighting bugs obvious), applied wholesale
when the object activates.

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

## The atmosphere preset (the knobs)
Since every value is a hardcoded literal, this file *is* the config. The exact settings it applies:

- **Ambient (all flat grey `128,128,128,255`):** `uiAmbientColor`, `uiAmbientCube0`–`uiAmbientCube5`,
  `uiRimColor`.
- **UI gradient colors (`0,0,255,0`):** `uiGradient0_Color2`, `uiGradient1_Color1`.
- **Atmosphere:** `fAtmosphereForce = 0`, `fAtmosphereLimit = 100`.
- **Bloom:** `fBloomAmount = 0.5`, `fBloomBlurRadius = 0.5`, `fBloomMultiplier = 0.8`, `fBloomThreshold = 0.8`,
  `fBloomTargetLuminance = 1.5`, `fBloomAdaptiveLuminancePercent = 0.49`, `fBloomAdaptiveLuminanceScale = 15`,
  `fBloomContastMultiplier = 0.925`, `fBloomContastLimit = 0.5` (spelling `Contast` is verbatim from source —
  the engine parameter names are misspelled, so match them exactly).
- **Light / time:** `fLightIntensity = 2.5`, `fTimeRestore = 0.55`.

## Notes for modders
- All 23 values are literal arguments in `OnActivate` — there's no config table or external input, so
  customizing this look means editing the literals above directly (or copying the `Begin()`…`End()` block
  into your own atmosphere script).
- The parameter strings are the engine's own — including the misspelled `fBloomContastLimit`/
  `fBloomContastMultiplier`. Use the exact spelling or the `SetValue` call silently does nothing.
- `Graphics.Atmosphere.Begin()`/`End()` bracket the whole batch; keep changes between them.