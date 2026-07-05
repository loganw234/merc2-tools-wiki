---
title: Binoculars
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: confirmed the whole 1-line source; clarified Use is an intentionally-empty engine hook (behaviour lives engine-side / in the GUI layer) and pointed at MrxGuiBinoculars for the real binoculars view; trimmed speculative prose'
---

# Binoculars

*Module: binoculars.lua*

## Overview
The entire `binoculars.lua` is a single empty `Use` hook. The engine calls it when the binoculars prop is
used, but the file scripts no behaviour — the actual binoculars view (zoom, overlay) is handled elsewhere,
see [MrxGuiBinoculars](mrxguibinoculars). This script exists so the prop has a valid `Use` entry point.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless utility module (no `uGuid`). It does not track any per-instance state.

## Functions
### `Use(aiguid, floatval)`
The engine-invoked "use" hook for the binoculars prop. Parameters `aiguid` and `floatval` are declared but
unused; the body is empty, so scripting nothing on use is the intended behaviour (the real binoculars view is
driven engine-side / by the GUI layer).

## Events
This module does not subscribe to or fire any engine events. `Use` is an engine callback, not an
`Event.Create` subscription.

## Notes for modders
- There is no existing behaviour to preserve — the hook is empty by design. If you fill in `Use`, note the
  real binoculars UI/zoom lives in [MrxGuiBinoculars](mrxguibinoculars), not here.