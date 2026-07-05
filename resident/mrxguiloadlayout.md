---
title: MrxGuiLoadLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, load screen]
verified: true
verified_note: 'deeper pass: re-confirmed the LoadStateChange/GuiInitialization→MrxGuiLoadScreen wiring, the single ReInit function, and no inherit against source; added the widget geometry constants (transparent root, black background, "Loading" text at 56,416 font_16)'
---

# MrxGuiLoadLayout

*Module: mrxguiloadlayout.lua*

## Overview
The `MrxGuiLoadLayout` module is responsible for defining and managing the layout of the loading screen GUI. It sets up a container widget that includes a background image and a text widget displaying "Loading". The module also handles reinitialization of these widgets.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiLoadScreen`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state but manages the loading screen GUI layout and reinitialization.

## Functions
### `ReInit()`
Reinitializes the loading screen GUI by removing any previously added widgets and then adding new ones based on the predefined `LocalWidgetList`. This function is likely called when the game needs to refresh or reset the loading screen. This is the only top-level function defined in this file.

## Events
No `Event.Create`/`Event.*` engine-event references appear in this file — confirmed by grep. The root "Loading Screen" widget in `LocalWidgetList` wires its `EventHandlers.LoadStateChange` key to `MrxGuiLoadScreen.HandleStateChangeEvent` and its `EventHandlers.GuiInitialization` key to `MrxGuiLoadScreen.HandleInit` — both are widget-level event handler names, not `Event.*` constants, and both handler functions live in `mrxguiloadscreen.lua`, not this file. `ReInit()` itself is not wired to anything here; it's a plain callable function invoked directly by other code.

## Widget geometry & constants
- **`"Loading Screen"` root:** full-screen `640×480` `container`, white but **fully transparent**
  (`TranslucencyLevel = 0`) — the visible loading content comes from the child widgets and the Scaleform movie
  [`MrxGuiLoadScreen`](mrxguiloadscreen) builds at runtime, not from this root.
- **`"Loading background"` child:** full-screen `640×480` **black** (`0,0,0,255`) image, no texture in the layout.
- **`"Loading text"` child:** the literal text `"Loading"` at `56,416`–`111,432`, `font_16`, left/bottom-anchored.
  This is a plain fallback label; the animated skull/save UI lives in [`MrxGuiLoadScreen`](mrxguiloadscreen).

## Notes for modders
- This file is pure layout data. The loading behavior — the `"loadingscreen"` `.gfx` movie, the spinning save
  icon, analog passthrough — all lives in [`MrxGuiLoadScreen`](mrxguiloadscreen); change the visuals there, not
  here.
- `ReInit()` is a full teardown/rebuild of the widget tree (same `AddedWidgetList`-must-pre-exist caveat as the
  other layout files).