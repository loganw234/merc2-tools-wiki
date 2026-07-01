---
title: MrxGuilTiprecachelayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui]
---

# MrxGuilTiprecachelayout

*Module: mrxguiltiprecachelayout.lua*

## Overview
The `MrxGuilTiprecachelayout` module defines a layout for a GUI widget used in the game's interface. This widget is responsible for managing the display and behavior of a specific graphical element, likely related to pre-caching or initializing certain UI components.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGuiLTIPrecache`

## Instance pattern
This is a stateless manager/utility module. It does not follow the per-instance pattern and instead defines a static layout configuration for a GUI widget.

## Functions
There are no top-level functions in this module.

## Events
This module does not define any event handlers directly. However, it references two event handlers from the imported `MrxGuiLTIPrecache` module:
- `HandleStateChangeEvent`
- `_Initialize`

These handlers are associated with events like `GuiGameStateChange` and `GuiInitialization`.

## Notes for modders
- This module defines a static layout configuration for a GUI widget. Modders should be cautious when modifying this configuration to ensure that the UI behaves as expected.
- The widget's behavior is managed by event handlers defined in the imported `MrxGuiLTIPrecache` module. Modders should refer to that module for more details on how these events are handled.
- This module does not have any per-instance state, so there is no need to create or delete instances of it.