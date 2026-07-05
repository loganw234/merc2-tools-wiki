---
title: MrxGuiHudFactionGauge
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, faction]
verified: true
verified_note: 'deeper pass: DELETED fabricated Events section (source has ZERO Event.* calls — no ObjectHibernation/TimerRelative/PlayerJoined; timers use a native oTimer object + GuiUpdate handler); corrected Instance pattern (stateless module + per-widget CustomData, not a singleton — the buffer duplicates one gauge per faction); surfaced all module constants (_knMin/_knMax/_ksPursuit, level thresholds {0,25,50,75}, level colors, mood/delta colors); flagged Initialize referencing undefined _RiseToValue/_CancelRise'
---

# MrxGuiHudFactionGauge

*Module: mrxguihudfactiongauge.lua*

## Overview
The `MrxGuiHudFactionGauge` module is responsible for managing the graphical representation of faction gauges in the game's HUD. It handles the initialization, updating, and animation of these gauges based on various factors such as value changes, pursuit status, and timer events. This module ensures that the faction gauge accurately reflects the player's or NPC's faction standing and provides visual feedback through color changes and animations.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase` (via [`import("MrxGuiBase")`](../glossary#importname)) — uses `MrxGuiBase.Widget.SetVisible` (saved as `_RealSetVisible`). See [MrxGuiBase](mrxguibase).

## Instance pattern
**Stateless module + per-widget `CustomData`.** The module-level level tables (`_tLevels`/`_tLevelNames`/`_tLevelColors`) are shared configuration, set once by `Init()` (or overridden by `SetLevels`). Everything else is per-gauge: `Initialize(oWidget)` populates that gauge's `oWidget.CustomData` (bar/delta/icon/mood/pursuit child widgets, animation points, cached geometry) and copies the module functions onto the widget as methods (`oWidget.SetValue = SetValue`, `oWidget.StartPursuit = StartPursuitGauge`, etc.). It is **not** a singleton — [MrxGuiHudFactionBuffer](mrxguihudfactionbuffer) duplicates one gauge widget per faction from a template.

### Module constants & configuration (the tunables)
- `_knMin = 0`, `_knMax = 100` — the gauge's value range.
- `_ksPursuit = "[0x1cab5133]"` — localized-string hash for the pursuit label text (shown while a pursuit is active). See [hash-lookup](../hash-lookup).
- `_tLevels` (default `{0, 25, 50, 75}`) — the four mood-band thresholds, set by `Init()`.
- `_tLevelNames` (default `{"[0x671b379b]", "[0x7c4225bc]", "[0xdb614732]", "[0x8c4d842e]"}`) — localized-string hashes for the four band names.
- `_tLevelColors` — per-band bar RGB, set by `Init()`: band1 `{255,96,96}` (red), band2 `{160,160,160}` (grey), band3 `{96,96,255}` and band4 `{96,96,255}` (blue). Applied to `oGaugeFront:SetColor`.
- **Delta-bar colors** (the trailing change indicator, in `SetValueAndLevel`): dropping = `(128,0,0)` dark red, rising = `(0,128,0)` dark green.
- **Mood-text animation points** (in `Initialize`): raise = `(64,255,64)`, lower = `(210,0,0)`, plus the widget's original color as the rest point.
- **Pursuit bar color**: `oGaugeFront:SetColor(210, 0, 0)` while pursuit runs.

`Init()`, `SetLevels`, and the level tables above are the "re-skin the reputation UI" levers. `SetLevels(tThresholds, tNames, sPursuitName, bDisplayResult)` validates its input (thresholds must be numbers, ascending, first == 0; names must be strings and equal in count) and `Debug.Printf`s a specific error and returns `false` on any violation.

## Functions

### Init()

Initializes the module by setting up the level thresholds, level names, and level colors. It also logs validation errors if any of the setup conditions are not met.

### GetBarValueAndName(nValue)

Calculates the current bar value and name based on the given `nValue`. It determines the appropriate level range for the value and computes a normalized bar value within that range.

