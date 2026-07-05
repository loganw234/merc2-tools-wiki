---
title: MrxGuiBinoculars
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, binoculars]
verified: true
verified_note: corrected Events section — handler names aren't Event.* constants, no Event.Create in this file; added the one real Event.Post("InFocus") call; flagged HandleFocusUpdate's Event.Post
---

# MrxGuiBinoculars

*Module: mrxguibinoculars.lua*

## Overview
The `MrxGuiBinoculars` module manages the behavior of the binoculars GUI in the game. It handles events related to entering and exiting the binoculars scope, updates various UI elements such as focus text, faction texture, and zoom level, and ensures proper HUD state management during these interactions.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGuiManager`, `MrxGui`, `MrxSound`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages the binoculars GUI based on events and player interactions.

## Functions
### `HandleBinocularsEnter(oWidget, tEvent)`
Called when a player enters the binoculars scope. It checks if the event's player GUID matches the widget's owner, plays the enter scope sound, sets the widget visible, toggles the HUD state if necessary, and animates the UI elements to their respective positions.

### `HandleBinocularsExit(oWidget, tEvent)`
Called when a player exits the binoculars scope. It disables all child widgets, animates the UI elements back to their original positions, restores the HUD state if toggled earlier, and plays the exit scope sound.

### `_FinishEnter(oWidget)`
A helper function that enables all child widgets, sets their locations, and makes them visible after the initial animation completes when entering the binoculars scope.

### `_FinishExit(oWidget)`
A helper function that hides the widget, restores the HUD state if toggled earlier, and resets various custom data fields after the exit animation completes.

### `HandleInitialization(oWidget)`
Initializes the binoculars GUI by setting it invisible, disabling all child widgets, storing references to key UI elements, and configuring animation points for zooming effects.

### `HandleHeadingUpdate(oWidget, tEvent)`
Updates the position of a pointer on the binoculars GUI based on the player's camera heading. It ensures the pointer stays within the bounds of the widget.

### `HandleZoomUpdate(oWidget, tEvent)`
Updates the position of a pointer on the binoculars GUI based on the zoom level. It ensures the pointer stays within the bounds of the widget.

### `HandleFactionUpdate(oWidget, tEvent)`
Updates the faction texture and translucency of the binoculars GUI based on the event's faction texture information.

### `HandleFocusUpdate(oWidget, tEvent)`
Updates the focus text and description in the binoculars GUI based on the event's focus name and GUID. If `tEvent.uFocusGuid` is set, also fires `Event.Post("InFocus", {uTarget = tEvent.uFocusGuid, uViewer = oWidget:GetOwner(), bSniper = false})` and populates the description via `MrxGui.GetObjectiveDescription(tEvent.uFocusGuid)`.

### `HandleVertScrollUpdate(oWidget, tEvent)`
Updates the vertical scroll position of a pointer on the binoculars GUI based on the player's pitch angle. It ensures the pointer stays within the bounds of the widget.

## Events
This file contains **no `Event.Create` calls** and none of its `Handle*` function names appear as
`Event.*` engine constants anywhere in the decompiled corpus. They are plain functions, almost
certainly wired up as widget-level `SetEventHandler`/`EventHandlers` callbacks from an external GUI
layout resource (`mrxguimanager.lua:10` loads `"MrxGuiBinocularsLayout"` via `MrxGui.LoadGuiFile`, but
that layout isn't among the decompiled `.lua` files, so the exact handler-name mapping can't be
confirmed from source — see `mrxguiattractlayout.lua` for what that mapping table looks like on a
layout file that *is* present). Treat the "Listens for" language below as "this function's name
strongly suggests it's bound to a same-named widget event," not a confirmed `Event.*` constant:
- `HandleBinocularsEnter`, `HandleBinocularsExit` — presumed bound to scope enter/exit.
- `HandleInitialization` — presumed bound to widget init.
- `HandleHeadingUpdate`, `HandleZoomUpdate`, `HandleFactionUpdate`, `HandleFocusUpdate`,
  `HandleVertScrollUpdate` — presumed bound to per-frame/per-change HUD update callbacks.

The one **confirmed** event-system interaction in this file is outbound: `HandleFocusUpdate` calls
`Event.Post("InFocus", {uTarget = tEvent.uFocusGuid, uViewer = oWidget:GetOwner(), bSniper = false})`
when a focus target is set.

## Notes for modders
- The exact widget-event names these handlers are bound to live in the (non-decompiled) `MrxGuiBinocularsLayout` GUI resource, not in this `.lua` file — don't assume the names in this doc are literal `Event.*` constants.
- Customize the appearance and behavior of the binoculars GUI by modifying the animation points, pointer positions, and other custom data fields as needed.
- Be aware that toggling the HUD state during binoculars use may affect the player's experience, so test thoroughly in multiplayer scenarios.
- `HandleFocusUpdate` fires a real `Event.Post("InFocus", ...)` — anything hooking into focus-target changes elsewhere in the codebase should listen for that.