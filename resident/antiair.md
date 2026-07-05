---
title: AntiAir
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: EnemyBlippable
tags: [anti-air, radar, missile]
verified: true
verified_note: deeper pass — re-confirmed all 17 functions/events, the _tLockOnUpdates dead field, and the tColor*=false disabling; surfaced the ksCue*/knCueAlertCooldown sound constants as a tunables block and cross-linked EnemyBlippable/HomingMissile/MrxSupport up the chain
---

# AntiAir

*Module: antiair.lua*

## Overview
The `AntiAir` module represents anti-aircraft systems in the game. It manages the activation and deactivation of these systems based on player proximity and handles their radar blips, sound cues, and homing lock-on behavior. The module supports four tiers: basic, medium, advanced, and jammer, each with different properties and behaviors.

The four tiers, read directly from `_tPrototype`:

| Tier (`iArg`) | Level | Range | Radar texture | HUD marker texture |
|---|---|---:|---|---|
| 1 | `basic` | 100 | `radar_AA` | `HUD_anti-air` |
| 2 | `medium` | 200 | `radar_SAM` | `HUD_SAM` |
| 3 | `advanced` | 200 | `radar_AA` | `HUD_anti-air` |
| 4 | `jammer` | 200 | `radar_Jammer` | `HUD_jammer` |

Which tier a given placed emplacement uses is set by whoever spawns it (`iArg` passed to `OnActivate`),
not something this module decides on its own.

Worth noting as a general pattern, not just an AntiAir detail: this module only fully "wakes up"
(`ActivateAA`) once the player comes within `nAARange` (`CreateNearnessEvent`/`Event.ObjectProximity`) —
outside that range it just sits idle waiting for a proximity event, rather than running its full
lock-on/targeting logic constantly. Worth copying if you're building something with a similar
always-present-but-rarely-relevant world object.

## Inheritance
- Inherits from: [`EnemyBlippable`](enemyblippable) (→ [`OrientedBlippable`](orientedblippable) → [`Blippable`](blippable) → [`Inheritable`](inheritable))
- Imports: [`MrxSupport`](mrxsupport), [`HomingMissile`](homingmissile)

