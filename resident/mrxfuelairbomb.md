---
title: MrxFuelAirBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: 'deeper pass: documented the "distance"-triggered drop (nSpeedScale 60), the two-stage ignition→fireball chain with all its particle/light template strings and the exp_oiltrucker sound cue, flagged the Test() dev helper and that only the smoke designator of the three imports is used; cross-linked Airstrike/MrxSupport'
---

# MrxFuelAirBomb

*Module: mrxfuelairbomb.lua*

## Overview
`MrxFuelAirBomb` is the thermobaric support weapon. It drops a **"Fuel Air Bomb Projectile"** that detonates
by **distance-to-target** rather than on impact, then plays a distinctive **two-stage** effect: an initial
airburst + debris, a ~1.6 s pause, then an **ignition** (light + `exp_oiltrucker` sound) and finally a
ground-hugging **fireball**. Extends [`MrxSupport`](mrxsupport). The screen-flash grade is the separate
[Airstrike_Atmosphere_FuelAirBomb](airstrike_atomsphere_fuelairbomb) object (whose 1.75 s delay is timed to
this ignition).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke),
  [`MrxSupportDesignatorLaser`](mrxsupportdesignatorlaser),
  [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite) — **only the smoke designator is actually
  instantiated**; the laser/satellite imports are unused in this file.

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support action.
- `sRecruit`: The type of recruit required for this support action, set to "Pilot".
- `oDesignator`: The designator used to target the bomb drop location.
- `sModuleName`: The name of the module, set to "MrxFuelAirBomb".
- `sDeliveryVehicle`: The name of the delivery vehicle used for the airstrike.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the jet performing the flyby.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Module constants & templates
No module-level named constants — all templates are literals in the effect chain:
- Ordnance: `"Fuel Air Bomb Projectile"` (velocity scale `nSpeedScale = 60`; detonation trigger
  `"distance"` with `nDistance = Math.Length(vector) - 24`, i.e. it explodes 24 units short of the target).
- Airburst particles (via `Airstrike.SpawnDirectedObject`): `"global_particle_airstrike_fuelairbomb"`,
  `"global_particle_explosion_flash_large"`.
- Ignition stage: `"Light_airstrike_fuelairbomb_sml"`, `"global_particle_exp_falling_debris_airstrike"`,
  plus sound cue `Sound.CueSound(0, "exp_oiltrucker")`.
- Fireball stage: `"Explosion (Fuel Air Bomb)"`, `"Light_airstrike_fuelairbomb_lrg_flash"`,
  `"global_particle_exp_shockwave_ground"`.

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a smoke designator (`SetValidationFunction(nil)`, `"basic"` AA test,
`SetTargetValidationRequired(false)`, `SetSmokeColor("red")`), sets owner / recruit `"Pilot"` / module name,
and copies the delivery-vehicle fields onto the instance.

### `DesignationCallback(self)`
Computes an approach and a set of offset vectors, flies the jet with `Airstrike.Flyby(…, 200, DropBomb,
{self})`, and plays a Misha VO (cues 06/07/16/24).

### `DropBomb(self)`
Reads jet + designator target, computes `nDistance = length(vector) - 24`, normalizes the direction, and
fires:
```lua
self.uSpawnedBomb = Airstrike.SpawnOrdnance("Fuel Air Bomb Projectile", nX, nY-5, nZ,
  nVX*60, nVY*60, nVZ*60, "distance", nDistance, self.uOwner, BombExplodes, {self, "distance"})
```
The `"distance"`/`nDistance` pair is what gives the fuel-air its **airburst** rather than a ground impact.

### `BombExplodes(self, sTrigger)`
First stage. Spawns the airburst + flash via `Airstrike.SpawnDirectedObject` (oriented back along the flight
vector), then schedules `Ignition` **1.6 s** later.

### `Ignition(nBombX … nVectorZ)`
Second stage. Spawns the ignition light + falling-debris particle at the target, plays
`Sound.CueSound(0, "exp_oiltrucker")`, and schedules `Fireball` **0.15 s** later.

### `Fireball(nBombX … nVectorZ)`
Final stage. Spawns `"Explosion (Fuel Air Bomb)"`, the large flash light, and a ground shockwave —
the visible thermobaric burst.

### `Test(nVZ, nVY, nVZ, nTargetX, nTargetY, nTargetZ)`
**Dev helper** — spawns a lone `"global_particle_airstrike_fuelairbomb"` at given coords. Not called by the
weapon; note its params are mistyped (`nVZ` declared twice), so it's clearly leftover debug scaffolding.

## Events
- **No `Event.Create` subscriptions.** The staged effect is driven entirely by `Event.TimerRelative`
  scheduling: `BombExplodes → +1.6 s → Ignition → +0.15 s → Fireball`. `DesignationCallback`/`DropBomb` are
  wired by the parent designation flow and the `Airstrike.Flyby`/`SpawnOrdnance` callbacks.

## Notes for modders
- **The `"distance"` detonation + `nDistance - 24` is the fuel-air's defining behavior** — change the `- 24`
  (in an override of `DropBomb`, a plain global) to burst higher or closer, or switch the trigger to
  `"impact"` for a ground detonation.
- The whole look is a **timer chain of particle spawns** (1.6 s then 0.15 s) — retime or reskin it by
  overriding `BombExplodes`/`Ignition`/`Fireball` (all plain globals) and swapping the template strings above.
- The `exp_oiltrucker` sound cue is the ignition "whoomph"; swap it in `Ignition` for a different blast SFX.
- `Test()` is safe to call from a dev/`OnKey` script to preview the airburst particle; it is not part of the
  live weapon.