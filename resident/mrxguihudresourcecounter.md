---
title: MrxGuiHudResourceCounter
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [gui, hud, resource]
---

# MrxGuiHudResourceCounter

*Module: mrxguihudresourcecounter.lua*

## Overview
The `MrxGuiHudResourceCounter` module is responsible for managing and displaying a resource counter on the HUD. It handles updating the counter's value, managing animations such as ticks and pulses, and displaying reasons for changes in the counter's value. This module is crucial for providing visual feedback to players about resource changes in real-time.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxPmc`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_nValue`: The current value of the counter.
- `_sAppendedString`: An optional string appended to the counter's display.
- `_bTicking`: A boolean indicating whether the counter is currently animating.
- `_nTickSpeed`: The speed at which the counter ticks.
- `_bSuppressed`: A boolean indicating whether the counter should be suppressed (not shown or updated).
- `_tReasonList`: A list of reasons and their associated amounts that contribute to the counter's value.
- `_knBufferSize`: The buffer size for displaying reasons, set to 4.
- `_tNumbers`: A table mapping numerical factors to their corresponding suffixes for formatting large numbers.

## Functions

### GetCounterValue(oSelf)
Returns the current value of the counter.

### SetCounterValue(oSelf, nNewValue, sReason, nIncrement)
Sets the new value for the counter, updates the display, and handles sound cues based on the change magnitude. If `nIncrement` is provided, it will be used instead of calculating the difference between the new and current values. Returns `true` if the value was updated, otherwise `false`.

### ModifyCounterValue(oSelf, nDeltaValue)
Modifies the counter's value by adding `nDeltaValue` to the current value.

### SetCounterAppendedString(oSelf, sAppendedString)
Sets an appended string to be displayed with the counter value. If `sAppendedString` is `nil`, it clears any existing appended string.

### SetCounterTickSpeed(oSelf, nSpeed)
Sets the tick speed for the counter's animation.

### IsTicking(oSelf)
Returns `true` if the counter is currently animating (ticking), otherwise `false`.

### _HandleCounterUpdateEvent(oSelf, nDeltaTime)
Handles the update event for the counter, updating the display value based on the delta value and checking if the animation should be halted or continued.

### _CounterInitialization(oSelf)
Initializes the counter with default values and sets up methods and animations for the widget.

### PulseRise(oCounter, nTime)
Starts a rising pulse animation for the counter.

### PulseFall(oCounter, nTime)
Starts a falling pulse animation for the counter.

### HaltPulse(oCounter, nTime)
Halts any ongoing pulse animation and resets to the base color.

### _PulseToBaseRise(oCounter, nTime)
Helper function for animating the counter to its rise state.

### _PulseToRiseRise(oCounter, nTime)
Helper function for completing the rise animation.

### _PulseToBaseFall(oCounter, nTime)
Helper function for animating the counter to its fall state.

### _PulseToFallFall(oCounter, nTime)
Helper function for completing the fall animation.

### _TopLevelInitialization(oSelf)
Initializes the top-level widget with default values and sets up methods and animations for the background elements and shake effect.

### _Show(oSelf, nTime)
Shows the counter widget, opening it with an animation if it is not already active.

### _FinishOpen(oBg, oSelf)
Finishes the open animation by setting the widget to fully visible and starting the update event handler.

### _Hide(oSelf)
Hides the counter widget, closing it with an animation if it is currently active.

### _FinishClose(oBg, oSelf)
Finishes the close animation by setting the widget to fully invisible.

### SetSuppressed(oSelf, bSuppress)
Sets whether the counter should be suppressed (not shown or updated).

### TopLevelSetValue(oSelf, nValue, sReason, nIncrement)
Sets the value for the top-level widget's counter and shows it if necessary.

### TopLevelSetAppendedString(oSelf, sString)
Sets the appended string for the top-level widget's counter.

### _TopLevelUpdate(oSelf, nDeltaTime)
Updates the top-level widget based on whether the counter is ticking and manages visibility timing.

### _HandleShowEvent(oSelf, tEvent)
Handles the show event by showing the widget with a specified duration.

### _HandleSetValueEvent(oSelf, tEvent)
Handles the set value event by updating the counter's value if the event's GUID matches the widget's owner or if no GUID is provided.

### _UpdateText(oWidget)
Updates the text displayed on the widget based on whether it should format money or display a raw number with an appended string.

### InitReasonList(oList)
Initializes a reason list for the counter, setting up default values and methods for adding reasons and hiding them.

### AddReason(oList, sReason, nAmount)
Adds a reason and its associated amount to the list. Updates the display of reasons and animates the list to show the new point.

- **Parameters:**
  - `oList`: The list object to which the reason is added.
  - `sReason`: The string representing the reason.
  - `nAmount`: The numerical amount associated with the reason.

### _Delay(oList)
Delays the animation of the list by moving it to a show point and then calls `_FadeReasons`.

- **Parameters:**
  - `oList`: The list object to animate.

### _FadeReasons(oList)
Fades out the reasons in the list by animating it to a hide point and then calls `_ClearReasons`.

- **Parameters:**
  - `oList`: The list object to animate.

### _ClearReasons(oList)
Clears the reasons from the list, sets the text to a space, and resets the reason display.

- **Parameters:**
  - `oList`: The list object to clear.

### _UpdateReasonDisplay(oList)
Updates the display of reasons in the list based on the current total and buffered reasons.

- **Parameters:**
  - `oList`: The list object whose display needs updating.

### _ConvertNumber(n)
Converts a number into a formatted string with appropriate suffixes for large numbers (e.g., billions, millions).

- **Parameters:**
  - `n`: The number to convert.

### Init()
Initializes the `_tNumbers` table with mappings of numerical factors to their corresponding suffixes for formatting large numbers.

## Events
(list engine events this module subscribes to/fires, and what triggers it)

- **Event.CounterUpdate**: Triggers when the counter's value is updated. This event is handled by `_HandleCounterUpdateEvent`.
- **Event.Show**: Triggers when the widget needs to be shown. This event is handled by `_HandleShowEvent`.
- **Event.SetValue**: Triggers when a new value needs to be set for the counter. This event is handled by `_HandleSetValueEvent`.

## Notes for modders
(call-order requirements, pitfalls, tunables, decompiler artifacts)

- **Call Order Requirements**:
  - Ensure that `Init()` is called before using any functions related to formatting numbers or managing reasons.
  - The `OnActivate` and `Awake` lifecycle functions should be used to set up the counter's initial state.

- **Pitfalls**:
  - Modifying the `_tNumbers` table directly can lead to unexpected behavior if the mappings are not correctly formatted.
  - Directly calling private methods (those prefixed with an underscore) may break encapsulation and lead to maintenance issues.

- **Tunables**:
  - `_kTickUpSound`, `_kTickDownSound`: These constants control the sound cues for when the counter value increases or decreases. Modifying these can change the auditory feedback.
  - `_kDefaultTickTime`, `_kTickLong`, `_kTickMedium`, `_kTickShort`, `_kPulseTime`, `_kWindowTime`: These constants control the timing of various animations and updates. Adjusting these values can affect the visual and auditory experience.

- **Decompiler Artifacts**:
  - The decompiler may produce unused local variables or redundant operator groupings, which should be ignored as they do not affect the functionality of the code.