---
title: MrxGuiNumericBox
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, numeric input]
---

# MrxGuiNumericBox

*Module: mrxguinumericbox.lua*

## Overview
The `MrxGuiNumericBox` module is responsible for creating and managing a numeric input box GUI widget. This widget allows players to enter numeric values through the game's user interface, with customizable messages, prefixes, suffixes, and callback functions for handling accept and cancel actions.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but provides functions to create and manage numeric input boxes for players. The module uses constants to define default styles, colors, and sound cues for the numeric box widget. Key fields include:

- `_ksFontSmall`: Font style for small text.
- `_ksFont`: Font style for regular text.
- `_knScale` and `_knScaleBig`: Scaling factors for text size.
- `_knTextR`, `_knTextG`, `_knTextB`: Default text color (156, 154, 133).
- `_knTextLitR`, `_knTextLitG`, `_knTextLitB`: Lit text color (210, 210, 190).
- `_ksAcceptSound`, `_ksCancelSound`, `_ksChangeSound`: Sound cues for accept, cancel, and change actions.

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
  - `bPause`: Boolean indicating whether to pause the game while the numeric box is open.

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

### `_ValidateParameter(Parameter, sType, DefaultValue)`
- **Description**: Validates that the given parameter is of the specified type; if not, returns a default value.
- **Parameters**:
  - `Parameter`: The value to validate.
  - `sType`: The expected type as a string (e.g., "number", "string").
  - `DefaultValue`: The value to return if validation fails.
- **Returns**: The validated parameter or the default value.

## Events

This module subscribes to and fires several engine events:

- **Subscribes to**:
  - `Event.Input`: Handles input events for interacting with the numeric box (e.g., button presses).
  - `Event.TimerRelative`: Used for timing animations and updates within the numeric box.
  
- **Fires**:
  - No specific events are fired by this module.

## Notes for modders

1. **Call-order requirements**: Ensure that `DisplayNumericBox` is called before attempting to interact with or close the numeric box. The order of parameters in `DisplayNumericBox` must be strictly followed to ensure proper functionality.
  
2. **Pitfalls**:
   - Be cautious with the callback functions (`fAcceptCallback`, `fCancelCallback`). Ensure they are defined and can handle the arguments passed correctly.
   - Validate all input parameters using `_ValidateParameter` to avoid unexpected behavior or errors.

3. **Tunables**: The module uses several constants for styling and sound effects (e.g., font sizes, colors, sound cues). Modifying these constants will change the appearance and behavior of the numeric box.

4. **Decompiler artifacts**:
   - There are no known decompiler artifacts in this module that require special attention. All variables and functions appear to be used as intended by the code.