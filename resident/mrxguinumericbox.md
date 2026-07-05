---
title: MrxGuiNumericBox
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, numeric input]
verified: true
verified_note: 'deeper pass: re-confirmed all functions/constants/bugs against source; added a THIRD confirmed bug (cancel branches insert _ComputeValue into tAcceptCallbackArgs but unpack tCancelCallbackArgs), noted DisplayNumericBox calls LTILibName.ChangeShellState(true) and _SetValue zero-pads to nMaximumDigit+1; kept the uPlayerGuid/bImmediate/_CompleteAnimation findings'
---

# MrxGuiNumericBox

*Module: mrxguinumericbox.lua*

## Overview
The `MrxGuiNumericBox` module is responsible for creating and managing a numeric input box GUI widget. This widget allows players to enter numeric values through the game's user interface, with customizable messages, prefixes, suffixes, and callback functions for handling accept and cancel actions.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`

## Instance pattern
Stateless singleton/utility module — plain module-level constants, no `Create`/`OnActivate`/`Awake`/`tInstance`. Each call to `DisplayNumericBox` builds one widget tree (via `_BuildNumericBox`) whose per-box state lives entirely on the returned widget's own `CustomData` table (`oSelectableList`, `nSelectedIndex`, `nHighlightedIdx`, `oCursor`, `oDigits`, `nMinimumDigit`/`nMaximumDigit`/`nMinimumValue`/`nMaximumValue`, `fAcceptCallback`/`tAcceptCallbackArgs`, `fCancelCallback`/`tCancelCallbackArgs`) — the widget itself is the "instance," this module doesn't track a registry of open boxes. Module-level constants:

- `_ksFontSmall` (`"english_18"`) / `_ksFont` (`"english_20"`): fonts for small vs. regular text.
- `_knScale` / `_knScaleBig`: both `1` — scaling factors for text size (small vs. regular).
- `_knTextR`, `_knTextG`, `_knTextB`: default (dim) text color (156, 154, 133).
- `_knTextLitR`, `_knTextLitG`, `_knTextLitB`: lit/highlighted text color (210, 210, 190).
- `_ksAcceptSound` (`"ui_PDA_Accept"`), `_ksCancelSound` (`"ui_PDA_Cancel"`), `_ksChangeSound` (`"ui_PDA_Scroll"`): sound cues played on accept/cancel/digit-change.
- `_knCursorHeight` (`70`): height of the selection cursor widget.
- `_knPulseTime` (`0.5`): duration of one half-cycle of the pulsing background animation (see `Pulse`/`_LoopToHigh`/`_LoopToLow`).
- `oldIdx`: initialized to `-1`, never read or written anywhere else in this file — appears unused/vestigial.

## Functions

### DisplayNumericBox(uPlayerGuid, sMessage, sPostFixMessage, sPrefix, sSuffix, nDefaultValue, nMinimumValue, nMaximumValue, nDefaultDigit, nMinimumDigit, nMaximumDigit, fAcceptCallback, tAcceptCallbackArgs, fCancelCallback, tCancelCallbackArgs, nXOffset, nYOffset, sHorizAnchor, sVertAnchor, bPause)

This function displays a numeric input box for the specified player. It validates various parameters and sets up the numeric box with the provided settings.

- **Parameters**:
  - `uPlayerGuid`: The GUID of the player to display the numeric box for.
  - `sMessage`: The main message to display in the numeric box.
  - `sPostFixMessage`: A postfix message to display after the input field.
  - `sPrefix`, `sSuffix`: Prefix and suffix text for the numeric value.
  - `nDefaultValue`, `nMinimumValue`, `nMaximumValue`: Default, minimum, and maximum values for the numeric input.
  - `nDefaultDigit`, `nMinimumDigit`, `nMaximumDigit`: Default, minimum, and maximum digits for the numeric input.
  - `fAcceptCallback`, `tAcceptCallbackArgs`: Callback function and arguments to call when the user accepts the input.
  - `fCancelCallback`, `tCancelCallbackArgs`: Callback function and arguments to call when the user cancels the input.
  - `nXOffset`, `nYOffset`: Offset for positioning the numeric box on the screen.
  - `sHorizAnchor`, `sVertAnchor`: Horizontal and vertical anchor points for positioning.
  - `bPause`: Boolean indicating whether to pause the game while the numeric box is open. Defaults to `true` when `nil`.

