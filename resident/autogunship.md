---
title: Autogunship
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [vehicle, ai]
---

# Autogunship

*Module: autogunship.lua*

## Overview
The `Autogunship` module represents an AI-controlled gunship that targets and attacks ground vehicles. It manages the gunship's blip on the radar, its targeting logic, and missile firing behavior.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tColor`: The color of the radar blip based on faction relation.
- `uLastTarget`: The last target selected for missile salvo.

## Functions
### `OnActivate(uGuid)`
Called when the gunship instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Creates a new per-instance table for the gunship using the module's prototype. It determines the faction relation of the gunship and sets its blip color accordingly. If the gunship has the "PMC" label, it makes it unkillable. It then adds a radar blip and schedules the first missile salvo after 3 seconds.

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
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the gunship's lifecycle.
- Customize blip colors by modifying the `tColorAlly`, `tColorNeutral`, and `tColorEnemy` fields.
- Adjust the missile salvo interval and target selection logic as needed for different gameplay scenarios.
- Be aware that making the gunship unkillable (`Object.SetUnkillable`) may affect player experience.