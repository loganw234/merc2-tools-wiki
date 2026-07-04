---
title: MrxGuiHudFactionGauge
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, faction]
verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- has an Init() setup function but no OnActivate/Create/tInstance anywhere in source)
---

# MrxGuiHudFactionGauge

*Module: mrxguihudfactiongauge.lua*

## Overview
The `MrxGuiHudFactionGauge` module is responsible for managing the graphical representation of faction gauges in the game's HUD. It handles the initialization, updating, and animation of these gauges based on various factors such as value changes, pursuit status, and timer events. This module ensures that the faction gauge accurately reflects the player's or NPC's faction standing and provides visual feedback through color changes and animations.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: only a one-time `Init()` setup function, no
`OnActivate`/`Create`/`tInstance` registry anywhere in source. This is one shared HUD gauge, not something
spawned per world object. Key fields:
- `_knMin`: Minimum value of the faction gauge (0).
- `_knMax`: Maximum value of the faction gauge (100).
- `_ksPursuit`: String key for the pursuit label ("[0x1cab5133]").
- `_tLevels`: Array to store the level thresholds.
- `_tLevelNames`: Array to store the names corresponding to each level.
- `_tLevelColors`: Array of tables, each containing RGB values for the color of each level.

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

- **Event.ObjectHibernation**: Listens for this event to activate or deactivate the widget instance.
- **Event.TimerRelative**: Used by `StartTimer` and `_AnimateToEnd` to handle timed animations and callbacks.
- **Event.PlayerJoined / Event.PlayerLeft**: May be used to adjust visibility or behavior based on player session changes.

## Notes for modders

1. **Call-order requirements**:
   - Ensure that `Init()` is called before using any other functions in the module, as it sets up essential data structures and validation.
   - `Initialize(oWidget)` must be called after creating a widget to set up its custom data and methods.

2. **Pitfalls**:
   - Modifying `_tLevels`, `_tLevelNames`, or `_tLevelColors` directly after initialization may lead to inconsistent behavior unless the module is re-initialized.
   - Incorrect input to `SetLevels` can result in validation errors and logged messages, so ensure that thresholds are in ascending order and start at 0.

3. **Tunables**:
   - Adjusting `_knMin` and `_knMax` can change the range of the faction gauge but may require corresponding changes in other related data structures.
   - Modifying `_tLevelThresholds`, `_tLevelNames`, and `_tLevelColors` allows customization of the gauge's appearance and behavior.

4. **Decompiler artifacts**:
   - Unused locals or redundant operator groupings are decompiler artifacts and should be ignored when interpreting the code logic.