- **Side effect**: before building the box, it calls `LTILibName.ChangeShellState(true)` (enters the shell/menu UI state). There is no matching `ChangeShellState(false)` in `Close` — teardown just releases focus and deletes widgets — so the shell-state flip is not undone by this module.
- **Returns**: The created numeric box object.

### Close(oBox)

This function closes the specified numeric box, releasing control focus and removing it from the GUI.

- **Parameters**:
  - `oBox`: The numeric box object to close.

### _BuildNumericBox(sMessage, sPostFixMessage, sPrefix, sSuffix, nDefaultValue, nMinimumValue, nMaximumValue, nDefaultDigit, nMinimumDigit, nMaximumDigit, fAcceptCallback, tAcceptCallbackArgs, fCancelCallback, tCancelCallbackArgs, nXOffset, nYOffset, sHorizAnchor, sVertAnchor)
This function constructs a numeric input box GUI widget. It takes various parameters to customize the appearance and behavior of the numeric box, such as messages, prefixes, suffixes, default values, digit ranges, and callback functions for accepting or canceling the input.

- **Parameters:**
  - `sMessage`: The main message displayed at the top of the numeric box.
  - `sPostFixMessage`: An optional postfix message that can be displayed below the numeric digits.
  - `sPrefix`: A prefix text that appears before the numeric digits.
  - `sSuffix`: A suffix text that appears after the numeric digits.
  - `nDefaultValue`: The default value for the numeric input.
  - `nMinimumValue` and `nMaximumValue`: The minimum and maximum values allowed for the numeric input.
  - `nDefaultDigit`, `nMinimumDigit`, and `nMaximumDigit`: Parameters related to the number of digits in the numeric box.
  - `fAcceptCallback` and `tAcceptCallbackArgs`: A callback function and its arguments that are called when the user accepts the input.
  - `fCancelCallback` and `tCancelCallbackArgs`: A callback function and its arguments that are called when the user cancels the input.
  - `nXOffset`, `nYOffset`, `sHorizAnchor`, and `sVertAnchor`: Parameters for positioning the numeric box on the screen.

- **Returns:**
  - The constructed numeric box widget (`oNumericBox`).

The function initializes various GUI widgets such as text, images, and buttons to create a user-friendly interface for entering numeric values. It also sets up event handling for interactions like moving the cursor, incrementing/decrementing digits, and accepting/canceling the input.

**Confirmed bug**: `_BuildNumericBox`'s parameter list does not include `uPlayerGuid`, yet its body references `uPlayerGuid` 16 times (`oNumericBox:SetOwner(uPlayerGuid)` and the same call on every text/image child it constructs — message text, prefix, each digit, digit background, cursor, cursor background, up/down callouts, suffix text, postfix message, callouts text, and the accept/cancel option text/boxes). Since `_BuildNumericBox` is a separate top-level function (not a closure nested inside `DisplayNumericBox`), it cannot see `DisplayNumericBox`'s local `uPlayerGuid` parameter — Lua locals don't cross function boundaries that way. Every `uPlayerGuid` reference inside `_BuildNumericBox` is therefore reading an **undeclared global**, which is `nil` unless something else in the loaded environment happens to set a global of that exact name. Net effect: every widget `_BuildNumericBox` creates gets `SetOwner(nil)`. `DisplayNumericBox` does correctly call `oBox:SetOwner(uPlayerGuid)` on the *returned* box afterward (line 38, using its own real local), which fixes the top-level `oNumericBox`'s owner — but none of its ~15 child widgets get a corrective `SetOwner` call anywhere, so they likely retain an incorrect/nil owner unless the engine's widget-ownership model inherits owner from parent automatically (not confirmable from static reading of this file alone).

