---
title: MrxGuiHudRadar
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, radar]
verified: true
verified_note: 'deeper pass: re-confirmed all functions + zero Event.*; surfaced the Scaleform minimap.gfx movie + AddZone/RemoveZone ActionScript callbacks, the _tIcons faction-icon table, marker constants (_sTargetName/_sGPSName, MiniMap_Icon_GPS_Marker), region offsets (35/40) and default color (64,64,160 α128), the AddObjective signature, and Pg.GetLineRegionPoints; re-verified the dead bAnimation param'
---

# MrxGuiHudRadar

*Module: mrxguihudradar.lua*

## Overview
The `MrxGuiHudRadar` module is responsible for managing the minimap and its various components such as faction-zone region overlays, GPS markers, target markers, and map-label flashes. It interacts with the Scaleform GUI to update and display these elements dynamically.

## Inheritance
- Inherits from: `none`
- Imports (via [`import()`](../glossary#importname)): `MrxGui`, `MrxGuiBase`, `MrxGuiManager`, `MrxTutorialManager` — see [MrxGui](mrxgui), [MrxGuiBase](mrxguibase), [MrxGuiManager](mrxguimanager), [MrxTutorialManager](mrxtutorialmanager). Region polygons come from [Pg](../namespaces/pg) (`Pg.GetLineRegionPoints`); the minimap itself is a Scaleform movie driven via `CallActionScriptCallback`.

## Instance pattern
**Stateless module + per-widget `CustomData`.** No module-level per-instance registry. `_Initialize(oMinimap)` copies `AddRegion`/`RemoveRegion` onto the minimap widget and stores its region bookkeeping in `oMinimap.CustomData` (`tRegions` by numeric id, `tRegionGuids` mapping object GUID → id, `bHaveFlash` load flag). Map-label state lives on the label widget's `CustomData`. The one true module-global table is `_tIcons` (built by `Init()`).

### Scaleform movie & constants (HIGH-VALUE knobs)
- **Movie**: `_Initialize` loads `minimap.gfx` via `SetSwfFile("minimap.gfx", _FinishInitialization, ...)`. The map-label text uses a child `FlashWidget` named `maplabeltext`.
- **ActionScript callbacks** into the movie: `"AddZone"` (per-vertex, plus a close/commit call), `"RemoveZone"` — these draw/erase the faction-zone region overlays.
- **Region defaults** (in `AddRegionToMinimap`): color falls back to RGB `(64, 64, 160)` and alpha `128` (alpha is then rescaled to a 0-100 percentage for Scaleform). Color is packed to a `"0xRRGGBB"` hex string. Region vertices are offset by `nXOffset = 35`, `nYOffset = 40` before being sent to the movie.
- **Marker names**: `_sTargetName = "Target marker"` (suffixed with `tData.number`), `_sGPSName = "GPS Beacon Marker"`. The GPS marker uses texture `MiniMap_Icon_GPS_Marker` at size `10.666667`, priority `4`; target markers use the caller's `tData.texture` at size `6`, priority `5` (via `oMap:AddObjective(sName, x, y, z, r, g, b, w, h, sTexture, uGuid, bShow, ?, ?, nPriority)`).
- **Faction icon table** (`_tIcons`, set in `Init()`): `All → HUD_faction_AN`, `Chi → HUD_faction_CH`, `Civ → HUD_faction_CV`, `Gur → HUD_faction_GR`, `Oil → HUD_faction_OC`, `Pir → HUD_faction_PR`, `Vz → HUD_faction_VZ`. Used by `_HandleTrespassIconEvent` to show the trespassed-faction badge.
- **Trespass label**: `_HandleMapLabelTrespassEvent` shows `"[red][Generic.Trespassing]"` (indefinite, `nDisplayTime = -1`) and kicks the `"Trespass"` tutorial via `MrxTutorialManager.StartTutorial`.
- **Map-label timing**: fades take `0.4`s; default display time is `4`s when the caller passes none (`nDisplayTime or 4`); a negative time holds indefinitely. Label flash geometry scale is `0.6666667`.

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
- **Recolor faction zones**: `AddRegionToMinimap(oMinimap, uGuid, nRed, nGreen, nBlue, nAlpha, bInvert)` draws a colored region for the world region identified by `uGuid`. Pass RGB 0-255 and alpha 0-255; omit any and it defaults to `(64,64,160)` α`128`. `bInvert` fills the *outside* of the region instead. Regions are queued if the movie hasn't loaded yet (`bHaveFlash`) and drawn on load.
- **Swap faction badges**: edit the `_tIcons` texture names in `Init()` to change the trespass/faction icons (e.g. `HUD_faction_PR` for pirates).
- **Move the region overlay**: `nXOffset = 35` / `nYOffset = 40` in `_DisplayMinimapRegion` shift every zone vertex — adjust if your minimap art has different padding.
- **Marker priorities**: target markers draw at priority `5`, GPS at `4` in the `AddObjective` call — higher-priority markers render on top. Change the trailing numeric arg to reorder.
- **Region GUID cleanup caveat**: `RemoveRegionFromMinimap` clears `tRegionGuids[nId]` (indexing by the numeric id) rather than `tRegionGuids[uGuid]` — so the `uGuid → id` entry is not actually removed, and the `tRegions[nId]` polygon data is left in place. Re-adding the same `uGuid` still works (the initial lookup finds the stale id and calls `RemoveRegion` first), but stale bookkeeping accumulates. Worth knowing if you churn many regions.

{: .warning }
> **Confirmed dead code in `ShowMapLabel`.** Line 160 (`bAnimation = false`) unconditionally overwrites the `bAnimation` parameter before it's read, so the `if bAnimation then ...` branch (blank-text + reveal-on-flash-load) can never run — only the fade-out/fade-in/timer `else` path executes, whatever the caller passes.