---
title: Weapon
parent: Engine Namespaces
nav_order: 19
---

# Weapon

## Overview

`Weapon` is an **engine namespace** — no `.lua` source file, no `import()` needed, always globally
available. It manages ammo reserves for a **player's hand-held/equipped weapon**. Found (and ruled out)
while investigating whether a "vehicle weapon editor" mod was feasible — every real call site operates on
a carried weapon `uGuid`, never a vehicle. If you're looking for anything related to a vehicle's mounted
gun or turret, this isn't it — see [Vehicle](vehicle) and [Airstrike](airstrike) instead.

## Provenance

**Not a complete enumeration** — no live `pairs(Weapon)` dump has been done. Everything below comes from
grepping real call sites. There may be more functions on this namespace with no call site in the corpus;
the three below are simply the ones confirmed real and in use.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetReserveAmmo` | `n = Weapon.GetReserveAmmo(uWeapon)` | Confirmed, e.g. `resident/hero.lua:98`, `resident/soldier.lua:27`, `resident/mrxplayer.lua:671`, `vz/wiftutorialc4.lua:20` — always called with a carried/equipped weapon guid, returns its current reserve ammo count. |
| `SetReserveAmmo` | `Weapon.SetReserveAmmo(uWeapon, nAmount)` | Confirmed, e.g. `resident/hero.lua:100` (`Weapon.SetReserveAmmo(weapon, max)`, refilling to max), `vz/pmccon001.lua:134`, `vz/vzacon001.lua:91,242`, `resident/mrxsupportdesignator.lua:145` (sets to a flat `1`). Also used as an event callback directly: `resident/mrxplayer.lua:706` registers it as `Event.Create(Event.ObjectHibernation, {uEquipment, "a"}, Weapon.SetReserveAmmo, {...})`, meaning it's called by the engine's event dispatcher, not just directly by name. |
| `GetMaxReserveAmmo` | `n = Weapon.GetMaxReserveAmmo(uWeapon)` | Confirmed, always paired with `SetReserveAmmo` to refill a weapon to full: `Weapon.SetReserveAmmo(uWeapon, Weapon.GetMaxReserveAmmo(uWeapon))` (`vz/vzacon001.lua:91,242`, `vz/pmccon001.lua:134`). |

## Notes for modders

- **Every confirmed call site operates on a carried player weapon guid** (`weapon`, `uWeaponGuid`,
  `uEquipment`, `uPrimary` in the variable names at each real call site) — never a vehicle guid. This
  namespace has no relationship to vehicle turrets/mounted guns.
- The "refill to max" pattern (`Weapon.SetReserveAmmo(uWeapon, Weapon.GetMaxReserveAmmo(uWeapon))`) appears
  identically across multiple unrelated missions (`pmccon001.lua`, `vzacon001.lua`) — a safe, confirmed
  one-liner if you want to refill a player's current weapon's reserve ammo from a mod.
