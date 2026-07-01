---
title: MrxMissionBoundary
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mission, boundary]
---

# MrxMissionBoundary

*Module: mrxmissionboundary.lua*

## Overview
The `MrxMissionBoundary` module is designed to manage mission boundaries or proximity-based triggers in the game. It handles player entry and exit events from a specified region or point, optionally triggering voice-over sequences and timers based on configuration.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxTimer`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages events and callbacks for mission boundaries or proximity triggers.

## Functions
### `Create(srcObj, tConfig)`
Initializes the mission boundary with the provided configuration. Sets up event listeners for player entry/exit from the specified region or point, and initializes timers and voice-over sequences if configured.

### `Cancel(self)`
Cancels all active events and stops any running timers associated with the mission boundary.

### `GetRegion(self)`
Returns the GUID of the region associated with the mission boundary.

### `_OutsideBoundary(self, uCharacter)`
Handles the event when a player exits the specified region. Triggers voice-over sequences if configured and starts a timer.

### `_InsideBoundary(self, uCharacter)`
Handles the event when a player re-enters the specified region after exiting. Stops any running timers and triggers return callbacks.

### `_OutsideRange(self, uCharacter)`
Handles the event when a player moves outside the specified proximity range from a point. Triggers voice-over sequences if configured and starts a timer.

### `_InsideRange(self, uCharacter)`
Handles the event when a player re-enters the specified proximity range after moving outside. Stops any running timers and triggers return callbacks.

### `_StartTimer(self)`
Creates and starts a timer based on the mission boundary configuration. The timer includes warning and fail times, and triggers corresponding callbacks.

### `_WarnTimeExpired(self)`
Handles the expiration of the warning time for the timer. Triggers voice-over sequences if configured and calls the warning callback.

### `_FailTimeExpired(self)`
Handles the expiration of the fail time for the timer. Calls the fail callback, stops the timer, and cleans up associated events.

### `_CallCallback(self, sStatus)`
Calls the configured callback function with the current status (e.g., "exit", "return", "warning", "fail") and any additional data provided in the configuration.

## Events
- Listens for `Event.Boundary` to handle player entry/exit from a specified region.
- Listens for `Event.ObjectProximity` to handle player proximity to a specified point.
- Creates and manages custom events for timer warnings and failures.

## Notes for modders
- Ensure that the configuration (`tConfig`) provided to `Create` includes necessary fields such as `sRegionName`, `sPoint`, `fRadius`, `fCallback`, etc.
- Use `Cancel` to properly clean up any active events and timers when the mission boundary is no longer needed.
- Customize voice-over sequences and timer settings through the configuration to enhance mission dynamics.
- Be aware that network synchronization may affect multiplayer behavior, especially if players are tethered or have different character positions.