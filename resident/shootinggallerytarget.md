---
title: ShootingGalleryTarget
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [shooting gallery]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (9 lines) — one OnStateChange callback, no Event.* calls; documented the two exact state hashes, the "pivot" door node, and that the target is driven as a Vehicle door (Vehicle.OpenDoor/CloseDoor); cross-linked Vehicle/Sys namespaces + MrxShootingGallery.'
---

# ShootingGalleryTarget

*Module: shootinggallerytarget.lua*

## Overview
The `ShootingGalleryTarget` module is the tiny per-target script for the pop-up targets used by the
[shooting gallery](mrxshootinggallery) contract. The target is built as a **vehicle-style object with
a door**: raising it "up" and lowering it "down" are done by opening/closing a door node named
`"pivot"`. The whole file is a single engine-invoked state-change callback that maps two specific
state hashes to open/close.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless utility module (no per-instance table). It does not track any persistent state.

## Functions
### `OnStateChange(uGuid, uiNodeHashName, uiStateHashName)`
Engine lifecycle callback fired when the target object changes state. It converts the state-hash
argument to a string via [`Sys.GuidToString`](../namespaces/sys) and branches on it:
- `"0x7687DF41"` → [`Vehicle.OpenDoor(uGuid, "pivot")`](../namespaces/vehicle) (raise the target).
- `"0xACB51200"` → `Vehicle.CloseDoor(uGuid, "pivot")` (lower the target).

`uiNodeHashName` is received but not used. Any state hash other than the two above is a no-op.

## Events
This file contains **no `Event.*` calls at all** — no `Event.Create`, no `Event.StateChange` constant
reference. `OnStateChange` is invoked directly by the engine as a naming-convention callback on the
world-object script (the same mechanism that calls `OnActivate`/`OnDeath` on other modules without those
modules registering anything explicitly), not through an `Event.Create` registration in this file.

## Module constants & tunables
- **State hashes** (the "open"/"close" triggers): `"0x7687DF41"` and `"0xACB51200"`. These are hashed
  state names baked into the target's world-object graph — to retarget behavior you change which
  states map to open vs. close.
- **Door node name**: `"pivot"` — the animated node that acts as the door. Both `Vehicle.OpenDoor`
  and `Vehicle.CloseDoor` operate on it.

## Notes for modders
- `OnStateChange` is a plain global, so you can override it to make targets do something other than
  raise/lower (e.g. play an effect on hit). See [Function override](../deep-dives/function-override).
- The two hashes are the only branches — any other state change silently does nothing, so if a
  target won't move, check that its authored state names hash to exactly these values.
- Scoring/timing lives in the [gallery controller](mrxshootinggallery) and the mission task, not here;
  this script only animates the physical target.