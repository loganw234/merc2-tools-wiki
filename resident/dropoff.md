---
title: Dropoff
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [dropoff, copter]
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
Handles the creation of a new cargo drop by helicopters. Determines the faction of the dropoff object, selects a random cargo template from the appropriate list, and creates the drop using `MrxCopterDrop.Create`. Increments the drop counter and restarts the timer if more drops are needed.

## Events
- Listens for `Event.ObjectHibernation` to start the timer when the object leaves hibernation.
- Listens for custom event `CargoDrop` to handle the creation of cargo drops.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the dropoff lifecycle.
- Customize the list of cargo templates by modifying the faction-specific tables (`tDropOffObjects`) in the script.
- Be aware that the interval between drops is randomized, with a default range of 30 to 60 seconds. Adjust this range by changing the parameters in `math.randf(30, 60)`.
- The module uses `MrxUtil.GetRandomTableElement` to select random cargo templates, so ensure that the faction-specific tables are correctly populated with valid object names.
- This module does not inherit from any other module and is a standalone utility for managing helicopter cargo drops.