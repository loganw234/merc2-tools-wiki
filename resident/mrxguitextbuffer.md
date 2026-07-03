---
title: MrxGuiTextBuffer
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, text buffer]
verified: true
verified_note: constructor bug and the working replacement confirmed by live testing (CoopChatUI); AddMessage parameter meanings confirmed directly from source, not independently exercised argument-by-argument
---

# MrxGuiTextBuffer

*Module: mrxguitextbuffer.lua*

## Overview

`MrxGuiTextBuffer` is the engine's scrolling-message-log widget — message arrays, text wrapping, priority
queuing, fade-in/out, and append-vs-evict rules, all built in. It's the right tool any time you need more
than one line of HUD text stacked over time (a chat window, a kill feed, a debug console) — see
[Building a Chat/Log UI](../deep-dives/coop-chat-ui) for a full reusable module (`CoopChatUI`) built on
top of this.

**Do not call `InstantiateTextBuffer`, its own documented constructor — it crashes the game.** Confirmed
directly in source:

```lua
function InstantiateTextBuffer(nX, nY, nWidth, nHeight, bFlowDown, bHasBackdrop)
  ...
  NewTextBuffer = MrxGui.ImageWidget:new()   -- line 72: no `local` -- a real global
  ...
  oWidget.CustomData.MessageIndex = {}       -- line 110: oWidget is never defined anywhere in this scope
  oWidget.CustomData.nNextMessageId = 1
  ...
```

