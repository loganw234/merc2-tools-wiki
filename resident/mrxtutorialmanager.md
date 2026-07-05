---
title: MrxTutorialManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tutorial, manager]
verified: true
verified_note: fixed fabricated Events section (source has no Event.* calls at all); added _sCurrentMessage/_bMessageDisplayed to Instance pattern
---

# MrxTutorialManager

*Module: mrxtutorialmanager.lua*

## Overview
The `MrxTutorialManager` module is responsible for managing in-game tutorials. It handles the creation, activation, and completion of various tutorial modules, ensuring that players receive appropriate guidance based on their actions within the game.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module (module-level globals, no `Create`/`uGuid`/`tInstance` pattern). It tracks the following key fields:
- `_tTutorials`: A table containing data for each tutorial, including its module name and whether it has been completed.
- `_sCurrentActiveTutorial`: The identifier of the currently active tutorial.
- `_sCurrentMessage`: The text of the tutorial message currently displayed (set/cleared by `ShowMessage`/`HideMessage`).
- `_bMessageDisplayed`: Whether a tutorial message is currently showing.

## Functions
### `Reset()`
Resets the tutorial system by clearing the current active tutorial and destroying events associated with all tutorials. Also hides any displayed messages.

### `Setup()`
Sets up the tutorial system by resetting it and then initializing each tutorial that has not been completed. It dynamically imports each tutorial module and creates an instance of it, setting up activation criteria.

### `BeginCustomTutorial(sIdentifierName, bDontNetSync)`
Begins a custom tutorial if tutorials are enabled and no other tutorial is currently active. Sets the current active tutorial to the specified identifier name.

### `EndCustomTutorial(sIdentifierName, bDontNetSync)`
Ends a custom tutorial if it matches the current active tutorial. Hides any displayed messages and clears the current active tutorial.

### `StartTutorial(sTutorialName, bDontNetSync)`
Activates a specific tutorial if it has not been completed and its instance exists.

### `SetCurrentTutorial(oTutorial, bDontNetSync)`
Sets the current tutorial by displaying its message. Returns false if tutorials are disabled or if a message is already displayed.

### `UpdateCurrentTutorial(oTutorial, bDontNetSync)`
Updates the current tutorial by displaying its message. Returns false if the tutorial name does not match the current active tutorial.

### `HideCurrentTutorial(oTutorial, bComplete, bDontNetSync)`
Hides the current tutorial and marks it as complete in the save data. Returns true if successful.

### `GetTutorial(sTutorial)`
Retrieves the instance of a specific tutorial.

### `DestroyTutorial(oTutorial)`
Destroys a tutorial by removing its module and clearing its instance.

### `ShowMessage(sMessage, bDontNetSync, sIdentifierName)`
Displays a tutorial message. If networking is enabled and not disabled, it sets the tutorial message on the server. Returns false if the same message is already displayed or if another tutorial is active.

### `HideMessage(bDontNetSync, sIdentifierName)`
Hides the current tutorial message. If networking is enabled and not disabled, it clears the tutorial message on the server.

### `SaveSingleton()`
Saves the state of completed tutorials by returning a list of their names.

### `LoadSingleton(tSaveData)`
Loads the saved data for completed tutorials, marking them as complete in the module's internal state.

## Events
No `Event.*` calls appear anywhere in this file. Tutorial activation/completion is driven entirely by direct function calls (`Setup`, `StartTutorial`, `SetCurrentTutorial`, `HideCurrentTutorial`, etc.) from other modules (individual `WifTutorial*` modules), not by engine events raised here. Networking uses `Net.SetTutorialMessage`/`Net.IsServer` directly, not the `Event` system.

## Notes for modders
- Ensure that `Setup` is called appropriately to initialize tutorials.
- Use `StartTutorial` to activate specific tutorials as needed.
- Be aware of the network synchronization (`bDontNetSync`) parameter when managing tutorial messages in multiplayer scenarios.
- The module uses dynamic imports, so ensure that all referenced tutorial modules are available.