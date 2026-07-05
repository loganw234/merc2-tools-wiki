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
available. Treat the function list below as "at least this many," not "exactly this many" — the
opposite confidence direction from a page like [Vehicle](vehicle) or [Marker](marker), which start from a
live dump and are genuinely complete.

`SpawnOrdnance`/`SpawnTargettedOrdnance` are the single-projectile primitives; the rest of the list are
the delivery/spread/tool helpers the airstrike modules build on top of them. The usual pipeline is
**`Flyby`** (spawn a strike plane and fly it to the target) → its **drop callback** → one or more
**`SpawnOrdnance`/`ConeSpawn`/`SpawnCarpetBombLine`** calls at the drop point.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SpawnOrdnance` | `uOrdnanceGuid = Airstrike.SpawnOrdnance(vTemplate, nX, nY, nZ, nVelX, nVelY, nVelZ, vDetonation, nParam, [uOwner], [fCallback], [tCallbackArgs])` | The core call. `vTemplate` is a **named ordnance template string** (e.g. `"Gunship Shell"`) matched against something compiled into the engine, not a Lua data structure — see the catalog below. Position and velocity are plain numeric triples. **The tail of the argument list is not consistent across real call sites** — some pass `"impact"`/a distance number directly as argument 8; others insert a target `uGuid` first (e.g. `mrxbombingrun.lua:42`: `Airstrike.SpawnOrdnance(sProjectileName, nSpawnX, nSpawnY, nSpawnZ, nVectorX*nSpeedScale, nVectorY*nSpeedScale, nVectorZ*nSpeedScale, uTarget, "impact", nil, self:GetOwner(), BombExplodes, {self})`). Don't assume a single fixed signature — check the specific call site you're modeling your own call after. Returns an ordnance object guid. |
| `SpawnTargettedOrdnance` | `uOrdnanceGuid = Airstrike.SpawnTargettedOrdnance(vTemplate, nX, nY, nZ, nVelX, nVelY, nVelZ, uTarget, vDetonation, nParam, [uOwner], [fCallback], [tCallbackArgs])` | Same shape as `SpawnOrdnance` but always takes an explicit `uTarget` guid — used for homing/guided ordnance (missiles) rather than ballistic ordnance (bombs/shells). Confirmed e.g. `mrxharmstrike.lua:70`: `Airstrike.SpawnTargettedOrdnance("Vehicle AT Missile", nSpawnX, nSpawnY, nSpawnZ, nVectorX*nSpeedScale, nSpeedScale, nVectorZ*nSpeedScale, uTarget, "impact", 1, nil, BombExplodes, {uBomb})`. |
| `Flyby` | `uJet = Airstrike.Flyby(vDeliveryVehicle, nStartX, nStartZ, nEndX, nEndZ, nY, nSpeed, [fDropCallback], [tCallbackArgs])` | The **strike-plane run that most airstrikes ride on** (17 call sites — the single most-used call here after the two spawners). Spawns a delivery aircraft that flies from a start point to an end point and invokes `fDropCallback` at the drop point, where the module then does the actual `SpawnOrdnance`/`ConeSpawn`/`SpawnCarpetBombLine`. **Watch the argument order: two XZ pairs, then Y** — `(startX, startZ, endX, endZ, Y, speed)`, not XYZ triples. `vDeliveryVehicle` is either a template string (`"Support Vehicle (B2)"`, `"Support Vehicle (Cruise Missile)"`) or a per-instance `self.uDeliveryVehicle` field. Callback + args are optional — `mrxfactionmanager.lua:1552` omits them. Speeds seen 50–200. Returns the jet guid. Call sites incl. `mrxbombingrun.lua:25`, `mrxcarpetbomb.lua:27`, `mrxcombatairpatrol.lua:25`, `mrxcruisemissile.lua:45`, `mrxfuelairbomb.lua:41`. |
| `ConeSpawn` | `Airstrike.ConeSpawn(vTemplate, nX, nY, nZ, nDirX, nDirY, nDirZ, nConeAngleDeg, nSpeed, nCount)` | Spawns `nCount` ordnance objects of `vTemplate` in a **cone** of half-angle `nConeAngleDeg` degrees around the direction vector — the cluster/shrapnel spread. Modules stack several calls with widening angles + counts for a denser pattern: `mrxclusterbomb.lua:55-56` fires a `15°/10` ring then a `30°/20` ring; `mrxsatclusterbomb.lua:58-61` stacks four (10°/15°/30°/50°); `mrxstrategicmissile.lua:63-64` two. Template is `"Cluster Bomblet Projectile"` in the cluster modules, `sShrapnelName` in the strategic missile. No return value used. |
| `SpawnCarpetBombLine` | `nNextX, nNextZ = Airstrike.SpawnCarpetBombLine(nX, nY, nZ, nHeading, uOwner, nil, nSpacing, nCount)` | Drops one row of a carpet-bomb pattern along `nHeading` and **returns the next row's start XZ**, so the caller walks it in a loop. Only call site is `mrxcarpetbomb.lua` — `:36` seeds the line, `:47` continues from `oAirstrike.nNextX/nNextZ`; the `nil` 6th arg and trailing `5, 15` (spacing & per-row count) are inferred from that single usage, so treat the exact tail as less certain than the higher-traffic calls above. |
| `SpawnDirectedObject` | `uObject = Airstrike.SpawnDirectedObject(vTemplate, nX, nY, nZ, nDirX, nDirY, nDirZ)` | Spawns a **directed effect/particle object** (not ordnance) oriented along the direction vector — used for oriented explosion/fireball FX. Here `vTemplate` is a `global_particle_*` name, **not** an ordnance-template string (e.g. `mrxfuelairbomb.lua:66-67,82`: `"global_particle_airstrike_fuelairbomb"`, `"global_particle_explosion_flash_large"`). Returns the spawned object guid. |
| `EquipDesignator` | `uWeaponGuid = Airstrike.EquipDesignator(uOwner, sDesignationType, [fCallback], [tCallbackArgs], bFireImmediately)` | Equips a **target-designator "weapon"** on `uOwner` — the tool the player aims to call in a strike (laser / smoke / flare / satellite / beacon; see the [Support & Airstrikes](../resident/cat-support-airstrikes) designator family). `sDesignationType` is a per-instance string; `fCallback`/`tCallbackArgs` fire when designation completes (`LaserFinished`, `BeginSatelliteDesignation`; `nil` = fire-and-forget); `bFireImmediately` skips the aim step. Call sites: `mrxsupportdesignator.lua:143` (base), `mrxsupportdesignatorlaser.lua:35`, `mrxsupportdesignatorsatellite.lua:64`. Returns the equipped weapon guid. |

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
