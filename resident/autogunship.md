---
title: Autogunship
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [vehicle, ai]
verified: true
verified_note: found likely bug — Start(uGuid) references uRuntimeOwner, which is not a parameter of Start and is never assigned anywhere in the file (always nil in practice); corrected Instance pattern to note tColor/uLastTarget/uTarget/nRelation are plain module-level globals, not fields set on oInstance
---

# Autogunship

*Module: autogunship.lua*

## Overview
The `Autogunship` module represents an AI-controlled gunship that targets and attacks ground vehicles. It manages the gunship's blip on the radar, its targeting logic, and missile firing behavior.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`) — `Start` calls `oPrototype:Create(uGuid, uRuntimeOwner)`,
which resolves through `OrientedBlippable`/`Blippable` inheritance to build the actual per-`uGuid` table
(`oInstance`), and `oInstance.tColor` is set on that instance. However, several other values the source
touches are **plain module-level globals**, not instance fields — they're shared/overwritten across every
active autogunship rather than tracked per-`uGuid`:
- `tColor`, `tColorAlly`, `tColorNeutral`, `tColorEnemy`: module-level default color tables; `oInstance.tColor`
  (the actual per-instance field) is assigned one of these based on faction relation.
- `uLastTarget`, `uTarget`: bare globals (no `local`) written and read in `Salvo` — not stored on
  `oInstance`, so they're effectively shared/last-write-wins state if multiple gunships are active
  simultaneously, not truly per-gunship.
- `nRelation`: also a bare global, computed fresh each time in `Start` and not read afterward.

## Functions
### `OnActivate(uGuid)`
Called when the gunship instance is activated. It sets up an event to call `Start` once the object leaves hibernation. Note only `uGuid` is passed through — `OnActivate`'s own `uRuntimeOwner`/`iArg` parameters (standard for this activation idiom elsewhere) are not part of this file's `OnActivate(uGuid)` signature, since it only declares the one parameter.

### `Start(uGuid)`
Creates a new per-instance table for the gunship using the module's prototype. It determines the faction relation of the gunship and sets its blip color accordingly. If the gunship has the "PMC" label, it makes it unkillable. It then adds a radar blip and schedules the first missile salvo after 3 seconds.

**Likely bug, confirmed in source:** `Start(uGuid)` declares only one parameter, but its body calls
`oPrototype:Create(uGuid, uRuntimeOwner)` — `uRuntimeOwner` is never a parameter, local, or assigned
global anywhere in this file. It resolves to a `nil` global at runtime, so every autogunship instance is
effectively created via `Create(uGuid, nil)`. Practical impact appears limited: `OrientedBlippable` (this
module's parent) has no `Create` of its own, and the chain resolves all the way up through `Blippable` to
[`Inheritable.Create(oPrototype, uGuid, iArg)`](inheritable), whose body never reads its third parameter —
so the `nil` currently passed through doesn't visibly break anything in the confirmed call chain. It's
still a genuine source-level defect (a reference to an undeclared variable) rather than intentional
`nil`-passing, and would matter if the inheritance chain ever changed to make use of that second argument.

### `Salvo(uGuid)`
Handles the logic for launching a salvo of missiles. It collects ground vehicles within a 200m radius around the player's position, selects a valid target based on faction labels, and fires 4 missiles at 0.25-second intervals. After each salvo, it schedules the next one after another 3 seconds.

Targeting is centered on the **player's** position, not the gunship's own — worth knowing if you're trying
to predict what it'll shoot at. Read directly from source, a target only qualifies if it's alive and has
one of these exact labels: `VZ`, `China`, or `Guerilla`.

### `LaunchMissile(uGuid, uTarget)`
Fires a single missile towards the specified target. It calculates the normalized direction vector from the gunship to the target with ±5 aim scatter, plays sound and particle effects, and spawns the missile with a speed of 100.

**Confirmed exact firing sequence** (a plain, non-`local` function — safe to override from an `OnLoad`
script, same pattern as everywhere else in this wiki):

```lua
Sound.CueSound(uGuid, "wpn_tankgun_fire_npc")
Pg.Spawn("global_particle_muzzleflash_tank", nSpawnX, nSpawnY, nSpawnZ)
Airstrike.SpawnOrdnance("Gunship Shell", nSpawnX, nSpawnY, nSpawnZ, nVectorX * nSpeedScale, nVectorY * nSpeedScale, nVectorZ * nSpeedScale, "impact", 1)
```

Three independently swappable pieces: the sound cue, the muzzle-flash particle effect (a separate
`Pg.Spawn` call, not part of the ordnance itself), and the [`Airstrike.SpawnOrdnance`](../namespaces/airstrike)
call — which is the actual projectile. Overriding this function and changing `"Gunship Shell"` to a
different confirmed ordnance template name (see the [Airstrike](../namespaces/airstrike) catalog) is a
real, buildable way to change what this specific gunship fires — e.g. `"Cluster Bomb Projectile"` instead
of a single shell. Found while investigating vehicle-turret weapon customization more broadly — see the
[Airstrike namespace page](../namespaces/airstrike) for the full verdict on what is and isn't reachable
this way.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- `Salvo` and `LaunchMissile` aren't event subscriptions in the usual sense — they're scheduled via
  `Event.TimerRelative` (a 3-second repeating loop for `Salvo`, and four staggered 0.25s-apart one-shots
  per salvo for `LaunchMissile`), not triggered by any external event source.

## Notes for modders
- This file only defines `OnActivate` — no local `OnDeactivate`/`OnDeath` override exists here; teardown
  falls through to whatever `OrientedBlippable`/`Blippable`/`Inheritable` provide via inheritance.
- Customize blip colors by modifying the `tColorAlly`, `tColorNeutral`, and `tColorEnemy` fields.
- Adjust the missile salvo interval and target selection logic as needed for different gameplay scenarios.
- Be aware that making the gunship unkillable (`Object.SetUnkillable`) may affect player experience.