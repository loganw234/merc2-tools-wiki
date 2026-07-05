---
title: Dropoff
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [dropoff, copter]
verified: true
verified_note: fixed Events section (CargoDrop is a table key, not an Event.* constant), noted unlocalized x/y/z globals and dead NumDrops reset in OnDeactivate
---

# Dropoff

*Module: dropoff.lua*

## Overview
The `Dropoff` module is responsible for managing the periodic dropping of random faction containers or vehicles by helicopters. It sets up a timer to trigger cargo drops at intervals between 30 and 60 seconds.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxCopterDrop`, `MrxUtil`

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

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the dropoff lifecycle.
- Customize the list of cargo templates by modifying the faction-specific tables (`tDropOffObjects`) in the script.
- Be aware that the interval between drops is randomized, with a default range of 30 to 60 seconds. Adjust this range by changing the parameters in `math.randf(30, 60)`.
- The module uses `MrxUtil.GetRandomTableElement` to select random cargo templates, so ensure that the faction-specific tables are correctly populated with valid object names.
- This module does not inherit from any other module and is a standalone utility for managing helicopter cargo drops.
- `x`, `y`, `z`, `HeloFaction`, `tDropOffObjects`, and `sCargoTemplate` in `SetupCargoDrop` are all plain globals (no `local`), so they leak into the shared module environment; this is how the source is actually written, not a wiki simplification.
- `OnDeactivate` sets the global `NumDrops = nil`, but nothing else in the file ever reads/writes that particular global (the real counter is passed as a parameter through `StartTimer`/`SetupCargoDrop`) — this line appears to be dead/vestigial cleanup.