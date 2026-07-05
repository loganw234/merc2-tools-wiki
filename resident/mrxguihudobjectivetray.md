---
title: MrxGuiHudObjectiveTray
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed all 6 functions + zero Event.*/SetEventHandler; surfaced tray constants (3 slots, spacing 5, default height 16, font english_18) and the MrxGuiManager HUD-registration calls; noted the dead local nSpacing=2 (overwritten by CustomData.nSpacing=5); re-verified the SetSlotToWidget dead nil-check bug'
---

# MrxGuiHudObjectiveTray

*Module: mrxguihudobjectivetray.lua*

## Overview
The `MrxGuiHudObjectiveTray` module manages the **3-slot vertical objective tray** on the HUD — the stacked right-justified text/icon entries (objective reminders, counters) shown at a screen edge. It exposes a small API to put text or an image into a slot, clear a slot (re-stacking the ones below), and query occupancy. Built on the native GUI framework ([MrxGui](mrxgui)); text/image widgets, no Scaleform.

## Inheritance
- Inherits from: none — base/utility module
- Imports (via [`import()`](../glossary#importname)): `MrxGui`, `MrxGuiBase`, `MrxGuiManager` — see [MrxGui](mrxgui), [MrxGuiBase](mrxguibase), [MrxGuiManager](mrxguimanager). Slot widgets are registered with the per-player HUD through `MrxGuiManager.AddWidgetToHud` / `RemoveWidgetFromHud`.

## Instance pattern
**Stateless module + per-widget `CustomData`.** No module-level state. `_HandleInitializationEvent` builds three child "slot" widgets on the tray, stores tray geometry in `oWidget.CustomData` (`nSpacing`, `nDefaultHeight`, `nDefaultWidth`), and copies the five API functions onto the tray widget as methods (`oWidget.SetSlotToText = SetSlotToText`, etc.). Other modules look the tray up by the name `"Objective Tray"` and call those methods.

### Constants (set in `_HandleInitializationEvent`)
- **Slots**: `3` (hard-coded loop bound; `SetSlotToWidget` also rejects `nSlot < 1 or > 3`).
- **`CustomData.nSpacing = 5`** — vertical gap between slots. (Note: a local `nSpacing = 2` is declared but never used — it's immediately shadowed by the `CustomData.nSpacing = 5` assignment. Dead.)
- **`CustomData.nDefaultHeight = 16`** — per-slot height in pixels.
- **`CustomData.nDefaultWidth`** — taken from the tray widget's authored width (`nX2 - nX1`).
- Text slots use font **`english_18`**, right-justified, anchored `left`/`top`.

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
- **Public API** (call as methods on the tray widget after it's looked up by name `"Objective Tray"`): `SetSlotToText(oTray, nSlot, sText)`, `SetSlotToImage(oTray, nSlot, sTexture, nTextureWidth, nTextureHeight)`, `SetSlotToWidget(oTray, nSlot, oWidget)`, `ClearSlot(oTray, nSlot)`, `IsSlotOccupied(oTray, nSlot)`. `nSlot` is `1..3`. `SetSlotToText`/`SetSlotToImage` reuse an existing text/image widget in the slot if the type matches (just updating text/texture), otherwise build a fresh one.
- **Clearing re-stacks**: `ClearSlot` shifts lower slots up if the cleared slot had grown taller than `nDefaultHeight` — so removing a multi-line entry compacts the tray. Positions are recomputed, not just hidden.
- **This tray is what the faction buffer hides**: [MrxGuiHudFactionBuffer](mrxguihudfactionbuffer) checks `oTray:IsSlotOccupied(3)` and hides the whole tray when a faction gauge needs the bottom slot's space, restoring it when the gauge clears. Slot 3 is the contested one.
- **HUD registration is manual**: widgets added to slots are also registered/unregistered with the player HUD via `MrxGuiManager.AddWidgetToHud`/`RemoveWidgetFromHud`. If you add widgets to a slot outside these functions, you must do the same or they won't participate in HUD show/hide.

{: .note }
> **Dead code in `SetSlotToWidget`.** Lines 17-20 default `nX2`/`nY2` to truthy numbers, then guard `if not nX2 or not nY2 then oWidget:SetLocation(...) end` — a condition that can never be true after the defaulting. That `SetLocation` never runs. The nil-check was likely meant to precede the `or`-defaulting; harmless but confusing.