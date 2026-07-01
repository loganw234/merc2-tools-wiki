---
title: LifestyleOilLif001Table
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [lifestyle, vehicle]
---

# LifestyleOilLif001Table

*Module: lifestyle_oillif001_table.lua*

## Overview
The `LifestyleOilLif001Table` module is responsible for initializing and managing the state of a specific vehicle asset model named "OilLif001 Table". It sets up two riders in the vehicle with predefined states related to an arm wrestling job.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state and operates globally on the specified vehicle asset model.

## Functions
### `Init()`
Called during the initialization phase of the game. Logs a debug message indicating that the initialization has been called and then calls `SetStaging`.

### `SetStaging(self)`
Sets up the staging for the "OilLif001 Table" vehicle. It logs a debug message, retrieves the GUID of the vehicle by name, and gets the list of riders in the vehicle. It then assigns the first rider to `iRider1` and the second rider to `iRider2`. Finally, it sets the states for both riders related to an arm wrestling job and logs another debug message.

## Events
- Listens for none (no engine events are subscribed to or fired).

## Notes for modders
- Ensure that the vehicle asset model "OilLif001 Table" exists in the game world.
- The `SetStaging` function assumes there are exactly two riders in the vehicle. If this is not the case, additional logic may be needed to handle different numbers of riders.
- The states set for the riders (`lifestylejobPlayerArmwrestlingWinningloop01` and `lifestylejobOpponentArmwrestlingWinningloop01`) are specific to the arm wrestling job scenario. Adjust these states as necessary for different scenarios.
- This module does not handle any lifecycle events (e.g., `OnActivate`, `OnDeactivate`). It is purely a one-time initialization script.