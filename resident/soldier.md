---
title: Soldier
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, pickup]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (one OnDeath, zero Event.* calls); collected the pickup template strings + the every-3rd-death / label / ammo / health drop rules into a constants section; re-confirmed tDrops/tEvents are dead and the lowercase math.* usage; cross-linked Object/Player/Weapon/Pg namespaces.'
---

# Soldier

*Module: soldier.lua*

## Overview
The `Soldier` module is the death handler for AI foot soldiers: when one dies, it decides whether to
drop a pickup and which kind (ammo / grenades / health), based on the soldier's class labels, a
one-in-three throttle, and the players' current ammo/health. This is the system that makes enemies
"conveniently" drop what you're low on.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxUtil`](mrxutil) — imported but not referenced in this file.

## Instance pattern
This is a stateless manager/utility module with no per-instance tables. It tracks the following key fields:
- `deathCount`: a module-level counter (`local`, but persists across calls since it's declared outside any
  function), incremented on every `OnDeath` call regardless of soldier type or whether a pickup spawns.
- `tDrops`: declared (`tDrops[0] = "Ammo Pickup (Bullet)"`, `tDrops[1] = "Ammo Pickup (Rocket)"`) but
  **never read anywhere in this file** — `OnDeath` picks `sPickup` via hardcoded string literals instead.
  Dead/unused table, likely leftover from an earlier version of the logic.
- `tEvents`: also declared (`local tEvents = tEvents or {}`) and also never referenced again anywhere in
  the file — same story, unused leftover.

## Functions
### `OnDeath(uGuid, iArg)`
Called when a soldier instance dies. Increments `deathCount` unconditionally, then bails out early
(no pickup) if `Object.InSeat(uGuid)` is true. Pickup logic only runs when
`Object.HasLabel(uGuid, "HeavySoldier")` is true **or** `deathCount` is an exact multiple of 3
(`deathCount / 3 == math.floor(deathCount / 3)`):
- Default pickup is `"Ammo Pickup (Small)"`.
- Upgraded to `"Ammo Pickup (Rocket)"` if the soldier has label `RocketSoldier` **and not** `MGSoldier`
  (the `MGSoldier` check suppresses the rocket-ammo drop for that combined label case).
- Upgraded to `"Ammo Pickup (Bullet)"` if the soldier has label `HeavySoldier` (checked after the
  Rocket/MG case, so `RocketSoldier` without `MGSoldier` wins if both labels apply).
- Then, for every player in `Player.GetAllPlayers()`: if any of that player's weapons is labeled
  `"Grenade"` and its `Weapon.GetReserveAmmo(...)` is under a random threshold
  (`math.randf(8)`), pickup becomes `"Ammo Pickup (Grenades)"`. Independently, if a random roll
  (`math.randf() * 80`) exceeds that player's current health, pickup becomes `"Health Pickup"`. Both
  checks run per-player in the same loop and the last matching player's outcome wins (loop keeps
  overwriting `sPickup`, no `break`).
- Note: `math.floor`/`math.randf` here are the standard Lua `math` library (lowercase), not the engine's
  `Math` namespace (capitalized) used in other modules like `randomlyteleportplayer.lua` — both exist,
  this file just uses the lowercase one throughout.
- Spawns the chosen pickup via `Pg.Spawn(sPickup, x, y + 0.1, z, 0, false, true, uGuid)`, applies a small
  downward impulse (`Object.ApplyImpulse(uNewGuid, 0, -0.5, 0)`), and adds it to the `"pickup"` disposer.

## Events
This file contains **no `Event.*` calls at all**. `OnDeath` is invoked directly by the engine as a
naming-convention callback (same mechanism as `OnActivate`/`OnDeath` elsewhere), not through an
`Event.Create` registration in this file.

## Module constants & tunables
All of these are hardcoded inside `OnDeath` (there is no config table — `tDrops` is dead code):

- **Pickup templates**: `"Ammo Pickup (Small)"` (default), `"Ammo Pickup (Rocket)"`,
  `"Ammo Pickup (Bullet)"`, `"Ammo Pickup (Grenades)"`, `"Health Pickup"`. Spawned via
  [`Pg.Spawn`](../namespaces/pg) at the corpse position, nudged down by an impulse, and added to the
  `"pickup"` disposer.
- **Drop throttle**: a pickup is only considered when the soldier has label `"HeavySoldier"` **or**
  every 3rd soldier death (`deathCount / 3 == math.floor(deathCount / 3)`). Change the `3` to make
  drops more/less frequent.
- **Class → ammo mapping** (checked via [`Object.HasLabel`](../namespaces/object)):
  `RocketSoldier` (and not `MGSoldier`) → rocket ammo; `HeavySoldier` → bullet ammo.
- **Grenade top-up**: if a player holds a `"Grenade"`-labelled weapon whose
  [`Weapon.GetReserveAmmo`](../namespaces/weapon) is below `math.randf(8)`, drop grenades.
- **Health top-up**: if `math.randf() * 80 > Object.GetHealth(uHero)` (roughly: the lower a player's
  health, the likelier), drop a health pickup — this overrides the ammo choice.
- Soldiers that die **while seated** (`Object.InSeat`) drop nothing.

## Notes for modders
- Retune drops by editing the throttle `3`, the label→pickup mapping, and the two random thresholds
  (`math.randf(8)`, `math.randf() * 80`) directly in `OnDeath`.
- `tDrops` and `tEvents` are dead code — populated/declared but never consulted. Editing `tDrops` will
  **not** change pickup selection; the strings are inline.
- This file uses the standard Lua `math.*` library (lowercase), not the engine `Math.*` namespace —
  keep that in mind if you copy logic between modules.