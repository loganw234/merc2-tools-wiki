---

title: MrxGuiTextBuffer

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, text buffer]

---



# MrxGuiTextBuffer



*Module: mrxguitextbuffer.lua*



## Overview

The `MrxGuiTextBuffer` module is responsible for managing text buffers in the game's GUI system. It provides functionality to create, update, and manage text messages within these buffers, including handling scrolling, message lifecycles, and visual properties.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxGuiManager`



## Instance pattern

This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:

- **tMessages**: A table storing all messages in the buffer.

- **nCurrentMessageIndex**: The index of the currently visible message.

- **bFlowDown**: Indicates whether text flows downwards.

- **bHasBackdrop**: Indicates whether the text buffer has a backdrop.

- **kScrollSpeed**: The scrolling speed for the text buffer.

- **tCustomData**: Custom data fields used for managing widget properties and states.

```



## Functions



### HandleInstantiationEventForTextBuffer(oWidget, tEvent)

This function handles the instantiation event for a text buffer widget. It sets up various properties and methods on the widget, including:

- Text font and scale.

- Scroll direction (`bFlowDown`).

- Backdrop visibility (`bHasBackdrop`).

- Border size and location adjustments.

- Message storage and management functions.



### InstantiateTextBuffer(nX, nY, nWidth, nHeight, bFlowDown, bHasBackdrop)

This function creates a new text buffer widget. It validates input parameters, initializes the widget with specified properties, sets up custom data fields, and adds event handlers for updates. It also adds methods for message management.



### SetLocation(oTextBuffer, nX1, nY1, nX2, nY2)

This function updates the location of a text buffer widget. It adjusts the widget's position and recalculates border-related custom data fields.



### AddMessage(oTextBuffer, sMessage, nPriority, nDisplayDuration, nFadeDuration, bClearBuffer, bAllowsAppends, fCallback, tCallbackData)

This function adds a new message to a text buffer. It validates input parameters, creates a new text widget for the message, sets its properties, and manages its display duration and callback functionality.



### CallCallback(oMessage)

This function calls a callback associated with a message if it exists. It unpacks the callback data and executes the callback function.



### AdvanceMessages(oTextBuffer)

This function advances messages in the text buffer by setting the display duration of the first current message to 0, effectively removing it from view.



### GetCurrentMessageId(oTextBuffer)

This function returns the IDs of currently visible messages in the text buffer.



### ClearMessages(oTextBuffer)

This function clears all messages and pending messages from the text buffer. It removes widgets from the HUD, deletes them, and resets message storage and indices.



### ClearVisibleMessages(oTextBuffer, bAdvance)

This function clears only the visible messages from the text buffer. If `bAdvance` is true, it advances any remaining pending messages into the buffer. It also sets the text buffer to be invisible if no messages remain.



### ModifyPendingMessage(oTextBuffer, nMessageId, sMessage, nDisplayDuration, nFadeDuration, bClearBuffer, bAllowsAppends, fCallback, tCallbackData)

Modifies an existing pending message in the text buffer. Updates the message's text, display duration, fade duration, clear buffer flag, allows appends flag, callback function, and callback data. If the message is found and modified successfully, returns `true`; otherwise, returns `false`.



### RemovePendingMessage(oTextBuffer, nMessageId)

Removes a pending message from the text buffer by its ID. If the message is found and removed successfully, returns `true`; otherwise, returns `false`.



### HandleTextBufferUpdateEvent(oTextBuffer, nTimeSinceLastUpdate)

Handles updates to the text buffer based on time elapsed since the last update. Manages the fading in and out of messages, advancing messages through the buffer, and removing expired messages.



### PushMessageIntoTextBuffer(oTextBuffer)

Attempts to push a pending message into the current messages buffer. If successful, it adjusts the layout and visibility of messages accordingly and returns `true`; otherwise, returns `false`.



### GetMessageHeight(oTextWidget)

Retrieves the height of a text widget.



### WrapText(oTextWidget)

Wraps the text in a text widget to fit within its bounds.



### IsEmpty(tTarget)

Checks if a table is empty. Returns `true` if the table is empty, otherwise returns `false`.



### MboxAbs(nNumber)

Returns the absolute value of a number.



### ValidateParameter(Parameter, sType, DefaultValue)

Validates a parameter against a specified type. If the parameter matches the type, it returns the parameter; otherwise, it returns a default value.



### HandleE3HudModeEvent(oWidget, tEvent)

This function handles the E3 HUD mode event for a given widget. If `tEvent.bOn` is true, it sets the `bE3HudMode` flag to true on the widget's custom data and hides all child widgets of the first child. If `tEvent.bOn` is false and the widget was previously in E3 HUD mode, it resets the `bE3HudMode` flag to false, shows all child widgets of the first child, and makes them visible.



### HandleAddMessageEvent(oWidget, tEvent)

This function handles adding a message event to a given widget. If `tEvent.sMessage` is provided, it adds the message to the widget with an optional duration specified by `tEvent.nDuration`.



### DrawDebugRectangle(TargetWidget)

This function draws a debug rectangle on the target widget. It creates a command table with properties such as position, size, color, and texture, and assigns this command to the second drawing command slot of the target widget.



## Events

- **HandleInstantiationEventForTextBuffer(oWidget, tEvent)**: This function handles the instantiation event for a text buffer widget. It sets up various properties and methods on the widget.

- **InstantiateTextBuffer(nX, nY, nWidth, nHeight, bFlowDown, bHasBackdrop)**: This function creates a new text buffer widget with specified properties.

- **SetLocation(oTextBuffer, nX1, nY1, nX2, nY2)**: This function updates the location of a text buffer widget and recalculates border-related custom data fields.

- **AddMessage(oTextBuffer, sMessage, nPriority, nDisplayDuration, nFadeDuration, bClearBuffer, bAllowsAppends, fCallback, tCallbackData)**: This function adds a new message to a text buffer with specified properties and manages its display duration and callback functionality.

- **CallCallback(oMessage)**: This function calls a callback associated with a message if it exists.

- **AdvanceMessages(oTextBuffer)**: This function advances messages in the text buffer by setting the display duration of the first current message to 0, effectively removing it from view.

- **GetCurrentMessageId(oTextBuffer)**: This function returns the IDs of currently visible messages in the text buffer.

- **ClearMessages(oTextBuffer)**: This function clears all messages and pending messages from the text buffer.

- **ClearVisibleMessages(oTextBuffer, bAdvance)**: This function clears only the visible messages from the text buffer. If `bAdvance` is true, it advances any remaining pending messages into the buffer.

- **ModifyPendingMessage(oTextBuffer, nMessageId, sMessage, nDisplayDuration, nFadeDuration, bClearBuffer, bAllowsAppends, fCallback, tCallbackData)**: This function modifies an existing pending message in the text buffer.

- **RemovePendingMessage(oTextBuffer, nMessageId)**: This function removes a pending message from the text buffer by its ID.

- **HandleTextBufferUpdateEvent(oTextBuffer, nTimeSinceLastUpdate)**: This function handles updates to the text buffer based on time elapsed since the last update.

- **PushMessageIntoTextBuffer(oTextBuffer)**: This function attempts to push a pending message into the current messages buffer.

- **GetMessageHeight(oTextWidget)**: This function retrieves the height of a text widget.

- **WrapText(oTextWidget)**: This function wraps the text in a text widget to fit within its bounds.

- **IsEmpty(tTarget)**: This function checks if a table is empty.

- **MboxAbs(nNumber)**: This function returns the absolute value of a number.

- **ValidateParameter(Parameter, sType, DefaultValue)**: This function validates a parameter against a specified type.

- **HandleE3HudModeEvent(oWidget, tEvent)**: This function handles the E3 HUD mode event for a given widget.

- **HandleAddMessageEvent(oWidget, tEvent)**: This function handles adding a message event to a given widget.

- **DrawDebugRectangle(TargetWidget)**: This function draws a debug rectangle on the target widget.



## Notes for modders

- **Call-order requirements**: Ensure that `InstantiateTextBuffer` is called before attempting to add messages or modify properties of the text buffer. The order of events and message management functions should be respected to maintain proper functionality.

- **Pitfalls**: Be cautious when modifying pending messages or clearing messages, as these actions can affect the visibility and behavior of messages in the text buffer.

- **Tunables**: Adjusting `kScrollSpeed` can change the scrolling speed of text buffers. Ensure that this value is set appropriately for the desired user experience.

- **Decompiler artifacts**: There may be unused locals or slightly unusual operator precedence groupings in the decompiled code, which are artifacts of the decompilation process and should not be interpreted as intentional logic.