---
title: OrientedBlippable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [blip, radar]
verified: true
verified_note: "deeper pass: re-confirmed all functions/events against source (OnActivate creates immediately, no hibernation wait; bRotate is a module constant; flash timer is Event.TimerRelative persistent @0.05s); added sibling cross-link to EnemyBlippable"
---

# OrientedBlippable

*Module: orientedblippable.lua*

## Overview
`OrientedBlippable` extends [`Blippable`](blippable) with rotation (blips that turn to match the object's
facing) and optional flashing (a blip that periodically re-adds itself with `bFlash=true`). It's the direct
parent of [`VehicleBlippable`](vehicleblippable), and a sibling of [`EnemyBlippable`](enemyblippable) in the
blip chain. The one module-level constant it adds is `bRotate = true`.

**`OnActivate` here does not defer through `Event.ObjectHibernation`/`Awake` like `Blippable`/`Inheritable`
do** — it calls `oPrototype:Create(uGuid, uRuntimeOwner)` immediately:

```lua
function OnActivate(uGuid, uRuntimeOwner, iArg)
  Debug.Printf("OrientedBlippable OnActivate")
  local oPrototype = getfenv()
  local oInstance = oPrototype:Create(uGuid, uRuntimeOwner)
end
```

No `Awake` function exists anywhere in this file. Whether this is intentional or an inconsistency with the
rest of the inheritance chain isn't confirmed either way — but a module built on `OrientedBlippable`
directly (rather than through `VehicleBlippable`, which defines its own `OnActivate`/`Start` and doesn't
use this one) creates its instance immediately on activation, not after leaving hibernation.

## Inheritance
- Inherits from: [`Blippable`](blippable)
- Imports: none

## Instance pattern
Per-instance field: `TimerEvent` — the persistent flash-timer handle, set by `SetBlipped` and cleared by
`ClearBlipped`.

`bRotate = true` is a **module-level constant** (declared once at the top of the file), not a per-instance
field — every instance reads the same shared value via the prototype-inheritance fallback (same mechanism
documented on [`Inheritable`](inheritable) and [`VehicleBlippable`](vehicleblippable)). `bOriented` is set
directly on `self` inside `SetBlipped` (`oSelf.bOriented = true`) — that one genuinely is per-instance,
though every instance ends up with the same value.

## Functions

### `OnActivate(uGuid, uRuntimeOwner, iArg)`
**See the callout above — creates the instance immediately, no hibernation wait.**

### `SetBlipped(oSelf)`
Sets `oSelf.bOriented = true`, calls `Blippable.SetBlipped(oSelf)` to do the actual radar/marker
registration, then — only if `oSelf.bFlash` is set and no `TimerEvent` already exists — starts a
persistent 0.05-second-interval timer (`TimerCallback`) that keeps re-adding the objective with flashing
enabled.

### `TimerCallback(oSelf)`
The flash-timer's own callback: just calls `oSelf:AddObjective(oSelf.bFlash)` every tick.

### `ClearBlipped(oSelf)`
Deletes the `TimerEvent` if one exists (stopping the flash), then calls `Blippable.ClearBlipped(oSelf)`.

## Events
- No `Event.ObjectHibernation` listener in this file — see the `OnActivate` callout above.
- `TimerEvent` (`Event.TimerRelative`, persistent, 0.05s interval) drives the flashing behavior when
  `bFlash` is set — created in `SetBlipped`, torn down in `ClearBlipped`.

## Notes for modders
- **Set `self.bFlash = true` before calling `SetBlipped`** if you want a flashing blip — flashing isn't
  automatic just from inheriting this module, it's opt-in per instance via that field.
- Everything else about configuring the blip itself (`tColor`, `sTexture`, `nSize`, `tMarker`, `bNetSync`)
  is inherited unchanged from [`Blippable`](blippable) — see that page for the full field list.
- If you're building something new on this module directly (not through `VehicleBlippable`), remember
  activation happens immediately, not after an `Event.ObjectHibernation` wait — don't assume the object is
  necessarily "awake" yet the way the `Inheritable`/`Blippable` pattern elsewhere on this wiki guarantees.
