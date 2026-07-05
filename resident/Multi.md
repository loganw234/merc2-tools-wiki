---
title: Multi
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: "deeper pass: made the spawn primitives concrete (Multi uses Pg.SpawnFromCamera at 10/0.5; Scatter uses Pg.FindPointFromCamera+Pg.Spawn with Event.TimerRelative spread and XZ jitter), corrected nOffset framing (jitter magnitude, not radius), added the source usage example; stateless framing and Events re-confirmed"
---

# Multi

*Module: Multi.lua*

## Overview
The `Multi` module provides utility functions for spawning multiple game objects in the world. It includes functions to spawn templates in front of the camera and to scatter objects over a specified area.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance tables or fields.

## Functions
### `Multi(tObjects)`
Spawns multiple templates in front of the camera. Iterates `tObjects` with `ipairs` and calls
`Pg.SpawnFromCamera(object, 10, 0.5)` for each — i.e. `10` metres out, `0.5` up (both hardcoded here). All
objects spawn at the same point, so they stack.
- **Parameters**: 
  - `tObjects`: A table (array) of object template names to spawn.
- **Returns**: None
- **Notes**: If no `tObjects` is provided, prints the usage string via `Debug.Printf` and returns.

### `Scatter(sObject, nNumber, nOffset, nTime, nDistance, nHeight)`
Spawns `nNumber` copies of a template near a point in front of the camera, spread out in time. Finds the base
point once with `Pg.FindPointFromCamera(nDistance, nHeight)`, spawns the first copy there immediately
(`Pg.Spawn`), then schedules the rest with `Event.TimerRelative` at evenly spaced offsets
(`nTime / nNumber * i`). Each subsequent copy's X and Z are jittered by `(math.randf()*nOffset -
math.randf()*nOffset)/2` — a small +/- wobble around the base point (`nOffset` is a jitter magnitude, not a
strict radius), while Y stays fixed.
- **Parameters**: 
  - `sObject`: The name of the object template to scatter.
  - `nNumber`: The number of objects to spawn (default `1`).
  - `nOffset`: The XZ jitter magnitude for each spawned object (default `0` — no jitter, objects stack).
  - `nTime`: The total time in seconds over which to spread the spawns (default `0` — all at once).
  - `nDistance`: Distance from the camera to the base point (default `10`).
  - `nHeight`: Height of the base point (default `0.5`).
- **Returns**: None
- **Notes**: If no `sObject` is provided, prints the usage/example string via `Debug.Printf` and returns.

## Events
- Listens for none — this module does not subscribe to any engine events.
- Fires: `Event.TimerRelative` to schedule the spawning of additional objects in the `Scatter` function.

## Notes for modders
- **These are camera-relative spawn helpers, handy from the console** — both print a usage string if called
  with no template, so `Multi()` / `Scatter()` alone tell you the argument shape. Example from source:
  `Scatter('assault rifle', 3, 0, 6)` stacks 3 assault rifles, one every two seconds.
- `Multi`'s `10`/`0.5` distance/height are hardcoded; `Scatter` exposes them as `nDistance`/`nHeight`
  (defaults `10`/`0.5`). Use `Scatter` if you need to control where the objects land.
- Templates must be real spawnable object names (the same names used elsewhere with `Pg.Spawn` /
  `Pg.SpawnFromCamera`); a bad name just fails to spawn.