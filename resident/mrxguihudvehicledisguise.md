---
title: MrxGuiHudVehicleDisguise
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- no OnActivate/Create/tInstance anywhere in source)
---

# MrxGuiHudVehicleDisguise

*Module: mrxguihudvehicledisguise.lua*

## Overview
The `MrxGuiHudVehicleDisguise` module is responsible for managing the vehicle disguise display on the HUD. It handles updating the faction icon, crossed-out icon, disguise level bar, and vehicle name identifier based on player interactions and game state.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui`

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is one shared HUD element, not something spawned per world object. Key fields:
- `nValue`: The current disguise level.
- `nBasePoint`, `nRedPoint`: Animation points for color transitions.
- `oIcon`, `oIconCross`: Widgets representing the faction icon and crossed-out icon, respectively.
- `oBarBack`, `oBarFront`: Widgets representing the background and front of the disguise bar.
- `oIdentifier`: Widget representing the vehicle name identifier.
- `nLastDisguiseLevel`, `nNewDisguiseLevel`: Track the current and new disguise levels.
- `bIsDisguised`, `bWasDisguised`: Flags indicating whether the vehicle is currently disguised.
- `bPulse`: Flag indicating if red pulsing animation is active.

## Functions
### `_Initialize(oWidget)`
Initializes the widget by setting up animation points, visibility management, and default values. It also sets up event handlers for disguise updates and vehicle name changes.

### `SetDisguiseLevel(oWidget, nValue, bDisguised)`
Sets the new disguise level and whether the vehicle is disguised. It clamps the disguise level between 0 and 100.

### `DisguiseUpdate(oWidget, nDeltaTime)`
Updates the visibility and appearance of the HUD elements based on the current disguise state and level. It handles transitions between different states (disguised, undisguised, gaining, losing) and updates the bar's progress.

### `SetVehicleName(oWidget, sName, uFaction, bDisguised)`
Sets the vehicle name and faction icon on the HUD. If no name is provided, it hides all elements. Otherwise, it sets up the necessary widgets and event handlers.

### `HandleVehicleNameUpdate(oWidget, sName, uFaction)`
Handles updates to the vehicle name by calling `SetVehicleName`.

### `_PulseRed(oWidget)`
Starts a red pulsing animation on the widget.

### `_PulseRedLoop(oWidget)`
Continues the red pulsing animation in a loop.

### `_PulseRedLoopLow(oWidget)`
Handles the low part of the red pulsing loop, adjusting speed based on disguise level.

### `_PulseRedLoopHigh(oWidget)`
Handles the high part of the red pulsing loop, adjusting speed based on disguise level.

### `_HaltPulse(oWidget, bImmediate)`
Stops the red pulsing animation. If `bImmediate` is true, it stops immediately without animation.

### `_HandleVehicleChange(oWidget, sVehicleName, nDisguiseLevel)`
Handles changes to the vehicle by setting the new name and disguise level.

### `HandleDisguiseUpdate(oWidget, nLevel, bDisguised)`
Updates the widget's disguise level and whether the vehicle is disguised.

### `SetUpVisibilityManagement(oWidget)`
Sets up visibility management for the widget, allowing it to be shown or hidden with animations.

### `ChangeVisibility(oWidget, bVisible, bInstant)`
Changes the visibility of the widget. If `bInstant` is true, the change happens immediately without animation.

### `_InitIdentifier(oWidget)`
Initializes the identifier widget by setting up animation points and default values.

### `SetIdentifier(oWidget, sName)`
Sets the text of the identifier widget to the provided name. If no name is provided, it hides the widget.

### `Init()`
Initializes the module by populating the `_tFactionTextures` table with faction GUIDs and their corresponding texture names.

## Events
- Listens for `GuiUpdate` to call `DisguiseUpdate`.
- Listens for custom event `HandleVehicleNameUpdate(oWidget, sName, uFaction)` to update the vehicle name.
- Listens for custom event `HandleDisguiseUpdate(oWidget, nLevel, bDisguised)` to update the disguise level.

## Notes for modders
- Ensure that `_Initialize` is called appropriately to set up the widget's initial state.
- Use `SetVehicleName` and `SetDisguiseLevel` to control the display of vehicle name and disguise level.
- Customize faction icons by modifying the `_tFactionTextures` table.
- Be aware that red pulsing animations can be controlled using `_PulseRed`, `_HaltPulse`, and related functions.