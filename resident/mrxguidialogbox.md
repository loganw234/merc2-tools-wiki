---

title: MrxGuiDialogBox

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, dialog]

---



# MrxGuiDialogBox



*Module: mrxguidialogbox.lua*



## Overview

The `MrxGuiDialogBox` module is responsible for creating and managing graphical user interface (GUI) dialog boxes in the game. It provides functionality to display dialog boxes with messages, options, and interactive elements such as buttons and scrollable text. The module also handles input events, animations, and callback functions to manage user interactions.



## Inheritance

- Inherits from: `none` (base/utility module)

- Imports: `MrxGuiBase`



## Instance pattern

This is a stateless manager/utility module that does not follow the per-instance object pattern. It manages dialog boxes through global functions and maintains state through global variables such as `oSelectableList`. The module tracks the following key fields:

- `_ksFont`: Font used for text in dialog boxes.

- `_knScale`: Scale factor for dialog box elements.

- `_knTextR, _knTextG, _knTextB`: Default color of text.

- `_knTextLitR, _knTextLitG, _knTextLitB`: Color of highlighted text.

- `_ksAcceptSound`, `_ksCancelSound`, `_ksChangeSound`: Sound cues for user interactions.

- `oSelectableList`: A global table to manage selectable options in dialog boxes.



