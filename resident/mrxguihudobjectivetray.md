---
title: MrxGuiHudObjectiveTray
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: confirmed zero Event.* and zero SetEventHandler calls in file; corrected Events section — _HandleInitializationEvent's own name was miscast as "a custom event it listens for" rather than a likely externally-wired GuiInitialization-style handler; flagged dead-code nil-check in SetSlotToWidget (lines 17-20)
---

# MrxGuiHudObjectiveTray

*Module: mrxguihudobjectivetray.lua*

## Overview
The `MrxGuiHudObjectiveTray` module is responsible for managing a 3-slot vertical tray on the HUD that can display text or image objective entries. It provides functions to set slots with widgets, clear slots, and check if slots are occupied.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxGuiManager`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but provides functions to manipulate HUD objective trays.

## Functions
### `SetSlotToWidget(oTray, nSlot, oWidget)`
Sets the specified slot in the tray with the given widget. Validates that the slot number is within range (1-3) and the widget is a table. Clears any existing widget in the slot, sets the widget's location, and adds it to the slot.

**Dead code**: lines 17-20 read `nX1, nY1, nX2, nY2 = oWidget:GetLocation()`, then default `nX2`/`nY2` with `nX2 = nX2 or nX1 + oTray.CustomData.nDefaultWidth` (and similarly for `nY2`), then check `if not nX2 or not nY2 then oWidget:SetLocation(nX1, nY1, nX2, nY2) end`. Because the defaulting on the two lines immediately above always leaves `nX2`/`nY2` as truthy numbers, the `not nX2 or not nY2` condition can never be true — that `SetLocation` call never executes. Likely an ordering bug (the nil-check was probably meant to run before the `or`-defaulting).

### `SetSlotToText(oTray, nSlot, sText)`
Sets the specified slot in the tray with a text widget displaying the given text. Validates that the text is a string. If the slot already contains a text widget, updates its text; otherwise, creates a new text widget and adds it to the slot.

### `SetSlotToImage(oTray, nSlot, sTexture, nTextureWidth, nTextureHeight)`
Sets the specified slot in the tray with an image widget displaying the given texture. Validates that the texture is a string. If the slot already contains an image widget, updates its texture; otherwise, creates a new image widget and adds it to the slot.

### `ClearSlot(oTray, nSlot)`
Clears the specified slot in the tray by removing any existing widget and adjusting the positions of subsequent slots if necessary.

### `IsSlotOccupied(oTray, nSlot)`
Checks if the specified slot in the tray is occupied by a widget. Returns true if the slot contains a widget; otherwise, returns false.

### `_HandleInitializationEvent(oWidget, tEvent)`
Handles the initialization event for the HUD objective tray. Sets up the tray with 3 slots, each spaced and sized according to default values (`nSlots=3`, spacing `5`, default height `16`). Assigns functions to the tray widget for managing its slots.

## Events
No `Event.*`/`Event.Create(...)` engine-event references and no `SetEventHandler` calls appear anywhere in this file — confirmed by grep. `_HandleInitializationEvent(oWidget, tEvent)` is a function this module *defines*, not an event it subscribes to; nothing in this file registers it against a handler key. By naming convention (and by analogy with `mrxguicinematiclayout.lua`'s `GuiInitialization`-keyed handlers), it is presumably wired externally as the tray widget's `GuiInitialization` handler in a layout file outside this module — no call site found in the decompiled `resident/` corpus. Once initialized, the tray's public API (`SetSlotToWidget`, `SetSlotToText`, `SetSlotToImage`, `ClearSlot`, `IsSlotOccupied`) is called directly by other modules (e.g. `mrxguihudfactionbuffer.lua` looks up the "Objective Tray" widget by name and calls `IsSlotOccupied`/`SetVisible` on it directly), not through events.

## Notes for modders
- Ensure that the `_HandleInitializationEvent` is called appropriately during the initialization of the HUD objective tray.
- Use `SetSlotToWidget`, `SetSlotToText`, and `SetSlotToImage` to manage the contents of the tray slots.
- Be aware that clearing a slot may affect the layout of subsequent slots, as their positions are adjusted accordingly.