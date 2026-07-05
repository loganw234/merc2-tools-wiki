---
title: AirstrikeAtomsphereClusterbomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint override (not an ordnance spawner), surfaced the high-bloom cluster-bomb Atmosphere tunables, cross-linked Graphics/Event/mrxclusterbomb'
---

# AirstrikeAtomsphereClusterbomb

*Module: airstrike_atomsphere_clusterbomb.lua*

## Overview
This module is the **screen-grade / post-process flash** for the Cluster Bomb airstrike — it does **not**
spawn any bomblets. On activation it overrides the global [`Graphics.Atmosphere`](../namespaces/graphics)
look (max bloom, neutral ambient) for a moment, then lets the engine restore the previous state. The
actual ordnance and its cone of bomblets are handled by [MrxClusterBomb](mrxclusterbomb) via
[`Airstrike.SpawnOrdnance`](../namespaces/airstrike)/`Airstrike.ConeSpawn`.

{: .note }
> `atomsphere` is a typo baked into the real in-game object name (it means *atmosphere*). Leave it as-is.

## Inheritance
- Inherits from: `none`
- Imports: `none`

## Instance pattern
Stateless utility module — no `Create`/instance pattern, no `uGuid` keying, no persistent state. Reacts to
one engine `OnActivate` call.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback. Schedules `_GraphicsAto` 0.1 s later via
`Event.Create(Event.TimerRelative, {0.1}, _GraphicsAto, {guid})`.

### `_GraphicsAto(guid)`
Runs the `Graphics.Atmosphere.Begin()` … `End()` override block (see tunables). `guid` is accepted but
unused (no `ShieldFace` in this variant).

## Module constants & tunables
Hardcoded literals inside `_GraphicsAto` (no named module constants). Notable for *this* variant:

| `Graphics.Atmosphere` key | Value | Effect |
|---|---|---|
| `fAtmosphereLimit` | `200` | Standard haze reach. |
| `fBloomAmount` / `fBloomBlurRadius` / `fBloomThreshold` | `1` | Bloom pinned to max — bright, hazy flash. |
| `fBloomMultiplier` | `0.8` | Strong bloom output. |
| `fLightIntensity` | `1` | Neutral scene light. |
| `fTimeRestore` | `1.7` | Blends back over ~1.7 s. |

Ambient/cube/rim colors are neutral grey `128,128,128,255`; gradient stops `uiGradient0_Color2` /
`uiGradient1_Color1` are zeroed to `0,0,255,0`.

## Events
- **Not an `Event.Create` subscription.** `Event.TimerRelative` schedules `_GraphicsAto` once, 0.1 s after
  activation. `OnActivate` is an engine lifecycle callback.

## Notes for modders
- Override `_GraphicsAto` (a plain global) from an `OnLoad` script to retune bloom/light/restore time.
- These overrides are **global** — they hit every player's screen, not just the strike zone. `fTimeRestore`
  controls how long the graded look lingers.
- To change the bomblet count/spread, edit [MrxClusterBomb](mrxclusterbomb) — this file is visuals only.