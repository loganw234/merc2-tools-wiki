---
title: MrxStrategicMissile
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, missile]
verified: true
verified_note: "deeper pass: surfaced the four module-level template locals, documented the two-stage launch (launch projectile -> ActivateDelay -> DropBomb -> BombExplodes) and the 6-cone shrapnel burst; cross-linked Airstrike/beacon"
---

# MrxStrategicMissile

*Module: mrxstrategicmissile.lua*

## Overview
`MrxStrategicMissile` is a beacon-designated, big-single-warhead strike: a launch projectile fires up near the player, a short delay later the real warhead drops onto the beacon, detonates with an explosion effect, and sprays six cones of shrapnel outward. It inherits from [`MrxSupport`](mrxsupport) and uses [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon) to target.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns the missile.
- `uSpawnedBomb`: The GUID of the spawned missile projectile.
- `oDesignator`: The designator beacon used to target the missile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the strategic missile using the module's prototype. Initializes the designator beacon and sets the owner, recruit, and module name.

### `DesignationCallback(self)`
Runs on beacon-designation complete. Plays a random Chinese-soldier "artillery/incoming" VO line, and chains `MissileLaunch` as the *second element of the same [`MrxVoSequence.Start`](mrxvosequence) sequence table* — so the launch is kicked off by the VO sequencer, not called directly.

### `MissileLaunch(self)`
Spawns the launch projectile (`"Strategic Missile Projectile Launch"`) near the camera via [`Airstrike.SpawnOrdnance`](../namespaces/airstrike) with an **upward** velocity `+100` and `"distance"` detonation `500`, passing `ActivateDelay` as its spawn callback. This is the visible "rocket goes up" stage.

### `ActivateDelay(self, uProjectileGuid)`
Waits 2 seconds ([`Event.TimerRelative`](../namespaces/event)), then calls `self.DropBomb` — the gap between launch-up and warhead-down.

### `DropBomb(self)`
Reads the beacon target, raises `nTargetY` by 100, and spawns the real warhead (`"Strategic Missile Projectile"`) falling with velocity `-100`, `"distance"` detonation `80`, callback `BombExplodes`. Stores the handle in `self.uSpawnedBomb`.

### `BombExplodes(self)`
The payoff. Logs the target coords (Debug.Printf noise), spawns `"Explosion (Strategic Missile)"` at the bomb, `Object.Kill`s the warhead, removes the beacon object if `Player.IsLocal(self.uOwner)`, then fires **six** [`Airstrike.ConeSpawn`](../namespaces/airstrike) shrapnel bursts of `"Strategic Missile Shrapnel"` at spread angles 5°/30°/45°/60°/75°/90° (counts 2,3,3,3,3,4) directed away from the impact along the bomb→target vector.

## Events
No event subscriptions. `DesignationCallback` is the beacon's completion callback (via [`MrxSupport:Commence`](mrxsupport)). The two-stage delay uses [`Event.TimerRelative`](../namespaces/event) (the 2s in `ActivateDelay`); the rest of the chain is driven by ordnance spawn callbacks.

## Module constants & tunables
Unlike the artillery modules, the payload names here are true module-level `local`s (top of file), so they are **not** reachable from outside — overriding the whole firing function is the only way to change them:
- `sProjectileName = "Strategic Missile Projectile"` (the warhead)
- `sProjectileLaunchName = "Strategic Missile Projectile Launch"` (the launch stage)
- `sShrapnelName = "Strategic Missile Shrapnel"`
- `sExplosionName = "Explosion (Strategic Missile)"`

Other bakes: launch velocity `+100` / detonation `"distance" 500`; warhead velocity `-100` / detonation `"distance" 80`; `ActivateDelay` 2s; six shrapnel cones (see `BombExplodes`).

## Notes for modders
- Because the four payload names are `local`, a field reassignment won't work here — override `MissileLaunch`/`DropBomb`/`BombExplodes` (all plain globals) to change the projectile, explosion, or shrapnel. See the [`local`-is-unreachable note on the Airstrike page](../namespaces/airstrike).
- The shrapnel cone pattern in `BombExplodes` is the tuning knob for "how deadly the blast footprint is" — add/remove [`Airstrike.ConeSpawn`](../namespaces/airstrike) calls or change the angle/count triples.
- `ActivateDelay`'s 2s timer is the only reason there's a visible arc; drop it and the warhead falls the instant the launch spawns.