### `_BuildStrokes(oWidget, nX1, nY1, nX2, nY2)`
- **Description**: Constructs and adds four stroke widgets to the given `oWidget` to create a rectangular border.
- **Parameters**:
  - `oWidget`: The widget to which strokes will be added.
  - `nX1`, `nY1`, `nX2`, `nY2`: Coordinates defining the rectangle's corners.

### `_ComputeValue(oNumericBox)`
- **Description**: Computes the total value represented by the digits in the numeric box.
- **Parameters**:
  - `oNumericBox`: The numeric box widget instance.
- **Returns**: The computed total value as a number.

### `_SetValue(oNumericBox, nTotalValue)`
- **Description**: Updates the text of each digit in the numeric box to reflect the given total value.
- **Parameters**:
  - `oNumericBox`: The numeric box widget instance.
  - `nTotalValue`: The new value to set.

### `_ModifySelection(oNumericBox, nIncrement)`
- **Description**: Modifies the selected digit's value by a specified increment and updates the displayed value accordingly.
- **Parameters**:
  - `oNumericBox`: The numeric box widget instance.
  - `nIncrement`: The amount to increment or decrement the selected digit.

### `_ChangeSelection(oNumericBox, nIncrement)`
- **Description**: Changes the currently selected digit in the numeric box by a specified increment and updates the cursor position.
- **Parameters**:
  - `oNumericBox`: The numeric box widget instance.
  - `nIncrement`: The amount to move the selection.

### `_CompleteAnimation(oCursor, nX1, nY1, nX2, nY2, oCurrentDigit)`
- **Description**: Completes an animation for the cursor and updates the color of the current digit.
- **Parameters**:
  - `oCursor`: The cursor widget instance.
  - `nX1`, `nY1`, `nX2`, `nY2`: Coordinates defining the destination location for the cursor.
  - `oCurrentDigit`: The currently selected digit.
- **Note**: no call sites for this function found anywhere in this file — appears to be dead code within `mrxguinumericbox.lua`. A different function of the same name (different signature: `(oCursor, nY1, nY2, oCurrentOption)`) exists in `mrxguidialogbox.lua` and is called from there — that's a separate, unrelated definition, not this one.

### `_HandleScrollUpdate(oBox, nDeltaTime)`
- **Description**: Handles scroll updates by highlighting or unselecting items in the numeric box based on user interaction.
- **Parameters**:
  - `oBox`: The numeric box widget instance.
  - `nDeltaTime`: Time elapsed since last update.

### `_UnselectAll(oBox)`
- **Description**: Unselects all items in the numeric box by resetting their colors.
- **Parameters**:
  - `oBox`: The numeric box widget instance.

### `_HandleInputEvent(oNumericBox, tEvent)`
- **Description**: Handles input events (e.g., button presses) to modify or change selection in the numeric box and perform accept/cancel actions.
- **Parameters**:
  - `oNumericBox`: The numeric box widget instance.
  - `tEvent`: The input event data.

### `Pulse(oWidget)`
- **Description**: Initiates a pulsing animation for the given widget, changing its translucency over time.
- **Parameters**:
  - `oWidget`: The widget to animate.

### `_LoopToHigh(oWidget)`
- **Description**: Continues the pulsing animation by animating the widget's translucency to a higher value.
- **Parameters**:
  - `oWidget`: The widget being animated.

### `_LoopToLow(oWidget)`
- **Description**: Continues the pulsing animation by animating the widget's translucency to a lower value.
- **Parameters**:
  - `oWidget`: The widget being animated.

### `HaltPulse(oWidget)`
- **Description**: Stops the pulsing animation for the given widget and sets its translucency to a high value.
- **Parameters**:
  - `oWidget`: The widget to stop animating.
