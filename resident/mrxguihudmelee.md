---
title: MrxGuiHudMelee
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: confirmed zero Event.* and zero SetEventHandler calls in file; corrected vague Events section; flagged likely bug in SetContextActionMessage (sCurrentText assigned from sText instead of sNewText in the fallback-to-next-queued-message path, line 51)
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

**Likely bug in the clear-and-fall-back-to-next-queued-message path** (`sText == nil` and `nPriority == oContextActionWidget.CustomData.nCurrentPriority`): the widget text is correctly set to the next queued message via the local `sNewText` (line 48, `SetText("[action] " .. sNewText)`), but `sCurrentText` is then assigned from `sText` instead of `sNewText` (line 51) — and `sText` is `nil` in this branch. So `sCurrentText` ends up `nil` even though the widget is now showing `sNewText`. Net effect: the dedup check earlier in the same branch (line 45, `sCurrentText ~= sNewText`) never has a chance to correctly suppress a repeat sound cue for this fallback path on a subsequent call, since `sCurrentText` never actually records what's displayed here.

### `ContextActionWidgetRemovalCallback(oContextActionWidget)`
A callback function that is called when the context action widget's removal animation completes. It hides the widget, clears its text, resets its priority, and sets its translucency level.

### `_Initialize(oWidget)`
Initializes a HUD widget by setting up custom data fields such as message queue, current priority, and animation points for visibility and fade effects.

## Events
No `Event.*`/`Event.Create(...)` engine-event references and no `SetEventHandler` calls appear anywhere in this file — confirmed by grep. `HandleUpdateEvent(oWidget, nTime)` and `HandleInitializationEvent(oWidget, oEvent)` are named following the `Handle*Event` convention used elsewhere for widget event handlers, but neither is registered to any handler key in this file — both are empty stubs (see Functions). `SetContextActionMessage` is the module's real entry point and is called directly by name from other modules (not event-driven); it looks up the "Context Action Text" widget via `MrxGui.GetWidgetByName`/`GetWidgetByNameAndOwner`, lazily calls the local `_Initialize` on first use, and manages message text/priority/animation itself.

## Notes for modders
- The functions `SetCounterMessageVisible`, `SetMeleeMessage`, and `DisplayCounterMessage` are currently stubbed and do not perform any actions. They can be extended to add custom functionality as needed.
- The `SetContextActionMessage` function is the primary entry point for setting context action messages. It handles message queuing, priority management, and widget animations.
- Customizing the behavior of the context action widget requires modifying or extending the functions related to widget initialization and animation handling.
- Be aware that sound cues (`ui_HUD_Contextual_Action_Alert`) are triggered when messages change, which may affect player experience.