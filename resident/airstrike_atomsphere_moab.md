---
title: Airstrike_Atmosphere_MOAB
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint override (not an ordnance spawner), documented ShieldFace and the long 3s restore, surfaced the bright MOAB Atmosphere tunables, cross-linked mrxmoab/MrxUtil/Graphics'
---

# Airstrike_Atmosphere_MOAB

*Module: airstrike_atomsphere_moab.lua*

## Overview
This is the **screen-grade / post-process flash** for the MOAB (Massive Ordnance Air Blast) airstrike — it
does **not** spawn the bomb. On activation it overrides the global
[`Graphics.Atmosphere`](../namespaces/graphics) look (bright over-exposed flash), then makes nearby heroes
shield their eyes via [`MrxUtil.ShieldFace`](mrxutil). The actual ordnance is delivered by
[MrxMOAB](mrxmoab) (which inherits from [MrxDaisyCutter](mrxdaisycutter)). Its numeric grade is the same as
the daisy-cutter variant except the restore takes longer.

{: .note }
> `atomsphere` is a typo baked into the real in-game object name (it means *atmosphere*). Leave it as-is.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
Stateless utility module — no per-instance pattern, no `uGuid` keying, no persistent state. Reacts to one
engine `OnActivate` call.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback. Schedules `_GraphicsAto` 0.1 s later via
`Event.Create(Event.TimerRelative, {0.1}, _GraphicsAto, {guid})`.

### `_GraphicsAto(guid)`
Runs the `Graphics.Atmosphere.Begin()` … `End()` override block (see tunables), then calls
`MrxUtil.ShieldFace(guid)` — plays the `"shieldface"` action on every player hero within **150 units** of
`guid`.

## Module constants & tunables
Hardcoded literals inside `_GraphicsAto` (no named module constants). Notable for *this* variant:

| `Graphics.Atmosphere` key | Value | Effect |
|---|---|---|
| `fAtmosphereLimit` | `250` | Wide haze reach. |
| `fBloomAmount` / `fBloomMultiplier` | `0.84` / `0.66` | Strong bloom. |
| `fLightIntensity` | `3.75` | Big over-bright flash. |
| `fTimeRestore` | `3` | Slow ~3 s blend back — the blast look lingers longer than the daisy cutter's 1.7 s. |

Ambient/cube/rim colors are neutral grey `128,128,128,255`; gradient stops `uiGradient0_Color2` /
`uiGradient1_Color1` are zeroed to `0,0,255,0`.

## Events
- **Not an `Event.Create` subscription.** `Event.TimerRelative` schedules `_GraphicsAto` once, 0.1 s after
  activation. `OnActivate` is an engine lifecycle callback.

## Notes for modders
- `fTimeRestore` (`3`) is what makes the MOAB flash linger — bump it for an even heavier "the whole area is
  washed out" feel, or lower it toward the daisy cutter's `1.7`.
- Override `_GraphicsAto` (a plain global) to retune the grade or drop the `ShieldFace` flinch (150-unit
  radius, defined in [`mrxutil`](mrxutil)).
- To change the bomb itself, edit [MrxMOAB](mrxmoab) — this file is visuals only.