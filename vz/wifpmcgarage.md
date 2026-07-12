---
title: WifPmcGarage
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 4
inherits: none
tags: [world-flow]
verified: false
---

# WifPmcGarage

## Overview
`WifPmcGarage` manages the player's PMC-HQ vehicle storage across three physical regions — the garage
(cars/tanks), the helipad (helicopters), and the dock (boats). It runs in one of two mutually-exclusive
modes: a simple "basic" mode with 3 fixed physical parking slots per region, and a one-way "advanced" mode
(unlocked later in the campaign) that replaces physical slots with a `MrxGuiGarage` menu backed by counted
`MrxPmc` support quantities. It also owns two unrelated pieces of PMC-HQ set dressing: the mechanic NPC
"Eva" who opens the garage menu, and Fiona's personal car.

## Inheritance
- Inherits from: none — singleton utility/manager module.
- Imports: `MrxState`, `MrxPmc`, `MrxSupportData`, [`WifPmcInterior`](wifpmcinterior), `MrxGuiGarage`,
  `MrxUtil`, `MrxVoSequence`.

## Instance pattern
Singleton-state manager (module-level fields, no `uGuid` — there's exactly one PMC garage). Key state:
- `_tStorage` — per-region (1 = garage, 2 = helipad, 3 = dock) vehicle storage; in basic mode a
  slot-indexed array of live vehicle GUIDs, in advanced mode a map of template GUID → stored count.
- `_bAdvanced` — the one-way mode switch (see `SetAdvancedMode`).
- `_tRegionEvents`, `_tGarageDoorEvents`, `_tLastVehicles` — per-region boundary/door event handles and
  the last vehicle dropped at each drop-off.
- `_bPmcAwake`, `_vCurrentRegion`/`_uCurrentRegion`/`_nCurrentSlot` — hibernation and
  current-trigger-region tracking.
- `_uEva`/`_uEvaAction` — the spawned mechanic NPC and her talk-context-action handle.
- `_uFionaCar`/`_uFionaCarDead`/`_uFionaCarEvent`/`_uFionaCarEnterEvent`/`_uFionaCarWinchEvent` — Fiona's
  personal car and its death/re-entry watchers.

## Functions

**Public API:**

### `Unlock()`
Sets `_bPmcAwake = true` and immediately calls `_OnAsleep()`. Because `_OnAsleep()`'s own guard requires
`_bPmcAwake` to already be true, this doesn't finish "waking up" the garage on its own — it arms the
hibernation watcher that calls `_OnWakeUp` once the PMC HQ prop next leaves hibernation. Called
externally from [`WifPmcInterior`](wifpmcinterior) when the PMC HQ unlocks.

### `SetAdvancedMode()`
One-way (guarded by `_bAdvanced`) switch from basic to advanced mode: exits the player's current region if
inside one, tears down per-slot boundary events beyond slot 1, converts every physically-stored vehicle
into a counted support entry via `_AddVehicle(..., -1)`, fades/relabels those vehicles out of the world,
and re-activates the garage doors.

### `ResetSingleton()`
In basic mode, deletes every currently-stored vehicle object outright; resets `_tStorage` to three empty
regions either way and re-arms the hibernation watcher via `_OnAsleep()`.

### `OpenVehicleInventory(fOnComplete, fOnCancel)`
Advanced-mode only (no-ops via `fOnCancel` otherwise); builds and shows the `MrxGuiGarage` menu, listing
both physically-stored vehicles and any support-type vehicle the player currently owns enough of
(`MrxSupportData.tSupportData`, filtered to Civilian/Heavy/Light/Heli/Boat types).

### `CheckFionaCar(bFromPmc)`
(Re)spawns Fiona's car (`_ksFionaCar = "Phoenix (Racing)"`) at its fixed spawn point and wires up its
death/enter/winch watchers. Called externally by [`WifPmcInterior`](wifpmcinterior) (with
`bFromPmc = true`) both on first PMC-HQ unlock and on load if the save already had it unlocked.

### `SaveSingleton()` / `LoadSingleton(tData)`
In advanced mode, saves/restores `_tStorage` as-is (support counts); in basic mode, saves each stored
vehicle's parent template plus position/yaw and respawns them via `Pg.Spawn` on load.

**Internal helpers** (brief): `_CompleteCallback`/`_SpawnVehicle`/`_SpawnVehicleCleanup` (GUI selection →
world spawn), `_ActivateEva`/`_DeactivateEva` (mechanic NPC lifecycle), `_ActivateGarageDoors`/
`_DeactivateGarageDoors`/`_OnGarageDoorEnter`/`_OnGarageDoorExit` (physical door open/close on boundary
trigger), `_OnWakeUp`/`_OnAsleep` (hibernation ping-pong), `_OnRegionEnter`/`_OnRegionExit`/
`_OnVehicleEnter`/`_OnVehicleExit`/`_OnVehicleDeath` (per-region vehicle in/out tracking),
`_CompleteOnVehicleEnter`/`_MoveCharacter`/`_OnAddComplete` (advanced-mode store-and-teleport-out
sequence), `_AddVehicle`/`_RemoveVehicle` (the actual storage bookkeeping for both modes),
`_FindVehicleInSupport`/`_AddVehicleToSupport`/`_RemoveVehicleFromSupport` (bridge to `MrxPmc` support
quantities), `_OnFionaCarEnter`/`_OnFionaCarDeath` (Fiona-car VO and insurance cost),
`_GetVehicleData`/`_SpawnVehicleFromData` (basic-mode save/load helpers).

## Events
`Event.Boundary` (region/garage-door enter and exit), `Event.ObjectInSeat` (vehicle enter/exit detection,
Fiona's car entry, winch-in), `Event.ObjectHibernation` (PMC HQ sleep/wake, Eva despawn, Fiona-car
respawn-after-death), `Event.ObjectDeath` (Fiona's car destroyed), `Event.ObjectIsReady` +
`Event.ContextAction` (Eva's talk prompt), `Event.TimerRelative` (post-spawn vehicle cleanup, post-store
fade-out).

## Notes for modders
- **Likely bug:** inside `CheckFionaCar`'s early-return guard, `_bPMCAwake` (capital PMC) is a *different*
  global from `_bPmcAwake` used everywhere else in this file (case mismatch) — since nothing ever sets
  `_bPMCAwake`, that guard clause never actually fires.
- **Dead code:** the locals `_tRegions` and `_knMaxVehicleSlots` (both declared near the top of the file)
  are never read anywhere in this file, and don't appear anywhere else in this corpus either — likely
  leftover from an earlier version of this system.
- **Dead code:** `_uDeath` is deleted/cleared in `SetAdvancedMode()` but never assigned anywhere in this
  file (or referenced anywhere else in the corpus) — that cleanup is a no-op in every case observable
  here.
- [`WifPmcInterior`](wifpmcinterior) is the only confirmed external caller (`Unlock()`,
  `CheckFionaCar(true)`) — treat it as the intended entry point rather than calling into this module
  directly from elsewhere.
