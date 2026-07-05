---
title: Dropoff
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [dropoff, copter]
verified: true
verified_note: 'deeper pass: re-confirmed all functions/events; added a Module constants & templates section (per-faction tDropOffObjects pools, HeloFaction codes VZ/GR/CH/OC/AL/PR, 30-60s interval) and cross-linked MrxCopterDrop/MrxUtil; prior fixes (CargoDrop is a table key, leaked x/y/z globals, dead NumDrops reset) still hold'
---

# Dropoff

*Module: dropoff.lua*

## Overview
The `Dropoff` module is responsible for managing the periodic dropping of random faction containers or vehicles by helicopters. It sets up a timer to trigger cargo drops at intervals between 30 and 60 seconds.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxCopterDrop`](mrxcopterdrop) (spawns the helicopter that flies the cargo in),
  [`MrxUtil`](mrxutil) (`GetFaction`, `GetRandomTableElement`)

## Instance pattern
This is a stateless manager utility module (no per-instance table). It tracks the following key fields:
- `tEvents`: A table to store event handles for each dropoff object.
- `NumDrops`: A counter for the number of drops made.

## Functions
### `OnActivate(uGuid)`
Called when the dropoff object is activated. Initializes event storage and sets up a timer to start the cargo drop process.

### `OnDeactivate(uGuid)`
Called when the dropoff object is deactivated. Cleans up any active events and resets the module's state.

### `StartTimer(uGuid, NumDrops)`
Sets up a relative timer to trigger the next cargo drop. The interval is randomly chosen between 30 and 60 seconds.

### `SetupCargoDrop(uGuid, NumDrops)`
Handles the creation of a new cargo drop by helicopters. Reads the object's position into unlocalized globals `x, y, z` via `Object.GetPosition(uGuid)`, determines the faction of the dropoff object via `MrxUtil.GetFaction`, selects a random cargo template from the matching faction table, and creates the drop using `MrxCopterDrop.Create(HeloFaction, sCargoTemplate, x, y, z, false)`. Increments `NumDrops` and restarts the timer (`StartTimer`) if `NumDrops < 1` (so at most one repeat happens per call chain, since `OnActivate` always calls `StartTimer(uGuid, 0)`).

Faction branches covered: `VZ`, `Guerilla`, `China`, `OC`, `Allied`, `Pirate`. Any other faction value falls through with no `tDropOffObjects`/`HeloFaction` assignment, and `sCargoTemplate = MrxUtil.GetRandomTableElement(tDropOffObjects)` would then operate on a stale/previous table (or nil on first run) — no explicit "unknown faction" handling exists in this file.

## Events
- Listens for `Event.ObjectHibernation` (via `Event.Create`) to start the timer when the object leaves hibernation.
- Listens for `Event.TimerRelative` (via `Event.Create` in `StartTimer`) to trigger `SetupCargoDrop` after the randomized interval.
- `CargoDrop` is **not** an event constant — it's the table key `tEvents[uGuid].CargoDrop` used to store/guard the `Event.TimerRelative` handle so only one timer runs per `uGuid` at a time.

## Module constants & tunables
- Drop interval: `math.randf(30, 60)` seconds (inline literal, per timer).
- Helicopter faction codes passed to `MrxCopterDrop.Create` (`HeloFaction`): `VZ`, `GR` (Guerilla),
  `CH` (China), `OC`, `AL` (Allied), `PR` (Pirate).
- Cargo template pools (`tDropOffObjects`), one per faction — first four entries are shipping-container
  props, the fifth is a drivable vehicle:
  - **VZ**: `_port_containera_light`..`_port_containerd_light`, `"M151 .50Cal (VZ)"`
  - **Guerilla**: `_port_containera`..`_port_containerd`, `"M151 (MG) (GR)"`
  - **China**: `_port_containera`..`_port_containerd`, `"NGLV (MG)"`
  - **OC**: `_port_containera_light`..`_port_containerd_light`, `"EXT"`
  - **Allied**: `_port_containera`..`_port_containerd`, `"HMMWV (Armored) (50Cal)"`
  - **Pirate**: `_port_containera_light`..`_port_containerd_light`, `"T300 (M60)"`
- A random pool entry is picked with `MrxUtil.GetRandomTableElement` and dropped via
  `MrxCopterDrop.Create(HeloFaction, sCargoTemplate, x, y, z, false)`.

## Notes for modders
- Customize the drop by editing the faction-specific `tDropOffObjects` pools above, or swap
  `MrxCopterDrop.Create` for a different delivery — see [MrxCopterDrop](mrxcopterdrop).
- The `NumDrops < 1` self-restart means each activation produces effectively **one** cargo drop (the counter
  starts at `0`, increments to `1`, then stops) — raise that threshold to make a dropoff repeat.
- Be aware that the interval between drops is randomized, with a default range of 30 to 60 seconds. Adjust this range by changing the parameters in `math.randf(30, 60)`.
- The module uses `MrxUtil.GetRandomTableElement` to select random cargo templates, so ensure that the faction-specific tables are correctly populated with valid object names.
- This module does not inherit from any other module and is a standalone utility for managing helicopter cargo drops.
- `x`, `y`, `z`, `HeloFaction`, `tDropOffObjects`, and `sCargoTemplate` in `SetupCargoDrop` are all plain globals (no `local`), so they leak into the shared module environment; this is how the source is actually written, not a wiki simplification.
- `OnDeactivate` sets the global `NumDrops = nil`, but nothing else in the file ever reads/writes that particular global (the real counter is passed as a parameter through `StartTimer`/`SetupCargoDrop`) — this line appears to be dead/vestigial cleanup.