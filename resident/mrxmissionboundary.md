---
title: MrxMissionBoundary
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mission, boundary]
verified: true
verified_note: corrected Instance pattern — this is a class-factory (Create returns a genuine per-call self table with setmetatable), not a stateless module as previously claimed; no tInstance/uGuid registry, caller holds the returned instance
---

# MrxMissionBoundary

*Module: mrxmissionboundary.lua*

## Overview
The `MrxMissionBoundary` module manages mission boundaries or proximity-based triggers. Callers create an instance via `Create(srcObj, tConfig)`, configured with either a named/GUID region (`Event.Boundary`) or a point + radius (`Event.ObjectProximity`). It fires a caller-supplied callback on exit/return/warning/fail, optionally plays voice-over lines on each transition, and runs an `MrxTimer` countdown (warn + fail thresholds) while the player is outside the boundary.

## Inheritance
- Inherits from: `none — base/utility module` (no `inherit(...)` call)
- Imports: `MrxTimer`, `MrxUtil`, `MrxVoSequence`

## Instance pattern
**Class-factory pattern, not per-`uGuid`.** `Create(srcObj, tConfig)` builds a new table `self = {}`, calls `setmetatable(self, srcObj)` and sets `srcObj.__index = srcObj` — so the returned instance's metatable is the caller-supplied `srcObj` itself (the module/prototype table the caller passes in), letting `self` fall back to `srcObj`'s methods/fields. There is no `tInstance` registry keyed by `uGuid`, no `OnActivate`/`Awake` — the caller (a mission/vz script) is fully responsible for holding onto the returned `self` and calling `Cancel(self)` when done. Returns `nil` if `tConfig == nil`.

Per-instance fields set in `Create`:
- `_tConfig`: the config table passed in, kept for later reference (VO tables, label, etc.).
- `tEvents`: table of active event handles, keyed `eOutside`/`eReturn` (reused/overwritten as the instance transitions between outside/inside states).
- `uRgn` or `uPoint` + `fRadius`: region-mode instances get `uRgn` (resolved via `Pg.GetGuidByName` if `tConfig.sRegionName` is a string, else used directly as a GUID); point-mode instances (when `tConfig.sRegionName` resolves to nothing) get `uPoint` (same resolution logic against `tConfig.sPoint`) and `fRadius` from `tConfig.fRadius`.
- `fCallback` / `tCallbackData`: from `tConfig.fCallback`/`tConfig.tCallbackData`, invoked by `_CallCallback`.
- `fWarnTime` / `fFailTime` / `iTray`: from `tConfig.fWarnTime`/`fFailTime`/`iTray`, defaulted via `MrxUtil.SetDefault` to `15`/`30`/`3` respectively.
- `oTimer`: set/cleared by `_StartTimer`/`Cancel`/`_InsideBoundary`/`_InsideRange`/`_FailTimeExpired` — the active `MrxTimer` instance, or `nil` when not running.

## Functions
### `Create(srcObj, tConfig)`
Returns `nil` immediately if `tConfig` is `nil`. Otherwise builds the instance (see Instance pattern above) and registers the initial "outside" watcher: if `tConfig.sRegionName` resolves to a GUID, creates an `Event.Boundary` "exit" listener (`_OutsideBoundary`) against `self.uRgn`; otherwise resolves `tConfig.sPoint`/`tConfig.fRadius` and creates an `Event.ObjectProximity` `">"` listener (`_OutsideRange`) against `self.uPoint`. Both listeners watch `Player.GetAnyCharacter()`.

### `Cancel(self)`
Cancels all active events and stops any running timers associated with the mission boundary.

### `GetRegion(self)`
Returns the GUID of the region associated with the mission boundary.

### `_OutsideBoundary(self, uCharacter)`
Callback for the `eOutside` `Event.Boundary` exit listener (region mode). Tether guard first: if the exiting character is the secondary player, a primary player exists, and the distance between them exceeds `Pg.GetTetherDiameterStart()`, it re-arms the same exit listener and returns — treats this as "still effectively outside due to tether pull," not a real exit. Otherwise: calls `self:_CallCallback("exit")`, arms an `Event.Boundary` "enter" listener (`_InsideBoundary`) on the specific `uCharacter` that exited, and either plays a random line from `self._tConfig.tExitVOs` via `MrxVoSequence.Start` (queuing `_StartTimer` to run after the VO) or calls `self:_StartTimer()` directly if no exit VOs configured.

