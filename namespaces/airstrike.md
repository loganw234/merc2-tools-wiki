---
title: Airstrike
parent: Engine Namespaces
nav_order: 18
---

# Airstrike

## Overview

`Airstrike` is an **engine namespace** — no `.lua` source file, no `import()` needed, always globally
available. It's the one and only mechanism found anywhere in the ~230-file decompiled corpus for actually
spawning a projectile/ordnance object in the world: bombs, missiles, gunship shells, artillery rounds,
cluster bomblets, flares. Every module in this codebase that makes something fly through the air and
detonate goes through this namespace, never anything else.

Found while investigating whether a "vehicle weapon editor" mod (swap what a vehicle's turret fires) was
feasible — see the [Custom Contract deep dive](../deep-dives/custom-contract) for the unrelated mod this
was found alongside, and the conversation that motivated this page for the full verdict on that
investigation.

## Provenance

**Unlike most pages in this section, this is not a complete enumeration.** No live `pairs(Airstrike)`
dump has been done — everything here comes from grepping real call sites across the decompiled corpus.
That means: every function listed below is real and confirmed to exist and be called this way, but there
could be more functions on this namespace that simply have no call site in any of the ~230 scripts
available. Treat the two-function list below as "at least this many," not "exactly this many" — the
opposite confidence direction from a page like [Vehicle](vehicle) or [Marker](marker), which start from a
live dump and are genuinely complete.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SpawnOrdnance` | `uOrdnanceGuid = Airstrike.SpawnOrdnance(vTemplate, nX, nY, nZ, nVelX, nVelY, nVelZ, vDetonation, nParam, [uOwner], [fCallback], [tCallbackArgs])` | The core call. `vTemplate` is a **named ordnance template string** (e.g. `"Gunship Shell"`) matched against something compiled into the engine, not a Lua data structure — see the catalog below. Position and velocity are plain numeric triples. **The tail of the argument list is not consistent across real call sites** — some pass `"impact"`/a distance number directly as argument 8; others insert a target `uGuid` first (e.g. `mrxbombingrun.lua:42`: `Airstrike.SpawnOrdnance(sProjectileName, nSpawnX, nSpawnY, nSpawnZ, nVectorX*nSpeedScale, nVectorY*nSpeedScale, nVectorZ*nSpeedScale, uTarget, "impact", nil, self:GetOwner(), BombExplodes, {self})`). Don't assume a single fixed signature — check the specific call site you're modeling your own call after. Returns an ordnance object guid. |
| `SpawnTargettedOrdnance` | `uOrdnanceGuid = Airstrike.SpawnTargettedOrdnance(vTemplate, nX, nY, nZ, nVelX, nVelY, nVelZ, uTarget, vDetonation, nParam, [uOwner], [fCallback], [tCallbackArgs])` | Same shape as `SpawnOrdnance` but always takes an explicit `uTarget` guid — used for homing/guided ordnance (missiles) rather than ballistic ordnance (bombs/shells). Confirmed e.g. `mrxharmstrike.lua:70`: `Airstrike.SpawnTargettedOrdnance("Vehicle AT Missile", nSpawnX, nSpawnY, nSpawnZ, nVectorX*nSpeedScale, nSpeedScale, nVectorZ*nSpeedScale, uTarget, "impact", 1, nil, BombExplodes, {uBomb})`. |

### Confirmed ordnance template name strings

Every distinct template name found passed as the first argument, across every real call site in the
corpus (`resident/autogunship.lua`, `mrxartillery.lua`, `mrxbombingrun.lua`, `mrxclusterbomb.lua`,
`mrxcombatairpatrol.lua`, `mrxcruisemissile.lua`, `mrxfuelairbomb.lua`, `mrxgunship.lua`,
`mrxharmstrike.lua`, `mrxrocketartillery.lua`, `mrxsatclusterbomb.lua`, `mrxsmartbomb.lua`,
`mrxstrategicmissile.lua`, `mrxsupportdesignatorflare.lua`, `mrxtankbuster.lua`, `proximitymine.lua`,
`vz/allcon002.lua`):

`"Gunship Shell"`, `"Artillery Shell"`, `"Bomb"`, `"Cluster Bomb Projectile"`, `"Airstrike AA Missile"`,
`"Cruise Missile Projectile"`, `"Fuel Air Bomb Projectile"`, `"Vehicle AT Missile"`,
`"Strategic Missile Projectile"`, `"Flare Projectile Stage 2"`, `"Smart Bomb Projectile"`,
`"Airstrike AT Missile"`, `"Grenade MG Projectile"`.

A few call sites (`mrxdaisycutter.lua`, `mrxlaserguidedbomb.lua`, `mrxsatelliteguidedbomb.lua`,
`mrxsurgicalstrike.lua`) pass `self.uBomb`/`oSelf.uBomb` instead of a literal — a per-instance field set
elsewhere in those modules, not a template name visible at the call site itself; check each module
individually if you need to know its actual default.

These are matched against something compiled into the engine's own asset data — **not defined anywhere in
the Lua corpus**. You can pick which of these existing templates fires; you cannot create a new one or
edit an existing template's damage/model/visual-effect from Lua.

## Notes for modders

- **This is the mechanism to hook if you want to change what a scripted/AI shooter fires.** Every module
  above is a plain, non-`local` file — e.g. `autogunship.lua`'s `LaunchMissile` (see
  [Autogunship](../resident/autogunship)) is a normal function, safe to override from an `OnLoad` script,
  same pattern used throughout this wiki. Redirecting its `Airstrike.SpawnOrdnance("Gunship Shell", ...)`
  call to a different template string (e.g. `"Cluster Bomb Projectile"`) is a real, buildable way to change
  what that specific NPC/vehicle fires.
- **Some modules expose their ordnance choice as a settable instance field, not just a hardcoded literal.**
  `mrxartillery.lua` sets `self.sAmmo = "Artillery Shell"` in its `Create`, then calls
  `Airstrike.SpawnOrdnance(self.sAmmo, ...)` later — since `self` is a real instance table (not a `local`),
  reassigning `oInstance.sAmmo` from outside before it fires is a cleaner customization point than
  overriding the firing function itself. Several other modules (`mrxdaisycutter.lua`,
  `mrxlaserguidedbomb.lua`, `mrxsatelliteguidedbomb.lua`, `mrxsurgicalstrike.lua`) use the same pattern with
  a `self.uBomb`/`oSelf.uBomb` field. Others (`mrxbombingrun.lua`, `mrxcruisemissile.lua`,
  `mrxstrategicmissile.lua`) bake the same idea into a true module-level `local sProjectileName = "..."` —
  genuinely unreachable from outside (see the `local`-is-impossible-not-just-harder point on the
  [Overriding a Function deep dive](../deep-dives/function-override)) — those need the whole firing
  function overridden instead, not just a field reassignment.
- **This is confirmed *not* how a player-driven vehicle's own mounted gun fires.** No call site anywhere in
  the corpus connects `Vehicle.EnableTurret`/`Vehicle.SetTurretPitch` (the only turret-related natives — see
  [Vehicle](vehicle)) to `Airstrike.SpawnOrdnance`. Player-operated vehicle weapons appear to be fully
  native with no Lua touchpoint at all.
- **`AntiAir`'s homing missiles do NOT go through this namespace.** `antiair.lua` never calls `Airstrike`
  anywhere — its `_HomingLaunched` only reacts to a missile that's already been fired (radar-blip
  bookkeeping), it doesn't launch anything itself. See [AntiAir](../resident/antiair) and
  [Junk](junk#alarms--gameplay)'s `SpawnHomingProjectile` for the likely (unconfirmed) real mechanism.
