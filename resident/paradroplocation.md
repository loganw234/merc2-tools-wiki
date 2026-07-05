---
title: ParadropLocation
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, mission]
verified: true
verified_note: 'deeper pass: re-confirmed both functions + the single Event.ObjectHibernation subscription; documented tTemplates (Support Vehicle paradop_ch/al), the exact Airstrike.Flyby argument pattern and the self-Object.Remove; cross-linked Paradrop/Airstrike/MrxUtil.'
---

# ParadropLocation

*Module: paradroplocation.lua*

## Overview
`ParadropLocation` is the **ground trigger** that summons a paradrop plane. It is the script on a
small marker object placed in the world: when that object wakes, it reads its own position and
faction, flies a faction-appropriate paradrop aircraft over the spot (via
[`Airstrike.Flyby`](../namespaces/airstrike)), then deletes itself.

The aircraft it summons runs the separate [`Paradrop`](paradrop) script, which is what actually
spawns the [`Paratrooper`](paratrooper) soldiers.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
Stateless — no per-instance table, no `Create`/`setmetatable`. It reacts once per activation through
its two top-level functions and then removes the triggering object.

## Functions
### `OnActivate(uGuid)`
Engine lifecycle callback. Wires an `Event.ObjectHibernation` `"awake"` event so `Start` runs once the
trigger object leaves hibernation.

### `Start(uGuid)`
Reads the object's position ([`Object.GetPosition`](../namespaces/object)) and faction
([`MrxUtil.GetFaction`](mrxutil)). If position, faction, and `tTemplates[sFaction]` are all valid it
calls `Airstrike.Flyby(tTemplates[sFaction], x - 50, z + 300, x, z, y + 100, 40)` — a flyby that
approaches offset from the trigger, passes over it at `y + 100` altitude, at speed `40` — then removes
the trigger object with [`Object.Remove`](../namespaces/object). If the faction has no template entry,
it returns early **without** removing the object.

## Events
- **`Event.ObjectHibernation`** (`"awake"` filter, wired in `OnActivate`) — the only subscription;
  fires `Start`. `OnActivate`/`Start` themselves are lifecycle/handler functions, not events.

## Module constants & tunables
- **`tTemplates`** — the summoned aircraft per faction:
  - `China = "Support Vehicle (paradop_ch)"`
  - `Allied = "Support Vehicle (paradop_al)"`

  Only these two factions are wired; any other faction is a no-op (the trigger stays in the world).
- **Flyby geometry**: approach offset `(-50, +300)`, over-point `(x, z)`, altitude `y + 100`, speed
  `40` — the arguments to `Airstrike.Flyby`. Adjust to change the approach path/height/speed.

## Notes for modders
- Swap the summoned plane by editing `tTemplates` (or add rows for more factions). The plane template
  must itself carry the [`Paradrop`](paradrop) script to actually drop soldiers.
- {: .note } The trigger self-deletes **only** on the success path. If you rely on it firing once,
  note that a faction with no `tTemplates` entry leaves the object alive (it could re-fire on a later
  wake).