- **Confirmed bug**: sets `oWidget.CustomData.bRising = false`, then checks `if bImmediate then ... else ... end`. `bImmediate` is not a parameter of `HaltPulse` (its only parameter is `oWidget`) and is never assigned anywhere in this file — it's an undeclared global, always `nil`/falsy. The `if bImmediate then` branch (which would animate proportionally to current alpha) is therefore permanently dead code; `HaltPulse` always takes the `else` branch (`oWidget:AnimateToPoint(oWidget.CustomData.nPulseHighPoint, 0, true)` — an instant snap to full brightness with no easing), regardless of what the caller might have intended.

### `_ValidateParameter(Parameter, sType, DefaultValue)`
- **Description**: Validates that the given parameter is of the specified type; if not, returns a default value.
- **Parameters**:
  - `Parameter`: The value to validate.
  - `sType`: The expected type as a string (e.g., "number", "string").
  - `DefaultValue`: The value to return if validation fails.
- **Returns**: The validated parameter or the default value.

## Events
No `Event.*` calls appear anywhere in this file. Input/interaction handling uses the widget-level `SetEventHandler` API instead, registered once in `_BuildNumericBox`:
- `oNumericBox:SetEventHandler("OnMouseMove", _HandleScrollUpdate)` — highlights/unselects selectable items as the mouse/highlight cursor moves over them.
- `oNumericBox:SetEventHandler("ControllerInput", _HandleInputEvent)` — handles D-pad/left-stick up/down (modify digit value), left/right (change selected digit), and two buttons (`BUTTON_PAD2_D`/`BUTTON_PAD2_R`) for accept/cancel.

This is a different mechanism from the engine `Event.*` system and from the `EventHandlers`/`EventHandlerNames`-table pattern used in layout files (e.g. `mrxguishelllayout.md`) — here the handler is wired imperatively at widget-construction time via a method call on the widget instance itself, not declared in a static table.

## Notes for modders

1. **Call-order requirements**: Ensure that `DisplayNumericBox` is called before attempting to interact with or close the numeric box. The order of parameters in `DisplayNumericBox` must be strictly followed to ensure proper functionality.

2. **Pitfalls**:
   - Be cautious with the callback functions (`fAcceptCallback`, `fCancelCallback`). The accept branch appends the computed value to `tAcceptCallbackArgs` and calls `fAcceptCallback(unpack(tAcceptCallbackArgs))` — correct. **Confirmed bug in both cancel paths**: they append the computed value to `tAcceptCallbackArgs` (the *accept* args) but then call `fCancelCallback(unpack(tCancelCallbackArgs))` — so the numeric value is inserted into the wrong table and the cancel callback receives its `tCancelCallbackArgs` *without* the appended value. If you rely on a numeric value reaching `fCancelCallback`, it won't be there; and `tAcceptCallbackArgs` accumulates a stray value.
   - `_SetValue` zero-pads with `string.format("%0" .. (nMaximumDigit + 1) .. "d", ...)`, so the box always shows `nMaximumDigit + 1` digit slots (default max digit `9` → 10 slots). Set `nMaximumDigit` to control the field width, not just the value range.
   - Validate all input parameters using `_ValidateParameter` to avoid unexpected behavior or errors.
   - See the confirmed bugs noted under `_BuildNumericBox` (undeclared global `uPlayerGuid`, affecting widget ownership) and `HaltPulse` (undeclared global `bImmediate`, making one of its two branches permanently unreachable) in the Functions section above.

3. **Tunables**: The module uses several constants for styling and sound effects (e.g., font sizes, colors, sound cues). Modifying these constants will change the appearance and behavior of the numeric box.

4. **Decompiler artifacts / dead code**: `_CompleteAnimation` is defined but has no call sites anywhere in this file. `oldIdx` (module-level, initialized to `-1`) is never read or written anywhere else in this file. Both appear to be unused leftovers rather than load-bearing state.