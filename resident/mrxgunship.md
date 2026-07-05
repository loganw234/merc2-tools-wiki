---
title: MrxGunship
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, gunship]
verified: true
verified_note: "deeper pass: documented the self-rescheduling Salvo loop, muzzle-flash particle + tankgun sound cue, VZ/China/Guerilla targeting, Gunship Shell payload; flagged undefined _NoValidation and the uPlayer global in SpawnOrdnance; cross-linked Airstrike/smoke"
---

# MrxGunship

*Module: mrxgunship.lua*

## Overview
`MrxGunship` is a loitering AC130 gunship: after the player pops red smoke, the gunship arrives and repeatedly strafes enemy targets near the smoke in rolling 4-shot salvos until it leaves range. It inherits from [`MrxSupport`](mrxsupport) and designates with [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) (plus [`MrxUtil`](mrxutil) for distance math).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke), [`MrxUtil`](mrxutil)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uJet`: The GUID of the AC130 jet.
- `uOwner`: The GUID of the player who owns this support vehicle.
- `oDesignator`: An instance of `MrxSupportDesignatorSmoke` used for designating targets.

## Functions
### `Create(self, uPlayerGuid)`
Builds the instance. Creates a [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) with color `"red"`, AA level `"basic"`, and `SetValidationFunction(_NoValidation)`. Recruit `"Fiona"`, module name `"MrxGunship"`.

{: .note }
> `_NoValidation` is referenced but **not defined** anywhere in this module or its parents — as written it resolves to `nil`, which is the same as "no validation function," so the intent (skip drop-zone validation) still holds by accident. Likely a decompile/leftover artifact; don't rely on `_NoValidation` being a real callable.

### `DesignationCallback(self)`
Runs on smoke-designation complete. Computes spawn/approach points from the camera, builds width/height basis vectors from the hero→smoke line, plays a Fiona VO line, then flies in `"Support Vehicle (AC130)"` with [`Airstrike.Flyby`](../namespaces/airstrike) (speed 45, callback `Salvo`, jet stored in `self.uJet`).

### `Salvo(self, uLastTarget)`
The loitering loop. Bails if the smoke target is gone, the jet is asleep, or the jet is more than **300 units** from the local character. Otherwise scans `Pg.GetAwakeObjects` within **100 units** of the smoke for a target labeled `"VZ"`, `"China"`, or `"Guerilla"` (skipping `uLastTarget`), schedules **4** `LaunchMissile` calls `0.25s` apart, then **re-schedules itself** 3 seconds later via [`Event.TimerRelative`](../namespaces/event) — this is what makes the gunship keep firing until it drifts out of range.

### `LaunchMissile(self, uTarget)`
Fires one shell. Jitters the target by `±25`, plays [`Sound.CueSound`](../namespaces/sound) `"wpn_tankgun_fire_npc"`, spawns particle `"global_particle_muzzleflash_tank"` at the jet, then spawns `"Gunship Shell"` via [`Airstrike.SpawnOrdnance`](../namespaces/airstrike) at speed scale 100, `"impact"`.

{: .warning }
> The `Airstrike.SpawnOrdnance("Gunship Shell", …, "impact", 1, uPlayer)` call passes `uPlayer` as the owner, but `uPlayer` is **never defined** in this module — it's a stray global that resolves to `nil`. So gunship-shell kills are un-attributed. Use `self.uOwner` if you fork this and want proper attribution.

### `_ValidateDropZone(fCallback, nX, nY, nZ, oSupport)`
Drop-zone validator wrapping `Ai.TestDropZone`. Defined but not wired up (validation is disabled via `_NoValidation`/`nil`); a spare hook.

## Events
No event subscriptions. `DesignationCallback` is the smoke designator's completion callback (via [`MrxSupport:Commence`](mrxsupport)); `Salvo` and `LaunchMissile` run on [`Event.TimerRelative`](../namespaces/event) timers. The self-rescheduling `Salvo` timer is the only reason the gunship keeps firing.

## Module constants & tunables
All inline (no module-level `local`s):
- Aircraft: `"Support Vehicle (AC130)"`; flyby speed 45.
- Payload: `"Gunship Shell"`, `nSpeedScale = 100`.
- Loop: scan radius **100** units, 4 shots per salvo `0.25s` apart, re-salvo every **3s**, gives up beyond **300** units from the jet.
- Targeting labels: `"VZ"`, `"China"`, `"Guerilla"`.
- FX: sound `"wpn_tankgun_fire_npc"`, muzzle particle `"global_particle_muzzleflash_tank"`.

## Notes for modders
- The 3-second self-rescheduling `Salvo` is the gunship's whole "loiter and keep firing" behavior — shorten the timer for a heavier gunship, lengthen it (or remove the re-schedule) to make it a one-pass strafe.
- Targeting is limited to VZ/China/Guerilla labels; edit the label check in `Salvo` to change who it engages.
- Swap `"Gunship Shell"` for another [Airstrike template](../namespaces/airstrike#confirmed-ordnance-template-name-strings), and the `"global_particle_muzzleflash_tank"` / `"wpn_tankgun_fire_npc"` pair if you want a different muzzle look/sound.