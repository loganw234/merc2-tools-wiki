---
title: MrxGuiHudRadar
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, radar]
verified: true
verified_note: confirmed zero Event.* calls (all wiring is widget-level SetEventHandler); corrected Events section to list all 4 confirmed handler-key registrations and flag trespass/icon functions with no SetEventHandler call site in this file; flagged dead-code bAnimation param in ShowMapLabel (line 160 overwrites it to false before use)
---

# MrxGuiHudRadar

*Module: mrxguihudradar.lua*

## Overview
The `MrxGuiHudRadar` module is responsible for managing the minimap and its various components such as faction-zone region overlays, GPS markers, target markers, and map-label flashes. It interacts with the Scaleform GUI to update and display these elements dynamically.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui`, `MrxGuiBase`, `MrxGuiManager`, `MrxTutorialManager`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but rather manages global minimap elements.

## Functions
### `_Clamp(n, nMin, nMax)`
A helper function to clamp a number `n` between `nMin` and `nMax`. Returns the clamped value or `nil` if `n` is not a number.

### `AddRegionToMinimap(oMinimap, uGuid, nRed, nGreen, nBlue, nAlpha, bInvert)`
Adds a region to the minimap with the specified color and alpha. If the region already exists, it removes it before adding it again. The function ensures that the color values are within valid ranges (0-255) and sets default values if none are provided.

### `RemoveRegionFromMinimap(oMinimap, uGuid)`
Removes a region from the minimap based on its GUID (`uGuid`). It also calls an ActionScript callback to remove the zone from the Scaleform GUI.

### `_Initialize(oMinimap)`
Initializes the minimap by setting up event handlers for target and GPS markers. It loads the `minimap.gfx` Scaleform file and prepares the custom data structures for managing regions.

### `_FinishInitialization(oMinimap)`
Completes the initialization of the minimap by enabling the flash feature and displaying any existing regions.

### `_DisplayMinimapRegion(oMinimap, nId)`
Displays a minimap region on the Scaleform GUI using ActionScript callbacks. It retrieves the region's points and color information from the custom data structures.

### `HandleSetTargetMarker(oMap, tData)`
Handles setting target markers on the minimap. If valid marker data is provided, it adds an objective with the specified properties; otherwise, it deletes the objective.

### `HandleSetGPSDest(oMap, tEvent)`
Handles setting GPS destinations by adding a GPS beacon marker to the minimap with default properties.

### `HandleClearGPSDest(oMap, tEvent)`
Handles clearing GPS destinations by deleting the GPS beacon marker from the minimap.

### `ShowMapLabel(oWidget, sString, nDisplayTime, bAnimation)`
Displays a map label on the widget. It handles animations and ensures that the label is visible for the specified duration.

**Confirmed dead code**: line 160, `bAnimation = false`, unconditionally overwrites the `bAnimation` parameter immediately on entry, before the `if bAnimation then ... else ... end` branch below it. The `then` branch (lines 161-166, which would show blank text and reveal the widget once its flash sub-widget finishes loading) can never execute regardless of what the caller passes — only the `else` branch (the fade-out/fade-in/timer path) ever runs.

### `_HandleTransition(oWidget, sString, nDisplayTime)`
Handles the transition of the map label by setting its visibility and starting the animation.

### `_HandleMapLabelInitialization(oWidget)`
Initializes the map label widget by setting up custom data structures and adding an animation point for fading in and out.

### `_CompleteTextFlashLoad(oFlash)`
Completes the loading of the text flash by marking it as loaded and setting up the close event handler.

### `_CompleteTextFlashAnimation(oFlash)`
Handles the completion of the text flash animation by hiding the parent widget.

### `_HandleMapLabelUpdateEvent(oWidget, nDeltaTime)`
Updates the map label's visibility based on the elapsed time. It animates the label to fade out when its display time is over.

### `_HandleMapLabelTrespassEvent(oWidget, tEvent)`
Handles trespass events by updating the map label to show a trespassing message if applicable.

### `_HandleTrespassIconInit(oIcon)`
Initializes the trespass icon by setting it to be invisible.

### `_HandleTrespassIconEvent(oIcon, tEvent)`
Handles trespass icon events by showing or hiding the icon based on the faction and trespass status.

### `Init()`
Initializes the module by setting up a table of faction icons used for displaying different factions on the minimap.

## Events
No `Event.*`/`Event.Create(...)` engine-event references appear in this file — confirmed by grep. All wiring uses widget-level `SetEventHandler` (string keys), registered in `_Initialize(oMinimap)`:
- `"SetTargetMarker"` → `HandleSetTargetMarker` — adds/removes a target-marker objective on the minimap.
- `"SetGPSDest"` → `HandleSetGPSDest` — adds a GPS beacon objective.
- `"ClearGPSDest"` → `HandleClearGPSDest` — removes the GPS beacon objective.

`ShowMapLabel` additionally sets `"GuiUpdate"` → `_HandleMapLabelUpdateEvent` dynamically (as the completion callback of an `AnimateToPoint` fade-in), and clears it (`SetEventHandler("GuiUpdate", nil)`) when the label starts fading out or updates.

`_HandleMapLabelTrespassEvent`, `_HandleTrespassIconInit`, and `_HandleTrespassIconEvent` are defined in this file but have **no `SetEventHandler` call site anywhere in it** — by naming convention they're presumably wired externally (layout file) similarly to other `Handle*Event`/`*Init` pairs seen elsewhere in this wiki (e.g. `mrxguicinematiclayout.md`'s `GuiInitialization` keys); no call site found in the decompiled `resident/` corpus for this page.

## Notes for modders
- Ensure that the minimap is properly initialized by calling `_Initialize` before using its functions.
- Use `AddRegionToMinimap` and `RemoveRegionFromMinimap` to manage faction-zone regions on the minimap.
- Customize target and GPS markers by providing appropriate data when calling `HandleSetTargetMarker` and `HandleSetGPSDest`.
- Be aware of the `_Clamp` function's behavior to ensure valid color values are used for map elements.
- The module uses Scaleform GUI callbacks extensively, so any modifications to these callbacks may affect the minimap's appearance and functionality.