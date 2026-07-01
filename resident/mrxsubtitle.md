---
title: MrxSubtitle
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, subtitle]
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
Accepts a string or table of messages; pushes each to `Hud.SubtitleBuffer:AddMessage` with `_knDisplayDuration`/`_knFadeDuration`; attaches callback to the final message. This function is used to queue subtitle messages for display.

### `ClearPending()`
Removes pending messages from the buffer by calling `Hud.SubtitleBuffer:RemovePendingMessage` for each stored message ID. Clears the `_tMsgIds` table after removal.

## Events
- Listens for custom event (not specified in provided code) to trigger subtitle addition.
- Listens for custom event (not specified in provided code) to trigger clearing of pending subtitles.

## Notes for modders
- Use `Add` to queue multiple subtitle messages with a callback for the final message.
- Use `ClearPending` to remove any queued subtitle messages from the buffer before adding new ones.
- Customize display and fade durations by modifying `_knDisplayDuration` and `_knFadeDuration`.
- Be aware that the module uses `Hud.SubtitleBuffer` for managing subtitle messages, so ensure this buffer is available in your game environment.