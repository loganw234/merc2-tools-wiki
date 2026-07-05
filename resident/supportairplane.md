---
title: SupportAirplane
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable, MrxFactionManager
tags: [support, aircraft, radar]
verified: true
verified_note: deeper pass — surfaced the sTexture/nSize/tColor* constants block, flagged the "PMC" (unkillable) vs "pmc" (green blip) case distinction, noted the double inherit(OrientedBlippable + MrxFactionManager), and added inheritance cross-links; icon/color/event tables re-confirmed against source
---

# SupportAirplane

*Module: supportairplane.lua*

## Overview
The `SupportAirplane` module is responsible for managing support aircraft in the game. It handles the creation and configuration of radar blips for these aircraft based on their faction, labels, and relation to the PMC (Player Managed Company). The module also ensures that certain aircraft are marked as unkillable if they have the "PMC" label.

## Inheritance
- Inherits from: [`OrientedBlippable`](orientedblippable) (→ [`Blippable`](blippable) → [`Inheritable`](inheritable)) **and** [`MrxFactionManager`](mrxfactionmanager)
- Imports: none

Note the double `inherit(...)` — this file calls `inherit("OrientedBlippable")` **and**
`inherit("MrxFactionManager")`, so `MrxFactionManager.GetFaction` is reachable as a plain call. It does
**not** inherit [`VehicleBlippable`](vehicleblippable), so it reimplements the ally/neutral/enemy/PMC color
logic locally against `OrientedBlippable` directly (see below).

## Instance pattern
This is a per-instance object module (keyed by `uGuid`), though `supportairplane.lua` itself defines no
`Create` — `oPrototype:Create(uGuid, uRuntimeOwner)` in `OnActivate` (line 28) resolves through the
inherited chain `OrientedBlippable` → `Blippable` → `Inheritable`, none of which override `Create` after
`Inheritable`, so it bottoms out at `Inheritable.Create`: the standard `setmetatable`/`tInstance[uGuid]`
factory described on [Resident Modules](index). Per-instance fields set directly on `oInstance` in
`OnActivate`:
- `tColor`: the color of the radar blip, chosen from `tColorPmc`/`tColorNeutral`/`tColorEnemy`/`tColorAlly`
  based on faction relation.
- `sTexture`: the radar blip icon texture, defaulting to `"temp_radar_icon_airplane"` and overridden per
  the label table below.

## Module constants & tunables
Declared at the top of `supportairplane.lua`:

| Constant | Value |
|---|---|
| `sTexture` | `"temp_radar_icon_airplane"` (default icon, before the per-label swap below) |
| `nSize` | `5` |
| `tColorPmc` | `{0, 255, 0}` (green) |
| `tColorAlly` | `{0, 127, 255}` (blue, relation ≥ 60) |
| `tColorNeutral` | `{200, 200, 200}` (gray, -60 < relation < 60) — note this is a slightly different neutral than [`VehicleBlippable`](vehicleblippable)'s `{230, 230, 255}` |
| `tColorEnemy` | `{255, 0, 0}` (red, relation ≤ -60) |

The per-label icon textures in the table below (`temp_radar_icon_c130`, `_mig27`, `_f35`, `_b2`, `_f117`,
`_a10`, `_ov10`, `_cruisemissile`) are not named constants — they're inline strings in the `OnActivate`
label ladder.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It creates a new per-instance table for the object using the module's prototype. It then determines the faction of the aircraft and sets its color based on the relation to the PMC. Finally, it sets the radar blip icon texture based on the aircraft's label and activates the blip.

{: .note }
> The two PMC checks use **different case** and do different things:
> `Object.HasLabel(uGuid, "PMC")` (uppercase) → `Object.SetUnkillable(uGuid, true, "Support")`, while
> `Object.HasLabel(uGuid, "pmc")` (lowercase) → green `tColorPmc` blip. A vehicle labelled one case but not
> the other gets only one of the two effects. This mirrors the same dual-label check in
> [`VehicleBlippable.SetBlipped`](vehicleblippable) (which tests `"pmc"` on both the vehicle and its rider).

Exact icon-by-label mapping, read directly from source — `OnActivate` checks `Object.HasLabel(uGuid, ...)`
against each of these in order and swaps the default `"temp_radar_icon_airplane"` texture accordingly:

| Label | Icon texture |
|---|---|
| `C130` | `temp_radar_icon_c130` |
| `Mig27` | `temp_radar_icon_mig27` |
| `F35` | `temp_radar_icon_f35` |
| `b2` | `temp_radar_icon_b2` |
| `f117` | `temp_radar_icon_f117` |
| `a10` | `temp_radar_icon_a10` |
| `ov10` | `temp_radar_icon_ov10` |
| `cruisemissile` | `temp_radar_icon_cruisemissile` |

Same relation-based coloring as [`VehicleBlippable`](vehicleblippable) (ally/neutral/enemy at the same
±60 thresholds), plus a PMC-specific green not present on the shared base class, and this module doesn't
inherit `VehicleBlippable` at all — it reimplements the same color logic locally against
`OrientedBlippable` directly instead.

## Events
Doesn't defer to `Event.ObjectHibernation` like most other `Vehicles` pages — `OnActivate` creates the
instance and configures the blip immediately, with no wait for the object to leave hibernation first.

## Notes for modders
- Ensure that `OnActivate` is called appropriately to manage the lifecycle of support aircraft.
- Customize radar blip colors by modifying the faction relation logic or directly setting `tColor`.
- Adjust radar blip textures by changing the label checks and corresponding texture assignments.
- Be aware that marking an aircraft as unkillable with the "PMC" label may affect gameplay balance.