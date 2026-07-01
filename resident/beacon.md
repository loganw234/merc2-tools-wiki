---
title: Beacon
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [weapon, timer]
---

# Beacon

*Module: beacon.lua*

## Overview
The `Beacon` module represents a beacon object in the game world. It is responsible for playing animations and sound cues when the beacon is activated or deactivated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module that does not track per-instance state. It uses a global table `tEvents` to manage event handles for each beacon instance.

## Functions
### `Init()`
Initializes the `tEvents` table if it hasn't been initialized yet. This function runs once when the module is loaded.

### `OnActivate(uGuid, args)`
Called when the beacon object is activated by the engine. It plays a material animation and sets up a timer event to play a sound cue after 1 second.

### `OnDeactivate(uGuid, args)`
Called when the beacon object is deactivated by the engine. It stops the material animation and the sound cue, deletes the timer event, and clears the corresponding entry in the `tEvents` table.

## Events
- **Listens for:**
  - `Event.TimerRelative`: Triggered after 1 second to play a sound cue.
- **Fires:**
  - None

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called in the correct order when extending or modifying beacon behavior.
- The `tEvents` table is used to manage event handles, so be cautious when modifying it directly.