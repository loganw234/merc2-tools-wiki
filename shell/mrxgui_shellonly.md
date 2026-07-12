---
title: MrxGui_ShellOnly
parent: Shell Modules
nav_order: 4
inherits: none
tags: [shell]
verified: false
---

# MrxGui_ShellOnly

## Overview
A facade module that imports `MrxGuiBase` and re-exposes a large chunk of its widget API as flat globals (`AddWidget`, `Widget`, `ImageWidget`, `GetWidgetByName`, etc.), wired up in `Init()`. On top of that facade it implements its own screen-fade system (`FadeToColor`/`FadeFromColor`), a HUD-message stub (`AddMessage`/`ClearMessages`), an objective-description callback hook, and an E3/demo-mode HUD toggle. It's the shell build's own distinct sibling to `resident`'s/shell's shared `mrxgui.lua` — not a copy of it.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`

Also references `MrxGuiDialogBox`, `MrxGuiNumericBox`, and a `MessageBox` global in `Init()`/`AddMessage()`/`ClearMessages()` without importing any of them — see the gotcha below.

## Instance pattern
Singleton-state manager. Module-level globals besides the large facade-alias block:
- `_fObjectiveInformationCallback` / `_tObjectiveInformationCallbackData` — the registered objective-description callback and its bound extra args.
- `_oGlobalScreenFadeWidget` / `_tGlobalFadeStack` — the shared (non-per-player) screen-fade widget and a stack of queued global fades. `_tGlobalFadeStack` starts as `false` and only becomes an actual table (`{}`) inside `Init()`.
- `_bE3HudModeOn` — whether the E3/demo-floor HUD mode is active.
- The facade block itself: roughly thirty module-level globals (`AddWidget`, `Widget`, `ImageWidget`, `GetWidgetByName`, `RemoveWidget`, `SendEvent`, `Joystick`, ...) declared as placeholder `0` at the top of the file and aliased to their real `MrxGuiBase` counterparts inside `Init()`.

## Functions

### GetObjectiveDescription(uGuid)
Returns `nil` if no callback is registered or `uGuid` isn't `userdata`. Otherwise copies `_tObjectiveInformationCallbackData` (if it's a table) into a fresh `tData`, appends `uGuid`, and calls `_fObjectiveInformationCallback(unpack(tData))`, returning its result. Likely used by shell-side UI (e.g. a mission-select/satellite screen) to fetch a human-readable description for a world object from whatever registered the callback.

### SetObjectiveInformationCallback(fCallback, tCallbackData)
Registers `fCallback` (type-checked) into `_fObjectiveInformationCallback`, and `tCallbackData` into `_tObjectiveInformationCallbackData` if it's a table (else `false`).

### FadeToColor(nTime, uPlayerGuid, nRed, nGreen, nBlue, nAlpha)
Fades the screen to a solid color, either for one player (`uPlayerGuid`) or globally. Defaults: `nTime=1`, color defaults to black (`0,0,0`), `nAlpha=255`. Lazily creates a fullscreen `ImageWidget` (named `"Fullscreen Fade Effect Widget"`) the first time it's called for a given owner, with two named animation points (`nFadeToTransparentPoint`/`nFadeFromTransparentPoint`) stashed in `CustomData`. A per-player fade, or a global fade when no other global fade is active, animates (or instantly jumps, if `nTime <= 0`) right away; a global fade requested while another is already showing is pushed onto `_tGlobalFadeStack` instead — **global fades queue, they don't replace.**

### FadeFromColor(nTime, uPlayerGuid)
Reverses a fade. Per-player: animates (or instantly clears) the per-player widget back to transparent, hiding it on completion via `_HideWhenDone`. Global: pops the top of `_tGlobalFadeStack`; if that empties the stack, clears the screen the same way as the per-player case; if there's still a queued fade underneath, it re-applies *that* fade's stored color/alpha instead of clearing — restoring what should still be showing under the fade that just ended.

{: .note }
> One branch of the "restore the next queued fade, no animation" path calls `oScreenWidget:SetTranslucency(nAlpha)` — but `nAlpha` isn't a parameter or local anywhere in `FadeFromColor` (only `nTime` and `uPlayerGuid` are). Every other reference in that branch correctly uses `tData.nAlpha`. As decompiled this reads like it should be `tData.nAlpha` too; it only matters once three or more global fades are stacked at once.

### SetFadeEnabled(bEnable)
Adds/removes `_oGlobalScreenFadeWidget` from the GUI via `MrxGuiBase.RemoveWidget`/`AddWidget`, only when `bEnable` actually differs from the widget's current `BasicData.bEnabled` — and only meaningful after at least one global `FadeToColor` call has created the widget.

### _HideWhenDone(oWidget)
One-line helper: `oWidget:SetVisible(false)`. Used as a fade-out completion callback.

### AddMessage(tArgs)
Reads `tArgs.sText`/`iPriority`/`nDuration`/`nFadeTime`/`bClear`/`sType`/`bExclusive` into locals with defaults (`sMessage` falls back to `" "`, `nPriority` to `5`, `nDisplayDuration` to `2`, `nFadeDuration` to `0.5`, `sType` to `"sText"`) — but the actual call at the bottom, `MessageBox:AddMessage(tArgs.sText, tArgs.iPriority, tArgs.nDuration, tArgs.nFadeTime, tArgs.bClear, tArgs.bExclusive)`, uses the raw `tArgs.*` fields directly instead. None of the locals it computes are ever passed anywhere — the defaulting logic here is dead code as decompiled, so callers need to supply real values in `tArgs` themselves rather than relying on it.

### ClearMessages()
`MessageBox:ClearMessages()`.

### SetE3HudMode(bOn) / IsE3HudModeActive()
`SetE3HudMode` posts a `{EventType="E3HudMode", bOn=bOn}` table through the module-level `SendEvent` alias and stores `bOn` in `_bE3HudModeOn`; `IsE3HudModeActive` returns that flag. `Init()` calls `SetE3HudMode(true)` automatically when `Sys.IsDemoMode()` is true — a trade-show/demo-floor HUD mode, switched on automatically for demo builds.

### FindShellWidget()
Looks up the widget named `"Shell"`; if it has `CustomData.oFlash`, returns `oFlash.BasicData.uId` (the underlying Scaleform/Flash instance ID). Returns `nil` otherwise.

### GetReticleSize(uPlayer)
Looks up the widget named `"reticle image"` and returns its width (`nX2 - nX1`) if found, else a default of `48`. The `uPlayer` parameter is never used in the body.

### Init()
Populates the entire facade block (`AddWidget = MrxGuiBase.AddWidget`, `Widget = MrxGuiBase.Widget`, and roughly thirty more assignments like it), sets `_tGlobalFadeStack = {}`, and turns on E3 HUD mode if `Sys.IsDemoMode()`.

## Events
No `Event.*` calls. `SetE3HudMode` posts through `SendEvent`, aliased in `Init()` to `MrxGuiBase.SentEvent` — a real function (confirmed in `mrxguibase.lua`, forwarding to `EventManager.SendEvent`) despite the unusual past-tense name. That's GUI-layer event dispatch, not `Event.Create`/`Event.Post`.

## Notes for modders
- **This is not the same file as the shared `mrxgui.lua`** (one of the 22 byte-identical resident/shell duplicates) — `MrxGui_ShellOnly` is a separate, genuinely shell-exclusive module that happens to do a similar `MrxGuiBase`-aliasing trick.
- **Three globals this file depends on are never imported here**: `MrxGuiDialogBox`, `MrxGuiNumericBox` (both referenced in `Init()`), and `MessageBox` (referenced in `AddMessage`/`ClearMessages`). They only resolve because something else has already loaded/populated them as globals by the time these functions run — don't assume `MrxGui_ShellOnly` is self-sufficient if you're extracting pieces of it.
- **`Init()` must run before any fade call** — `_tGlobalFadeStack` is `false` until `Init()` sets it to `{}`; calling `FadeToColor`/`FadeFromColor` on a global fade before that would error against a non-table.
- **Global screen fades stack, they don't replace** — see `FadeToColor`/`FadeFromColor` above. If you're scripting overlapping fades, know that a second global `FadeToColor` call queues rather than cancelling the first.
- **`AddMessage`'s default-filling logic is vestigial** — it computes defaulted locals it never uses; pass real values in `tArgs` rather than relying on the defaults the code appears to promise.
- Two harmless decompiler/source duplications, no behavior change: `RemoveAllWidgetsInLayout` is declared as a placeholder global twice, and both `PushAllTextToFront` and `_PushAllTextToFront` end up aliased to the same `MrxGuiBase.PushAllTextToFront`.
