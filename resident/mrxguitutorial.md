---

title: mrxguitutorial

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, tutorial]

verified: true
verified_note: 'deeper pass: fixed Imports (only MrxGuiBase, not MrxGui/MrxUtil); rewrote fabricated Events (there are ZERO Event.* calls — removed invented Event.OnPlayerJoined/OnPlayerLeft/OnInputReceived; real input is a "ControllerInput" widget handler); added arrow texture/prompt string/sound cues/_knIncrement=25/fonts and the tutorial-off toggle button'

---



# mrxguitutorial



*Module: mrxguitutorial.lua*



## Overview

The `mrxguitutorial` module is responsible for managing in-game tutorials that guide players through various game elements. It provides functionality to display, position, and animate tutorial messages, as well as handle user input and state changes related to these tutorials.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGuiBase` only (the source's single `import("MrxGuiBase")` — the previous draft's "MrxGui, MrxUtil" was wrong). It also calls `Gui.*`, `Sys.*`, and `Sound.*` engine namespaces directly without importing them. See [MrxGuiBase](mrxguibase) for the widget/animation/control-focus primitives it builds on.



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is the one shared tutorial-message system, not something spawned per world
object. Each `DisplayTutorial` call builds a fresh container widget whose state (`fCallback`,
`tCallbackData`) lives on that widget's `CustomData`. Module-level state/constants:

- `_bTutorialsOn = true`: fallback global "tutorials enabled" flag, used only when the engine's
  `Sys.TutorialsEnabled`/`Sys.SetTutorialsEnabled` aren't present.
- `_knIncrement = 25`: the pixel step `_OptimizeSize` uses when shrinking the text box to a squarer aspect.

## Module constants & tunables

- Tutorial body font is `"english_20"` at scale `1`.
- Every message has this prompt appended automatically:
  `"[n][n][confirm] [Generic.Continue][n][action] [Generic.DisableTutorials]"` — the two localized button
  hints. So the on-screen text is always your `sMessage` plus a Continue / Disable-Tutorials footer.
- The pointing arrow is a `SpriteWidget` with texture `"temp_tutorial_arrow"` (128×64 sheet, 32×64 frames),
  animated frames 0-3 at `0.25`s, looping; it's rotated 90/180/270° to point at the highlighted spot.
- Backdrop behind the text is black at alpha `192` (`SetColor(0,0,0,192)`).
- Sound cues: dismissing a tutorial plays `"ui_HUD_Continue"`; `SetTutorialWidgetText` (the info-image
  variant) plays `"ui_signal_ding_up"` on show.
- Open/close/resize animations run over `nTime = 0.5`s.



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

- **Description**: The `"ControllerInput"` handler bound in `_CreateTutorial`. `BUTTON_PAD2_D` (confirm) closes the tutorial; `BUTTON_PAD2_U` (the "disable tutorials" button) calls `_SetTutorialsEnabled(false)` *and* closes it. On close it plays `Sound.CueSound(0, "ui_HUD_Continue")`, fires `fCallback(unpack(tCallbackData))`, then `_DeleteTutorial`. Any other button is ignored.

- **Parameters**:

  - `oTutorial`: The tutorial container widget (holds the callback in `CustomData`).

  - `tInput`: The input event; `tInput.ButtonPress` is compared against `MrxGuiBase.Joystick.BUTTON_*` constants.



### _HandleStateChange(oTutorial, vStateInfo)

- **Description**: Empty stub — defined but does nothing and is not bound to anything in this file.



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



### ShowInfoImage(oImage)

**Not previously documented — `HideInfoImage`'s counterpart**, assigned to `oImage.Show` by `InitInfoImage`
the same way `HideInfoImage` is assigned to `oImage.Hide`. Sets `bVisible = true` and, unless already mid-
"open" animation, sets `sCurrentAnimation = "open"`, sets full translucency, and animates `oInfo`/`oMid`/
`oStart`/`oEnd` open the same way `HideInfoImage` animates them closed.

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

**There are no `Event.*` (engine event) subscriptions in this file** — the previous draft's
`Event.OnPlayerJoined`/`Event.OnPlayerLeft`/`Event.OnInputReceived` do not exist in the source and have been
removed. The only input plumbing is widget-level: `_CreateTutorial` calls
`oContainer:SetEventHandler("ControllerInput", _HandleInput)` and takes control focus with
`MrxGuiBase.GetControlFocus(oContainer, true)` (the `true` pauses). Dismissal is driven entirely by that
handler.

## Notes for modders

- **Entry points are `DisplayTutorial` / `DisplayTutorialForObject`.** `DisplayTutorialForObject` needs the
  engine's `Gui.FindGuiLocation(uPlayerGuid, uGuid)` to turn an object handle into a screen rect; if that
  function is absent it returns `false` and shows nothing.
- **Tutorials-off is a real gate, not a no-op.** If `_GetTutorialsEnabled()` is false, `DisplayTutorial`
  skips all UI, immediately calls your `fCallback(unpack(tCallbackData))`, and returns `true`. So your
  callback fires whether or not the tutorial was actually shown — don't put "user acknowledged" logic there
  and assume they saw it.
- **The enabled flag prefers the engine.** `_GetTutorialsEnabled`/`_SetTutorialsEnabled` use
  `Sys.TutorialsEnabled`/`Sys.SetTutorialsEnabled` when present and only fall back to the module global
  `_bTutorialsOn`. Pressing the disable button (`BUTTON_PAD2_U`) while a tutorial is up turns tutorials off
  for the rest of the session.
- **Retheme knobs**: swap the arrow texture `"temp_tutorial_arrow"`, change the appended prompt string, or
  adjust the `0.5`s animation time / `_knIncrement` box-shrink step (above). `_OptimizeSize` shrinks the text
  box toward a square-ish aspect within the available screen quadrant, which is how the tutorial picks a side
  (left/right/top/bottom) and arrow direction relative to the highlighted object.
- The `InitInfoImage`/`ShowInfoImage`/`HideInfoImage`/`ResizeInfoImage`/`SetTutorialWidgetText`/
  `TutorialWidgetInitialize`/`PushTutorialToFront` family is a **second, layout-driven tutorial widget**
  (four-piece expanding "info" panel with a typewriter text reveal), distinct from the coordinate-based
  `_CreateTutorial` path — these are bound from a GUI layout, not called by the two `Display*` entry points.