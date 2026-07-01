---
title: MrxGuiHudObjectiveTray
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
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
- Listens for custom event `_HandleInitializationEvent` to initialize the HUD objective tray.

## Notes for modders
- Ensure that the `_HandleInitializationEvent` is called appropriately during the initialization of the HUD objective tray.
- Use `SetSlotToWidget`, `SetSlotToText`, and `SetSlotToImage` to manage the contents of the tray slots.
- Be aware that clearing a slot may affect the layout of subsequent slots, as their positions are adjusted accordingly.