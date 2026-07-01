---
title: MrxGuiHudMelee
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
---

# MrxGuiHudMelee

*Module: mrxguihudmelee.lua*

## Overview
The `MrxGuiHudMelee` module is responsible for managing the melee and context-action HUD prompts in the game. It provides functions to set and display messages, handle widget updates, and manage the initialization of the context action widget.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any persistent state but manages HUD widgets and their interactions.

## Functions
### `SetCounterMessageVisible(bShow, uPlayerGuid)`
Sets the visibility of a counter message for a specific player. This function is currently stubbed and does not perform any action.

### `SetMeleeMessage(sString, uPlayerGuid)`
Sets a melee message for a specific player. This function is currently stubbed and does not perform any action.

### `DisplayCounterMessage(nDisplayTime, uPlayerGuid)`
Displays a counter message for a specified duration to a specific player. This function is currently stubbed and does not perform any action.

### `HandleUpdateEvent(oWidget, nTime)`
Handles update events for a given widget. This function is currently stubbed and does not perform any action.

### `HandleInitializationEvent(oWidget, oEvent)`
Handles initialization events for a given widget. This function is currently stubbed and does not perform any action.

### `HideOnComplete(oWidget)`
Hides a widget when its animation completes. This function is currently stubbed and does not perform any action.

### `SetContextActionMessage(sText, uPlayer, nPriority)`
Sets the context action message for a player or all players. It retrieves the appropriate HUD widget, initializes it if necessary, and updates the message queue based on priority. If the message changes, it triggers a sound cue and animates the widget to display the new message.

### `ContextActionWidgetRemovalCallback(oContextActionWidget)`
A callback function that is called when the context action widget's removal animation completes. It hides the widget, clears its text, resets its priority, and sets its translucency level.

### `_Initialize(oWidget)`
Initializes a HUD widget by setting up custom data fields such as message queue, current priority, and animation points for visibility and fade effects.

## Events
- Listens for engine events to handle widget updates and initialization.
- Manages the display of context action messages based on priority and player input.

## Notes for modders
- The functions `SetCounterMessageVisible`, `SetMeleeMessage`, and `DisplayCounterMessage` are currently stubbed and do not perform any actions. They can be extended to add custom functionality as needed.
- The `SetContextActionMessage` function is the primary entry point for setting context action messages. It handles message queuing, priority management, and widget animations.
- Customizing the behavior of the context action widget requires modifying or extending the functions related to widget initialization and animation handling.
- Be aware that sound cues (`ui_HUD_Contextual_Action_Alert`) are triggered when messages change, which may affect player experience.