```



## Functions



### DisplayDialogBox(uPlayerGuid, sMessage, tOptions, nDefaultCursorIndex, fCallback, tCallbackArgs, nXOffset, nYOffset, sHorizAnchor, sVertAnchor, bPause, nCancelOption)

- **Description**: Displays a dialog box with the given message and options. Validates input parameters and constructs the dialog box using `_BuildDialogBox`.

- **Parameters**:

  - `uPlayerGuid`: Unique identifier for the player.

  - `sMessage`: The message to display in the dialog box.

  - `tOptions`: Table of option strings to display.

  - `nDefaultCursorIndex`: Default index for the cursor position.

  - `fCallback`: Callback function to be called when an option is selected.

  - `tCallbackArgs`: Arguments to pass to the callback function.

  - `nXOffset, nYOffset`: Offset for positioning the dialog box.

  - `sHorizAnchor, sVertAnchor`: Horizontal and vertical anchor points for positioning.

  - `bPause`: Boolean indicating whether to pause the game when the dialog is displayed.

  - `nCancelOption`: Index of the cancel option.



### Close(oBox)

- **Description**: Closes the given dialog box by releasing control focus, removing it from the widget hierarchy, and deleting it with its children.

- **Parameters**:

  - `oBox`: The dialog box instance to close.



### _BuildDialogBox(sMessage, tOptions, nDefaultCursorIndex, fCallback, tCallbackArgs, uPlayerGuid, nXOffset, nYOffset, sHorizAnchor, sVertAnchor, nCancelOption)

- **Description**: Constructs and returns a new dialog box widget with the specified message, options, and other parameters.

- **Parameters**:

  - `sMessage`: The message to display in the dialog box.

  - `tOptions`: Table of option strings to display.

  - `nDefaultCursorIndex`: Default index for the cursor position.

  - `fCallback`: Callback function to be called when an option is selected.

  - `tCallbackArgs`: Arguments to pass to the callback function.

  - `uPlayerGuid`: Unique identifier for the player.

  - `nXOffset, nYOffset`: Offset for positioning the dialog box.

  - `sHorizAnchor, sVertAnchor`: Horizontal and vertical anchor points for positioning.

  - `nCancelOption`: Index of the cancel option.



### Pulse(oWidget)

- **Description**: Starts a pulsing animation on the given widget to draw attention to it.

- **Parameters**:

  - `oWidget`: The widget instance to pulse.



### _LoopToHigh(oWidget)

- **Description**: Helper function for the pulsing animation, animates the widget's translucency level up.

- **Parameters**:

  - `oWidget`: The widget instance being animated.



### _LoopToLow(oWidget)

- **Description**: Helper function for the pulsing animation, animates the widget's translucency level down.

- **Parameters**:

  - `oWidget`: The widget instance being animated.



### HaltPulse(oWidget)

- **Description**: Stops the pulsing animation on the given widget.

- **Parameters**:

  - `oWidget`: The widget instance to stop pulsing.



### _ChangeSelection(oDialogBox, bUp)

- **Description**: Changes the selected option in the dialog box by moving the cursor up or down.

- **Parameters**:

  - `oDialogBox`: The dialog box instance.

  - `bUp`: Boolean indicating whether to move the cursor up (true) or down (false).



### _CompleteAnimation(oCursor, nY1, nY2, oCurrentOption)

- **Description**: Completes the animation of moving the cursor to a new option and updates the selected option's color.

- **Parameters**:

  - `oCursor`: The cursor widget instance.

  - `nY1, nY2`: Y coordinates for the animation.

  - `oCurrentOption`: The current selected option widget.



### _HandleInputEvent(oDialogBox, tEvent)

- **Description**: Handles input events for the dialog box, such as changing selection and confirming an option.

- **Parameters**:

  - `oDialogBox`: The dialog box instance.

  - `tEvent`: Event data containing information about the input event.



### _HandleDialogUpdate(oDialogBox, tEvent)

This function handles updates to the dialog box. It checks for widget highlights and updates the selected index accordingly. If the selected index changes, it updates the color of the previously selected option, sets the new selected option's color, and animates the cursor.



### _CloseAndCallCallback(oDialogBox, nSelectedIndex)

This function closes the dialog box and calls a callback function with the selected index as an argument. It releases control focus from the dialog box, retrieves the callback function and its arguments, and then deletes the dialog box.



### DisplayScrollingDialogBox(uPlayer, sText, fCallback, tCallbackData, bDisplayWager, sAcceptString, sDeclineString, sWagerString)

This function displays a scrolling dialog box for a given player. It constructs the dialog box with text, options (accept, decline, and optionally wager), and sets up event handlers for updates, mouse movement, and controller input. It also positions the dialog box on the screen.



### _BuildScrollingDialogBox(uPlayer, sText, bDisplayWager, fCallback, tCallbackData, sAcceptString, sDeclineString, sWagerString)

This function builds a scrolling dialog box for a given player. It creates text widgets, scrollable windows if needed, and option buttons (accept, decline, and optionally wager). It sets up the layout, colors, and event handlers for the dialog box.



### _BuildStrokes(oWidget, nX1, nY1, nX2, nY2)

This function builds strokes around a widget. It creates image widgets to form the borders of the given widget with specified coordinates and colors.



### _HandleScrollUpdate(oBox, nDeltaTime)

This function handles scrolling updates for the dialog box. If there is a scrollable window and the scroll value is significant, it offsets the text within the scrollable window based on the delta time.



### _HandleMouseUpdate(oBox, nDeltaTime)

This function handles mouse updates for the dialog box. It checks for widget highlights and updates the selected index accordingly. It also updates the highlight state of the up and down arrows in the scrollable window if applicable.



### _HandleScrollInput(oBox, tEvent)

This function handles scroll input for a GUI dialog box. It updates the scroll position based on joystick button presses and adjusts the selected option accordingly. If the down or up arrow is highlighted and pressed, it scrolls the text. If the accept button is pressed, it calls the callback with the selected option. If the cancel button is pressed, it cancels the selection.



### _CallScrollBoxCallback(fCallback, tData, n)

This function calls a callback function with provided data and an additional parameter `n`. It ensures that the callback is only called if it exists and inserts `n` into the data table before unpacking and passing it to the callback.



### CloseScrollingBox(oBox)

This function closes a scrolling box by releasing control focus, removing the widget with its children, and deleting the box itself.



### _SetScrollOption(oOptions, nOption)

This function sets the selected option in a scrollable options list. It updates the cursor's animation points and location based on the selected option's position.



### _CompleteScrollAnimation(oCursor, nX1, nX2)

This function completes the scrolling animation by setting the cursor's location to `nX1` and `nX2`, then animates it back to its open point.



### _CreateScrollableWindow(uPlayer, oTextWidget, nX, nY, nWidth, nHeight)

This function creates a scrollable window for displaying text. It sets up the text container, scrollbar, and arrow buttons, and initializes their positions and properties.



### _OffsetText(oScroll, nOffset)

This function offsets the text within the scrollable window by adjusting its location based on the provided offset value. It also updates the scrollbar position accordingly.



### _Clamp(n, lo, hi)

This function clamps a number `n` to be within the range defined by `lo` and `hi`.



### _UpdateTextAlpha(oTextContainer)

This function updates the translucency of text lines based on their proximity to the top and bottom edges of the visible area. It ensures that text near the edges fades out smoothly.



### _ValidateParameter(Parameter, sType, DefaultValue)

This function validates a parameter by checking if it matches the specified type `sType`. If it does not match, it returns the default value.



### OpenSystemDialogBox(sTitle, sMessage, sButton)

This function opens a system dialog box with a title, message, and button. It ensures that any existing widgets are closed before creating and displaying the new dialog box.



### SystemDialogBoxLoadedCallBack(oFlash, sTitle, sMessage, sButton)

This function is called when the system dialog box SWF file has loaded. It sets up the control focus, calls an action script callback to display the message, and sets up an event handler for closing the dialog box.



### CloseSystemDialogBox()

This function closes the system dialog box by creating a timer event that delays the actual closure to ensure proper cleanup.



### CloseSystemDialogBoxDelayed(oFlash)

This function handles the delayed closure of the system dialog box. It releases control focus, removes the widget, and deletes it.



## Events

- **`Event.InputReceived`**: Listens for input events (e.g., button presses) to handle selection changes and confirmations in dialog boxes.

- **`Event.TimerRelative`**: Used for timing animations like pulsing effects or scrolling updates.

- **`Event.WidgetHighlighted`**: Tracks widget highlights to update the selected index and color of options in dialog boxes.

- **`Event.SwfLoaded`**: Triggered when a system dialog box SWF file has loaded, setting up control focus and event handlers.



## Notes for modders

- **Call-order requirements**: Ensure that `DisplayDialogBox` or `DisplayScrollingDialogBox` is called before any other functions to properly initialize the dialog box.

- **Pitfalls**: Be cautious with callback functions; ensure they are defined and can handle the expected arguments. Avoid using global variables within callbacks as they may lead to unexpected behavior.

- **Tunables**: The constants `_ksFont`, `_knScale`, text colors, and sound cues can be modified to customize the appearance and behavior of dialog boxes.

- **Decompiler artifacts**: Some local variables in functions like `_HandleInputEvent` and `_HandleScrollUpdate` appear unused or are assigned but never read. These are decompiler artifacts and should not affect functionality.