---
title: MrxCinematic
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [cinematic, slideshow]
verified: true
verified_note: "deeper pass: surfaced the temp_placeholder default texture and the forced-zero fade times, documented the slide-chaining behavior of PlaceholderSequence, noted the MrxUtil import is unused; both functions and zero-Event.* re-confirmed"
---

# MrxCinematic

*Module: mrxcinematic.lua*

## Overview
The `MrxCinematic` module is a placeholder slideshow system used for displaying sequences of slides in the game's HUD. It provides functions to chain and display slides with zero fade times, using default textures if none are specified.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxUtil`](mrxutil) (imported but no `MrxUtil.*` call appears in the two functions — the import
  looks vestigial)

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
- **This is exactly what the name says — a placeholder.** Every fade time is forced to `0` and any slide
  without an `sTexture` falls back to the debug texture `"temp_placeholder"`. It renders through
  `Hud.CinematicPlaceholder:Show(tSlideData)`. Treat it as stand-in cinematic scaffolding, not a finished
  slideshow system.
- **Slide table shape**: pass `PlaceholderSequence(tSlides, fCallback, tCallbackArgs)` where `tSlides` is an
  array of slide-data tables (each may carry `sTexture`, plus whatever `Hud.CinematicPlaceholder:Show`
  consumes). `PlaceholderSequence` rewrites the `fCallback`/`tCallbackData`/`nFadeInTime`/`nFadeOutTime`
  fields to chain the slides, so don't set those yourself — the final callback you pass fires after the last
  slide.