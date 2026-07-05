---
title: AirstrikeAtomsphereCarpetbomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint override (not an ordnance spawner), documented the ShieldFace 150-unit reaction, surfaced the darker carpet-bomb Atmosphere tunables, cross-linked mrxcarpetbomb/MrxUtil/Graphics'
---

# AirstrikeAtomsphereCarpetbomb

*Module: airstrike_atomsphere_carpetbomb.lua*

## Overview
This is the **screen-grade / post-process flash** for the Carpet Bomb airstrike — it does **not** spawn
any bomblets. On activation it overrides the global [`Graphics.Atmosphere`](../namespaces/graphics) look
for a moment, then also makes nearby player characters flinch and shield their eyes via
[`MrxUtil.ShieldFace`](mrxutil). The bomb lines themselves are laid down by
[MrxCarpetBomb](mrxcarpetbomb). Compared to the other variants this one dials brightness/bloom *down*
(dark, smoky feel) rather than up.

{: .note }
> `atomsphere` is a typo baked into the real in-game object name (it means *atmosphere*). Leave it as-is.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
Stateless utility module — no per-instance table, no `uGuid` keying, no persistent state. Reacts to one
engine `OnActivate` call.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback. Schedules `_GraphicsAto` 0.1 s later via
`Event.Create(Event.TimerRelative, {0.1}, _GraphicsAto, {guid})`.

### `_GraphicsAto(guid)`
Runs the `Graphics.Atmosphere.Begin()` … `End()` override block (see tunables), then calls
`MrxUtil.ShieldFace(guid)`. `ShieldFace` looks up the effect object's position and, for every player whose
hero is within **150 units**, plays the `"shieldface"` action on that hero — the flinch-from-the-blast
animation. Here `guid` **is** used (it's the anchor for that distance check).

## Module constants & tunables
Hardcoded literals inside `_GraphicsAto` (no named module constants). Notable for *this* variant:

| `Graphics.Atmosphere` key | Value | Effect |
|---|---|---|
| `fAtmosphereLimit` | `200` | Standard haze reach. |
| `fBloomAmount` / `fBloomMultiplier` | `0.1` / `0.08` | Very low bloom — the darkest of the family. |
| `fLightIntensity` | `0.25` | Dims the scene (smoke/soot feel), opposite of the nuke variants. |
| `fTimeRestore` | `0.6` | Quick blend back to normal. |

Ambient/cube/rim colors are neutral grey `128,128,128,255`; this variant does **not** touch the gradient
stops.

## Events
- **Not an `Event.Create` subscription.** `Event.TimerRelative` schedules `_GraphicsAto` once, 0.1 s after
  activation. `OnActivate` is an engine lifecycle callback.

## Notes for modders
- Override `_GraphicsAto` (a plain global) to retune the grade or to drop the `ShieldFace` flinch.
- The **150-unit** radius in `MrxUtil.ShieldFace` is the trigger distance for the eye-shield animation —
  change it in [`mrxutil`](mrxutil) (shared by every ShieldFace-using bomb), not here.
- To change the actual bomb pattern/count, edit [MrxCarpetBomb](mrxcarpetbomb) — this file is visuals only.