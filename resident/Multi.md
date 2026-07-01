---
title: Multi
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
---

# Multi

*Module: Multi.lua*

## Overview
The `Multi` module provides utility functions for spawning multiple game objects in the world. It includes functions to spawn templates in front of the camera and to scatter objects over a specified area.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module with no per-instance tables or fields.

## Functions
### `Multi(tObjects)`
Spawns multiple templates 10 meters in front of the camera. The function takes a table of object templates as input and spawns each template sequentially.
- **Parameters**: 
  - `tObjects`: A table containing the names of the object templates to spawn.
- **Returns**: None
- **Notes**: If no `tObjects` is provided, it prints usage instructions.

### `Scatter(sObject, nNumber, nOffset, nTime, nDistance, nHeight)`
Scatters a specified number of objects over an area in front of the camera. The function spawns objects at random positions within a given radius and at regular intervals.
- **Parameters**: 
  - `sObject`: The name of the object template to scatter.
  - `nNumber`: The number of objects to spawn (default is 1).
  - `nOffset`: The maximum offset for each spawned object (default is 0).
  - `nTime`: The total time over which to scatter the objects (default is 0).
  - `nDistance`: The distance from the camera where objects should be spawned (default is 10 meters).
  - `nHeight`: The height at which objects should be spawned (default is 0.5 meters).
- **Returns**: None
- **Notes**: If no `sObject` is provided, it prints usage instructions.

## Events
- Listens for none — this module does not subscribe to any engine events.
- Fires: `Event.TimerRelative` to schedule the spawning of additional objects in the `Scatter` function.

## Notes for modders
- Ensure that the object templates specified in `Multi` and `Scatter` exist in the game's data files.
- Adjust parameters like `nNumber`, `nOffset`, `nTime`, `nDistance`, and `nHeight` to control the scattering behavior.
- Be aware of potential performance implications when spawning a large number of objects.