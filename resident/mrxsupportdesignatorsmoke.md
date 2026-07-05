---
title: MrxSupportDesignatorSmoke
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupportDesignator
tags: [support, designator]
verified: true
verified_note: "deeper pass: surfaced the color->hash and color->denial-particle tables, the smoke model + hardpoint hash, 10s lifetime, and the NETEVENT_SMOKEACTIVATE net-sync path; documented the color-hash-to-particle map and OnDeny denial smoke; cross-linked base + consumers"
---

# MrxSupportDesignatorSmoke

*Module: mrxsupportdesignatorsmoke.lua*

## Overview
`MrxSupportDesignatorSmoke` is the colored-smoke [designator](mrxsupportdesignator) subtype — the marker used by air-support strikes ([`MrxGunship`](mrxgunship), [`MrxTankBuster`](mrxtankbuster)). When designation completes it starts a colored smoke emitter on the thrown grenade object, network-syncs the smoke to remote players so everyone sees it, and auto-removes it after 10 seconds. A **denied** throw instead spawns a "failure" smoke variant. It's the only designator subtype that does its own net replication.

## Inheritance
- Inherits from: [`MrxSupportDesignator`](mrxsupportdesignator)
- Imports: none

## Instance pattern
**Same class-factory pattern as `MrxSupportDesignator`, not per-`uGuid`** — `Create(self, oNewDesignator)`
builds a new table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no
`tInstance` registry. It tracks the following key fields:
- `uOwner`: The owner of the designator.
- `bDesignateOnDeath`: Whether to designate on death.
- `bDesignationComplete`: Indicates if the designation is complete.
- `sDesignationType`: The type of designation, set to "Smoke Designator".
- `fValidationFunction`: Function used for validation, set to `MrxSupportDesignator.ValidateGroundDropZone`.
- `tCallbackList`: List of callbacks for designation completion.
- `sSmokeHash`: Hash value for the smoke color.
- `sDenialSmokeTemplate`: Template for denial smoke.
- `sAATestLevel`: Anti-air test level, set to "basic".
- `nX`, `nY`, `nZ`: Position coordinates of the designator.
- `uGuid`: Unique identifier for the instance.

## Functions
### `Init()` / `Deinit()`
Engine lifecycle hooks (called by the loader). Load/unload the smoke grenade model `Pg.LoadAsset("global_weapon_m34wp", "model")`.

### `Create(self, oNewDesignator)`
Stamps the smoke fields: `sDesignationType = "Smoke Designator"`, `sAATestLevel = "basic"`, `bDesignateOnDeath = false`, `fValidationFunction = MrxSupportDesignator.ValidateGroundDropZone` (ground-only). Defaults `sSmokeHash = "0x02f6773f"` (red) and `sDenialSmokeTemplate = "global_particle_flaresmoke_fail"`, and registers `DesignationCompleteCallback` as the completion callback.

### `DesignationCompleteCallback(self)`
Fires the local smoke. Starts a particle emitter on the grenade object with `ObjectState.StartEmitter(self.uGuid, uHp, uTemplate)` — where `uHp = StringToGuid("0x16516bb1")` is the emitter **hardpoint** and `uTemplate = StringToGuid(self.sSmokeHash)` is the colored smoke. Disables physics on the grenade, then `Net.SendCustomEvent("MrxSupportDesignatorSmoke", NETEVENT_SMOKEACTIVATE, {...})` so remote players spawn the same smoke (looked up by particle name via `tColorHashToName`), and schedules `RemoveSmoke` in **10s** via [`Event.TimerRelative`](../namespaces/event).

### `NetEventCallback(nEventType, tArgs)`
Remote handler. When it receives `NETEVENT_SMOKEACTIVATE`, calls `NetSafeDesignationCompleteCallback` with the unpacked args — this is how the smoke appears on other players' machines.

### `NetSafeDesignationCompleteCallback(sTemplateHashName, nx, ny, nz, sBeaconId)`
Spawns the replicated smoke particle at the given coords ([`Pg.Spawn`](../namespaces/pg)), stores it in `tSmokeGuids[nSmokeGuids]`, schedules its removal in 10s, and increments `nSmokeGuids`.

### `NetSafeRemoveSmoke(sBeaconId)`
Removes a replicated smoke by its index into `tSmokeGuids`.

### `RemoveSmoke(self)`
Removes the local designator/grenade object if it still has a `uGuid`.

### `OnDeny(self, uGuid)`
Denial path. Removes the grenade and, at its position, spawns `self.sDenialSmokeTemplate` (the color-matched **"_fail" particle**) via [`Pg.Spawn`](../namespaces/pg) — the visual "support denied here" puff.

### `SetSmokeColor(self, sColor)`
Sets `sSmokeHash` (from `tColorList`) and `sDenialSmokeTemplate` (from `tDenialColorList`) for the given color string; unknown colors fall back to red. Both [`MrxGunship`](mrxgunship) and [`MrxTankBuster`](mrxtankbuster) call `SetSmokeColor("red")`.

### `GetType(self)`
Returns `"smoke"`.

## Events
No `Event.Create` subscriptions. Cross-machine sync is via `Net.SendCustomEvent` / `NetEventCallback` (custom net events, not `Event.*`). The two 10-second lifetimes (local `RemoveSmoke`, remote `NetSafeRemoveSmoke`) are scheduled with [`Event.TimerRelative`](../namespaces/event).

## Module constants & tunables
Module-level tables/values (top of file) — the reskin/tuning surface:
- `NETEVENT_SMOKEACTIVATE = 0` — the custom net-event id.
- `tColorList` — color → smoke template hash: `red = "0x02f6773f"`, `green = "0x41675d0b"`, `blue = "0x6efe9d26"`, `yellow = "0xf8171566"`.
- `tColorHashToName` — hash → particle name for the **remote** spawn: `"global_particle_flaresmoke"` (red), `"..._green"`, `"..._lightblue"` (blue), `"..._yellow"`.
- `tDenialColorList` — color → failure particle: `"global_particle_flaresmoke_fail"`, `"..._green_fail"`, `"..._lightblue_fail"`, `"..._yellow_fail"`.
- Model asset `"global_weapon_m34wp"`; emitter hardpoint hash `"0x16516bb1"`.
- Lifetime: **10 seconds** (both local and replicated).

## Notes for modders
- `SetSmokeColor` is the clean color switch (`"red"`/`"green"`/`"blue"`/`"yellow"`); it updates both the live smoke and the denial puff together. Anything else falls back to red.
- To change the smoke duration, edit the two `Event.TimerRelative` `{10}` timers (local in `DesignationCompleteCallback`, remote in `NetSafeDesignationCompleteCallback`) — change only one and the smoke will linger on some clients longer than others.
- This is the only designator subtype with its own net replication path (`Net.SendCustomEvent` + `NetEventCallback`). If you add a new color, you must extend all three tables (`tColorList`, `tColorHashToName`, `tDenialColorList`) or the remote spawn/denial visual will be wrong.
- `fValidationFunction = ValidateGroundDropZone` means smoke is **ground-only** (unlike the water-capable flare); reassign it to allow water placement.