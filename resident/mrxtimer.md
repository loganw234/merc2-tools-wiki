---
title: MrxTimer
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [timer, hud]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxTimer

*Module: mrxtimer.lua*

## Overview
The `MrxTimer` module is responsible for managing countdown and stopwatch timers in the game's user interface. It provides functionality to start, pause, resume, stop, and display timer values on the HUD (Heads-Up Display). The timer can be configured with various properties such as start time, stop time, step size, and whether to use tenths of a second.

## Inheritance
- Inherits from: `none` — base/utility module
- Imports: `MrxUtil`, `MrxGuiInterface`

## Instance pattern
**Not per-`uGuid`** — same class-factory pattern used elsewhere in `resident/`: `Create(mModule, self)` is
`self = self or {}; setmetatable(self, {__index = mModule}); return self`, no `tInstance` registry. It
tracks the following key fields:
- `nStartTime`: The starting time of the timer.
- `nStopTime`: The stopping time of the timer.
- `nStep`: The increment/decrement step size for each tick.
- `bUseTenths`: Whether to display tenths of a second.
- `nWarning`: The time at which warning sounds and visual alerts are triggered.
- `iTray`: The HUD tray slot where the timer is displayed.
- `bPlaySounds`: Whether to play sound cues for various timer events.
- `_iCurrentTime`: The current time value of the timer.
- `_bCountdown`: Indicates whether the timer is counting down or up.
- `_TimerEvent`: The event handle for the timer's update callback.
- `sLabel`: An optional label text displayed with the timer.
- `tWarnCallbacks`: Callback functions triggered when the timer reaches the warning time.
- `tDoneCallbacks`: Callback functions triggered when the timer reaches its stop time.

## Functions
### `Create(mModule, self)`
Creates a new per-instance table for the timer using the module's prototype. Initializes default values for various fields if they are not provided.

### `Start(self)`
Initializes the timer with the starting time and sets up the update event to call `_Update` at regular intervals. Plays a start sound if enabled.

### `Display(self)`
Updates the HUD display of the timer based on the current time value, applying color changes for warnings and appending any optional label text.

### `Pause(self)`
Pauses the timer by deleting the update event.

### `Resume(self)`
Resumes the timer by setting up the update event again.

### `AddTime(self, iTime)`
Adds a specified amount of time to the current timer value and updates the display.

### `Stop(self)`
Stops the timer by clearing the HUD slot and deleting the update event. Plays an end sound if enabled.

### `_Update(self)`
The internal function that updates the timer's current time, checks for warning conditions, triggers callbacks, and updates the display. Also handles the transition to stop time and plays alert sounds as needed.

### `GetTime(self)`
Returns the current time value of the timer.

### `SetTime(self, iNewTime)`
Sets a new time value for the timer and updates the display.

### `_CallCallbacks(t)`
A helper function that calls all registered callbacks in a table with optional arguments.

## Events
- Listens for custom event triggers within its own methods to manage timer state and fire callbacks.

## Notes for modders
- Ensure that `Start`, `Pause`, `Resume`, and `Stop` are called appropriately to manage the timer's lifecycle.
- Customize timer behavior by setting fields like `nStartTime`, `nStopTime`, `bUseTenths`, and `iTray`.
- Use `AddTime` to dynamically adjust the timer value during runtime.
- Register callbacks for warning and done events using the `tWarnCallbacks` and `tDoneCallbacks` tables.
- Be aware that sound cues (`bPlaySounds`) may affect player experience, especially in multiplayer scenarios.