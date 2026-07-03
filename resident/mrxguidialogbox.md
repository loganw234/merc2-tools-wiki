---
title: MrxGuiDialogBox
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, dialog, beginner-friendly]
verified: true
verified_note: DisplayDialogBox, keyboard/arrow-key navigation, and the callback argument order all confirmed by live testing (CommonSpawnMenu); the rest of the function list is read directly from source
---

# MrxGuiDialogBox

*Module: mrxguidialogbox.lua*

## Overview

`MrxGuiDialogBox` is the engine's native menu system — a message plus a list of selectable text options,
with built-in cursor animation and keyboard/controller navigation already wired up. **This is what powers
the game's own dev cheat menu** (`_G.Cheat.DisplayOptions()`, see [`MrxCheatBootstrap`](mrxcheatbootstrap))
and every other in-game dialog/menu prompt — confirmed by the fact that `Cheat.DisplayOptions()` builds its
menus through this exact module. If you want a working, arrow-keys-and-Enter menu for your own mod without
building any GUI from scratch, this is the tool.

**Confirmed working by live testing** — see `CommonSpawnMenu.lua` on the
[OnKey Scripts](../sample-scripts-onkey) page for a complete real example (a vehicle-spawn picker with a
free-text fallback option).

## Quick start

```lua
import("MrxGuiDialogBox")

local function OnMenuSelect(nSelectedIndex)
  Loader.Printf("Selected option #" .. tostring(nSelectedIndex))
end

MrxGuiDialogBox.DisplayDialogBox(
  Player.GetLocalPlayer(),
  "Pick one",
  {"First option", "Second option", "Cancel"},
  1,               -- nDefaultCursorIndex: which option starts highlighted
  OnMenuSelect,
  {},              -- tCallbackArgs
  nil, nil, nil, nil,
  true,            -- bPause
  3                -- nCancelOption: index of the "Cancel" entry
)
```

Arrow keys move the selection, Enter confirms — both confirmed working with no extra input handling of
your own required. `bPause=true` (the default if omitted) pauses the game for the duration, matching how
the game's own menus behave; the engine handles taking and releasing player control focus internally via
`MrxGuiBase.GetControlFocus`/`ReleaseControlFocus`, called from within `DisplayDialogBox`/`Close` — you
don't need your own `Player.SetInputEnabled` calls around this, unlike a custom-built widget.

**Also seen in real source** (`resident/mrxguisupportshop.lua`) as `MrxGui.DisplayDialogBox(...)` instead
of `MrxGuiDialogBox.DisplayDialogBox(...)` — both names reach the same function; either import works.

### Callback argument order — confirmed from `_CloseAndCallCallback`

```lua
function _CloseAndCallCallback(oDialogBox, nSelectedIndex)
  ...
  local tCallbackArgs = oDialogBox.CustomData.tCallbackArgs
  ...
  if fCallback then
    table.insert(tCallbackArgs, nSelectedIndex)
    fCallback(unpack(tCallbackArgs))
  end
end
```

Whatever you pass as `tCallbackArgs` comes first, and `nSelectedIndex` (the 1-based index into `tOptions`
of whichever option was chosen) is always appended as the *last* argument — so
`DisplayDialogBox(..., fCallback, {oSomeObject})` calls `fCallback(oSomeObject, nSelectedIndex)`, not the
other way around.

### Cancel handling

`nCancelOption` wires a specific option index to fire automatically if the player presses whatever maps to
the "B"/cancel button (`MrxGuiBase.Joystick.BUTTON_PAD2_R`) — confirmed in `_HandleInputEvent` below. Real
shipped code (`mrxguisupportshop.lua`) also just appends an explicit `"[Generic.Cancel]"` string to
`tOptions` and points `nCancelOption` at that same index, so both a deliberate selection and the
cancel-button shortcut land on the same callback branch. `CommonSpawnMenu.lua` does the same with a plain
`"Cancel"` entry.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`

## Instance pattern
Stateless manager module — no `Create`/`uGuid` pattern. Manages dialog boxes through global functions,
plus a few module-level constants/globals: `_ksFont`, `_knScale` (text font/scale), `_knTextR/G/B` and
`_knTextLitR/G/B` (normal vs. highlighted-option text color), `_ksAcceptSound`/`_ksCancelSound`/`_ksChangeSound`
(sound cues for navigation/confirm/cancel).

## Functions

### `DisplayDialogBox(uPlayerGuid, sMessage, tOptions, nDefaultCursorIndex, fCallback, tCallbackArgs, nXOffset, nYOffset, sHorizAnchor, sVertAnchor, bPause, nCancelOption)`
**The main entry point — see Quick Start above.** Validates `sMessage` (must be a string) and `tOptions`
(must be a table; if empty, defaults to a single `"[Generic.Ok]"` entry). Builds the dialog via
`_BuildDialogBox`, then calls `MrxGuiBase.GetControlFocus(oBox, bPause)` to take input focus (and
optionally pause). Returns the dialog box widget.

### `Close(oBox)`
Releases control focus, removes the widget (with children), and deletes it. Assigned as `oBox.Close` by
`DisplayDialogBox`, so it's called as `oBox:Close()`.

### `_BuildDialogBox(...)`
Constructs the actual widget tree: background, message text, one text widget per option, and the animated
cursor. Wires `SetEventHandler("ControllerInput", _HandleInputEvent)` and
`SetEventHandler("OnMouseMove", _HandleDialogUpdate)` on the box (see Events below).

### `_ChangeSelection(oDialogBox, bUp)`
Moves the cursor to the previous/next option, wrapping around at either end, and animates the cursor
widget to the new position.

### `_CloseAndCallCallback(oDialogBox, nSelectedIndex)`
**Confirmed callback mechanism — see above.** Releases control focus, closes the box, then calls
`fCallback` with `tCallbackArgs` followed by `nSelectedIndex`.

### `_HandleInputEvent(oDialogBox, tEvent)`
The actual navigation logic, confirmed directly from source:

```lua
function _HandleInputEvent(oDialogBox, tEvent)
  if MrxGuiBase.Joystick.BUTTON_PAD1_D == tEvent.ButtonPress or MrxGuiBase.Joystick.BUTTON_L_STICK_D == tEvent.ButtonPress then
    oDialogBox:_ChangeSelection(false)   -- down
  elseif MrxGuiBase.Joystick.BUTTON_PAD1_U == tEvent.ButtonPress or MrxGuiBase.Joystick.BUTTON_L_STICK_U == tEvent.ButtonPress then
    oDialogBox:_ChangeSelection(true)    -- up
  elseif MrxGuiBase.Joystick.BUTTON_PAD2_D == tEvent.ButtonPress then
    _CloseAndCallCallback(oDialogBox, oDialogBox.CustomData.nSelectedIndex)  -- confirm
  elseif MrxGuiBase.Joystick.BUTTON_PAD2_R == tEvent.ButtonPress and oDialogBox.CustomData.nCancelOption then
    _CloseAndCallCallback(oDialogBox, oDialogBox.CustomData.nCancelOption)   -- cancel
  end
