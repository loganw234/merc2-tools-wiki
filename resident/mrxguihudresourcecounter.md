---
title: MrxGuiHudResourceCounter
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud, resource]
verified: true
verified_note: 'deeper pass: DELETED fabricated Events section (zero Event.* calls — no CounterUpdate/Show/SetValue) and fabricated Instance-pattern fields (_nValue/_sAppendedString/_bTicking/etc. do not exist; state is in CustomData); surfaced real constants (money magnitude thresholds 1M/100K, cash sounds, tick times, pulse colors, _tNumbers suffix hashes, _knBufferSize=4) and the Money/Fuel Counter branching; pruned OnActivate/Awake boilerplate'
---

# MrxGuiHudResourceCounter

*Module: mrxguihudresourcecounter.lua*

## Overview
The `MrxGuiHudResourceCounter` module is responsible for managing and displaying a resource counter on the HUD. It handles updating the counter's value, managing animations such as ticks and pulses, and displaying reasons for changes in the counter's value. This module is crucial for providing visual feedback to players about resource changes in real-time.

## Inheritance
- Inherits from: none — base/utility module
- Imports (via [`import()`](../glossary#importname)): `MrxGui`, `MrxPmc` — see [MrxGui](mrxgui) and [MrxPmc](mrxpmc). `MrxPmc.GetFuelCapacity()` supplies the low-fuel threshold; the money-formatting suffixes are localized-string hashes.

## Instance pattern
**Stateless module + per-widget `CustomData`.** All mutable state lives on the counter widgets in `oWidget.CustomData` (`nCurrentValue`, `nDisplayValue`, `nDeltaValue`, `nTickSpeed`, `bActive`, `bSuppressed`, `nMagnitude`, `sAppend`, `oReasonList`, `bFormatMoney`, `bPersistWhenLow`/`bPersist`). The init functions (`_CounterInitialization`, `_TopLevelInitialization`, `InitReasonList`) copy the module functions onto their widgets as methods (`oSelf.SetValue = SetCounterValue`, `oSelf.Show = _Show`, etc.).

{: .note }
> The earlier draft listed module-level fields `_nValue`, `_sAppendedString`, `_bTicking`, `_nTickSpeed`, `_bSuppressed`, `_tReasonList`. **None of these exist in the source** — the corresponding state is per-widget `CustomData`. Removed.

The only real module-level names are the constants below plus `_knBufferSize = 4` (max reasons shown in a reason list) and `_tNumbers` (large-number suffix map, built by `Init()`).

### Module constants (the tunables)
- **Sounds** (looping tick cues): `_kTickUpSound = "ui_HUD_Money_Gain"`, `_kTickDownSound = "ui_HUD_Money_Lose"`. Magnitude-based one-shots in `SetCounterValue`: `UI_hud_cashUp_large`/`_med`/`_small` and `UI_hud_cashDown_large`/`_med`/`_small`.
- **Magnitude thresholds** (pick the sound/tick speed): change `> 1000000` (large), `> 100000` (medium), else small — mirrored for negatives at `< -1000000` / `< -100000`.
- **Tick/animation times**: `_kDefaultTickTime = 0.5`, `_kTickLong = 2.05`, `_kTickMedium = 1.25`, `_kTickShort = 0.5`, `_kPulseTime = 0.2`, `_kWindowTime = 0.1` (open/close shutter time).
- **Pulse colors** (`_CounterInitialization`): base = widget's authored color; fall/loss = RGB `(255, 64, 64)`; rise/gain = RGB `(255, 255, 255)`.
- **Number formatting** (`_ConvertNumber`): emits `"[SHELL.Common.Money:whole:tenths:suffix]"`; `_tNumbers` maps `1e3/1e6/1e9/1e12/1e15` to localized suffix hashes (`[0xe00c096a]` for thousands, etc.); values are clamped to `≤ 1e15` and `≥ 0`.

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

{: .warning }
> **This file has zero `Event.*` engine calls** (grep-confirmed). The earlier draft listed `Event.CounterUpdate`, `Event.Show`, `Event.SetValue` — **none exist** and have been removed. (`tEvent.nTime`/`tEvent.uGuid`/`tEvent.nValue` are just fields of the payload passed to widget handlers, not engine events.)

Animation and value ticking are driven by widget-level handlers via `SetEventHandler("GuiUpdate", ...)`:
- `_HandleCounterUpdateEvent` — set while a value change is animating; interpolates `nDisplayValue` toward `nCurrentValue` each frame, then halts/persists the pulse when done.
- `_TopLevelUpdate` — runs the shake effect while ticking and the auto-hide `nVisibleTime` countdown.
- `_HandleShowEvent(oSelf, tEvent)` / `_HandleSetValueEvent(oSelf, tEvent)` are handler callbacks (wired in a layout), reading `tEvent.nTime` / `tEvent.uGuid`+`tEvent.nValue`. `_HandleSetValueEvent` only applies if `tEvent.uGuid` matches the widget owner or is `nil` (broadcast).

## Notes for modders

- **`Init()` must run before any money formatting**: it builds `_tNumbers`. Until then `_ConvertNumber` iterates an unset table (`_tNumbers = false`) and errors — this is the module's one hard init requirement.
- **Two counter instances** are recognized by widget name in `_CounterInitialization`: `"Money Counter"` (sets `bFormatMoney = true`, so it renders via the `[SHELL.Common.Money:...]` template) and `"Fuel Counter"` (sets `bPersistWhenLow = true` and gives its reason list `nBufferSize = 0`, i.e. no reason lines). Renaming these widgets changes which behavior they get.
- **Low-fuel persistence**: when `bPersistWhenLow`, the counter stays on screen while its value is at/below `MrxPmc.GetFuelCapacity() * 0.1` (10% of capacity, default `300` → `30`). Gains above that threshold clear the persist flag. Change the `0.1` to re-tune the "low fuel stays visible" band.
- **Reason list**: each `SetValue` with a `sReason` string adds a line to a floating reason list (`AddReason`); with no reason it falls back to `[Generic.MoneyReasons.Credit]` / `[Generic.MoneyReasons.Debit]`. The list shows a running total colored `[green]`/`[red]`/`[white]`, holds `2`s, fades `0.5`s. `_knBufferSize = 4` caps how many individual lines display (only the most recent 4).
- **Suppression**: `SetSuppressed(oSelf, true)` snaps the counter to its value without animation/sound and hides it — use it to silently sync a value (e.g. on load) without the tick/shake/cash sounds.
- **Shake effect**: `_TopLevelUpdate` cycles through 4 hard-coded jitter offsets (`tShakePoints[1..4]`, ±1-2px) while ticking. Purely cosmetic.

{: .note }
> Do not call the underscore-prefixed helpers directly; the public levers are the methods copied onto the widget (`SetValue`, `ModifyValue`, `SetAppendedString`, `SetTickSpeed`, `Show`, `Hide`, `SetSuppressed`, `IsTicking`).