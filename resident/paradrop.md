---
title: Paradrop
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [support, paratrooper]
verified: true
verified_note: corrected Instance pattern (nRelation/x/y/z/yaw are bare globals, not per-instance fields); removed fabricated OnDeactivate reference (no such function in source); documented two undefined-global reads (uRuntimeOwner in Start, iArg passed to DropDude's Event.Create) that evaluate to nil at runtime; fixed Events section
---

# Paradrop

*Module: paradrop.lua*

## Overview
The `Paradrop` module is responsible for deploying a squad of paratroopers via an aircraft. It inherits from `OrientedBlippable` to manage radar blips and orientation, and uses the `MrxUtil` library for faction-related utilities. The module sets up a timed sequence to drop 16 paratroopers at intervals.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`

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
Called by the timer event to drop a paratrooper. Checks if the aircraft is still alive, retrieves its position and orientation, and spawns a paratrooper near the aircraft's position with a random offset. `iArg` is accepted as a parameter but never referenced in the function body — and per the bug above, it is always called with `nil` anyway, so this parameter is effectively dead in practice.

## Events
- `Event.ObjectHibernation`: Wired in `OnActivate` to call `Start` when the object leaves hibernation.
- `Event.TimerRelative`: Used 16 times in `Start` to schedule each `DropDude` call at staggered delays. `DropDude` is a plain delayed callback, not a distinct engine event type — there is no `Event.DropDude` or similar.

## Notes for modders
- There is no `OnDeactivate` in this file — only `OnActivate`, `Start`, and `DropDude`. A previous version of this page referenced `OnDeactivate`; that function does not exist here (nor does this module override any deactivation lifecycle from `OrientedBlippable`).
- Customize the number of paratroopers, their spawn interval, and their initial position by modifying the relevant parameters in the script.
- Be aware that the radar blip color is determined by the faction relation between the aircraft's faction and the PMC. Adjustments to faction relations may affect the blip color — but see the confirmed `nRelation`-is-a-global bug above; the value one instance computes can be clobbered by another instance's `Start` call before it's used elsewhere.
- The `DropDude` function uses random offsets for paratrooper positions, which can be modified to achieve different drop patterns.
- See the confirmed bugs in `Start`/`DropDude` above (`uRuntimeOwner`/`iArg` undefined globals) before relying on either value.