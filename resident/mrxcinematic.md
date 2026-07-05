---
title: MrxCinematic
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [cinematic, slideshow]
verified: true
verified_note: spot-checked against source (2 functions, zero Event.* references, no inherit/tInstance) — page already accurate, no changes needed
---

# MrxCinematic

*Module: mrxcinematic.lua*

## Overview
The `MrxCinematic` module is a placeholder slideshow system used for displaying sequences of slides in the game's HUD. It provides functions to chain and display slides with zero fade times, using default textures if none are specified.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any persistent state.

## Functions
### `PlaceholderSequence(tSlides, fCallback, tCallbackArgs)`
Chains slides so each `_DisplaySlide` calls the next. The last slide carries the final callback with arguments. Sets fade times to zero for all slides.

### `_DisplaySlide(tSlideData)`
Displays a single slide using the HUD's cinematic placeholder system. Defaults the texture to `"temp_placeholder"` if none is provided and shows the slide.

## Events
- Listens for no specific engine events (internal chaining mechanism).

## Notes for modders
- Ensure that `PlaceholderSequence` is called with valid slide data to display the slideshow.
- Customize slides by providing a table of slide data, including textures and callbacks.
- Be aware that fade times are set to zero, which may affect the visual transition between slides.