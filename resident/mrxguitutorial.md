---

title: mrxguitutorial

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, tutorial]

verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- no OnActivate/Create/tInstance anywhere in source)

---



# mrxguitutorial



*Module: mrxguitutorial.lua*



## Overview

The `mrxguitutorial` module is responsible for managing in-game tutorials that guide players through various game elements. It provides functionality to display, position, and animate tutorial messages, as well as handle user input and state changes related to these tutorials.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxUtil`



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is the one shared tutorial-message system, not something spawned per world
object. Key fields:

- `_bTutorialsOn`: A boolean flag indicating whether tutorials are enabled globally.

- `_knIncrement`: An integer constant used in the `_OptimizeSize` function to adjust text size incrementally.



The module manages tutorial widgets, their children, and associated animations. It also handles input events and state changes to ensure proper functionality and user experience.

```



## Functions



### DisplayTutorialForObject(uPlayerGuid, sMessage, uGuid, fCallback, tCallbackData)

- **Description**: Displays a tutorial message for a specific object. If `Gui.FindGuiLocation` is available, it uses the object's location to position the tutorial; otherwise, it returns false.

- **Parameters**:

  - `uPlayerGuid`: The GUID of the player who will see the tutorial.

  - `sMessage`: The message to display in the tutorial.

  - `uGuid`: The GUID of the object associated with the tutorial.

  - `fCallback`: A callback function to be called after the tutorial is closed or dismissed.

  - `tCallbackData`: Data to pass to the callback function.



### DisplayTutorial(uPlayerGuid, sMessage, nX1, nY1, nX2, nY2, sHorizAnchor, sVertAnchor, fCallback, tCallbackData)

- **Description**: Displays a tutorial message at specified coordinates. Adjusts the position and size of the tutorial based on the provided parameters.

- **Parameters**:

  - `uPlayerGuid`: The GUID of the player who will see the tutorial.

  - `sMessage`: The message to display in the tutorial.

  - `nX1`, `nY1`, `nX2`, `nY2`: Coordinates defining the area where the tutorial should be displayed.

  - `sHorizAnchor`, `sVertAnchor`: Horizontal and vertical anchor points for positioning the tutorial.

  - `fCallback`: A callback function to be called after the tutorial is closed or dismissed.

  - `tCallbackData`: Data to pass to the callback function.



### _CreateTutorial(sMessage, nPointX1, nPointY1, nPointX2, nPointY2, sHorizAnchor, sVertAnchor, fCallback, tCallbackData, uPlayerGuid)

- **Description**: Creates and displays a tutorial widget with the specified message and position. Handles text wrapping and arrow positioning.

- **Parameters**:

  - `sMessage`: The message to display in the tutorial.

  - `nPointX1`, `nPointY1`, `nPointX2`, `nPointY2`: Coordinates defining the area where the tutorial should be displayed.

  - `sHorizAnchor`, `sVertAnchor`: Horizontal and vertical anchor points for positioning the tutorial.

  - `fCallback`: A callback function to be called after the tutorial is closed or dismissed.

  - `tCallbackData`: Data to pass to the callback function.

  - `uPlayerGuid`: The GUID of the player who will see the tutorial.



### _OptimizeSize(oText, nMaxWidth, nMaxHeight, bEnforceHeight)

- **Description**: Adjusts the size of a text widget to fit within specified width and height constraints while maintaining aspect ratio.

- **Parameters**:

  - `oText`: The text widget to optimize.

  - `nMaxWidth`, `nMaxHeight`: Maximum width and height for the text widget.

  - `bEnforceHeight`: A boolean indicating whether to enforce the maximum height constraint.



### _HandleInput(oTutorial, tInput)

- **Description**: Handles input events for a tutorial widget. Closes the tutorial if certain buttons are pressed and calls the callback function.

- **Parameters**:

  - `oTutorial`: The tutorial widget that received the input.

  - `tInput`: A table containing information about the input event.



### _HandleStateChange(oTutorial, vStateInfo)

- **Description**: Handles state change events for a tutorial widget. Currently does nothing (stub function).



### _DeleteTutorial(oTutorial)

- **Description**: Deletes a tutorial widget and its children, releasing control focus and removing it from the GUI.

