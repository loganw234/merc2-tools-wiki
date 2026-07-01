---
title: Paradrop
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [support, paratrooper]
---

# Paradrop

*Module: paradrop.lua*

## Overview
The `Paradrop` module is responsible for deploying a squad of paratroopers via an aircraft. It inherits from `OrientedBlippable` to manage radar blips and orientation, and uses the `MrxUtil` library for faction-related utilities. The module sets up a timed sequence to drop 16 paratroopers at intervals.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tColor`: The color of the radar blip based on faction relation.
- `nRelation`: The relation between the aircraft's faction and the PMC.

## Functions
### `OnActivate(uGuid)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid)`
Creates a new per-instance table for the object using the module's prototype. Determines the faction relation and sets the radar blip color accordingly. Activates the radar blip and schedules 16 paratrooper drops at intervals of 0.75 seconds starting at 5.25 seconds.

### `DropDude(uGuid, iArg)`
Called by the timer event to drop a paratrooper. Checks if the aircraft is still alive, retrieves its position and orientation, and spawns a paratrooper near the aircraft's position with a random offset.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for custom event `DropDude` to drop each paratrooper at scheduled intervals.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the paradrop mission.
- Customize the number of paratroopers, their spawn interval, and their initial position by modifying the relevant parameters in the script.
- Be aware that the radar blip color is determined by the faction relation between the aircraft's faction and the PMC. Adjustments to faction relations may affect the blip color.
- The `DropDude` function uses random offsets for paratrooper positions, which can be modified to achieve different drop patterns.