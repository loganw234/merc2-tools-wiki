---
title: Paradrop
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [support, paratrooper]
verified: true
verified_note: 'deeper pass: added the module constants (tTemplates China/Allied Paratrooper, radar sTexture "temp_radar_icon_airplane" nSize 5, the three tColor* RGBs + ±60 relation thresholds, 16 drops @ 0.75s from 5.25s); re-confirmed the nRelation-global and uRuntimeOwner/iArg undefined-global bugs; cross-linked OrientedBlippable/MrxUtil/namespaces.'
---

# Paradrop

*Module: paradrop.lua*

## Overview
The `Paradrop` module is the script on the **paradrop aircraft** itself: once it wakes it puts a
radar blip on the plane (colored by the plane's faction relation to the PMC) and then spawns 16
paratroopers underneath it at a steady interval as it flies. It inherits blip/orientation handling
from [`OrientedBlippable`](orientedblippable) and uses [`MrxUtil`](mrxutil) for faction lookup.

Note this is distinct from [`ParadropLocation`](paradroplocation) (a ground trigger that *summons* the
plane) and [`Paratrooper`](paratrooper) (the individual dropped soldier).

## Inheritance
- Inherits from: [`OrientedBlippable`](orientedblippable) (→ [`Blippable`](blippable) →
  [`Inheritable`](inheritable))
- Imports: [`MrxUtil`](mrxutil)

Blip creation/coloring (`SetBlipped`, the `Create` factory that keys instances by `uGuid`) comes from
the [`OrientedBlippable`](orientedblippable)/[`Blippable`](blippable) chain; this file only sets the
blip's `tColor` and schedules the drops.

## Instance pattern
Genuinely per-instance for one field, but with a real bug: `Start(uGuid)` calls `oPrototype:Create(uGuid, uRuntimeOwner)` and sets `oInstance.tColor` correctly (a true per-instance field, keyed by `uGuid` via the inherited `OrientedBlippable`/`Inheritable` `Create`). However:
- `nRelation` (line 35/37/42/44/46) is written as a **bare global** (`nRelation = Ai.GetRelation(...)`, no `local`, no `oInstance.` prefix) — it is not stored on the instance at all, despite being computed from per-instance data (the aircraft's faction). Every active `Paradrop` instance overwrites the same shared global when it calls `Start`, so with more than one paradrop aircraft active simultaneously, each one's `Start` call clobbers the last one's relation value module-wide. This looks like a decompiled/original-source bug, not a wiki error — the field is read nowhere else in this file, so the practical impact is limited to whatever else in the codebase might read this global, if anything (no other call sites found in the decompiled corpus).
- `tColor`: The color of the radar blip based on faction relation — the one field that *is* correctly set on `oInstance`.

## Functions
### `OnActivate(uGuid)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Creates a new per-instance table for the object using the module's prototype (`oPrototype:Create(uGuid, uRuntimeOwner)`), determines the faction relation and sets the radar blip color (`tColor`) accordingly, activates the radar blip, and schedules 16 paratrooper drops at intervals of 0.75 seconds starting at 5.25 seconds (via `Event.Create(Event.TimerRelative, ...)`).

**Confirmed bug**: `Start` only takes one parameter (`uGuid`), but its body reads `uRuntimeOwner` (passed as the second arg to `Create`) and, inside the drop-scheduling loop, `iArg` (passed as the second element of `DropDude`'s args table). Neither name is a parameter, local, or otherwise assigned anywhere in `Start`'s scope — both resolve to undefined globals (`nil`) at runtime. In practice this means every `Paradrop` instance is created via `Create(uGuid, nil)` (the second argument is always `nil` instead of whatever `uRuntimeOwner` was meant to carry), and every one of the 16 scheduled `DropDude` calls receives `iArg = nil` as its second argument (see below).

### `DropDude(uGuid, iArg)`
Called by each timer to drop one paratrooper. If the aircraft is still alive, it reads the plane's
position/yaw and spawns `tTemplates[sFaction]` (`"Chinese Paratrooper"` or `"Allied Paratrooper"`) via
[`Pg.Spawn`](../namespaces/pg) at a random ±10-unit horizontal offset (same `y` as the plane, so the
soldier appears at the aircraft's altitude and falls). `iArg` is accepted but never used — and per the
bug above it is always `nil`.

{: .note }
> `tTemplates` only has `China` and `Allied` keys. If the plane's faction is anything else,
> `tTemplates[sFaction]` is `nil` and nothing spawns for that tick.

## Events
- `Event.ObjectHibernation`: Wired in `OnActivate` to call `Start` when the object leaves hibernation.
- `Event.TimerRelative`: Used 16 times in `Start` to schedule each `DropDude` call at staggered delays. `DropDude` is a plain delayed callback, not a distinct engine event type — there is no `Event.DropDude` or similar.

## Module constants & tunables
- **`tTemplates`** — the spawned soldier per faction: `China = "Chinese Paratrooper"`,
  `Allied = "Allied Paratrooper"`. Swap these to change who drops.
- **Radar blip**: `sTexture = "temp_radar_icon_airplane"`, `nSize = 5`.
- **Blip colors by relation** (`Ai.GetRelation` of plane faction vs. `"PMC"`):
  - `tColorAlly = {0, 127, 255}` when relation `>= 60`
  - `tColorNeutral = {200, 200, 200}` when `-60 < relation < 60`
  - `tColorEnemy = {255, 0, 0}` when relation `<= -60`
- **Drop schedule**: 16 paratroopers, one every `0.75s`, first at `5.25 + 1*0.75 = 6.0s` after wake,
  last at `5.25 + 16*0.75 = 17.25s`. Change the loop bound (`for i = 1, 16`) and the
  `5.25 + i * 0.75` timing to retune.
- PMC-owned paradrop planes are made unkillable while dropping (`Object.SetUnkillable(uGuid, true,
  "Support")`).

## Notes for modders
- There is no `OnDeactivate` here — only `OnActivate`, `Start`, `DropDude`. This module does not
  override any deactivation lifecycle from [`OrientedBlippable`](orientedblippable).
- To change **who/how many/how fast** drop, edit `tTemplates`, the `for i = 1, 16` bound, and the
  `5.25 + i * 0.75` interval respectively.
- {: .warning } Two confirmed source bugs (see above): `nRelation` is a **module global** (multiple
  live paradrop planes clobber each other's value), and `Start` reads undefined globals
  `uRuntimeOwner`/`iArg` (both resolve to `nil`). Neither breaks the visible drop behavior, but don't
  build on those values.