end
```

These are `MrxGuiBase.Joystick.BUTTON_*` constants, not raw keyboard codes — the engine translates keyboard
input to the same button events for menu contexts, which is why arrow keys/Enter navigate correctly with
no extra keyboard-specific handling needed (confirmed by live testing).

### `_HandleDialogUpdate(oDialogBox, tEvent)`
Mouse-hover equivalent of `_ChangeSelection` — checks for a newly-highlighted option widget and updates the
cursor/colors to match, so mouse and keyboard/controller navigation both keep the cursor state consistent.

### `Pulse(oWidget)` / `_LoopToHigh` / `_LoopToLow` / `HaltPulse` / `_CompleteAnimation`
The cursor's idle pulsing animation and the "move to new option" animation completion callback.

### `DisplayScrollingDialogBox(uPlayer, sText, fCallback, tCallbackData, bDisplayWager, sAcceptString, sDeclineString, sWagerString)`
A second, separate dialog type for long scrollable text (accept/decline, optionally with a wager option)
rather than a short option list — used for things like end-of-mission reports. Builds via
`_BuildScrollingDialogBox`, with its own scroll/highlight/input handlers
(`_HandleScrollUpdate`/`_HandleMouseUpdate`/`_HandleScrollInput`) and `CloseScrollingBox` to tear down.

### `OpenSystemDialogBox(sTitle, sMessage, sButton)` / `CloseSystemDialogBox()`
A third, simpler dialog type — a title/message/single-button system prompt, loaded from its own Scaleform
SWF (`SystemDialogBoxLoadedCallBack` fires once that loads). Closes via a short delayed timer
(`CloseSystemDialogBoxDelayed`) rather than immediately, presumably to let a close animation finish.

### `_ValidateParameter(Parameter, sType, DefaultValue)` / `_Clamp(n, lo, hi)` / `_BuildStrokes(...)` / `_OffsetText(...)` / `_UpdateTextAlpha(...)` / `_SetScrollOption(...)` / `_CompleteScrollAnimation(...)` / `_CreateScrollableWindow(...)` / `_CallScrollBoxCallback(...)`
Internal validation and layout helpers for the scrolling dialog variant — not things a mod needs to call
directly.

## Events
- `oDialogBox:SetEventHandler("ControllerInput", _HandleInputEvent)` — navigation/confirm/cancel, see
  `_HandleInputEvent` above.
- `oDialogBox:SetEventHandler("OnMouseMove", _HandleDialogUpdate)` — mouse-hover highlight tracking.
- `DisplayScrollingDialogBox`'s box wires its own separate `"ControllerInput"` (`_HandleScrollInput`) and
  update handlers for the scrolling variant.
- `OpenSystemDialogBox` waits on an SWF-load callback (`SystemDialogBoxLoadedCallBack`) rather than a
  generic engine event, since that dialog type loads its own Scaleform file.

## Notes for modders
- **Start here for any in-game menu you want to build** — it's already used for the game's own cheat menu
  and multiple shop/briefing dialogs, has working keyboard navigation out of the box, and needs no manual
  control-focus/pause handling.
- **Remember the callback argument order**: `tCallbackArgs` first, `nSelectedIndex` last. Passing `{}` for
  `tCallbackArgs` means your callback just receives `(nSelectedIndex)`.
- **Give yourself an explicit "Cancel" option** rather than relying only on `nCancelOption`/the
  cancel-button shortcut — see the Cancel handling section above.
- See [`MrxMultiPageMenu`](mrxmultipagemenu) for a higher-level paginated-menu wrapper if you need more
  options than comfortably fit in one screen (used by `ConsoleCheatsMenu.lua` on the
  [OnKey Scripts](../sample-scripts-onkey) page).
