---
title: MrxSubtitle
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, subtitle]
verified: true
verified_note: corrected Events section (no Event.* calls in source, module is called directly) and noted table.getn as legacy Lua 5.0 API
---

# MrxSubtitle

*Module: mrxsubtitle.lua*

## Overview
The `MrxSubtitle` module manages the queueing and display of subtitles in the game. It provides functionality to add multiple subtitle messages with a callback for the final message, as well as clear pending messages from the buffer.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It tracks the following key fields:
- `_tMsgIds`: A table to store message IDs of queued subtitles.
- `_knDisplayDuration`: The default display duration for each subtitle message.
- `_knFadeDuration`: The default fade duration for each subtitle message.

## Functions
### `Add(vMsgs, fCallback, tCallbackArgs)`
Accepts a string or table of messages (`type(vMsgs)` branches on `"string"` vs `"table"`; any other type
is a silent no-op — returns with no error and nothing queued). Builds one `tConfig` per message
(`sMessage`, `nDuration = _knDisplayDuration`, `nFadeTime = _knFadeDuration`, `bClearBuffer = true`,
`bAllowsAppends = false`) and pushes each to `Hud.SubtitleBuffer:AddMessage(tConfig)`. Only the **last**
message in the batch (`i == nMsgs`, via `table.getn(tMsgs)`) gets `tConfig.fCallback`/
`tConfig.tCallbackData` set from `fCallback`/`tCallbackArgs` — earlier messages in a multi-message call get
no callback. Every message ID returned by `AddMessage` is appended to `_tMsgIds`.

### `ClearPending()`
Removes pending messages from the buffer by calling `Hud.SubtitleBuffer:RemovePendingMessage({tMessageIds
= tMsgId})` for each stored message ID. Reassigns `_tMsgIds` to a fresh empty table after removal (source
does `_tMsgIds = nil` immediately followed by `_tMsgIds = {}`, rather than clearing in place).

## Events
No `Event.*` references anywhere in this file — this module is **not** event-driven. `Add` and
`ClearPending` are plain functions called directly by whichever script wants to display or clear
subtitles; there are no call sites for either inside this file, so triggering is entirely external (no
call sites found in the decompiled corpus for either from this side).

## Notes for modders
- Use `Add` to queue multiple subtitle messages with a callback for the final message only — if you need
  a callback per-message, call `Add` once per message instead of batching them.
- Use `ClearPending` to remove any queued subtitle messages from the buffer before adding new ones.
- Customize display and fade durations by modifying `_knDisplayDuration` and `_knFadeDuration`.
- Be aware that the module uses `Hud.SubtitleBuffer` for managing subtitle messages, so ensure this buffer is available in your game environment.
- `Add` uses `table.getn(tMsgs)`, a Lua 5.0-era API (removed in later Lua versions) rather than the `#`
  length operator — consistent with this codebase's older Lua runtime, not a bug.