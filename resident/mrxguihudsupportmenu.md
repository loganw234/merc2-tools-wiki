---

title: MrxGuiHudSupportMenu

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, support]

---



# MrxGuiHudSupportMenu



*Module: mrxguihudsupportmenu.lua*



## Overview

The `MrxGuiHudSupportMenu` module is responsible for managing the in-game HUD support menu. It handles adding, removing, and displaying support items such as weapons, supplies, and other resources. The module also manages animations, input handling, and UI updates to provide a dynamic and interactive user experience.



## Inheritance

- Inherits from: none — base/utility module
- Imports: 

  - `MrxGuiBase`

  - `MrxPmc`

  - `MrxGuiManager`

  - `MrxSupport`

  - `MrxSupportManager`



## Instance pattern

This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:

- `tItems`: A list of support items available in the menu.

- `nSelectedIndex`: The index of the currently selected item.

- `bOpen`: Indicates whether the menu is open or closed.

- `bAnimating`: Indicates whether an animation is currently in progress.

- `bShootingGalleryMode`: Indicates whether the shooting gallery mode is enabled.

- `nIdleTime`: Accumulated idle time for handling periodic updates.

- `tDisplayList`: A list of items currently displayed on the menu.

- `tPendingItems`: A queue of pending items to be added or removed.

- `oFrame`: The frame widget representing the support menu.

- `oArrowUp`, `oArrowDown`: Arrow widgets for navigation.

- `oBullet1`, `oBullet2`, `oBullet3`: Bullet widgets for visual effects.

- `oDescriptor`: Descriptor widget for additional information.

- `nCash`, `nFuel`: Current cash and fuel amounts available in the menu.