### SetLevels(tLevelThresholds, tLevelNames, sPursuitName, bDisplayResult)

Sets up the faction gauge levels with the provided thresholds, names, and pursuit name. Validates the input data to ensure it meets certain conditions (e.g., thresholds are in ascending order, first threshold is 0). If validation fails, it logs an error message.

### Initialize(oWidget)

Initializes the widget by setting up its custom data, children widgets, and animation points. It also sets up methods for interacting with the faction gauge (e.g., `SetValue`, `ChangeValue`, `StartTimer`).

### SetValue(oWidget, nValue, bInitialize)

Sets the value of the faction gauge to `nValue`. If `bInitialize` is true, it initializes the gauge by animating it from its current value to the new value. It also handles pursuit logic and updates the mood text accordingly.

### _TransitionToLevel(oWidget, nTargetLevel, nTargetValue, nRemainingTime, bRising)

Handles the transition between levels of the faction gauge. It calculates the time required for each level change and animates the gauge accordingly.

### SetValueAndLevel(oWidget, nNewValue, bInitialize, nTime, nNewLevel, fCallback, tCallbackData)

Sets the value and level of the faction gauge with optional animation. It updates the gauge's appearance (e.g., color, texture coordinates) and handles callbacks if provided.

### _SnapBarToValue(oWidget, nValue)
Adjusts the gauge bar's position and texture coordinates based on the given value. It also updates the color of the gauge front if a current level is set.

### GetValue(oWidget)
Retrieves the current value of the widget from its custom data.

### SetIcon(oWidget, sTexture)
Sets the texture for the icon associated with the widget.

### SetIconVisible(oWidget, bVisible, nTranslucency)
Controls the visibility and translucency of the icon associated with the widget.

### ChangeValue(oWidget, nDelta, bInitialize)
Changes the value of the widget by a specified delta. If `bInitialize` is true, it initializes the gauge to the new value.

### StartTimer(oWidget, nTime, fCallback, tCallbackData)
Starts a timer for the widget with a specified duration and callback function. It also sets up the timer's custom data.

### StopTimer(oWidget)
Stops the timer associated with the widget and clears its callback function and data.

### _TimerCallback(oWidget)
Handles the timer callback by executing the stored callback function if it exists, then clears the callback data.

### _FinishGaugeAnimation(oUnused, oWidget, fSecondCallback, tData, bSkipAnimationInsert)
Finishes the gauge animation by setting the mood text to the current level name and calling a second callback if provided.

### StartPursuitGauge(oWidget, nTime, fCallback, tCallbackData)
Starts a pursuit gauge for the widget with a specified duration and callback function. It also sets up the pursuit gauge's custom data.

### _AnimateToEnd(oGauge, oWidget, nTime)
Animates the gauge to its end position based on the current value and length.

### StopPursuitGauge(oWidget)
Stops the pursuit gauge associated with the widget and resets its state.

### IsPursuitActive(oWidget)
Checks if the pursuit gauge is currently active for the widget.

### GetRemainingPursuitTime(oWidget)
Retrieves the remaining time of the pursuit gauge for the widget.

### _LoopToRed(oPursuit)
Animates the pursuit gauge to the red point and then loops back to the base point.

### _LoopToBase(oPursuit)
Animates the pursuit gauge to the base point and then loops back to the red point.

### _PursuitAnimationComplete(oWidget)
Handles the completion of the pursuit animation by stopping the pursuit gauge and executing the stored callback function if it exists.

### _SetVisible(oWidget, bVisible, bShowTimer, bShowPursuit)
Sets the visibility of various components of the widget based on the provided flags.

### _Min(nA, nB)
Returns the minimum of two numbers.

### _Max(nA, nB)
Returns the maximum of two numbers.

### _Clamp(n, nMin, nMax)
Clamps a number between a specified minimum and maximum value.

### _Abs(n)
Returns the absolute value of a number.

