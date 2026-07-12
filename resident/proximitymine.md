---
title: ProximityMine
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mine, proximity]
verified: true
verified_note: 'deeper pass: re-confirmed all 6 functions + the ObjectProximity/TimerRelative subscriptions; documented the exact trigger (6-unit "human" filter, non-networked flags) and the Airstrike.SpawnOrdnance payload ("Grenade MG Projectile", +8 up, distance 1.8, Object.Kill cleanup); cross-linked Airstrike/Object/Event namespaces + mine.'
---

# ProximityMine

*Module: proximitymine.lua*

## Overview
`ProximityMine` implements a buried anti-personnel mine: when any human comes within 6 units, the mine
removes itself and fires a `"Grenade MG Projectile"` straight up from its position, killing whoever
tripped it. (Contrast the more general [`mine`](mine) module.)

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
plain module-level table, `uEvent[uGuid]`, set up once via `Init()` alongside a single shared `uFilter`
(both true singleton/module-level fields, not per-instance), with no `Create`/`setmetatable`/rich-instance
factory anywhere. Each activated mine gets one event handle entry in `uEvent`, not a full instance object
with inherited methods. It tracks the following key fields:
- `uEvent`: A table to store event handles for each instance.
- `uFilter`: A single shared object filter used to detect human players, set up once in `Init()` — not per-instance.

## Functions
### `Init()`
Initializes the module by creating an event handle table and setting up an object filter to detect humans.

### `Deinit()`
Cleans up the module by clearing the event handle table and object filter.

### `OnActivate(uGuid, nArg)`
Engine lifecycle callback. Registers an `Event.ObjectProximity` event using the shared `uFilter`
(humans only), radius `6`, comparison `"<"`, and the two trailing `false` flags. Stores the handle in
`uEvent[uGuid]`. `nArg` is unused.

### `OnDeactivate(uGuid)`
Deletes the proximity event for this mine and clears `uEvent[uGuid]`.

### `Triggered(uGuid, tListOfObjects)`
Proximity callback. Schedules `Popup` after `0.001s` via [`Event.TimerRelative`](../namespaces/event)
(a one-frame defer). `tListOfObjects` is received but not used.

### `Popup(uGuid)`
Reads the mine's position (bails if it has none), removes the mine, and fires the ordnance:
```lua
Airstrike.SpawnOrdnance("Grenade MG Projectile", nX, nY, nZ, 0, 8, 0, "distance", 1.8, nil, Object.Kill, {})
```
i.e. a grenade projectile launched with a `+8` vertical velocity component, `"distance"` fuze mode at
`1.8`, and `Object.Kill` as the on-hit callback. See [`Airstrike`](../namespaces/airstrike).

## Events
- **`Event.ObjectProximity`** (in `OnActivate`, handle `uEvent[uGuid]`) — detects a human within 6
  units. This is a real subscription; `OnActivate`/`OnDeactivate` themselves are lifecycle callbacks.
- **`Event.TimerRelative`** (`0.001`s, in `Triggered`) — defers `Popup` by a frame.

## Module constants & tunables
- **Trigger radius**: `6` (units), the `Event.ObjectProximity` distance in `OnActivate`.
- **Filter**: `uFilter` is created once in `Init()` as `ObjectFilter.SetFilter(uFilter, "human")` — the
  mine only reacts to humans, not vehicles.
- **Ordnance**: template `"Grenade MG Projectile"`, launch offset `(0, 8, 0)`, `"distance"` fuze
  `1.8`, cleanup callback `Object.Kill`. These are the payload knobs.
- **Detonation delay**: `0.001s` (effectively immediate).

## Notes for modders
- Change the **radius** (`6`) in `OnActivate` and the **ordnance** args in `Popup` to retune the mine
  (bigger blast, different projectile, longer arming distance, etc.).
- The proximity filter is **humans only** by design — this mine ignores vehicles. Rebuild `uFilter` in
  `Init()` if you want it to trigger on something else.
- `Init()` must run before any mine activates (it creates `uEvent`/`uFilter`); `Deinit()` clears them.
  These are **shared module-level singletons**, not per-mine state.