`oWidget` doesn't exist anywhere in this function's scope — the real widget it built is `NewTextBuffer`. A
straightforward copy-paste mistake in the shipped game code, not a subtle misread: calling this constructor
throws `attempt to index a nil value (global 'oWidget')` and crashes whatever called it, confirmed by
actually calling it. Patching the typo doesn't fix it either — the patched copy runs in the *patching
script's* environment, not this module's private one, and immediately fails again on the first
`AddMessage` call because `AddMessage`/`ClearMessages`/`SetLocation` etc. only resolve unqualified from
inside `mrxguitextbuffer.lua` itself. See the [function-override deep dive](../deep-dives/function-override)
and the [Glossary](../glossary#importname) for why monkey-patching from outside a module's own file doesn't
work the way it looks like it should.

## The real entry point: `HandleInstantiationEventForTextBuffer`

The module has a second, bug-free constructor-equivalent that's never touched by the bug above — an
event-driven initializer where `oWidget` really is the function's own first parameter:

```lua
function HandleInstantiationEventForTextBuffer(oWidget, tEvent)
  ...
  if "MessageBox" == oWidget.BasicData.name then
    bHasBackdrop = true
    oWidget:SetTranslucency(128)
  end
  ...
  oWidget.CustomData.MessageIndex = {}
  oWidget.AddMessage = AddMessage
  oWidget.ClearMessages = ClearMessages
  ...
```

It wires up exactly the same private methods the buggy constructor was trying to
(`AddMessage`/`ClearMessages`/`ClearVisibleMessages`/`RemovePendingMessage`/`ModifyPendingMessage`/`SetLocation`),
via a path that was never broken. It also confirms the `"MessageBox"` name trick: naming a widget that
before handing it to this function is what flips on the translucent backdrop.

**Working pattern, confirmed by live testing:**

```lua
import("MrxGui")
import("MrxGuiTextBuffer")

local oBox = MrxGui.ImageWidget:new()
oBox:SetLocation(20, 20, 300, 140)
oBox.BasicData = oBox.BasicData or {}
oBox.BasicData.name = "MessageBox"  -- triggers the translucent backdrop

local initFunc = _G.HandleInstantiationEventForTextBuffer or MrxGuiTextBuffer.HandleInstantiationEventForTextBuffer
initFunc(oBox, {})

MrxGui.AddWidget(oBox)
oBox:AddMessage("Hello, HUD!", 5, 15, 1, false, true)
```

No patch, no touching the buggy constructor at all — build a bare widget by hand, name it, and call this
function on it directly. Full walkthrough, including the dead-end attempts and why they failed, on
[Building a Chat/Log UI](../deep-dives/coop-chat-ui).

**A confirmed discrepancy worth knowing about separately**: `MrxGui.ImageWidget:new()` and
`MrxGui.AddWidget(...)` above genuinely work live, but `resident/mrxgui.lua` declares `ImageWidget`,
`TextWidget`, `AddWidget`, and `RemoveWidget` as literal `= 0` in decompiled source and never reassigns
them anywhere in that file — static source reading alone would conclude these aren't callable at all. Same
"decompiled source doesn't reflect final runtime shape" pattern as `MrxSupportData.tSupportData` (starts
empty in source, populated at runtime).

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxGuiManager`

## Instance pattern
Not the per-`uGuid` world-object pattern — this attaches its state directly onto whatever GUI widget you
hand it, via `CustomData`. Key fields once initialized: `CurrentMessages` (array of visible message
widgets), `PendingMessages` (5 priority-bucketed queues, indices 1-5), `MessageIndex` (message-id lookup
for `ModifyPendingMessage`/`RemovePendingMessage`), `nRemainingSpace`, `bFlowDown`, `bHasBackdrop`.

## Functions

### `HandleInstantiationEventForTextBuffer(oWidget, tEvent)`
**The real entry point — see above.** Sets up font/scale, scroll direction, backdrop, border sizing, and
attaches `AddMessage`/`ClearMessages`/etc. to `oWidget`.

### `InstantiateTextBuffer(nX, nY, nWidth, nHeight, bFlowDown, bHasBackdrop)`
**Broken — do not call.** See above.

### `AddMessage(oTextBuffer, sMessage, nPriority, nDisplayDuration, nFadeDuration, bClearBuffer, bAllowsAppends, fCallback, tCallbackData)`
Confirmed directly from source. Defaults if omitted: `nPriority=5`, `nDisplayDuration=2`,
`nFadeDuration=0.25`, `bClearBuffer=false`, `bAllowsAppends=true`. `nPriority` is clamped to `0`-`5`;
`0` is special — it forcibly evicts however many current messages are needed to make room rather than
queuing behind them, for anything urgent enough to jump the line. A negative `nDisplayDuration` makes the
message persistent (`bPersistent=true`, internally set to display for 10000 "seconds" instead) — it stays
until something else clears it rather than fading out on its own. `bAllowsAppends=false` prevents the
*next* message from sharing the buffer's remaining space alongside this one. Returns the new message's
numeric ID (usable with `ModifyPendingMessage`/`RemovePendingMessage`), or `nil` if `oTextBuffer`/`sMessage`
have the wrong type.

### `SetLocation(oTextBuffer, nX1, nY1, nX2, nY2)`
Moves the widget and recalculates the border-adjusted internal bounds (`x1`/`y1`/`x2`/`y2`) other
functions read from.

### `ClearMessages(oTextBuffer)` / `ClearVisibleMessages(oTextBuffer, bAdvance)`
`ClearMessages` wipes everything — current and pending — and hides the widget. `ClearVisibleMessages` only
clears what's currently on-screen; pass `bAdvance=true` to immediately pull the next pending message(s) in
to fill the freed space rather than leaving it empty.

### `ModifyPendingMessage(...)` / `RemovePendingMessage(oTextBuffer, nMessageId)`
Edit or cancel a message that's still queued (by the ID `AddMessage` returned) before it's actually
displayed. Both return `false` if the ID doesn't correspond to a still-pending message — e.g. it already
scrolled onto screen, or never existed.

### `AdvanceMessages(oTextBuffer)`
Zeroes out the currently-showing message's remaining display duration, forcing it to advance/dismiss on
the very next update tick instead of waiting out its normal timer.

### `GetCurrentMessageId(oTextBuffer)`
Returns an array of the numeric IDs of every message currently visible (not pending).

### `HandleTextBufferUpdateEvent` / `PushMessageIntoTextBuffer` / `GetMessageHeight` / `WrapText` / `IsEmpty` / `MboxAbs` / `ValidateParameter` / `HandleE3HudModeEvent` / `HandleAddMessageEvent` / `DrawDebugRectangle`
Internal plumbing — fade/scroll animation, pulling queued messages into the visible list, text
measurement/wrapping, and small utility helpers. Not things a mod needs to call directly; documented in
the decompiled source if you're extending the buffer's own behavior rather than just using it.

## Events
- `HandleTextBufferUpdateEvent` is wired to the widget's own `"GuiUpdate"` event by
  `HandleInstantiationEventForTextBuffer` — this is what drives fading and scrolling frame to frame. You
  don't need to hook this yourself.

## Notes for modders
- **Never call `InstantiateTextBuffer` — see above.** Build the widget by hand and call
  `HandleInstantiationEventForTextBuffer(oWidget, tEvent)` on it instead.
- **Name the widget `"MessageBox"` before initializing it** if you want the translucent backdrop — that
  string match, not a parameter, is what turns it on.
- **`CoopChatUI`** (on [Building a Chat/Log UI](../deep-dives/coop-chat-ui)) is a small, complete, reusable
  wrapper around this module — `Init`/`Show`/`Toggle`/`AddMessage`/`SetInputText`/`Destroy` — worth using
  directly rather than re-deriving this pattern from scratch for a new mod.
- **`nPriority=0` on `AddMessage` is the "interrupt" priority** — use it for anything that must appear
  immediately even if it means evicting whatever's currently showing.
