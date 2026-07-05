---
title: MrxGuiHudFactionBuffer
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed all 11 functions + zero Event.* calls; corrected Instance pattern (stateless module + per-widget CustomData, not "no tables"); surfaced slot-lifetime constants (5s / 5+nTime / pursuit), the SetValue delta<3 snap, and Objective Tray slot-3 hide interplay; re-verified the StartTimer/StartPursuit undeclared-bInitialize bug'
---

# MrxGuiHudFactionBuffer

*Module: mrxguihudfactionbuffer.lua*

## Overview
The `MrxGuiHudFactionBuffer` module is a manager for up to two on-screen faction gauges. It handles the lifecycle of these gauges, including adding, updating, and removing them based on faction activity. The module also manages the visibility of the "Objective Tray" HUD element, temporarily hiding it when a gauge occupies the bottom slot.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGui` (via [`import("MrxGui")`](../glossary#importname)) — the buffer duplicates a template [MrxGuiHudFactionGauge](mrxguihudfactiongauge) child and manages it. See [MrxGui](mrxgui).

## Instance pattern
**Stateless module + per-widget `CustomData`.** The functions carry no per-instance metatable; all state lives on the buffer widget in `oWidget.CustomData` (aliased `tData` in most functions). `Initialize` also copies the module functions onto the widget itself (`oWidget.AddFactionGauge = AddFactionGauge`, `oWidget.SetValue = SetValue`, etc.) so callers can invoke them as methods. The one module-level constant is `_knNumSlots = 2` (two gauge slots).

Per-widget state (`tData.*`), all set up in `Initialize`:
- `tData.tSlotLife[1..2]`: seconds of remaining life for each slot (counts down in `_Update`).
- `tData.tSlotPointData[1..3]`: animation-point specs — slots 1-2 are the on-screen positions (`TranslucencyLevel = 255`), slot `_knNumSlots+1` (index 3) is the off-screen/hidden point at `y = nY2, TranslucencyLevel = 0`.
- `tData.tSlotOccupants[1..2]`: which gauge widget currently holds each slot.
- `tData.tFactionGauges[sFactionName]`: faction name → its gauge widget (created by `AddFactionGauge`).
- `tData.oTemplateGauge`: the first child, removed from display and kept as the duplication template.
- `tData.bTrayDisabled`: set true while the "Objective Tray" is force-hidden by a bottom-slot gauge.

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
- **Slot count**: `_knNumSlots = 2` — at most two faction gauges show at once. Raising it requires the layout to provide vertical room (`tSlotPointData` positions are computed from the template gauge's height stacked downward).
- **Slot lifetime constants** (how long a gauge lingers before fading out): `SetValue` sets `tSlotLife = math.max(5, previous)` — a value change keeps the gauge up ~5s. `StartTimer` sets `tSlotLife = 5 + nTime`. `StartPursuit` overwrites `nTime = -3` then sets `tSlotLife = 2 + nTime` (i.e. `-1`), so a pursuit gauge does not use a fixed linger — its life is refreshed each `_Update` to `oGauge:GetRemainingPursuitTime() + 2` while the pursuit stays active. Fade-out animation is a fixed `0.25`s to the hidden point.
- **Value "snap"**: `SetValue` treats any change smaller than `3` (`nDeltaValue < 3`) as an initialize — it forces `bInitialize = true`, animating in `0`s (instant) instead of `0.25`s. Small nudges don't re-trigger the slide-in.
- **Objective Tray interplay**: when a gauge takes a slot and the [Objective Tray](mrxguihudobjectivetray) is visible with its slot 3 occupied (`oTray:IsSlotOccupied(3)`), the tray is force-hidden and `bTrayDisabled` is set; `_Update` restores it once the buffer empties (`_IsBufferEmpty`). The tray is looked up by the exact name `"Objective Tray"`.
- **Delegated gauge behavior**: `AddFactionGauge` duplicates the template and calls `oGauge:_Initialize()`, `oGauge:SetIcon(...)`, and `oGauge.CustomData.oTimer:_Initialize()` — the actual bar/timer/pursuit rendering lives on the gauge widget ([MrxGuiHudFactionGauge](mrxguihudfactiongauge)), not here. This module only sizes, positions, and schedules slots.

{: .warning }
> **Confirmed bug — undeclared `bInitialize` in `StartTimer` and `StartPursuit`.** Both read a bare `bInitialize` (lines 119 and 150) to decide `nLifeTime` (0 vs 0.25), but `bInitialize` is not a parameter of either function, not declared `local`, and never a module global — it is always `nil`, so the `nLifeTime = 0` branch is dead and the animate-in time is always `0.25`s. `SetValue` has a real `bInitialize` parameter used identically; this is leftover copy-pasted code, not intentional.

- **Placeholder stubs**: `SetInsideFactionZone`, `ModifyFactionMood`, and `ShowAll` are empty (`function ... end`) — they do nothing. Don't rely on them; implement the logic yourself if you need it.