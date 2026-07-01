---

title: MrxGuiBase

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: Inheritable

tags: [gui, widget]

---



# MrxGuiBase



*Module: mrxguibase.lua*



## Overview

The `MrxGuiBase` module is a foundational component for managing graphical user interface (GUI) elements in the game. It provides a comprehensive set of functions and classes to create, manage, and manipulate various types of widgets such as text, images, flash animations, minimaps, sprites, and movies. The module also handles screen resolution changes, input events, and widget lifecycle management.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `EventManager`



## Instance pattern

This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:

- **Joystick**: A table defining constants for different joystick buttons.

- **ControlFocusQueue**: A table that manages the focus queue for widgets, indexed by owner GUID or "global".

- **ControlModeManager**: A table that tracks whether a control mode is paused or not, indexed by owner GUID or "global".



The module also maintains global state related to screen dimensions and resolution settings:

- `nWidgetSpaceScreenWidth`: The width of the widget space in pixels.

- `nWidgetSpaceScreenHeight`: The height of the widget space in pixels.

- `nScreenWidth`: The current screen width in pixels.

- `nScreenHeight`: The current screen height in pixels.

- `nScreenPositionX`: The X position of the screen.

- `nScreenPositionY`: The Y position of the screen.

- `nPixelWidth`: The width of a pixel.

- `nPixelHeight`: The height of a pixel.

- `nScreenScaleFactor`: The scale factor for the screen.



The module defines several widget classes such as `Widget`, `TextWidget`, `ImageWidget`, `FlashWidget`, `SpriteWidget`, and `MovieWidget`, each with its own set of properties and methods for managing specific types of GUI elements.

