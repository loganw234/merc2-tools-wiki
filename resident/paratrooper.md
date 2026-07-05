---
title: Paratrooper
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, airborne]
verified: true
verified_note: 'deeper pass: re-confirmed all 3 functions + the ObjectHibernation/ObjectHealth subscriptions; added tTemplates (Chinese/Allied Airborne), the <100 health threshold, the 0.25s fade on Object.Remove; pruned the fabricated OnDeactivate modder note; cross-linked Paradrop/MrxUtil/namespaces.'
---

# Paratrooper

*Module: paratrooper.lua*

## Overview
The `Paratrooper` module is the script on a **falling paratrooper** (the soldier spawned by
[`Paradrop`](paradrop)). Its only job is the mid-air-to-ground handoff: once the trooper's health
drops below 100 — i.e. as soon as it takes any damage, including the landing impact — it swaps the
parachuting paratrooper object for a normal grounded "airborne" faction unit at the same
position/heading.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxUtil`](mrxutil)

## Instance pattern
**Not the `Inheritable` pattern — this file has no `inherit(...)` call at all.** Confirmed from source:
`tEvents = tEvents or {}` is declared at module scope but never actually indexed or assigned anywhere in
the file — genuinely dead/vestigial, not a real per-`uGuid` table in active use. Each activation just runs
its reactive `OnActivate` → `Start` → `RemoveChute` chain directly on the `uGuid` passed through as a
plain argument, with no stored per-instance state at all.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the paratrooper instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, iArg)`
Sets up an event listener for the `Event.ObjectHealth` event, which triggers when the paratrooper's health drops below 100. This event calls `RemoveChute`.

### `RemoveChute(uGuid, iArg)`
Reads the trooper's faction ([`MrxUtil.GetFaction`](mrxutil)), position and yaw, fades the paratrooper
object out over `0.25s` (`Object.Remove(uGuid, 0.25)`), and spawns `tTemplates[sFaction]`
(`"Chinese Airborne"` / `"Allied Airborne"`) at the same spot via [`Pg.Spawn`](../namespaces/pg).
`iArg` is threaded through the whole chain but never used.

{: .note }
> The trailing `Object.SetYaw(uGuid, yaw)` runs *after* `Object.Remove(uGuid, ...)`, so it targets the
> object being faded out (the newly spawned unit already got its yaw from the `Pg.Spawn` call) — a
> harmless leftover.

## Events
Both are real [`Event.Create`](../namespaces/event) subscriptions:

- **`Event.ObjectHibernation`** (`"awake"`, in `OnActivate`) → `Start`.
- **`Event.ObjectHealth`** filtered `"<", "100"` (in `Start`) → `RemoveChute`. Note the threshold is
  passed as the **string** `"100"`, matching the engine's filter format.

## Module constants & tunables
- **`tTemplates`** — the grounded unit spawned on landing/damage: `China = "Chinese Airborne"`,
  `Allied = "Allied Airborne"`. Only these two factions are wired; any other faction spawns nothing
  (`tTemplates[sFaction]` is `nil`).
- **Health threshold**: `"100"` — the `<` comparison in the `Event.ObjectHealth` filter. Since troopers
  presumably spawn at 100, essentially the first damage tick triggers the swap.
- `tEvents = tEvents or {}` is declared at module scope but never read or written — dead/vestigial.

## Notes for modders
- Swap which grounded units appear by editing `tTemplates`; pair with [`Paradrop`](paradrop)'s own
  `tTemplates` (the falling models) to keep faction sets consistent.
- The chute-to-ground swap is triggered purely by the `< 100` health filter — there is no timer or
  landing detection, so anything that damages the trooper mid-air also triggers it.
- There is **no** `OnDeactivate` in this file; do not assume a deactivation hook exists.