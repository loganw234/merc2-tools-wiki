---
title: AirstrikeAtomsphereBombrun
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [airstrike, atmosphere]
verified: true
verified_note: 'deeper pass: reframed as a screen-tint/atmosphere override (NOT an ordnance spawner) — surfaced the full Graphics.Atmosphere tunable set, cross-linked Graphics/Event/mrxbombingrun, pruned boilerplate'
---

# AirstrikeAtomsphereBombrun

*Module: airstrike_atomsphere_bombrun.lua*

## Overview
This module is the **screen-grade / post-process flash** for the Bombing Run airstrike — it does **not**
spawn the bomb. When the effect object is activated it briefly overrides the global
[`Graphics.Atmosphere`](../namespaces/graphics) settings (ambient light, bloom, light intensity) to punch
up the moment of detonation, then lets the engine restore the previous look. The actual ordnance for this
weapon is dropped by [MrxBombingRun](mrxbombingrun) via [`Airstrike.SpawnOrdnance`](../namespaces/airstrike);
one of the game's `atomsphere` effect objects is spawned alongside it purely for the visual punch.

{: .note }
> `atomsphere` is a typo baked into the real in-game module/object name (it means *atmosphere*). It is
> **not** a mistake in this wiki — do not "correct" it or the object lookup will fail.

## Inheritance
- Inherits from: `none`
- Imports: `none`

## Instance pattern
Stateless utility module — no per-instance table, no `uGuid` keying, no module-level state. It reacts to a
single engine `OnActivate` lifecycle call and does its work through two top-level functions.

## Functions
### `OnActivate(guid)`
Engine lifecycle callback fired when the effect object is activated. Schedules `_GraphicsAto` 0.1 s later
via `Event.Create(Event.TimerRelative, {0.1}, _GraphicsAto, {guid})`. (`OnActivate` is called by the
engine, not by a modder.)

### `_GraphicsAto(guid)`
Opens a scoped `Graphics.Atmosphere.Begin()` block, pushes a fixed set of `SetValue`/`SetColorValue`
overrides, then `Graphics.Atmosphere.End()`. `guid` is accepted but unused in this variant. See the
tunables below for the exact values.

## Module constants & tunables
All values are hardcoded literals inside `_GraphicsAto` (there are no module-level named constants — to
change them you override the whole function). The distinctive ones for *this* variant:

| `Graphics.Atmosphere` key | Value | Effect |
|---|---|---|
| `fAtmosphereLimit` | `125` | Lower than the other bomb variants (200–400) — a tighter haze reach. |
| `fBloomAmount` / `fBloomMultiplier` | `0.75` / `0.55` | Moderate bloom punch. |
| `fLightIntensity` | `1.55` | Slight over-bright flash. |
| `fTimeRestore` | `0.5` | Seconds to blend the atmosphere back to normal — the shortest of the family (this is a quick flash, vs. `5.5` for the tact-nuke). |

All ambient/cube/rim colors are set to neutral grey `128,128,128,255`; two gradient stops are zeroed
(`uiGradient0_Color2`, `uiGradient1_Color1` → `0,0,255,0`).

## Events
- **Not an `Event.Create` subscription.** The only `Event.*` use is scheduling: `Event.TimerRelative`
  fires `_GraphicsAto` once, 0.1 s after activation. `OnActivate` itself is an engine lifecycle callback,
  not an event subscription.

## Notes for modders
- **This is the "make the explosion flash look different" lever, nothing more.** Override `_GraphicsAto`
  from an `OnLoad` script (both functions are plain non-`local` globals) to retune bloom/light/restore
  time. To change the *bomb* — template, radius, count — edit [MrxBombingRun](mrxbombingrun) instead.
- `fTimeRestore` is the knob for how long the graded look lingers; raise it for a slower "recover" after the
  blast, lower it for a snappier flash.
- Because the overrides are **global**, they affect the whole screen for every player, not just the target
  area — the short `fTimeRestore` is what keeps that from being obtrusive.