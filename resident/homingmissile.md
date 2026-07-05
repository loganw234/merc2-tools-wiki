---
title: HomingMissile
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [vehicle, blip]
verified: true
verified_note: "deeper pass: re-confirmed all 4 functions and the single Event.CreatePersistent(TimerRelative,0.1) flash timer; surfaced concrete blip constants (tColor {255,0,0}, tFlash {255,255,255}, nSize 1, nSortOrder 1, sTexture nil) as tunables; _HomingLaunched keys off tData.uAmmoGuid via GetFromGuid — confirmed direct call from antiair.lua, not an event"
---

# HomingMissile

*Module: homingmissile.lua*

## Overview
The `HomingMissile` module represents a homing missile in the game world. It inherits from the `Blippable` module to manage radar blips and adds specific behavior for flashing blips at regular intervals.

## Inheritance
- Inherits from: `Blippable`
- Imports: `none`

## Instance pattern
This is the [Blippable](blippable) rich-instance pattern (keyed by `uGuid`): `OnActivate` calls
`getfenv():Create(uGuid, uRuntimeOwner)` to mint a per-object instance whose prototype is this module. The
module-level blip fields become the prototype defaults every instance inherits:
- `tColor` = `{255, 0, 0}` (red) — default radar blip color.
- `tFlash` = `{255, 255, 255}` (white) — the color it flashes to.
- `nSize` = `1`, `nSortOrder` = `1`, `sTexture` = `nil` (no custom texture — uses the Blippable default).

Per-instance runtime fields set on `oSelf`:
- `bActive`: set `true` by `_HomingLaunched` once the missile is live.
- `bFlash`: toggled every tick by the flash timer; passed to `AddObjective` to alternate the blip color.
- `TimerEvent`: handle to the persistent flash timer (see Events); guarded so it's only created once.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the missile instance is activated. It creates a new per-instance table for the object using the module's prototype.

### `SetBlipped(oSelf)`
Calls `Blippable.SetBlipped(oSelf)` (the inherited base), then — if `oSelf.TimerEvent` isn't already set —
registers a persistent `Event.TimerRelative` at `0.1` s that flips `oSelf.bFlash` and calls
`oSelf:AddObjective(oSelf.bFlash)` each tick, producing the flashing blip. The handle is stored in
`oSelf.TimerEvent`.

### `ClearBlipped(oSelf)`
Removes the radar blip and marker for the missile. Deletes the timer event if it exists.

### `_HomingLaunched(oWidget, tData)`
A helper function that activates the missile when it is launched. It sets the missile as active and calls `SetBlipped` to add its blip.

**Confirmed: this does not spawn or fire the missile itself, despite the module name — it only reacts to
one that already exists.** `tData` carries a reference to an already-live missile object (`uAmmoGuid` per
the calling convention used at [`AntiAir`](antiair)'s own `_HomingLaunched`, which just forwards here).
The real spawn/launch is handled by something native, outside this file entirely — see
[`AntiAir`](antiair)'s notes and [`Junk.SpawnHomingProjectile`](../namespaces/junk#alarms--gameplay) for
the likely (unconfirmed) mechanism, and [`Airstrike`](../namespaces/airstrike) for the *other*, confirmed
projectile-spawning namespace this module does **not** use.

**Not wired via `Event.Create` in this file.** `HomingMissile._HomingLaunched` is invoked as a plain
cross-module function call, directly from `antiair.lua`'s own `_HomingLaunched(oWidget, tData)`
(confirmed: `src/resident/antiair.lua:399` reads
`HomingMissile._HomingLaunched(oWidget, tData)`). `AntiAir`'s version is presumably the actual
event/widget-callback target registered with the engine — that registration is `AntiAir`'s concern, not
this file's. `homingmissile.lua` itself contains zero `Event.*` references of any kind.

## Events
- `Event.TimerRelative` — one `Event.CreatePersistent(Event.TimerRelative, {0.1}, ...)` in `SetBlipped`,
  driving the 0.1 s blip flash. Deleted in `ClearBlipped`. This is the only `Event.*` reference in the file.
- `_HomingLaunched` is **not** an event. It's a plain function called directly by [AntiAir](antiair)
  (`src/resident/antiair.lua:399` → `HomingMissile._HomingLaunched(oWidget, tData)`), not an
  `Event.Create` registration. Any engine event/widget wiring lives in `AntiAir`, not here.

## Notes for modders
- **Blip appearance:** change the module-level `tColor` (`{255,0,0}`), `tFlash` (`{255,255,255}`), `nSize`
  (`1`), and `sTexture` (`nil`) to restyle the radar blip — these are inherited by every instance from
  [Blippable](blippable). Set `sTexture` to a texture name to give it a custom icon.
- **Flash rate:** the `0.1` in `SetBlipped`'s `Event.TimerRelative` is the flash period; raise it to slow
  the blink.
- **What this module does *not* do:** it does not spawn or fly the missile — it only blips one that already
  exists. The launch is driven by [AntiAir](antiair) / native code, which calls `_HomingLaunched` with
  `tData.uAmmoGuid` identifying the live projectile.