### `_InsideBoundary(self, uCharacter)`
Callback for the `eReturn` `Event.Boundary` enter listener. Checks every other player's character with `Object.InsideBoundary(char, self.uRgn)` — if any other player is still outside the region, re-arms the enter listener on that other character and returns (waits for *all* players back inside, not just the one that triggered this callback). Once all are inside: stops/clears `self.oTimer` if running, re-arms the `eOutside` exit listener, and calls `self:_CallCallback("return")`.

### `_OutsideRange(self, uCharacter)`
Point/radius-mode equivalent of `_OutsideBoundary`, using `Event.ObjectProximity` instead of `Event.Boundary`. Same tether re-arm guard. On a real exit: calls `self:_CallCallback("exit")`, arms an `Event.ObjectProximity` `"<="` listener (`_InsideRange`) at `self.fRadius - 10` (a smaller inner radius than the outer trigger — hysteresis to avoid flapping at the boundary edge) on the exiting character, then plays exit VO or starts the timer exactly like `_OutsideBoundary`.

### `_InsideRange(self, uCharacter)`
Point/radius-mode equivalent of `_InsideBoundary`. Checks every other player's distance from `self.uPoint` via `Object.GetDistanceFrom(char, self.uPoint, true)` — if any other player is still beyond `self.fRadius`, re-arms the inner-radius listener on that character and returns. Once all are within range: stops/clears the timer, re-arms the outer `">"` exit listener, plays a random `self._tConfig.tReturnVOs` line if configured, then calls `self:_CallCallback("return")`. (Note: unlike `_InsideBoundary`, the VO-play happens *before* `_CallCallback("return")` here, not queued through `_StartTimer`-style sequencing — order matches source, not necessarily deliberate.)

### `_StartTimer(self)`
Creates and starts a timer based on the mission boundary configuration. The timer includes warning and fail times, and triggers corresponding callbacks.

### `_WarnTimeExpired(self)`
Handles the expiration of the warning time for the timer. Triggers voice-over sequences if configured and calls the warning callback.

### `_FailTimeExpired(self)`
Handles the expiration of the fail time for the timer. Calls the fail callback, stops the timer, and cleans up associated events.

### `_CallCallback(self, sStatus)`
Calls the configured callback function with the current status (e.g., "exit", "return", "warning", "fail") and any additional data provided in the configuration.

## Events
Two real `Event.*` types are used, both via `Event.Create` (not `CreatePersistent`), stored in `self.tEvents` and cleaned up by `Cancel`:
- `Event.Boundary` — region mode. Exit variant: `{Player.GetAnyCharacter(), self.uRgn, "exit", false}` → `_OutsideBoundary`. Enter variant: `{uCharacter, self.uRgn, "enter", false}` → `_InsideBoundary`.
- `Event.ObjectProximity` — point/radius mode. Exit variant: `{Player.GetAnyCharacter(), self.uPoint, ">", self.fRadius, false, true}` → `_OutsideRange`. Enter variant: `{uCharacter, self.uPoint, "<=", self.fRadius - 10, false, true}` → `_InsideRange`.

There is no separate "timer event" system here — `_StartTimer` builds an `MrxTimer` instance (not an `Event.*` call) with `tDoneCallbacks`/`tWarnCallbacks` pointing at `_FailTimeExpired`/`_WarnTimeExpired`; `MrxTimer` internally handles its own scheduling (not covered by this file).

## Notes for modders
- `tConfig` fields actually read by `Create`: `sRegionName` (string name or GUID) OR `sPoint`+`fRadius` (string name or GUID + number), `fCallback`, `tCallbackData`, `fWarnTime` (default 15), `fFailTime` (default 30), `iTray` (default 3), `sLabel` (used by `_StartTimer` for the `MrxTimer` label), `tExitVOs`/`tReturnVOs`/`tWarnVOs` (VO line tables, all optional).
- `fCallback` is invoked as `fCallback(self, sStatus, ...)` with `sStatus` one of `"exit"`, `"return"`, `"warning"`, `"fail"` — plan for all four, not just success/fail.
- Use `Cancel(self)` to tear down: deletes every handle in `self.tEvents` and stops/clears `self.oTimer`. There's no automatic cleanup otherwise.
- `_StartTimer` itself has a guard: if any player is already within `self.fRadius - 10` of `self.uPoint` when it runs, it skips starting the timer entirely (only meaningful in point/radius mode — this check uses `self.uPoint`, so in pure region mode without a point configured this guard would always pass through, since `self.uPoint` would be `nil` and `Object.GetDistanceFrom` against `nil` is not confirmable from static reading alone).
- The tether re-arm guard (in `_OutsideBoundary`/`_OutsideRange`) only fires for the secondary player relative to the primary — be aware behavior differs between single-player-with-partner and other multiplayer configurations.