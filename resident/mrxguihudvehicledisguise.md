---
title: MrxGuiHudVehicleDisguise
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed all functions + zero Event.* calls; corrected Instance pattern (stateless module + per-widget CustomData, not singleton); surfaced the STATE_* enum, faction-GUID→texture map with real GUIDs, bar colors (gaining 255,102,102 / losing 200,255,200), pulse/name-time constants, default icon temp_radar_icon_pmc, and the Player.GetVehicleDisguise() visibility gate; noted dead _knMoveTime'
---

# MrxGuiHudVehicleDisguise

*Module: mrxguihudvehicledisguise.lua*

## Overview
The `MrxGuiHudVehicleDisguise` module is responsible for managing the vehicle disguise display on the HUD. It handles updating the faction icon, crossed-out icon, disguise level bar, and vehicle name identifier based on player interactions and game state.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui` (via [`import("MrxGui")`](../glossary#importname)). Also calls the [Player](../namespaces/player) namespace (`Player.GetVehicleDisguise`) and `StringToGuid` (from [stdlib](../lua-bridge-api/stdlib)) for the faction GUID lookups.

## Instance pattern
**Stateless module + per-widget `CustomData`.** No `tInstance`/metatable. All state (`nValue`, `nBasePoint`/`nRedPoint` animation points, the child-widget references `oIcon`/`oIconCross`/`oBarBack`/`oBarFront`/`oIdentifier`, `nLastDisguiseLevel`/`nNewDisguiseLevel`, `bIsDisguised`/`bWasDisguised`, `bPulse`) lives in `oWidget.CustomData`, populated by `_Initialize`. Methods are copied onto the widget (`oWidget.SetDisguiseLevel = SetDisguiseLevel`, `oWidget.SetVehicleName = SetVehicleName`, `oWidget.PulseRed = _PulseRed`, etc.). The only true module-level names are the constants below and the `_tFactionTextures` map (built by `Init()`).

### Module constants (the tunables)
- `_knPulseTime = 0.4` — normal red-pulse half-cycle; `_knPulseTimeFast = 0.1` — used when disguise level `< 25` (urgent flashing as cover blows).
- `_knMoveTime = 2` — **declared but never referenced** (dead constant).
- `nVehicleNameTime = 3` — seconds the vehicle-name identifier stays up before auto-hiding.
- **State enum** (module globals, used by `DisguiseUpdate`): `STATE_DISGUISED = 1`, `STATE_UNDISGUISED = 2`, `STATE_GAINING = 3`, `STATE_LOSING = 4`.
- **Bar colors**: gaining disguise = `(255, 102, 102)` red-ish; losing disguise = `(200, 255, 200)` green-ish. The identifier auto-hides once disguise drops below `50` while disguised.
- **Default/fallback icon**: `temp_radar_icon_pmc` (used when no faction or an unmapped faction is passed).
- **`_tFactionTextures`** (faction GUID → HUD icon texture, built by `Init()` via `StringToGuid`): `0xbbc34ef4 → HUD_faction_AN` (Allies), `0x41359cce → HUD_faction_CH` (China), `0xe947b797 → HUD_faction_OC` (Oil), `0xb10d73ce → HUD_faction_GR` (Guerrilla/PLAV), `0xc18215fe → HUD_faction_PR` (Pirate), `0xdcc8b14d → HUD_faction_CV` (Civilian), `0xb4420059 → HUD_faction_VZ` (VZ), `0x30e4a26f → HUD_faction_PMC` (PMC).

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

{: .note }
> No `Event.*` engine calls appear in this file. The wiring is widget event handlers via `SetEventHandler` (a widget `EventHandlers` key, not an engine `Event.*` constant):

- `SetVehicleName` registers `"GuiUpdate"` → `DisguiseUpdate` when a name is set (per-frame bar/icon/state animation), and clears it (`SetEventHandler("GuiUpdate", nil)`) when the name is cleared.
- `HandleVehicleNameUpdate(oWidget, sName, uFaction)` and `HandleDisguiseUpdate(oWidget, nLevel, bDisguised)` are handler-callback entry points (wired to named widget events in the HUD layout); they just forward to `SetVehicleName` / `SetDisguiseLevel`. `_HandleVehicleChange` similarly forwards to `SetVehicleName`.

## Notes for modders
- **Driving the display**: call `SetVehicleName(oWidget, sName, uFaction, bDisguised)` to show the panel (name + faction icon) and `SetDisguiseLevel(oWidget, nValue, bDisguised)` to update the meter (`nValue` is clamped to `0..100`). Passing `sName = nil` to `SetVehicleName` hides everything and unregisters the update handler.
- **Final visibility is gated by `Player.GetVehicleDisguise()`**: even after `DisguiseUpdate` decides which children to show, all four (icon, cross, bar front/back) are `SetVisible(Player.GetVehicleDisguise())`. If that returns false the panel stays hidden regardless — this is the master on/off for the whole disguise HUD.
- **Re-skin faction icons**: edit the texture names in `_tFactionTextures` (`Init()`). The keys are faction GUIDs decoded from hash strings via `StringToGuid` — to add a faction, add its GUID hash and a `HUD_faction_*` texture.
- **Pulse tuning**: `_PulseRed`/`_PulseRedLoop`/`_HaltPulse` drive the low-disguise red flash. It speeds up (`_knPulseTimeFast = 0.1` vs `_knPulseTime = 0.4`) once `nLastDisguiseLevel < 25`. `_HaltPulse(oWidget, true)` snaps back to base color immediately.
- **State thresholds**: the identifier text hides when disguise `< 50` while disguised; the undisguised "crossed-out icon" shows for `1`s (`nIconTimeUntilHide`) then hides. Adjust those literals in `DisguiseUpdate` to change the feedback timing.