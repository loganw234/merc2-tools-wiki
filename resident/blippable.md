---
title: Blippable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [blip, radar]
verified: true
verified_note: read directly from source; corrects an inaccuracy in the previous Events section (HideMarker is a plain function, not an event listener)
---

# Blippable

*Module: blippable.lua*

## Overview
`Blippable` adds radar-objective and off-screen-world-marker support to anything built on
[`Inheritable`](inheritable) — the base every other blip-related module
([`VehicleBlippable`](vehicleblippable), [`EnemyBlippable`](enemyblippable),
[`OrientedBlippable`](orientedblippable)) builds on in turn. It provides `SetBlipped`/`ClearBlipped` to
toggle visibility, with the actual radar/marker plumbing in `AddObjective`/`RemoveObjective`.

## Inheritance
- Inherits from: [`Inheritable`](inheritable)
- Imports: `MrxUtil`

## Instance pattern
Per-instance object module (keyed by `uGuid`, via `Inheritable`). A subclass typically sets some subset of
these fields on itself before calling `self:SetBlipped()`:
- `sName` — the objective's name (defaults to `tostring(uGuid)`, set by `Inheritable.Create`).
- `tColor` (`{r, g, b}`) — default radar dot color; falls back to `{255, 51, 51}` (red) if unset.
- `tFlash` — an alternate color used instead of `tColor` when `AddObjective(true)` is called.
- `nWidth`/`nHeight`, or just `nSize` (used for both if the specific ones aren't set) — radar dot
  dimensions.
- `sTexture` — radar icon texture name.
- `bSticky` — whether the blip stays on-screen regardless of distance/rotation.
- `bRotate` / `bOriented` — whether the blip rotates to match the object's facing.
- `nSortOrder` — draw/priority order among overlapping blips.
- `bNetSync` — whether blip add/remove is replicated to other players (see `AddObjective`/`RemoveObjective`
  below — this gates real `Net.SendEvent_*` calls, not just a cosmetic flag).
- `tMarker` (table, optional) — if present, also adds an off-screen world marker via `Marker.AddBlip`, with
  its own `sTexture`/`nSize`/`tColor`/`tFlash`/`nVerticalOffset`/`nNearDist`/`nFarDist`/`nClampDist`/
  `sGroup`/`bJust2DCheck` sub-fields (all individually defaulted if omitted — see source for exact
  fallback values).
- `bActive` — set by `SetBlipped`/cleared by `ClearBlipped`; whether the blip is currently shown.

Module-level (shared across all instances, not per-object): `tHiddenGuids` — a list of GUIDs that
`AddObjective` silently refuses to blip at all (checked at the top of the function), populated by
`HideMarker`.

## Functions

### `OnActivate(uGuid, uRuntimeOwner, iArg)` / `Awake(uGuid, iArg)`
Standard `Inheritable`-pattern activation — see [`Inheritable`](inheritable) for the general mechanism.

### `SetBlipped(self)`
Calls `self:AddObjective()` and sets `self.bActive = true`. The normal way to turn a blip on.

### `ClearBlipped(self)`
Calls `self:RemoveObjective()` and clears `self.bActive`. The normal way to turn a blip off.

### `AddObjective(self, bFlash)`
The actual radar/marker registration. Skips entirely (returns with no effect) if `self.uGuid` is in the
module-level `tHiddenGuids` list. Builds a `Hud.Radar:AddObjective({...})` call from the instance's fields
(see Instance pattern above for what each one does), using `tFlash` instead of `tColor` if `bFlash` is
true. If `tMarker` is set, also removes any previous marker and adds a new one via `Marker.AddBlip`, and —
**only if `Net.IsServer()` and `self.bNetSync`** — sends `Net.SendEvent_AddMarkerObjective` to replicate
the marker to other players.

### `RemoveObjective(self)`
The inverse of `AddObjective` — removes the radar objective and, if present, the world marker, sending
`Net.SendEvent_RemoveMarkerObjective` under the same `Net.IsServer()`/`bNetSync` conditions.

### `HideMarker(uGuid)`
**A plain function, not an event listener** (see the Events correction below) — call this directly to
force-hide a specific object's blip regardless of its own `bActive` state. If the object's instance is
currently loaded (found in `tInstance`), removes its objective immediately; either way, adds `uGuid` to
`tHiddenGuids` so any *future* `AddObjective` call for it is silently skipped.

### `Delete(self)`
Clears any active blip (`self:ClearBlipped()`) before deferring to `Inheritable.Delete(self)` — overriding
the base `Delete` specifically to avoid leaving a stale radar objective behind when the instance goes away.

## Events
- Listens for `Event.ObjectHibernation` inside `OnActivate` (via the standard `Inheritable` pattern).
- **`HideMarker` is not an event** — it's a directly-callable function, `Blippable.HideMarker(uGuid)`
  (import the module first). An earlier version of this page incorrectly listed it as a listened-for
  custom event.

## Notes for modders
- **The common pattern**: set `tColor`/`sTexture`/`nSize` (and optionally `tMarker`) on your instance, then
  call `self:SetBlipped()` to turn the blip on and `self:ClearBlipped()` to turn it off — you rarely need
  to call `AddObjective`/`RemoveObjective` directly.
- **`bNetSync` genuinely gates network replication**, not just display — if you want a blip visible to
  other players in co-op, set `bNetSync = true` on the instance; otherwise it's local-only.
- **`HideMarker(uGuid)` is a permanent-until-you-remove-it suppression** — it adds to a list nothing in
  this module ever clears. If you use it, you're responsible for removing the entry from `tHiddenGuids`
  yourself if you want that object blippable again later.
- See [`VehicleBlippable`](vehicleblippable) and [`OrientedBlippable`](orientedblippable) for the actual
  subclasses most vehicle/world-object modules use directly, rather than inheriting from `Blippable`
  itself.