The blip draw/teardown primitives (`AddObjective`/`RemoveObjective`, `SetBlipped`/`ClearBlipped`) come from
[`EnemyBlippable`](enemyblippable)/[`Blippable`](blippable) up the chain; this file overrides `SetBlipped`/
`ClearBlipped` to layer on the `MrxSupport.AddAntiAir`/`RemoveAntiAir` registration and the homing-lock
subsystem, then calls back up to the base versions.

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tPrototype`: Defines the properties of each anti-air tier (module-level, shared across instances — set as the `__index` metatable for each tier via `Init`).
- `tEvent`: Per-`uGuid` table of event handles for proximity/distance events (`oClose`, `oFar`, `oInstance`).
- `_tLockOns`: Keyed by owner GUID, manages active homing lock-on states.
- `_tLockOnState`: Keyed by player GUID, tracks targeting/targeted counts for sound-cue bookkeeping.
- `_tLockOnUpdates`: **Declared (`= {}`) but never read or written anywhere else in this file** — dead
  field, not an active tracker despite the name suggesting otherwise.

## Functions
### `Init(param)`
Initializes the module by setting up metatables for each prototype in `_tPrototype`.

### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It sets up an event to call `Awake` once the object leaves hibernation.

### `Awake(uGuid, iArg)`
Creates a new per-instance table for the object using the module's prototype and activates the anti-air system if within range or creates nearness events otherwise.

### `OnDeactivate(uGuid)`
Tears down the per-instance table by deleting proximity and distance events and calling the base class's `OnDeactivate`.

### `CreateNearnessEvent(uGuid, iArg)`
Creates an event to activate the anti-air system when the player comes within range.

### `ActivateWithEvents(uGuid, iArg)`
Activates the anti-air system and creates a distance event to deactivate it when the player moves out of range.

### `DeactivateWithEvents(uGuid, iArg)`
Deactivates the anti-air system and creates a nearness event to reactivate it when the player comes back within range.

### `ActivateAA(uGuid, iArg)`
Activates the anti-air system by creating an instance based on the prototype for the given tier.

### `CreateDistanceEvent(uGuid, iArg)`
Creates an event to deactivate the anti-air system when the player moves out of range.

### `SetBlipped(oSelf, bCalledByDriver)`
Adds a radar objective and marker for the object. Registers with `MrxSupport.AddAntiAir` if hostile.

### `ClearBlipped(oSelf, bCalledByDriver)`
Removes the radar objective and marker for the object. Clears any active homing lock-on states and unregisters from `MrxSupport.RemoveAntiAir`.

### `_CooldownComplete()`
Resets the alert cooldown flag after a sound cue has been played.

### `_SetSound(bPlay, sCue)`
Plays sound cues based on the type of event and manages cooldowns to prevent rapid alerts.

### `_UpdateHomingState(uPlayerGuid, bTargeted, sAction, bTransfer)`
Updates the targeting and targeted states for players and plays appropriate sound cues.

### `_HomingLockStart(oWidget, tData)`
Initializes a homing lock-on state for an anti-air system.

### `_HomingLockUpdate(oWidget, tData)`
Updates the homing lock-on state based on the lock percentage and player proximity.

### `_HomingLockClear(oWidget, tData, nEvent)`
Clears the homing lock-on state and resets related fields.

### `_HomingLaunched(oWidget, tData)`
Handles the launch of a homing missile by calling into `HomingMissile._HomingLaunched`.

**Confirmed: this function is purely reactive — it does not fire/spawn anything itself.** Its exact body
is just `HomingMissile._HomingLaunched(oWidget, tData)`, forwarding to
[`HomingMissile`](homingmissile)'s own radar-blip bookkeeping. `antiair.lua` never calls
[`Airstrike`](../namespaces/airstrike) anywhere (confirmed by direct search) — the actual missile
spawn/launch happens through some other, native mechanism this file only reacts to after the fact. See
[`Junk.SpawnHomingProjectile`](../namespaces/junk#alarms--gameplay) for the likely (but unconfirmed)
candidate.

## Events
All confirmed by direct grep of this file:
- `Event.ObjectHibernation` — twice: `OnActivate` waits for it to call `Awake`; `_HomingLockStart` also
  creates one on the homer object (`"s"` state) to clear the lock if the homer goes to sleep.
- `Event.ObjectProximity` — `CreateNearnessEvent` (player closer than `nAARange` triggers
  `ActivateWithEvents`) and `CreateDistanceEvent` (player farther than `nAARange` triggers
  `DeactivateWithEvents`).
- `Event.TimerRelative` — `_SetSound` schedules `_CooldownComplete` after `knCueAlertCooldown` (1s).
- `Event.ObjectDeath` — `_HomingLockStart` watches both the ridden vehicle (`uHomee`) and the
  homer/owner (`uHomer`) for death, clearing the lock via `_HomingLockClear`.
- `Event.ObjectInSeat` — `_HomingLockStart` watches the ridden vehicle for the rider exiting (`"d"`,
  `"x"`), clearing the lock.
- `Event.Timer` — `_HomingLockUpdate` sets a 1-second one-shot fallback to force-clear a lock if it's
  "left hanging" (not otherwise updated or cleared).

## Module constants & tunables
Beyond the four `_tPrototype` tiers (radar texture, HUD marker texture, `nAARange`, `nSize = 8`,
`nSortOrder = 2`, `bSticky = true` — table above), the lock-on tones and cooldown are module-level constants:

| Constant | Value | Meaning |
|---|---|---|
| `ksCueTargeted` | `"ui_hud_sam_targeted"` | played once when a player becomes fully locked |
| `ksCueTargeting` | `"ui_hud_radar_targeting_alert"` | played when a player first comes under partial lock |
| `ksCueAlert` | `"ui_hud_radar_targeting_new_alert"` | re-alert tone for an additional lock while already targeted |
| `knCueAlertCooldown` | `1` (seconds) | debounce so `ksCueAlert` can't spam every frame |

`tColorAlly`/`tColorNeutral`/`tColorEmpty`/`tColorPmc` are all set to `false` at the top of the file —
AntiAir is always drawn with the enemy/hostile coloring from [`EnemyBlippable`](enemyblippable), so those
non-enemy color slots are deliberately disabled.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the anti-air system.
- Customize the behavior by modifying `_tPrototype` fields such as `nAARange`, `sTexture`, and `tMarker`.
- Swap the targeting tones by overriding `ksCueTargeted`/`ksCueTargeting`/`ksCueAlert` (all plain module
  globals) with different [`Sound`](../namespaces/sound) cue strings.
- Be aware of the homing lock-on subsystem, which drives targeting tones and visual cues.
- `bNetSync` is never referenced directly in `antiair.lua` itself — it's read by `Blippable.AddObjective`/
  `RemoveObjective` further up the inheritance chain, so network-sync behavior for this module's radar
  blips is inherited, not something `antiair.lua` sets or checks on its own.