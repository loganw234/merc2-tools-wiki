---
title: MrxGuiHudFactionBuffer
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: confirmed zero Event.* calls (GuiUpdate is a widget EventHandlers key); flagged StartTimer/StartPursuit referencing an undeclared bInitialize (always nil, likely copy-paste leftover from SetValue)
---

# MrxGuiHudFactionBuffer

*Module: mrxguihudfactionbuffer.lua*

## Overview
The `MrxGuiHudFactionBuffer` module is a manager for up to two on-screen faction gauges. It handles the lifecycle of these gauges, including adding, updating, and removing them based on faction activity. The module also manages the visibility of the "Objective Tray" HUD element, temporarily hiding it when a gauge occupies the bottom slot.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGui`

## Instance pattern
This is a stateless manager/utility module with no per-instance tables. It tracks the following key fields:
- `_knNumSlots`: The number of slots available for faction gauges (set to 2).
- `tData.tSlotLife`: An array tracking the remaining life time of each slot.
- `tData.tSlotPointData`: An array storing animation point data for each slot.
- `tData.tSlotOccupants`: An array mapping slots to currently occupied faction gauges.
- `tData.tFactionGauges`: A table mapping faction names to their respective gauge widgets.

## Functions
### `Initialize(oWidget)`
Initializes the faction buffer manager. Sets up the template gauge, calculates slot positions, and initializes various data structures. Adds event handlers for GUI updates and defines additional methods on the widget (`AddFactionGauge`, `SetInsideFactionZone`, etc.).

### `AddFactionGauge(oWidget, sFactionName, sTexture)`
Adds a new faction gauge for the specified faction name with an optional texture. Duplicates the template gauge, sets its icon, and adds it to the widget's children.

### `SetInsideFactionZone(oWidget, sFactionName, bInside, bInitialize)`
Sets whether the specified faction is inside their zone. This function is currently a placeholder and does not perform any actions.

### `SetValue(oWidget, sFactionName, nLevel, bInitialize)`
Updates the value of the gauge for the specified faction. Handles animations and slot management to ensure smooth transitions between different states.

### `StartTimer(oWidget, sFactionName, nTime, fFunction, tCallbackData)`
Starts a timer for the specified faction's gauge. This function is used to manage timed events associated with the faction gauge. **Likely bug**: reads a bare `bInitialize` (line 119) to decide `nLifeTime` (0 vs 0.25), but `bInitialize` is not a parameter of this function, not declared `local` anywhere in scope, and never set as a module-level global in this file — it is always `nil`/falsy here, so the `if bInitialize then nLifeTime = 0 end` branch never fires in practice. `SetValue` (above) has a real `bInitialize` parameter used the same way; this looks like leftover copy-pasted code rather than an intentional design.

### `StartPursuit(oWidget, sFactionName, nTime, fFunction, tCallbackData)`
Starts a pursuit event for the specified faction's gauge. Similar to `StartTimer`, but specifically for pursuit-related actions. Has the same bare/undeclared `bInitialize` reference (line 150) as `StartTimer`, with the same effect — always falsy, so `nLifeTime` is always `0.25`.

### `HideGauge(oWidget, sFactionName)`
Hides the gauge for the specified faction by animating it out and clearing its slot occupation.

### `ModifyFactionMood(oWidget, sFactionName, nLevel, bInitialize)`
Modifies the mood of the specified faction. This function is currently a placeholder and does not perform any actions.

### `ShowAll(oWidget, nDuration)`
Shows all faction gauges for a specified duration. This function is currently a placeholder and does not perform any actions.

### `_Update(oWidget, nDeltaTime)`
Per-frame update function that manages the lifecycle of faction gauges. Updates slot lifetimes, handles animations, and manages the visibility of the "Objective Tray" HUD element.

### `_FindSlot(oWidget, sFactionName)`
Finds an available slot for the specified faction gauge. Returns the slot index and whether it is currently active.

### `_IsBufferEmpty(oWidget)`
Checks if all slots are empty. Returns `true` if no gauges are present, otherwise returns `false`.

## Events
No `Event.*`/`Event.Create(...)` engine-event references appear in this file — confirmed by grep. `Initialize(oWidget)` registers `_Update` as the widget's `"GuiUpdate"` handler (a widget-level `EventHandlers` key, not an `Event.*` constant) for per-frame slot-lifetime bookkeeping and Objective Tray visibility restoration. All other lifecycle (`AddFactionGauge`, `SetValue`, `StartTimer`, `StartPursuit`, `HideGauge`) is driven by direct function calls from other modules, not engine events.

## Notes for modders
- Ensure that the widget passed to `Initialize` is properly set up with a template gauge.
- Use `AddFactionGauge`, `SetValue`, `StartTimer`, and `StartPursuit` to manage faction gauges dynamically.
- Be aware that the "Objective Tray" HUD element may be temporarily hidden when a gauge occupies the bottom slot.
- The module currently has placeholder functions for `SetInsideFactionZone`, `ModifyFactionMood`, and `ShowAll`. Implementing these functions will require additional logic.