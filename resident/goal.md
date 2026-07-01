---
title: Goal
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [goal, soccer]
---

# Goal

*Module: goal.lua*

## Overview
The `Goal` module is responsible for handling the soccer easter egg in the game. When a ball enters the `LR_Goal` boundary, it triggers a Fiona voice-over and awards the player 100,000 cash.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `MrxVoSequence`, `MrxPmc`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tEvents`: A table to store event handles and other state related to the goal.

## Functions
### `OnActivate(uGuid)`
Called when the goal instance is activated. It logs a debug message and sets up an event to call `SetupGoal` once the object leaves hibernation.

### `OnDeactivate(uGuid)`
Called when the goal instance is deactivated. It logs a debug message, deletes any associated voice-over events, and cleans up the `tEvents` table entry for this GUID.

### `SetupGoal(uBallGuid)`
Sets up the boundary event to listen for the ball entering the `LR_Goal`. When the ball enters, it starts Fiona's voice-over, adds 100,000 cash to the player's PMC, and removes the goal object from the world.

## Events
- Listens for `Event.ObjectHibernation` to call `SetupGoal` when the object leaves hibernation.
- Listens for custom event `Boundary` to handle the ball entering the goal.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the goal's lifecycle.
- Customize the voice-over and cash reward by modifying the `MrxVoSequence.Start` and `MrxPmc.AddCashQty` calls in `SetupGoal`.
- Be aware that the goal object is removed from the world after being triggered, so it will not be reusable.