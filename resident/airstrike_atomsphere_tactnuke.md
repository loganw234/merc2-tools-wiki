---
title: AirstrikeAtomsphereTactNuke
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint override (not an ordnance spawner), documented ShieldFace and the extreme nuke grade (fLightIntensity 6 / fTimeRestore 5.5 — the strongest of the family), cross-linked mrxbunkerbuster/MrxUtil/Graphics'
---

# AirstrikeAtomsphereTactNuke

*Module: airstrike_atomsphere_tactnuke.lua*

## Overview
This is the **screen-grade / post-process flash** for the tactical-nuke effect — it does **not** detonate
anything. On activation it overrides the global [`Graphics.Atmosphere`](../namespaces/graphics) look with
the most extreme grade of the whole airstrike family (blinding light, huge bloom, a slow ~5.5 s recovery),
then makes nearby heroes shield their eyes via [`MrxUtil.ShieldFace`](mrxutil). The "nuke" itself is the
*Nuclear* branch of [MrxBunkerBuster](mrxbunkerbuster) — its `FinalExplosion` spawns
`global_particle_airstrike_tactnuke` and posts a `"Nuked"` event; this module supplies the whiteout flash.

{: .note }
> `atomsphere` is a typo baked into the real in-game object name (it means *atmosphere*). Leave it as-is.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
Stateless utility module — no per-instance tables, no `uGuid` keying, no persistent state. Reacts to one
engine `OnActivate` call.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback. Schedules `_GraphicsAto` **0.15 s** later via
`Event.Create(Event.TimerRelative, {0.15}, _GraphicsAto, {guid})`.

### `_GraphicsAto(guid)`
Runs the `Graphics.Atmosphere.Begin()` … `End()` override block (see tunables), then calls
`MrxUtil.ShieldFace(guid)` — plays the `"shieldface"` action on every player hero within **150 units** of
`guid`.

## Module constants & tunables
Hardcoded literals inside `_GraphicsAto` (no named module constants). This variant is the strongest grade
in the family:

| `Graphics.Atmosphere` key | Value | Effect |
|---|---|---|
| `fAtmosphereLimit` | `400` | Widest haze reach of any variant. |
| `fBloomAmount` | `2` | Double the normal max — pushes into full whiteout. |
| `fBloomMultiplier` | `1.8` | Heaviest bloom output. |
| `fLightIntensity` | `6` | Blinding flash (others top out at 3.75). |
| `fTimeRestore` | `5.5` | Longest recovery — the washed-out look lingers ~5.5 s. |

Ambient/cube/rim colors are neutral grey `128,128,128,255`; gradient stops `uiGradient0_Color2` /
`uiGradient1_Color1` are zeroed to `0,0,255,0`.

## Events
- **Not an `Event.Create` subscription.** `Event.TimerRelative` schedules `_GraphicsAto` once, 0.15 s after
  activation. `OnActivate` is an engine lifecycle callback.

## Notes for modders
- This is the "nuke whiteout" grade. `fLightIntensity` (`6`) and `fTimeRestore` (`5.5`) are the two knobs
  that make it feel nuclear — dial them down toward the other variants for a subtler blast, or up for an
  even longer blind.
- Override `_GraphicsAto` (a plain global) to retune, or drop the `ShieldFace` flinch (150-unit radius,
  defined in [`mrxutil`](mrxutil)).
- The nuclear detonation logic lives in [MrxBunkerBuster](mrxbunkerbuster)'s `FinalExplosion`, not here.