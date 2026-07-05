---
title: Soldier
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, pickup]
verified: true
verified_note: removed fabricated Event.ObjectDeath claim (zero Event.* calls in file), flagged tDrops/tEvents as declared-but-unused, added MGSoldier exclusion detail to OnDeath description
---

# Soldier

*Module: soldier.lua*

## Overview
The `Soldier` module handles the death logic for soldier AI entities in the game. It determines what type of pickup to drop based on the soldier's class and the player's current state, such as health and ammo reserve.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

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

## Notes for modders
- Ensure that `OnDeath` is called appropriately to manage pickup spawning logic.
- `tDrops` is dead code — it's populated but never consulted by `OnDeath`. Don't expect editing it to
  change pickup selection; the pickup strings are hardcoded inline in the function body instead.
- Customize the pickup logic by editing the `sPickup` string literals and label/health/ammo conditions directly in `OnDeath`.
- Be aware that network synchronization (`Pg.Spawn`) may affect multiplayer behavior when spawning pickups.