### _Animate(oUnused, oWidget, nPoint, nTime, bImmediate, fCallback, tCallbackData)
Animates the widget to a specified point with a given duration and callback function.

### _InitializeFactionTimer(oTimer)
Initializes the faction timer by setting its text, visibility, and custom data. It also sets up the timer's methods.

### SetFactionTimerCallback(oTimer, fCallback, tData)
Sets the callback function and data for the faction timer.

### StartFactionTimer(oTimer, nTime)
Starts the faction timer with a specified duration and sets up the update event handler.

### StopFactionTimer(oTimer)
Stops the faction timer and clears its update event handler.

### _UpdateTimer(oTimer, nTime)
Updates the faction timer's text based on the remaining time and executes the callback function if the timer expires.

### IsActive(oWidget)
Checks if the widget is currently active.

## Events

{: .warning }
> **This file contains zero `Event.*` engine calls** (grep-confirmed). The earlier draft listed `Event.ObjectHibernation`, `Event.TimerRelative`, and `Event.PlayerJoined/PlayerLeft` — **none exist in the source** and have been removed. Nothing here subscribes to or posts an engine event.

Timing and callbacks are handled without the engine `Event` system:
- **The gauge timer** (`StartTimer`/`StopTimer`) drives a native timer *object* stored at `oWidget.CustomData.oTimer` — `oTimer:Start(nTime)`, `oTimer:Stop()`, `oTimer:SetCallback(...)`. When it fires, `_TimerCallback` runs the stored Lua callback.
- **The faction "countdown" timer** (`_InitializeFactionTimer` / `StartFactionTimer` / `_UpdateTimer`) uses a per-frame widget handler: `oTimer:SetEventHandler("GuiUpdate", _UpdateTimer)` (a widget `EventHandlers` key, not `Event.*`), counting down `nTime` and formatting `MM:SS:CS` text.
- **Bar/color transitions** are `AnimateToPoint` tweens with Lua callback chains (`_TransitionToLevel`, `_FinishGaugeAnimation`, `_Animate`), not events.
- **The pursuit ring** uses `oPursuit:SetClockAnimation(...)` + `oPursuit:SetClockAnimationCallback(_PursuitAnimationComplete, ...)`.

## Notes for modders

- **Re-skin the reputation bands**: change `_tLevels` (thresholds), `_tLevelNames` (label hashes), and `_tLevelColors` (per-band RGB) in `Init()`, or call `SetLevels(...)` at runtime. Thresholds must start at `0`, be ascending, and match the name count, or `SetLevels` logs a `"Faction display level setup error: ..."` line and returns `false` without applying anything.
- **`SetLevels` does NOT update `_tLevelColors`** — it only rewrites `_tLevels`, `_tLevelNames`, and (optionally) `_ksPursuit`. If you change the number of bands via `SetLevels`, the color array from `Init()` can end up mismatched. Edit `Init()` for a consistent re-skin.
- **`bDisplayResult` on `SetLevels`** prints each band range and name via `Debug.Printf` (`"[min, max) = name"`) — handy when watching the log to confirm your thresholds parsed.
- **`GetBarValueAndName` computes but discards `nBarValue`**: it returns `nValue` (raw) and the level name, not the normalized bar value — a likely decompiler-visible quirk; don't rely on the first return being clamped/normalized.
- **Interaction with the buffer**: this module renders one gauge; slot placement, lifetime, and the two-at-a-time limit are handled by [MrxGuiHudFactionBuffer](mrxguihudfactionbuffer), which calls these methods (`SetValue`, `StartTimer`, `StartPursuit`, `SetIcon`) on each duplicated gauge.

{: .note }
> **`Initialize` references two undefined functions.** Lines 182-183 set `oWidget._RiseToValue = _RiseToValue` and `oWidget._CancelRise = _CancelRise`, but neither `_RiseToValue` nor `_CancelRise` is defined anywhere in this file — both evaluate to `nil`, so those two methods are effectively unset. Likely leftover from a refactor; nothing in this file calls them.