---
title: MrxOutpostManager
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [manager, outpost]
verified: true
verified_note: confirmed no Event.* calls in source (Events section corrected from vague "custom event" wording); all 4 functions and no-inherit/stateless claims verified accurate.
---

# MrxOutpostManager

*Module: mrxoutpostmanager.lua*

## Overview
The `MrxOutpostManager` module is responsible for managing outposts in the game world. It provides functionality to register and unregister outposts, as well as handle status changes such as capture or destruction. This module tracks outpost-specific callbacks and executes them when a status change occurs.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It tracks the following key fields:
- `_tOutposts`: A table mapping outpost GUIDs to their callback data.

## Functions
### `RegisterOutpost(uOutpost)`
Registers an outpost by adding it to the `_tOutposts` table if it is not already registered. Initializes the outpost with an empty list of callbacks.

### `UnregisterOutpost(uOutpost)`
Unregisters an outpost by removing its entry from the `_tOutposts` table if it exists.

### `RegisterOutpostEvent(uOutpost, fCallback, tCallbackArgs)`
Registers a callback function for a specific outpost. Ensures the outpost is registered and then adds the callback along with its arguments to the outpost's list of callbacks.

### `OutpostStatusChange(uOutpost, nStatus)`
Handles a status change for an outpost by executing all registered callbacks associated with that outpost. Logs a debug message for each callback execution. After executing the callbacks, it unregisters the outpost.

## Events
None. This file contains no `Event.*` calls at all — it registers no listeners itself. `OutpostStatusChange(uOutpost, nStatus)` is a plain function; something external (another module, e.g. a specific outpost's world-object script) must call it directly when a capture/destroy happens. There's no event wiring visible in this file to confirm what calls it.

## Notes for modders
- Use `RegisterOutpostEvent` to add callbacks that should be executed when an outpost's status changes.
- Ensure that outposts are properly registered and unregistered to avoid memory leaks or incorrect behavior.
- The `nStatus` parameter in `OutpostStatusChange` can be used to determine the new state of the outpost; the module itself defines `knStatusCaptured = 1` and `knStatusDestroyed = 2` as the two known values.
- Be aware that unregistering an outpost after executing its callbacks is a default behavior; this may need to be adjusted based on specific mod requirements.
- `OutpostStatusChange` calls `MrxUtil.CallWithOptionalArgs(tCallback.fCallback, {unpack(tCallback.tCallbackArgs), uOutpost, nStatus})` for each registered callback — the callback receives its own registered args first, followed by `uOutpost` and `nStatus`.