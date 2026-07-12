---
title: Human
parent: Engine Namespaces
nav_order: 10
---

# Human

## Overview

`Human` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Its functions operate on
human/character `uGuid`s and cover weapon equip and inventory management, action/animation playback,
swim and grapple state, ragdoll and knockdown, and corpse-cleanup control. A nested sub-table,
`Human.Inventory`, holds the weapon-inventory-specific subset of that functionality (see Notes for
modders below).

## Provenance

This page's function list comes from a live `pairs(Human)` enumeration in-game, not from reading engine
source — the engine implementation isn't available to us. That dump gives names and raw function
pointers only, nothing about parameters or behavior. It found 29 confirmed functions: 20 top-level plus
9 more nested under a `Human.Inventory` sub-table (the same nested-table pattern seen elsewhere in this
project, e.g. `Event.Create` or `Hud.Tutorial.SetText`). Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, this page shows a real argument pattern. Where it isn't called
anywhere in that corpus, only the name is known — arguments, return values, and behavior for those are
unconfirmed and not guessed beyond the `uGuid`-first convention that holds for every confirmed function
on this namespace.

## Functions

### Weapons & Inventory

| Function | Signature (best-known) | Notes |
|---|---|---|
| `EquipWeapon` | `Human.EquipWeapon(uGuid, ...)` | No call sites found anywhere in the decompiled corpus under the top-level form `Human.EquipWeapon(...)` — exists (confirmed via live `pairs(Human)` enumeration) but usage/arguments unconfirmed. See Notes for modders below: only the `Human.Inventory.EquipWeapon` form actually appears in real source. |
| `Human.Inventory.EquipWeapon` | `Human.Inventory.EquipWeapon(uGuid, uWeaponGuid)` | Confirmed with two `uGuid`-shaped arguments in real scripts, e.g. `Human.Inventory.EquipWeapon(uPlayer, tWeapons.Secondary1)` (`resident/mrxshootinggallery.lua`), swapping the player's currently-held weapon for one previously fetched via `GetPrimaryWeapon`/`GetSecondaryWeapon`. |
| `Human.Inventory.DropWeapon` | `Human.Inventory.DropWeapon(uCharGuid, uWeaponGuid)` | Very common in real scripts, always a character `uGuid` and a weapon `uGuid`, e.g. `Human.Inventory.DropWeapon(uCharacter, uWeapon)` (`vz/pmccon018.lua` and many other `vz/` mission scripts). |
| `Human.Inventory.SetAllWeapons` | `Human.Inventory.SetAllWeapons(uCharGuid, tWeaponGuids)` | Confirmed in real scripts with a character `uGuid` and a plain array-style table of weapon `uGuid`s, e.g. `Human.Inventory.SetAllWeapons(uCharGuid, {uPrimary, uGrenade, uC4})` (`resident/mrxplayer.lua`). Also seen called with a single `uGuid` in place of the table in some `vz/` scripts (e.g. `Human.Inventory.SetAllWeapons(uCharacter, Pg.GetGuidByName("Grenade Launcher"))`), meaning the full accepted shapes are not fully pinned down. |
| `Human.Inventory.GetAllWeapons` | `t = Human.Inventory.GetAllWeapons(uCharGuid [, bFlag])` | Extremely common in real scripts with a plain character `uGuid`, returning a table of weapon guids (e.g. `resident/hero.lua`, `resident/soldier.lua`). Some call sites pass a second boolean argument (e.g. `Human.Inventory.GetAllWeapons(uCharGuid, true)` in `resident/mrxplayer.lua`); its effect is unconfirmed. |
| `Human.Inventory.GetPrimaryWeapon` | `uWeaponGuid = Human.Inventory.GetPrimaryWeapon(uCharGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.Inventory.GetPrimaryWeapon(Player.GetLocalCharacter())` (`resident/mrxstatsmanager.lua`), returning a weapon `uGuid`. |
| `Human.Inventory.GetSecondaryWeapon` | `uWeaponGuid = Human.Inventory.GetSecondaryWeapon(uCharGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.Inventory.GetSecondaryWeapon(uPlayer)` (`resident/mrxshootinggallery.lua`), returning a weapon `uGuid`. |
| `Human.Inventory.ReloadAll` | `Human.Inventory.ReloadAll(uCharGuid, bFlag)` | Confirmed with a character `uGuid` and a boolean in one real call site: `Human.Inventory.ReloadAll(uCharacter, false)` ([`vz/xQ!L.lua`](../vz/xql)). |
| `Human.Inventory.GetVehicleWeapon` | `Human.Inventory.GetVehicleWeapon(uGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Human.Inventory.DestroyAllWeapons` | `Human.Inventory.DestroyAllWeapons(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Actions & Animation

| Function | Signature (best-known) | Notes |
|---|---|---|
| `DoAction` | `Human.DoAction(uGuid, sActionName)` | Confirmed with a character `uGuid` and an action-name string in real scripts, e.g. `Human.DoAction(uGuid, "Cower")`, `Human.DoAction(self.guid, "Stand")`, `Human.DoAction(uStarter, "Proximity")` — action names observed include `"Cower"`, `"Stand"`, `"VerifyCamera"`, `"shieldface"`, `"Proximity"`. |
| `PlayRawAnimation` | `bSuccess = Human.PlayRawAnimation(uGuid, sAnimName, bLoop, bFlag2, nBlendTime, bFlag4 [, bFlag5])` | Confirmed with 6-7 arguments in real scripts, e.g. `Human.PlayRawAnimation(uCharacter, "player_mattias_bare_technoviking", false, false, 0, false)` (`resident/danceradio.lua`) and `Human.PlayRawAnimation(uGuid, sAnim, false, false, -1, true, true)` (`resident/mrxbriefing.lua`); one call site captures a returned success boolean. Exact meaning of each flag/blend argument beyond the animation name and loop flag is not confirmed. |
| `SetState` | `Human.SetState(uGuid, sStateName, sAnimOrValue)` | Very common in real scripts, always a character `uGuid`, a state-name string, and a third string argument. Observed state names: `"InVehicle"` (paired with an animation name, e.g. `Human.SetState(self._hijacker, "InVehicle", sHijackerAnimation)` in `resident/mrxactionhijack.lua`), `"Upright"` (paired with `"Idle"`, e.g. `Human.SetState(uChar, "Upright", "Idle")`), and `"Subdued"` (paired with `"Idle"`, e.g. `resident/mrxtaskobjectiverelease.lua`). |
| `SetJostleEnabled` | `Human.SetJostleEnabled(uGuid, bOn)` | Confirmed with a character `uGuid` and a boolean in one real call site: `Human.SetJostleEnabled(uChar, bOn)` (`resident/mrxbriefing.lua`). |
| `Emote` | `Human.Emote(uGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### State Queries

| Function | Signature (best-known) | Notes |
|---|---|---|
| `IsSwimming` | `b = Human.IsSwimming(uGuid)` | Used with a plain character `uGuid` argument in real scripts, e.g. `Human.IsSwimming(uCharacter)` (`resident/mrxsupporttransit.lua`), used to decide whether a called-in support drop should be treated as a water pickup. One call site guards the call with `if Human.IsSwimming and uCharacter and ...`, suggesting the function's presence was historically treated as uncertain in some contexts. Not related to the HUD's built-in `"[Tutorial.Swimming]"` tutorial-message string documented in [Snippets](../snippets) — that's a localization key shown by `Hud`/`Gui` messaging, not this function; no call-site link between the two was found. |
| `IsCarrying` | `b = Human.IsCarrying(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `if Human.IsCarrying(uChar) then` (`resident/mrxbriefing.lua`, `resident/mrxplayer.lua`, `resident/mrxutil.lua`) — always checked immediately before a paired `Human.Drop` call. |
| `IsGrappling` | `b = Human.IsGrappling(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `if Human.IsGrappling(uCharGuid) then` (`resident/mrxplayer.lua`, `resident/mrxutil.lua`) — always checked immediately before a paired `Human.StopGrappling` call. |

### Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Drop` | `Human.Drop(uGuid [, bFlag])` | Confirmed in real scripts with a plain character `uGuid` (`resident/mrxbriefing.lua`) and, in other call sites, a second boolean argument (e.g. `Human.Drop(uCharGuid, true)` in `resident/mrxplayer.lua`, `Human.Drop(tOperation.uHero, true)` in `resident/mrxutil.lua`) — always called right after `Human.IsCarrying` returns true, dropping whatever the character is carrying. |
| `StopGrappling` | `Human.StopGrappling(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.StopGrappling(uCharGuid)` (`resident/mrxplayer.lua`, `resident/mrxutil.lua`) — always called right after `Human.IsGrappling` returns true. |
| `Knockdown` | `Human.Knockdown(uGuid, nDuration)` | Confirmed with a character `uGuid` and a numeric duration in real scripts, e.g. `Human.Knockdown(self._hijacker, nKnockdownDuration)` (`resident/mrxactionhijack.lua`), `Human.Knockdown(uCharacter, 0.5)` (`vz/pmccon002.lua`). |
| `SetPreemptiveRagdoll` | `Human.SetPreemptiveRagdoll(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.SetPreemptiveRagdoll(self._hijackee)` (`resident/mrxactionhijack.lua`), always used in hijack setup/failure paths alongside `Knockdown` and `ForceExitSeatNoSnap`. |
| `ForceExitSeatNoSnap` | `Human.ForceExitSeatNoSnap(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.ForceExitSeatNoSnap(self._hijackee)` (`resident/mrxactionhijack.lua`), `Human.ForceExitSeatNoSnap(uCharacter)` (`vz/oilcon020.lua`, `vz/pmccon001.lua`, [`vz/xQ!L.lua`](../vz/xql)) — forces a character out of a vehicle seat without the normal snap-to-ground/exit animation. |
| `PersistTransform` | `Human.PersistTransform(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.PersistTransform(uGuid)` (`resident/mrxbriefing.lua`), `Human.PersistTransform(tOperation.uHero)` (`resident/mrxutil.lua`). |
| `Scrub` | `Human.Scrub(uGuid)` | Confirmed with a plain character `uGuid` argument in one real call site: `Human.Scrub(uChar)` (`resident/mrxbriefing.lua`), immediately following a `Human.Drop`/`Human.SetState("Upright", "Idle")` cleanup sequence — likely resets/clears transient character state, but the exact effect is not confirmed. |
| `SetAllowCorpseCleanup` | `bPrev = Human.SetAllowCorpseCleanup(uGuid, bAllow)` | Confirmed with a character `uGuid` and a boolean in real scripts, e.g. `Human.SetAllowCorpseCleanup(uGuid, false)` / `Human.SetAllowCorpseCleanup(uGuid, true)` (`resident/mrxtaskobjectiveverify.lua`), `Human.SetAllowCorpseCleanup(uBlanco, false)` (`vz/pmccon002.lua`). One call site wraps the call in `Debug.Printf(... tostring(Human.SetAllowCorpseCleanup(...)))`, implying it returns a value (presumably the previous state), though that is inferred, not confirmed. |
| `SetFireLock` | `Human.SetFireLock(uGuid, bLocked)` | Confirmed with a character `uGuid` and a boolean in real scripts, e.g. `Human.SetFireLock(uChar1, false)`, `Human.SetFireLock(uChar, true)` (`resident/mrxshootinggallery.lua`) — used to prevent/allow weapon firing during a scripted shooting-gallery sequence. |
| `DisableWeapons` | `Human.DisableWeapons(uGuid)` | Extremely common in real scripts, always a plain character `uGuid` argument, e.g. `Human.DisableWeapons(uCharacter)` (`resident/danceradio.lua`, `resident/mrxbriefing.lua`, `resident/mrxutil.lua`, many `vz/` mission scripts) — always paired with `EnableWeapons` elsewhere in the same modules. |
| `EnableWeapons` | `Human.EnableWeapons(uGuid)` | Confirmed with a plain character `uGuid` argument in real scripts, e.g. `Human.EnableWeapons(uCharacter)` (`resident/danceradio.lua`), `Human.EnableWeapons(uChar)` (`resident/mrxutil.lua`) — counterpart to `DisableWeapons`. |

## Notes for modders

- **`EquipWeapon` exists in two places, and only one is actually used.** The live `pairs(Human)` dump
  lists a top-level `Human.EquipWeapon` *and* a nested `Human.Inventory.EquipWeapon` as two distinct
  confirmed function pointers. Grepping the full ~230-script decompiled corpus for real call sites turned
  up **zero** uses of the top-level `Human.EquipWeapon(...)` form, but **four** confirmed uses of
  `Human.Inventory.EquipWeapon(uPlayer, uWeaponGuid)`, all in `resident/mrxshootinggallery.lua`. Whether
  the top-level form is a genuine alias, a different (e.g. lower-level/immediate) equip path, or legacy/
  dead surface area is not something call-site evidence can settle — treat it as real but unverified, and
  prefer `Human.Inventory.EquipWeapon` since that's the only form with confirmed working usage.
- `Human.Inventory` is a nested sub-table, not a separate namespace — the same pattern seen elsewhere in
  this project (`Event.Create`, `Hud.Tutorial.SetText`). All 9 of its functions are weapon-inventory
  operations (equip, drop, reload, query primary/secondary/vehicle weapon, destroy all).
- `DisableWeapons`/`EnableWeapons` and `IsCarrying`/`Drop` and `IsGrappling`/`StopGrappling` all follow the
  same pattern seen elsewhere in this wiki: a state-query function checked immediately before a matching
  action function, in the same block of code, at essentially every real call site.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Human)` dump) but their
  argument shape beyond a presumed leading `uGuid` is a guess based on naming convention only — don't
  build mods around them without testing in-game first.
