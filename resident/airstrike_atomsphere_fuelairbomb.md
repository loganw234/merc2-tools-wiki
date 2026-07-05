---
title: Airstrike_Atmosphere_FuelAirBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint override (not an ordnance spawner), documented the 1.75s delay (times the two-stage fuel-air detonation) and ShieldFace, surfaced the Atmosphere tunables, cross-linked mrxfuelairbomb/MrxUtil/Graphics'
---

# Airstrike_Atmosphere_FuelAirBomb

*Module: airstrike_atomsphere_fuelairbomb.lua*

## Overview
This is the **screen-grade / post-process flash** for the Fuel-Air Bomb airstrike — it does **not** spawn
the bomb. On activation it waits **1.75 s** (longer than every other variant), then overrides the global
[`Graphics.Atmosphere`](../namespaces/graphics) look and makes nearby heroes shield their eyes via
[`MrxUtil.ShieldFace`](mrxutil). The 1.75 s delay lines up with the fuel-air weapon's characteristic
*delayed secondary ignition*: [MrxFuelAirBomb](mrxfuelairbomb) drops the projectile, sprays fuel, then
ignites the fireball on its own timers — this grade is meant to hit at the ignition, not the initial drop.

{: .note }
> `atomsphere` is a typo baked into the real in-game object name (it means *atmosphere*). Leave it as-is.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
Stateless utility module — no per-instance table, no `uGuid` management, no persistent state. Reacts to one
engine `OnActivate` call.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback. Schedules `_GraphicsAto` **1.75 s** later via
`Event.Create(Event.TimerRelative, {1.75}, _GraphicsAto, {guid})` — the delay is what distinguishes this
from the other variants (which fire at 0.1–0.15 s).

### `_GraphicsAto(guid)`
Runs the `Graphics.Atmosphere.Begin()` … `End()` override block (see tunables), then calls
`MrxUtil.ShieldFace(guid)` — plays the `"shieldface"` action on every player hero within **150 units** of
`guid`.

## Module constants & tunables
Hardcoded literals inside `_GraphicsAto` (no named module constants). Notable for *this* variant:

| Constant | Value | Effect |
|---|---|---|
| `OnActivate` delay | `1.75` s | Times the grade to the fuel-air *ignition*, not the drop. |
| `fAtmosphereLimit` | `200` | Standard haze reach. |
| `fBloomAmount` / `fBloomMultiplier` | `1` / `0.8` | Max bloom (bright fireball). |
| `fLightIntensity` | `2.5` | Strong over-bright flash. |
| `fTimeRestore` | `1.7` | Blends back over ~1.7 s. |

Ambient/cube/rim colors are neutral grey `128,128,128,255`; gradient stops `uiGradient0_Color2` /
`uiGradient1_Color1` are zeroed to `0,0,255,0`.

## Events
- **Not an `Event.Create` subscription.** `Event.TimerRelative` schedules `_GraphicsAto` once, 1.75 s
  after activation. `OnActivate` is an engine lifecycle callback.

## Notes for modders
- **The 1.75 s `OnActivate` delay is the interesting knob here** — override `OnActivate` if you want the
  grade to hit sooner/later relative to the fuel-air ignition sequence in [MrxFuelAirBomb](mrxfuelairbomb).
- Override `_GraphicsAto` (a plain global) to retune the grade or drop the `ShieldFace` flinch (150-unit
  radius, defined in [`mrxutil`](mrxutil)).