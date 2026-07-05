---
title: MrxTimer
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [timer, hud]
verified: true
verified_note: "deeper pass: surfaced all field defaults (nStartTime 30, nWarning 5, iTray 1, etc.) and the four ui_HUD_Timer_* sound cues, fixed the vague Events section to the real Event.TimerRelative persistent timer, noted countdown-vs-up is inferred from start/stop; all functions re-confirmed against source"
---

# MrxTimer

*Module: mrxtimer.lua*

## Overview
The `MrxTimer` module is responsible for managing countdown and stopwatch timers in the game's user interface. It provides functionality to start, pause, resume, stop, and display timer values on the HUD (Heads-Up Display). The timer can be configured with various properties such as start time, stop time, step size, and whether to use tenths of a second.

## Inheritance
- Inherits from: `none` — base/utility module
- Imports: [`MrxUtil`](mrxutil), [`MrxGuiInterface`](mrxguiinterface)

## Instance pattern
**Not per-`uGuid`** — same class-factory pattern used elsewhere in `resident/`: `Create(mModule, self)` is
`self = self or {}; setmetatable(self, {__index = mModule}); return self`, no `tInstance` registry. It
tracks the following key fields:
- `nStartTime`: Starting time of the timer (default `30`). If `nStartTime > nStopTime`, the timer counts
  **down** (`_bCountdown` is set); otherwise it counts up.
- `nStopTime`: Time the timer stops at (default `0`).
- `nStep`: Seconds per tick / increment-decrement size (default `1`). Also the `Event.TimerRelative` interval.
- `bUseTenths`: Whether to display tenths of a second (default `false`).
- `nWarning`: Threshold at which the display turns `[red]` and warning sounds/`tWarnCallbacks` fire
  (default `5`).
- `iTray`: HUD `Hud.ObjectiveTray` slot the timer text is written to (default `1`).
- `bPlaySounds`: Whether to play the timer sound cues (default `true`).
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
- The only `Event.*` used is `Event.CreatePersistent(Event.TimerRelative, {self.nStep}, self._Update,
  {self})` — a persistent timer that fires `_Update` every `nStep` seconds. Created in `Start`/`Resume`,
  torn down with `Event.Delete` in `Pause`/`Stop`. No `Event.Create` subscriptions to game events; the
  `tWarnCallbacks`/`tDoneCallbacks` "callbacks" are plain Lua function tables the module calls directly, not
  engine events.

## Notes for modders
- **Sound cues fired (all via `Sound.CueSound(0, ...)`, gated on `bPlaySounds`)**: `"ui_HUD_Timer_Start"`
  on `Start`; `"ui_HUD_Timer_Increment"` when the display crosses a minute/10s/1s boundary (the
  `nIncrementAlert` step in `_Update`); `"ui_HUD_Timer_Alert"` when crossing `nWarning`;
  `"ui_HUD_Timer_End"` when reaching `nStopTime`. Set `bPlaySounds = false` for a silent timer.
- **The set-up pattern**: build a table of the fields above, pass it to `Create`, register
  `tWarnCallbacks`/`tDoneCallbacks` (each an array of `{fn, args}` pairs — `_CallCallbacks` runs them via
  `MrxUtil.CallWithOptionalArgs`), then call `Start`. Use `AddTime`/`SetTime` to adjust mid-run.
- **Countdown vs. count-up is inferred, not a flag** — it's decided in `Start` purely from
  `nStartTime > nStopTime`. To count up, set `nStartTime < nStopTime`.
- **`Display` colors the text `[red]`** once inside the warning band and prepends `sLabel` if set — the
  timer is written to `Hud.ObjectiveTray` slot `iTray`, so two timers need different `iTray` values or they
  overwrite each other.