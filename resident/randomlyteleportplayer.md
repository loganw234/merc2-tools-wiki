---
title: RandomlyTeleportPlayer
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [stress test, teleportation]
---

# RandomlyTeleportPlayer

*Module: randomlyteleportplayer.lua*

## Overview
The `RandomlyTeleportPlayer` module is a stress test utility that randomly teleports the local player to predefined locations in the game world. It sets up a timer to repeatedly perform this teleportation, adding variability by changing both the destination and the delay between teleports.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any persistent state beyond local variables used within its functions.

## Functions
### `Init()`
Called once when the module initializes. It starts the teleportation process by calling `Go`.

### `Go()`
Performs the random teleportation of the player:
1. Selects a random location from the predefined list.
2. Retrieves the GUID for the selected location.
3. If the GUID is valid, gets the position of the location.
4. If the position is valid, teleports the player to that position with an additional Y offset of 20 units.
5. Sets up a timer to call `Go` again after a random delay between 5 and 20 seconds.

## Events
- Listens for `Event.TimerRelative` to trigger the next teleportation.

## Notes for modders
- This module is intended as a stress test utility and should not be used in production environments.
- The list of locations (`tLocation`) can be modified to include other valid game locations.
- The random delay between teleports can be adjusted by changing the range in `Math.randf(5, 20)`.
- Be aware that frequent teleportation may cause disorientation or gameplay issues.