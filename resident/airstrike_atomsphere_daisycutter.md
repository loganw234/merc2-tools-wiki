---
title: Airstrike_Atmosphere_Daisycutter
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint override (not an ordnance spawner), documented the ShieldFace 150-unit reaction, surfaced the bright daisy-cutter Atmosphere tunables, cross-linked mrxdaisycutter/MrxUtil/Graphics'
---

# Airstrike_Atmosphere_Daisycutter

*Module: airstrike_atomsphere_daisycutter.lua*

## Overview
This is the **screen-grade / post-process flash** for the Daisy Cutter airstrike — it does **not** spawn
the bomb. On activation it overrides the global [`Graphics.Atmosphere`](../namespaces/graphics) look
(bright over-exposed flash) for a moment, then makes nearby player heroes flinch and shield their eyes via
[`MrxUtil.ShieldFace`](mrxutil). The actual ordnance is delivered by [MrxDaisyCutter](mrxdaisycutter).

{: .note }
> `atomsphere` is a typo baked into the real in-game object name (it means *atmosphere*). Leave it as-is.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
Stateless utility module — no per-instance tables, no `uGuid` management, no persistent state. Reacts to
one engine `OnActivate` call.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback. Schedules `_GraphicsAto` 0.1 s later via
`Event.Create(Event.TimerRelative, {0.1}, _GraphicsAto, {guid})`.

### `_GraphicsAto(guid)`
Runs the `Graphics.Atmosphere.Begin()` … `End()` override block (see tunables), then calls
`MrxUtil.ShieldFace(guid)`, which plays the `"shieldface"` action on every player hero within **150 units**
of `guid` (the flinch-from-the-blast animation).

## Module constants & tunables
Hardcoded literals inside `_GraphicsAto` (no named module constants). Notable for *this* variant:

| `Graphics.Atmosphere` key | Value | Effect |
|---|---|---|
| `fAtmosphereLimit` | `250` | Wider haze reach than the standard 200. |
| `fBloomAmount` / `fBloomMultiplier` | `0.84` / `0.66` | Strong bloom. |
| `fLightIntensity` | `3.75` | Big over-bright flash (matches the MOAB variant). |
| `fTimeRestore` | `1.7` | Blends back over ~1.7 s. |

Ambient/cube/rim colors are neutral grey `128,128,128,255`; gradient stops `uiGradient0_Color2` /
`uiGradient1_Color1` are zeroed to `0,0,255,0`. (Identical numeric grade to the MOAB variant except
`fTimeRestore`.)

## Events
- **Not an `Event.Create` subscription.** `Event.TimerRelative` schedules `_GraphicsAto` once, 0.1 s after
  activation. `OnActivate` is an engine lifecycle callback.

## Notes for modders
- Override `_GraphicsAto` (a plain global) to retune the grade or to drop the `ShieldFace` flinch.
- The **150-unit** eye-shield radius lives in [`mrxutil`](mrxutil)'s `ShieldFace` (shared by several bomb
  effects); change it there, not here.
- To change the bomb itself, edit [MrxDaisyCutter](mrxdaisycutter) — this file is visuals only.