```



## Functions



### AddItem(oSupportMenu, tData)

Adds a support item to the menu. It checks if the item is valid and then processes it based on various conditions such as whether input is suspended or if the item needs network synchronization. If the item is valid, it adds it to the internal list and handles animations.



### _AddItemToInternalList(oSupportMenu, tData)

A helper function that inserts a support item into the internal list of the menu. It ensures the item is not already added and sets up its properties like fuel and cash costs.



### RemoveItem(oSupportMenu, sItemName, bDontNetSync)

Removes a support item from the menu by name. It checks for pending items first and then removes the item from both the internal list and the network if necessary. It also updates the display information and closes the menu if there are no more items.



### RemoveAll(oSupportMenu)

Removes all items from the menu, resets counters, and closes the menu if it is enabled.



### Trigger(oSupportMenu)

Triggers the selected support item. It checks for resource constraints (fuel and cash) and denial conditions before proceeding with the trigger action. If successful, it plays a sound and animates the icon.



### Open(oSupportMenu, bAnimateAdd)

Opens the support menu. It sets up various UI elements, handles animations, and updates the display information. It also posts an event for opening the menu.



### Close(oSupportMenu)

Closes the support menu. It releases control focus, hides resource indicators, processes pending items, and plays a sound. It also posts an event for closing the menu.



### SetCash(oSupportMenu, nCash)

Sets the cash amount for the menu. This function is currently empty.



### SetFuel(oSupportMenu, nFuel)

Sets the fuel amount for the menu. This function is currently empty.



### SetShootingGalleryMode(oSupportMenu, bEnabled)

Sets the shooting gallery mode for the menu. This mode affects how items are handled and displayed.



### HandleInitializationEvent(oWidget, tEvent)

This function initializes the HUD support menu widget by setting up its display items, handling animations, and initializing various UI elements such as arrows, bullets, and descriptors. It also sets up event handlers for input and game state changes.



### _SetDisplayInformation(oWidget)

This private function updates the display information of the support menu based on the current selected item index and the list of items. It handles visibility, texture setting, and denial conditions for each displayed item.



### _ScrollDown(oWidget)

This private function scrolls the support menu down by one item. It updates the display list, sets up animations, and handles input suspension to prevent rapid scrolling.



### _ScrollUp(oWidget)

This private function scrolls the support menu up by one item. Similar to `_ScrollDown`, it updates the display list, sets up animations, and manages input suspension.



### CreateInternalListItem(tData)

This function creates an internal list item with default values for missing parameters such as `sIcon` and `sLitIcon`. It also sets up a trigger function for the item.



### TriggerItem(oSupport)

This function triggers the support item by creating a new instance of the support and commencing its action. It ensures that the support has the necessary methods (`Create` and `Commence`) before proceeding.



### UpdateDisplayText(oWidget, bHalt)

This function updates the display text for the support menu widget. It calls two helper functions to update displayed text and clock icon visibility.



### _FixText(oWidget)

This private function schedules a timer event to call `UpdateDisplayText` with a delay of 0.1 seconds, ensuring that text updates are handled correctly.



### `_UpdateDisplayedText(oWidget)`

- **Purpose:** Updates the displayed text for a widget based on the selected support item.

- **Parameters:**

  - `oWidget`: The widget whose text needs to be updated.

- **Behavior:**

  - Retrieves the currently selected item's data and associated support object.

  - Sets the support name text.

  - Checks denial conditions and updates fuel cost, stockpile text, and designator text accordingly.

  - Adjusts colors based on availability and resource constraints.



### `_UpdateClockIcon(oWidget, bHalt)`

- **Purpose:** Updates the clock icon for a widget to indicate cooldown time of the selected support item.

- **Parameters:**

  - `oWidget`: The widget whose clock icon needs to be updated.

  - `bHalt`: A boolean indicating whether to halt the animation callback.

- **Behavior:**

  - Retrieves the currently selected item's data and associated support object.

  - Sets the visibility of the clock icon based on cooldown time.

  - Updates the clock animation if within cooldown period.

  - Sets or clears the animation callback based on conditions.



### `_UpdateStatusDisplay(oSupportMenu)`

- **Purpose:** Updates the status display for a support menu based on the selected items and their availability.

- **Parameters:**

  - `oSupportMenu`: The support menu whose status needs to be updated.

- **Behavior:**

  - Iterates through the display list and updates each item's status based on denial conditions, stock count, and fuel cost.



### `_UpdateDisplayPeriodic(oSupportMenu)`

- **Purpose:** Periodically updates the displayed text, status, and clock icon for a support menu.

- **Parameters:**

  - `oSupportMenu`: The support menu to be updated.

- **Behavior:**

  - Calls `_UpdateDisplayedText` and `_UpdateStatusDisplay`.

  - Updates the clock icon if it is not visible.



### `HandleUpdateForIdle(oWidget, nDeltaTime)`

- **Purpose:** Handles periodic updates for a widget when it is idle.

- **Parameters:**

  - `oWidget`: The widget to be updated.

  - `nDeltaTime`: The time elapsed since the last update.

- **Behavior:**

  - Accumulates idle time and triggers periodic updates if the accumulated time exceeds a threshold.



### `_FrameClosed(oFrame)`

- **Purpose:** Handles the closure of a frame by adjusting its position and visibility.

- **Parameters:**

  - `oFrame`: The frame to be closed.

- **Behavior:**

  - Adjusts the position of frame pieces based on text width.

  - Sets the frame's visibility to false.



### `HandleUpdateForTriggerUp(oWidget, nDeltaTime)`

- **Purpose:** Handles updates for a widget when a trigger is activated in the "up" direction.

- **Parameters:**

  - `oWidget`: The widget to be updated.

  - `nDeltaTime`: The time elapsed since the last update.

- **Behavior:**

  - Triggers various animations and events based on accumulated time.



### `HandleUpdateForTriggerDown(oWidget, nDeltaTime)`

- **Purpose:** Handles updates for a widget when a trigger is activated in the "down" direction.

- **Parameters:**

  - `oWidget`: The widget to be updated.

  - `nDeltaTime`: The time elapsed since the last update.

- **Behavior:**

  - Triggers various animations and events based on accumulated time.



### `HandleUpdateForOpen(oWidget, nDeltaTime)`

- **Purpose:** Handles updates for a widget when it is opened.

- **Parameters:**

  - `oWidget`: The widget to be updated.

  - `nDeltaTime`: The time elapsed since the last update.

- **Behavior:**

  - Triggers various animations and events based on accumulated time. Adjusts visibility and translucency of arrow backgrounds.



### HandleUpdateForClose(oWidget, nDeltaTime)

This function handles the update logic for closing a widget. It manages animations and visibility changes based on elapsed time (`nDeltaTime`). The function updates the `CustomData` of the widget to track animation times and triggers various animations and state changes at specific points in time.



### _PassedPoint(nPreviousValue, nNewValue, nPoint)

This helper function checks if a given point (`nPoint`) has been passed between two values (`nPreviousValue` and `nNewValue`). It returns `true` if the point is within the range defined by the previous and new values, considering both increasing and decreasing scenarios.



### _SetVisible(oUnused, oWidget, bVisible)

This function sets the visibility of a widget. The first argument `oUnused` appears to be unused in this context. The function calls `oWidget:SetVisible(bVisible)` to change the visibility state of the widget.



### _SetupItemAnimationPoints(nIndex, tDisplayList)

This function sets up animation points and custom data for an item widget at a specific index (`nIndex`) within a display list (`tDisplayList`). It initializes various components like icons, borders, orbits, and status elements, adding animation points for movement, scaling, and fading effects. It also assigns methods to the widget for handling different animations and state changes.



### _SetItemTexture(oWidget, sIcon)

This function sets the texture of an item's icon. The `oWidget` parameter is the widget whose icon needs to be updated, and `sIcon` is the path or identifier of the new icon texture.



### _SetItemStatus(oWidget, sStatus)

This function updates the status of an item based on a given status string (`sStatus`). It sets texture coordinates for the status element based on predefined conditions. The function also manages whether the status is in use by setting a boolean flag in `CustomData`.



### _StartStatusPulse(oStatus)

This helper function starts pulsing the status element by calling `_StatusPulseToOpaque` to animate it to full opacity.



### _HaltStatusPulse(oStatus, bVis)

This function halts the pulsing animation of the status element. If `bVis` is `true`, it animates the status back to full visibility; otherwise, it fades it out.



### _StatusPulseToClear(oStatus)

This helper function animates the status element to clear (transparent) by calling `_StatusPulseToOpaque` after a delay.



### _StatusPulseToOpaque(oStatus)

This helper function animates the status element to opaque (fully visible) by calling `_StatusPulseToClear` after a delay, creating a pulsing effect.



### _SetUpFlipPoints(oWidget, oPrev, oNext)

This function sets up animation points for flipping an item widget. It calculates midpoints and end points for width and height based on the current widget and its neighboring widgets (`oPrev` and `oNext`). It also sets up scaling points and assigns a method `_ScaleTo` to handle scaling animations.



### _SetUpScaledPoints(oWidget, oPrev, oNext)

This function sets up animation points for scaling an item widget. It calculates midpoints and end points for width and height based on the current widget and its neighboring widgets (`oPrev` and `oNext`). It also assigns a method `_ScaleTo` to handle scaling animations.



### _ScaleTo(oWidget, nWidth, nHeight, nTime, bImmediate, fCallback, tCallbackData)

This function scales an item widget to new dimensions (`nWidth` and `nHeight`) over a specified time (`nTime`). If the animation is immediate (`bImmediate`), it sets the location directly. Otherwise, it animates the widget to the new dimensions using predefined animation points. It also supports optional callbacks after the animation completes.



### _MoveTo(oWidget, nPoint, nTime, bImmediate, fCallback, tCallbackData)

This function moves an item widget to a specified point (`nPoint`) over a given time (`nTime`). If the movement is immediate (`bImmediate`), it sets the location directly. Otherwise, it animates the widget to the target point using predefined animation points. It also supports optional callbacks after the movement completes.



### `_TriggerItemNext(oWidget, nTime)`

Triggers the animation for moving to the next item in a widget. It animates the widget from its previous point to its origin point over the specified time. Additionally, it scales various components of the widget (icon background, icon, border, orbit, and status) to their respective end states and then back to their original states.



### `_TriggerItemPrev(oWidget, nTime)`

Triggers the animation for moving to the previous item in a widget. It animates the widget from its next point to its origin point over the specified time. Similar to `_TriggerItemNext`, it scales various components of the widget (icon background, icon, border, orbit, and status) to their respective end states and then back to their original states.



### `_SetupItemNext(oWidget)`

Sets up the widget for moving to the next item by positioning it at its previous point and scaling its components (icon background, icon, border, orbit, and status) to their previous end states.



### `_SetupItemPrev(oWidget)`

Sets up the widget for moving to the previous item by positioning it at its next point and scaling its components (icon background, icon, border, orbit, and status) to their next end states.



### `_TriggerSquish(oItem, nTime, bEntering, bTop)`

Triggers the squish animation for an item. If `bEntering` is true, it scales the item's icon and background to a smaller width and animates the item to its origin point. If `bEntering` is false, it animates the item to either its top or bottom squish point and scales the icon and background back to their original widths.



### `_SetupSquish(oItem, bEntering, bTop)`

Sets up the squish animation for an item by positioning it at its squish point (top or bottom) and scaling its components (icon and background) to a smaller width. If `bEntering` is false, it animates the item back to its origin point and scales its components back to their original widths.



### `_SetupItemOpen(oItem)`

Sets up an item for opening by moving it to its exit point, hiding its icon and background, setting the translucency of its border and orbit to 0, and animating them to a fade-out point.



### `_TriggerItemOpenMain(oItem, nTime)`

Triggers the main animation for opening an item. It animates the item to its enter point, fades in the border and icon, and if the status component is in use, it sets it visible and animates it to a fade-in point.



### `_TriggerItemClose(oItem, nTime)`

Triggers the animation for closing an item. It animates the item to its exit point, fades out the border and orbit, scales the icon and background back to their original widths, and hides the status component after fading it out.



### `_InitializeBullets(oWidget)`

Initializes bullet components within a widget by adding fade-in and fade-out animation points and setting up each bullet's target point and original rotation. It also assigns the `_AnimateBullet` function to `oWidget.AnimateBullet`.



### `_AnimateBullet(oWidget, nNumber, nTime, nFromRotationOffset, nToRotationOffset, nDirection, bHide)`

Animates a specific bullet within the widget by rotating it from its original rotation plus a specified offset and animating it to another rotation offset over the specified time. After the animation, it calls `_ResetBullet` to reset the bullet's rotation and optionally hide it.



### `_ResetBullet(oBullet, bHide)`

Resets a bullet's rotation to its original state and hides it if `bHide` is true.



### _CreateFlyingIcon(oTemplateWidget)

- **Description**: Creates a new flying icon widget based on the provided template widget.

- **Parameters**:

  - `oTemplateWidget`: The template widget to base the new icon on.

- **Returns**: The newly created flying icon widget.



### _CopyImageParameters(oTemplateWidget)

- **Description**: Copies image parameters from a template widget to a new image widget.

- **Parameters**:

  - `oTemplateWidget`: The template widget to copy parameters from.

- **Returns**: A new image widget with copied parameters.



### _CompleteIconTranslation(oWidget)

- **Description**: Completes the translation of an icon widget by removing it and its children.

- **Parameters**:

  - `oWidget`: The widget to complete the translation for.



### _StartIconTranslation(oWidget)

- **Description**: Starts the translation of an icon widget, including scaling animations.

- **Parameters**:

  - `oWidget`: The widget to start the translation for.



### ValidateParameter(Parameter, sType, DefaultValue)

- **Description**: Validates a parameter against a specified type and returns it if valid; otherwise, returns a default value.

- **Parameters**:

  - `Parameter`: The parameter to validate.

  - `sType`: The expected type of the parameter.

  - `DefaultValue`: The default value to return if validation fails.

- **Returns**: The validated parameter or the default value.



### Min(nA, nB)

- **Description**: Returns the minimum of two numbers.

- **Parameters**:

  - `nA`: The first number.

  - `nB`: The second number.

- **Returns**: The minimum of `nA` and `nB`.



### HandleInputEvent(oSupportMenu, tEvent)

- **Description**: Handles input events for a support menu widget.

- **Parameters**:

  - `oSupportMenu`: The support menu widget to handle the event for.

  - `tEvent`: The input event data.



### WrapIndex(nIndex, nMaxIndex)

- **Description**: Wraps an index within a specified range.

- **Parameters**:

  - `nIndex`: The index to wrap.

  - `nMaxIndex`: The maximum index value.

- **Returns**: The wrapped index.



### _AnimationCompleteCallback(oUnused, oWidget)

- **Description**: Callback function for when an animation completes on a widget.

- **Parameters**:

  - `oUnused`: Unused parameter (likely a placeholder).

  - `oWidget`: The widget the animation completed on.



### _FrameAnimationCompleteCallback(oWidget, oParent)

- **Description**: Callback function for when a frame animation completes on a widget.

- **Parameters**:

  - `oWidget`: The widget the animation completed on.

  - `oParent`: The parent widget of the animated widget.



### _HandleGameStateChangeEvent(oWidget, sStateName, sStateAction)

- **Description**: Handles game state change events for a widget.

- **Parameters**:

  - `oWidget`: The widget to handle the event for.

  - `sStateName`: The name of the game state that changed.

  - `sStateAction`: The action performed on the game state.



### _RemoveOnAnimationComplete(oWidget, oAmmoIcon)

- **Description**: Removes a widget and its ammo icon when an animation completes.

- **Parameters**:

  - `oWidget`: The widget to remove.

  - `oAmmoIcon`: The ammo icon associated with the widget.



### _RemoveAddAnimationComplete(oWidget)

- **Description**: Removes a widget during an add animation complete event.

- **Parameters**:

  - `oWidget`: The widget to remove.



### _DelayedSupportMenuCloseCallback(oSupportMenu, fFunction, tCallbackData)

- **Description**: Callback function for delayed support menu closure.

- **Parameters**:

  - `oSupportMenu`: The support menu to close.

  - `fFunction`: A callback function to execute after closing.

  - `tCallbackData`: Data to pass to the callback function.



### _AddAnimationComplete(oUnused, oSupportMenu, fCallback, tCallbackData)

- **Description**: Adds an animation complete event for a support menu widget.

- **Parameters**:

  - `oUnused`: Unused parameter (likely a placeholder).

  - `oSupportMenu`: The support menu widget to add the event for.

  - `fCallback`: A callback function to execute when the animation completes.

  - `tCallbackData`: Data to pass to the callback function.



### _PerformAddAnimation(oWidget, fCallback, tCallbackData)

- **Description**: Performs an add animation on a support menu widget.

- **Parameters**:

  - `oWidget`: The support menu widget to perform the animation on.

  - `fCallback`: A callback function to execute after the animation completes.

  - `tCallbackData`: Data to pass to the callback function.



### _HandleUpdateForAdd(oWidget, nDeltaTime)

- **Description**: Handles update events for an add animation on a support menu widget.

- **Parameters**:

  - `oWidget`: The support menu widget to handle the update for.

  - `nDeltaTime`: The time elapsed since the last update.



### InitAddWidget(nX, nY, nSize, uOwner)

This function initializes a new widget for the HUD support menu. It creates various child widgets such as an icon background (`oIconBg`), an icon (`oIcon`), an icon frame (`oIconFrame`), and a text widget (`oText`). These widgets are positioned and configured with specific textures, coordinates, and animation points. The function sets up the initial state of these widgets, including their visibility and owner, and adds them to the HUD. It also initializes custom data for the main widget, such as a queue for new items to be displayed and flags for active state.



### ShowNewAddAnimation(oAdd, sIcon, sText)

This function queues a new item to be shown in the HUD support menu. The item is represented by an icon texture (`sIcon`) and text (`sText`). If the widget is not already active, it sets the widget as active and starts the animation sequence for displaying the first queued item.



### HideNewAddAnimation(oAdd)

This function hides the HUD support menu widget. It animates all child widgets (icon background, icon, icon frame, and text) to their hide points and resets the active state of the widget. It also clears the queue of any remaining items.



### RemoveNewAddItem(oAdd, sText)

This function removes a specific item from the queue of new items in the HUD support menu. The item is identified by its text (`sText`). If the item is found in the queue, it is removed.



### _NewAddProcessQueue(oUnused, oAdd, bInitial)

This internal function processes the queue of new items to be displayed in the HUD support menu. It handles the animation sequence for showing and hiding each item. If there are no more items in the queue, it hides the widget. Otherwise, it removes the first item from the queue, updates the icon and text widgets, and starts the animation sequence.



### _NewAddStep2(oIconBg, oText, oIcon, oIconFrame, oAdd)

This internal function is part of the animation sequence for displaying an item in the HUD support menu. It animates the child widgets to their show points and sets up the next step in the animation sequence.



### _NewAddStep3(oIconBg, oText, oIcon, oIconFrame, oAdd)

This internal function is part of the animation sequence for hiding an item in the HUD support menu. It animates the child widgets back to their hide points and processes the next item in the queue.



### _NewAddStepInitial2(oIconBg, oText, oIcon, oIconFrame, oAdd)

This internal function is part of the initial animation sequence for displaying an item in the HUD support menu. It animates the child widgets to their hide points and sets up the next step in the animation sequence.



### _NewAddStepInitial3(oIconBg, oText, oIcon, oIconFrame, oAdd)

This internal function is part of the initial animation sequence for displaying an item in the HUD support menu. It animates the child widgets to their show points and sets up the next step in the animation sequence.



## Events



- **`Event.ObjectHibernation`**: Listens for this event to trigger the `Awake` function, which initializes the per-instance table for the HUD support menu.

- **`Event.InputEvent`**: Handles input events for the support menu widget through `HandleInputEvent`.

- **`Event.GameStateChange`**: Manages game state changes with `_HandleGameStateChangeEvent`.

- **`Event.TimerRelative`**: Used for periodic updates and animations, such as `_FixText`, `_UpdateDisplayPeriodic`, and handling idle time in `HandleUpdateForIdle`.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `InitAddWidget` is called before attempting to show or hide the add animation.

   - The sequence of functions like `_NewAddStep2`, `_NewAddStep3`, and `_NewAddProcessQueue` should not be manually invoked; they are part of the internal animation process.



2. **Pitfalls**:

   - Directly modifying `CustomData` without understanding its structure can lead to unexpected behavior.

   - Be cautious with resource constraints (fuel and cash) when triggering support items, as it may result in denial conditions or insufficient resources.



3. **Tunables**:

   - The constant `_knFrame = 0.022222223` is used for timing calculations. Modifying this value can affect the smoothness of animations.

   - Animation durations and points (e.g., in `_ScaleTo`, `_MoveTo`) can be adjusted to change the visual behavior of the support menu.



4. **Decompiler artifacts**:

   - Unused local variables or redundant operator groupings are decompiler artifacts and should not be interpreted as intentional logic.