```



## Functions



### GetControlFocus(oWidget, bPause, bGlobal)

Manages the focus queue for a given widget. If `bPause` is true, it sets the dialog box mode; otherwise, it sets the support menu mode.



### ReleaseControlFocus(oWidget, uUseOwnerGuid, bWasGlobal)

Removes a widget from the control focus queue and updates the control mode accordingly.



### GetCurrentControlHolder(uOwnerGuid)

Returns the current widget holding control for a given owner GUID or "global".



### InformControlOwnerChanged(oWidget, uPreviousOwner)

Placeholder function that currently does nothing.



### IsPlayerLocal(uPlayerGuid)

Checks if a player is local. Returns true if the player GUID is nil, not in multiplayer, or if the viewport ID is 1.



### IsViewportLocal(uViewportId)

Checks if a viewport is local. Returns true if the viewport ID is nil, not in multiplayer, or if the viewport ID is 1.



### SentEvent(tEvent)

Sends an event to the `EventManager`.



### ProcessEventImmediate(tEvent)

Processes an event immediately based on its type.



### AddWidget(WidgetToAdd)

Adds a widget to the `WidgetManager`.



### AddWidgetWithChildren(WidgetToAdd)

Adds a widget and all its children to the `WidgetManager`.



### RemoveWidget(WidgetToRemove)

Removes a widget from the `WidgetManager`.



### RemoveWidgetWithChildren(WidgetToRemove)

Removes a widget and all its children from the `WidgetManager`.



### PushAllTextToFront()

Pushes all text widgets to the front.



### PushWidgetToFront(oWidget)

Pushes a specific widget to the front.



### PushWidgetToBack(oWidget)

Pushes a specific widget to the back.



### GetWidgetByName(sWidgetName)

Retrieves a widget by its name.



### GetAllWidgetsByName(sWidgetName)

Retrieves all widgets with a given name.



### GetWidgetByNameAndOwner(sWidgetName, uOwnerGuid)

Retrieves a widget by its name and owner GUID.



### _DestroyWidget(oWidget)

Deletes a widget.



### DeleteTransientWidgets(uPlayer)

Deletes all transient widgets owned by a specific player.



### Widget:new(NewWidget)

Creates a new widget instance.



### Widget:delete()

Deletes a widget instance.



### Widget:DeleteWithChildren()

Deletes a widget instance and all its children.



### Widget:SetName(Name)

Sets the name of a widget.



### Widget:GetName()

Retrieves the name of a widget.



### Widget:SetVisible(isVisible)

Sets the visibility of a widget.



### Widget:GetVisible()

Retrieves the visibility status of the widget by calling `_GuiInternal.GetWidgetVisible` with the widget's unique ID.



### Widget:SetSleeping(bSleeping)

Sets the sleeping state of the widget. If `_GuiInternal.SetWidgetSleep` is available, it calls this function with the widget's unique ID and the new sleeping state (`bSleeping`).



### Widget:GetSleeping()

Retrieves the current sleeping state of the widget by calling `_GuiInternal.GetWidgetSleep` with the widget's unique ID.



### Widget:SetUseImmortalEvents(bUse)

Sets whether the widget should use immortal events. If `bUse` differs from the current setting, it updates the flag and toggles the widget's enabled state to reapply event handlers if necessary. It also recursively sets this property for all child widgets.



### Widget:SetTransient(bTransient)

Sets the transient state of the widget. If `bTransient` is false, it clears the transient flag; otherwise, it sets it to the provided value.



### Widget:SetEventHandler(EventType, EventHandlerFunction)

Sets an event handler for a specific event type. It handles different types of events such as "GuiInitialization", "GuiUpdate", and others. For persistent events, it registers or unregisters the event handler based on whether `EventHandlerFunction` is provided. It also checks if the widget requires an owner for certain events.



### Widget:_InitAnimationData()

Initializes the animation data for the widget, setting up tables to manage animation points and their completion status.



### Widget:AddAnimationPoint(tPoint)

Adds a new animation point to the widget's animation sequence. It validates and normalizes the input parameters before inserting them into the `AnimationPoints` table.



### Widget:SetAnimationPoint(nPointNumber, tPoint)

Sets or updates an existing animation point in the widget's animation sequence. It validates and normalizes the input parameters before updating the specified point.



### Widget:AnimateToPoint(nPointNumber, nTime, bImmediate, fComplete, tUserData, nElapsedTime)

Animates the widget to a specific animation point. It handles immediate animations, sets up completion callbacks, and manages the animation queue.



### Widget:IsAnimating()

Checks if the widget is currently animating by examining the `AnimationData` table.



### _HandleAnimationComplete(self)

Handles the completion of an animation by calling the completion callback, managing the animation queue, and initiating the next animation point.



### Widget:SetEnabled(bEnabled)

Enables or disables the widget. It manages event handlers based on the enabled state, ensuring that only necessary events are registered.



### Widget:SetLocation(x, y, x1, y1)

Sets the location of the widget using `_GuiInternal.SetWidgetLocation`. It allows partial updates by providing optional parameters.



### Widget:SetHighlightable(setting)

Sets the highlightable property of the widget using `_GuiInternal.SetWidgetHighlightable`.



### Widget:SetCoordinates(x, y, x1, y1)

Updates the coordinates of the widget. It retrieves the current location if not all new coordinates are provided and then sets them.



### Widget:GetLocation()

Retrieves the current location of the widget by calling `_GuiInternal.GetWidgetLocation`.



### Widget:SetCorrectedLocation(nX1, nY1, nX2, nY2)

Sets the corrected location of the widget using `_GuiInternal.SetWidgetCorrectedLocation` if available.



### Widget:GetCorrectedLocation()

Retrieves the corrected location of the widget by calling `_GuiInternal.GetWidgetCorrectedLocation` if available.



### Widget:SetColor(r, g, b, a, bSuppressPropogation)

Sets the color of the widget using `_GuiInternal.SetWidgetColor`. It allows suppression of propagation to child widgets.



### Widget:GetColor()

Retrieves the current color of the widget by calling `_GuiInternal.GetWidgetColor`.



### Widget:SetTranslucency(level, bSuppressPropogation)

Sets the translucency level of the widget by setting the alpha channel using `_GuiInternal.SetWidgetColor`. It allows suppression of propagation to child widgets.



### Widget:GetTranslucency()

Retrieves the current translucency level of the widget by getting the alpha channel from `_GuiInternal.GetWidgetColor`.



### Widget:SetAnchoring(sHorizontalAnchor, sVerticalAnchor)

Sets the anchoring properties of the widget. It converts string inputs ("left", "right", "center" for horizontal and "top", "bottom", "center" for vertical) to numeric values before setting them using `_GuiInternal.SetWidgetAnchoring`.



### Widget:SetFullscreen(sType)

Sets the fullscreen property of the widget using `_GuiInternal.SetWidgetFullscreen`.



### Widget:GetFullscreen()

Retrieves the fullscreen state of the widget. Currently, this function returns `nil`.



### Widget:Duplicate(oParent)

Duplicates the widget and its properties. The new widget will have the same location, color, owner, visibility, basic data, custom data, event handlers, and children as the original widget. The `uId` is not copied to ensure a unique identifier for the new widget.



### Widget:SetOwner(uGuid)

Sets the owner of the widget. If the owner GUID changes, it updates the internal tracking in `WidgetManager.WidgetNamePlayerIndex`. It also refreshes the widget's viewport if enabled.



### Widget:GetOwner()

Returns the GUID of the current owner of the widget.



### Widget:GetType()

Returns the type of the widget (e.g., "text", "image").



### Widget:GetChildren()

Retrieves a list of child widgets associated with this widget. It uses internal engine functions to get the list of child IDs and maps them to their respective widget objects.



### Widget:AddChild(oChild)

Adds a child widget to this widget using the engine's internal function.



### Widget:SetChild(nIndex, oChild)

Sets a child widget at a specific index using the engine's internal function.



### Widget:RemoveChild(oChild)

Removes a child widget from this widget using the engine's internal function.



### Widget:RemoveAllChildren()

Removes all child widgets from this widget using the engine's internal function.



### Widget:SetIgnoresPause(bIgnore)

Sets whether the widget ignores pause state changes. It uses the engine's internal function to update this setting.



### Widget:GetIgnoresPause()

Returns whether the widget ignores pause state changes.



### TextWidget:new(NewWidget, uId)

Creates a new text widget with default properties such as type, enabled status, unique ID, text content, font, and transient flag. It sets up basic data, custom data, event handlers, and registers the widget in `WidgetIdIndex`.



### TextWidget:SetText(t)

Sets the text content of the widget. If the text is empty, it defaults to a space character.



### TextWidget:SetLocation(x, y, x1, y1)

Sets the location of the widget using the engine's internal function.



### TextWidget:OffsetLocation(x, y)

Offsets the current location of the widget by the specified amount. It handles wrapping if enabled.



### TextWidget:SetFont(font)

Sets the font of the text widget using the engine's internal function.



### TextWidget:GetFont()

Returns the current font of the text widget.



### TextWidget:SetJustification(sJustification)

Sets the justification of the text widget using the engine's internal function.



### TextWidget:GetJustification()

Returns the current justification of the text widget.



### TextWidget:Wrap()

Enables text wrapping for the widget and updates the engine's internal state.



### TextWidget:SetWrapping(bWrap)

Sets whether text wrapping is enabled for the widget and updates the engine's internal state.



### TextWidget:GetText()

Retrieves the current text content of the widget using the engine's internal function.



### TextWidget:GetWidth()

Returns the width of the text widget. If `GetTextWidth` is available, it uses that; otherwise, it calculates the width based on location coordinates.



### TextWidget:GetHeight()

Returns the height of the text widget.



### TextWidget:SetScale(nScale)

Sets the scale of the text widget using the engine's internal function.



### TextWidget:GetScale()

Retrieves the current scale of the text widget.



### TextWidget:SplitIntoLines()

Splits the text into multiple lines if supported by the engine. It creates new `TextWidget` instances for each line and sets their properties accordingly.



### TextWidget:PerformTextAnimation(sType)

Performs a text animation of the specified type using the engine's internal function.



### TextWidget:HaltTextAnimation()

Halts any ongoing text animation using the engine's internal function.



### ImageWidget:new(NewWidget)

Creates a new image widget with default properties such as type, enabled status, unique ID, and transient flag. It sets up basic data, custom data, event handlers, and registers the widget in `WidgetIdIndex`.



### ImageWidget:OffsetLocation(x, y)

Offsets the current location of the image widget by the specified amount.



### ImageWidget:Move(x, y)

Moves the image widget to the specified coordinates.



### ImageWidget:SetTextureCoordinates(nU1, nV1, nU2, nV2)

Sets the texture coordinates of the image widget using the engine's internal function.



### ImageWidget:GetTextureCoordinates()

Retrieves the current texture coordinates of the image widget.



### ImageWidget:SetTileSize(nTileWidth, nTileHeight)

Sets the tiling size of the image widget if supported by the engine.



### ImageWidget:SetTexture(TextureName)

Sets the texture of the image widget using the engine's internal function.



### ImageWidget:GetTexture()

Retrieves the current texture name of the image widget.



### ImageWidget:SetRotation(nDegrees, nAnchorX, nAnchorY)

Sets the rotation of the image widget using the engine's internal function.



### ImageWidget:GetRotation()

Retrieves the current rotation angle of the image widget.



### ImageWidget:SetClockAnimation(nElapsedTime, nTotalTime, bFill, bClockwise)

Sets a clock animation for the image widget using the engine's internal function.



### ImageWidget:SetClockAnimationCallback(fCallback, tData)

Sets a callback function for the clock animation using the engine's internal function.



### ImageWidget:GetClockElapsedTime()

Retrieves the elapsed time of the clock animation.



### ImageWidget:SetPieSliceRender(fStartAngle, fEndAngle)

Renders a pie slice of the image widget if supported by the engine.



### ImageWidget:DisablePieSliceRender()

Disables pie slice rendering for the image widget if supported by the engine.



### FlashWidget:new(NewWidget)

Creates a new flash widget with default properties such as type, enabled status, unique ID, and transient flag. It sets up basic data, custom data, event handlers, and registers the widget in `WidgetIdIndex`. If the engine does not support flash widgets, it defaults to creating a standard widget.



### FlashWidget:SetSwfFile(sSwfName, fCallback, tData)

Sets the SWF file for the flash widget using the engine's internal function and sets up a callback if provided.



### FlashWidget:GetSwfFile()

Retrieves the current SWF file name of the flash widget.



### FlashWidget:SetPlaySpeed(nSpeed)

Sets the play speed of the flash widget using the engine's internal function.



### FlashWidget:GetPlaySpeed()

Retrieves the current play speed of the flash widget.



### FlashWidget:Pause()

Pauses the flash animation using the engine's internal function.



### FlashWidget:Play()

Plays the flash animation using the engine's internal function.



### FlashWidget:Restart()

Restarts the flash animation using the engine's internal function.



### FlashWidget:SetFlashEventHandler(sEvent, fCallback, tCallbackData)

Sets an event handler for the flash widget using the engine's internal function and wraps the callback to include additional data.



### FlashWidget:CallActionScriptCallback(sName, tArgs)

Calls an ActionScript callback in the flash widget with the specified name and arguments.



### FlashWidget:SetTesselationAllowed(bAllow)

Sets whether tessellation is allowed for the flash widget using the engine's internal function.



### _FlashCallback(oWidget, fFunction, tCallbackData, sParam)

A helper function that processes callbacks from the flash widget. It unpacks callback data and calls the provided function with the appropriate arguments.



### `_HandleInputForFlashWidget(oWidget, tEvent)`

Handles input events for Flash widgets. It iterates through the event table and sends corresponding input to the widget based on whether the key contains "ButtonPress" or "ButtonReleased".



### `FlashWidget:HandleLeftAnalogInput(nX, nY)`

Handles left analog stick input for a Flash widget. If both `nX` and `nY` are provided and `_GuiInternal.SendFlashLeftAnalogInput` is available, it sends the input to the widget.



### `FlashWidget:HandleRightAnalogInput(nX, nY)`

Handles right analog stick input for a Flash widget. If both `nX` and `nY` are provided and `_GuiInternal.SendFlashRightAnalogInput` is available, it sends the input to the widget.



### `SpriteWidget:new(NewWidget)`

Creates a new SpriteWidget instance. It initializes the widget with basic data such as type, enabled status, unique ID, texture name, and transient flag. It also sets up custom data and event handlers, and registers the widget in `WidgetIdIndex`.



### `SpriteWidget:SetTexture(sTexture)`

Sets the texture for the sprite widget using `_GuiInternal.SetSpriteTexture`.



### `SpriteWidget:SetTextureSize(nWidth, nHeight)`

Sets the texture size for the sprite widget using `_GuiInternal.SetSpriteTextureSize`.



### `SpriteWidget:SetFrameSize(nWidth, nHeight)`

Sets the frame size for the sprite widget using `_GuiInternal.SetSpriteFrameSize`.



### `SpriteWidget:SetFrame(nFrame)`

Sets the current frame for the sprite widget using `_GuiInternal.SetSpriteFrame`.



### `SpriteWidget:PlayAnimation(nStartFrame, nEndFrame, nTime, bLoop)`

Plays an animation for the sprite widget using `_GuiInternal.AnimateSprite`.



### `SpriteWidget:HaltAnimation()`

Halts any ongoing animation for the sprite widget using `_GuiInternal.HaltSpriteAnimation`.



### `MovieWidget:new(NewWidget)`

Creates a new MovieWidget instance. It initializes the widget with basic data such as type, enabled status, unique ID, and transient flag. If `_GuiInternal.CreateMovieWidget` is available, it creates the movie widget; otherwise, it falls back to creating a generic widget.



### `MovieWidget:SetMovie(sFileName)`

Sets the movie file for the movie widget using `_GuiInternal.SetMovieFile`.



### `MovieWidget:Play(bLoop)`

Plays the movie widget using `_GuiInternal.PlayMovie`.



### `MovieWidget:Stop()`

Stops the movie widget using `_GuiInternal.StopMovie`.



### `MovieWidget:Pause()`

Pauses the movie widget using `_GuiInternal.PauseMovie`.



### `MovieWidget:SetEndCallback(fCallback, tData)`

Sets an end callback for the movie widget using `_GuiInternal.SetMovieEndCallback`.



### `MovieWidget:GetCurrentFrame()`

Gets the current frame number of the movie widget using `_GuiInternal.GetMovieCurrentFrameNumber`. Returns -1 if not available.



### `MinimapWidget:SetOwner(uGuid)`

Sets the owner GUID for the minimap widget. It updates both the internal state and the engine's minimap owner using `_GuiInternal.SetMinimapOwner`.



### `MinimapWidget:SetUpMinimap(name, nXLoc, nYLoc, nRadius, texture, texWidth, texHeight, worldXMin, worldXMax, worldZMin, worldZMax, HorizAnchor, VertAnchor)`

Sets up the minimap widget with various parameters such as location, radius, texture, and anchors. It creates the minimap using `_GuiInternal.MinimapCreate` and registers it in `WidgetIdIndex`. It also sets event handlers and adds the widget to the widget manager.



### `MinimapWidget:SetLocation(x, y)`

Sets the location of the minimap widget (currently a no-op).



### `MinimapWidget:SetVisible(bVisible)`

Sets the visibility of the minimap widget using `_GuiInternal.SetWidgetVisible`. It also updates the visibility of any child widgets.



### `MinimapWidget:SetPlayerLocation(x, y, z)`

Sets the player location on the minimap using `_GuiInternal.MinimapSetPlayerLocation`.



### `MinimapWidget:SetFocusLocation(x, y, z)`

Sets the focus location on the minimap using `_GuiInternal.MinimapSetFocusLocation`.



### `MinimapWidget:SetRotation(nRotation)`

Sets the rotation of the minimap using `_GuiInternal.MinimapSetRotation`.



### `MinimapWidget:SetRange(nRange)`

Sets the range of the minimap using `_GuiInternal.MinimapSetRange`.



### `MinimapWidget:SetBorder(sBorderTexture, nTextureWidth, nTextureHeight)`

Sets the border texture for the minimap using `_GuiInternal.SetMinimapBorder`.



### `MinimapWidget:AddObjective(name, x, y, z, r, g, b, width, height, texture, uGuid, bSticky, bRotate, bOriented, nSortOrder)`

Adds an objective to the minimap using `_GuiInternal.MinimapAddObjective`.



### `MinimapWidget:AnimateObjectiveSize(name, duration, minWidth, minHeight, maxWidth, maxHeight, bOneWay, speedWidth, speedHeight)`

Animates the size of an objective on the minimap using `_GuiInternal.MinimapAnimateObjectiveSize`.



### `MinimapWidget:AnimateObjectiveAlpha(name, duration, minAlpha, maxAlpha, bOneWay, speed)`

Animates the alpha (transparency) of an objective on the minimap using `_GuiInternal.MinimapAnimateObjectiveAlpha`.



### `MinimapWidget:AnimateObjectiveSonar(name, duration, sTexture, nTotalBlips, nVisibleBlips, nMinWidth, nMaxWidth, nBlipDelay, nAlphaAtMin, nAlphaAtMax, nGrowSpeed, r, g, b)`

Animates a sonar effect for an objective on the minimap using `_GuiInternal.MinimapAnimateObjectiveSonar`.



### `MinimapWidget:UnanimateObjective(name, type)`

Stops any animations for an objective on the minimap using `_GuiInternal.MinimapUnanimateObjective`.



### `MinimapWidget:AddObjectiveWithGuid(sName, uGuid, nX, nY, nZ, nR, nG, nB, nWidth, nHeight, sTexture, bSticky, bRotate, bOriented, nSortOrder)`

Adds an objective to the minimap with a GUID using `_GuiInternal.MinimapAddObjective`.



### `MinimapWidget:UpdateObjective(name, x, y, z, r, g, b, width, height, texture, bSticky, bRotate, bOriented, nSortOrder)`

Updates an existing objective on the minimap by adding a new one with the same name.



### `MinimapWidget:DeleteObjective(name)`

Deletes an objective from the minimap using `_GuiInternal.MinimapRemoveObjective`.



### `MinimapWidget:Delete()`

Deletes the minimap widget and removes it from `WidgetIdIndex` using `_GuiInternal.MinimapDelete`.



### `MinimapDataUpdateHandler(Minimap, FocusX, FocusY, FocusZ, Rotation)`

Handles data updates for the minimap. It updates the minimap's position and rotation, adjusts the range based on player velocity, and corrects widget resolution.



### `MinimapHandleE3HudModeEvent(oMinimap, tEvent)`

Handles E3 HUD mode events by setting the visibility of the minimap based on whether the event is "on" or "off".



### `LoadGUIFile(sFile, fFinishedLoadingCallback, uOwnerGuid)`

Loads a GUI file dynamically. It sets up a callback that calls `GUIFileLoadedCallback` and an optional finished loading callback.



### `RemoveAllWidgetsInLayout(Module)`

Removes all widgets in a given module by iterating through the `AddedWidgetList` and calling `RemoveWidgetWithChildren`.



### `ReAddAllWidgets(Module)`

Re-adds all widgets in a given module by iterating through the `AddedWidgetList` and calling `AddWidgetWithChildren`.



### `HideAllWidgets(Module)`

Hides all widgets in a given module by setting their visibility to false.



### `ShowAllWidgets(Module)`

Shows all widgets in a given module by setting their visibility to true.



### `SetAllWidgetsSleep(Module, bSleep)`

Sets the sleeping state for all widgets in a given module.



### `PushAllTextToFront(Module)`

Pushes all text widgets in a given module to the front.



### `AssignLayoutToPlayer(Module, uGuid)`

Assigns a layout to a player by setting the owner GUID for each widget in the module's `AddedWidgetList`.



### `DuplicateLayout(Module)`

Duplicates a GUI layout by creating a new module with a copy of the original's `LocalWidgetList`. It calls `GUIFileLoadedCallback` to initialize the new module.



### `GUIFileLoadedCallback(ModuleName, uOwnerGuid)`

Handles the loading of a GUI file. It initializes the `AddedWidgetList`, loads and adds widgets from the `LocalWidgetList`, triggers any initialization events, and corrects widget resolution for each widget.



### LoadAndAddWidgetFromLayoutFileData(WidgetData, WidgetList, ParentWidget, uOwnerGuid)

This function creates and adds a new widget to the GUI based on the provided layout data. It handles different types of widgets such as images, text, minimaps, flash, and sprite widgets. The function sets various properties for each widget, including texture, rotation, location, visibility, color, and event handlers.



### UnloadGUIFile(vFile)

This function unloads a GUI file by calling `dynamic_remove` with the provided file.



### ChangeScreenResolution(nWidth, nHeight, nNewPixelWidth, nNewPixelHeight, nX, nY)

This function changes the screen resolution and updates the screen dimensions and scale factor accordingly. It also marks all widgets as needing correction for the new resolution.



### ChangeScreenPixelSize(nWidth, nHeight)

This function changes the pixel size of the screen and updates the pixel width and height accordingly.



### ValidateParameter(Parameter, sType, DefaultValue)

This function validates a parameter against a specified type. If the parameter matches the type, it returns the parameter; otherwise, it returns a default value.



### Run()

This function processes events using `EventManager.ProcessEvents`.



### GetEventListTable()

This function returns the event list table from `EventManager.EventList`.



### SetDialogBoxMode(uPlayerGuid, bActivate)

This function sets the dialog box mode for a player. It checks if the provided parameters are of the correct types and then calls `_SetDialogBoxMode` with the player GUID and activation status.



### SetSupportMenuMode(uPlayerGuid, bActivate)

This function sets the support menu mode for a player. It checks if the provided parameters are of the correct types and then calls `_SetSupportMenuMode` with the player GUID and activation status.



### Init()

This function initializes various widget types (TextWidget, ImageWidget, FlashWidget, MinimapWidget, SpriteWidget, MovieWidget) and sets their transient properties to `nil`. It also adjusts joystick button mappings if necessary.



### ReInit()

This function is intended for reinitializing the GUI but currently does nothing.



### DeInit()

This function is intended for deinitializing the GUI but currently does nothing.



## Events



- **Event.ObjectHibernation**: Listens for this event to wake up and initialize world object instances.

- **Event.ObjectWinched**: Listens for this event to handle winch-related state changes.

- **Event.TimerRelative**: Listens for timer events to trigger timed actions or animations.

- **Event.PlayerJoined / Event.PlayerLeft**: Listens for player session changes to update GUI states accordingly.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `Init()` is called before using any GUI-related functions to properly initialize widget types and settings.

   - When adding or removing widgets, ensure that the parent-child relationships are maintained to avoid visual glitches or logical errors.



2. **Pitfalls**:

   - Be cautious when modifying screen resolution or pixel size as it can affect the positioning and scaling of all widgets on the screen.

   - Directly manipulating widget properties (e.g., location, color) without using the provided setter functions may lead to unexpected behavior or inconsistencies.



3. **Tunables**:

   - Adjusting joystick button mappings in `Init()` allows for customizing input handling based on different controller configurations.

   - The transient state of widgets can be toggled to control their persistence across game sessions or player actions.



4. **Decompiler artifacts**:

   - Unused local variables or redundant operator groupings are decompiler artifacts and should not be interpreted as intentional logic in the code.