- **Parameters**:

  - `oTutorial`: The tutorial widget to delete.



### _DeleteChildren(oWidget)

- **Description**: Recursively deletes all child widgets of a given widget.

- **Parameters**:

  - `oWidget`: The parent widget whose children are to be deleted.



### _GetTutorialsEnabled()

- **Description**: Retrieves the current state of the tutorials enabled flag. Uses the system function if available, otherwise returns the module-level flag `_bTutorialsOn`.



### _SetTutorialsEnabled(bEnable)

- **Description**: Sets the state of the tutorials enabled flag. Updates the system setting if available, otherwise updates the module-level flag `_bTutorialsOn`.

- **Parameters**:

  - `bEnable`: A boolean indicating whether to enable or disable tutorials.



### TutorialWidgetInitialize(oTutorial)

- **Description**: Initializes a tutorial widget by setting up its children and custom data.

- **Parameters**:

  - `oTutorial`: The tutorial widget to initialize.



### SetTutorialWidgetText(oTutorial, sText)

- **Description**: Sets the text of a tutorial widget. Handles visibility, text animation, and resizing of associated images.

- **Parameters**:

  - `oTutorial`: The tutorial widget whose text is being set.

  - `sText`: The new text to display in the tutorial.



### InitInfoImage(oImage)

- **Description**: Initializes an info image by setting up its children and custom data, including animation points for various parts of the image.

- **Parameters**:

  - `oImage`: The info image to initialize.



### HideInfoImage(oImage)

Hides an info image by animating its components. It sets the current animation to "close" and adjusts the positions of `oInfo`, `oMid`, `oStart`, and `oEnd` widgets over a specified time (`nTime`). The function also calls `_ExecTwoAnims` to animate two widgets simultaneously.



### _ExecAnim(unused, oWidget, nPoint, nTime)

Executes an animation on a widget. It animates the widget to a specific point (`nPoint`) over a given time (`nTime`).



### _ExecTwoAnims(unused, oWidget1, nPoint1, nTime1, oWidget2, nPoint2, nTime2, oParent)

Animates two widgets simultaneously. It calls `_EndAnim` when both animations are complete.



### _EndAnim(oUnused, oParent)

Sets the translucency of a parent widget to 0 and marks it as not visible (`bVisible = false`).



### ResizeInfoImage(oImage, nWidth)

Resizes an info image by adjusting its width. It checks if resizing should be animated based on the `bAnimateResize` flag. If true, it performs the resize animation using `PerformResizeAnimation`.



### PerformResizeAnimation(oImage, nWidth)

Performs the actual animation of resizing the info image. It adjusts the positions and animations of `oInfo`, `oMid`, `oStart`, and `oEnd` widgets over a specified time (`nTime`).



### PushTutorialToFront(oTutorial)

Brings a tutorial to the front by pushing its children widgets to the front using `MrxGuiBase.PushWidgetToFront`. It ensures that all relevant components of the tutorial are visible and in the correct order.



## Events



- **Event.OnPlayerJoined**: This module listens for this event to initialize tutorials when a new player joins the session.

- **Event.OnPlayerLeft**: This module listens for this event to clean up any active tutorials when a player leaves the session.

- **Event.OnInputReceived**: This module listens for input events to handle interactions with tutorial widgets, such as closing them.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `DisplayTutorialForObject` or `DisplayTutorial` is called after the GUI has been fully initialized and before any player interaction that might trigger a tutorial.

   - The `_CreateTutorial` function should not be called directly by modders unless they have a specific need to bypass the standard tutorial creation process.



2. **Pitfalls**:

   - Modifying the internal functions (those prefixed with an underscore) can lead to unexpected behavior or instability, as these are intended for internal use only.

   - Be cautious when changing the size constraints (`nMaxWidth`, `nMaxHeight`) in `_OptimizeSize` to ensure that text remains readable and does not overflow.



3. **Tunables**:

   - The `_knIncrement` constant can be adjusted to change how much the text size is incremented during optimization, which might affect readability on different screen resolutions.

   - The `bAnimateResize` flag in `ResizeInfoImage` controls whether resizing animations are performed, allowing modders to disable animations for performance reasons.



4. **Decompiler artifacts**:

   - There are no known decompiler artifacts in this module that require special attention or interpretation.