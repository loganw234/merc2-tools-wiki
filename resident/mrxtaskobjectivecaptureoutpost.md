---
title: MrxTaskObjectiveCaptureOutpost
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, outpost]
verified: true
verified_note: deeper pass — corrected the Activated description (it registers an MrxOutpostManager outpost event on config uOutpostBldg, NOT an "Awake" hibernation event); confirmed status handling (knStatusCaptured → CompletePart, knStatusDestroyed → CancelPart) and all icon overrides; cross-linked MrxOutpostManager
---

# MrxTaskObjectiveCaptureOutpost

*Module: mrxtaskobjectivecaptureoutpost.lua*

## Overview
The `MrxTaskObjectiveCaptureOutpost` module is a specific type of task objective that focuses on capturing or destroying outposts. It inherits from the `MrxTaskObjective` module and integrates with the `MrxOutpostManager` to handle outpost status changes.

## Inheritance
- Inherits from: [`MrxTaskObjective`](mrxtaskobjective)
- Imports: [`MrxOutpostManager`](mrxoutpostmanager)

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page). This subclass adds **no** per-instance state of its own
beyond what it puts in the shared config: the single outpost building it watches is `tConfig.uOutpostBldg`,
and progress is tracked through the inherited target/quota machinery.

## Functions
### `Activated(self)`
Calls `MrxTaskObjective.Activated(self)`, then — if config `uOutpostBldg` is set — registers a status
callback on that outpost via `MrxOutpostManager.RegisterOutpostEvent(uOutpostBldg, self._HandleOutpostStatusChange, {self})`.
That registration (not any engine `Event.*`) is how capture/destroy notifications arrive.

### `Cleanup(self)`
`MrxOutpostManager.UnregisterOutpost(tConfig.uOutpostBldg)` if one was registered, then defers to
`MrxTaskObjective.Cleanup(self)`.

### `_HandleOutpostStatusChange(self, uOutpost, nStatus)`
The status callback. On `MrxOutpostManager.knStatusCaptured` it `RemoveTarget` + `CompletePart` (success);
on `MrxOutpostManager.knStatusDestroyed` it `RemoveTarget` + `CancelPart` (failure). Any other status is
ignored.

### `_GetShortDescription()`
Returns a short description for the task objective, which is "[Generic.ObjectiveOutpost]".

### `GetInlineIcon(self)`
Returns an inline icon based on whether the outpost capture is optional. If optional, returns `[objoutpost2]`; otherwise, returns `[objoutpost]`.

### `_GetTargetRadarIcon()`
Returns the radar icon for the task objective target, which is `"objective_outpost"`.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon for the task objective target based on whether it's optional. If optional, returns `"icon_outpost_2_mc"`; otherwise, returns `"icon_outpost_1_mc"`.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the task objective target, which is `"HUD_objective_outpost"`.

## Events
No engine `Event.*` subscriptions of its own. Capture/destroy notifications come through
[`MrxOutpostManager`](mrxoutpostmanager)'s registration API (`RegisterOutpostEvent` /
`UnregisterOutpost`), not `Event.Create`. Inherits [`MrxTaskObjective`](mrxtaskobjective)'s
`Event.TimerRelative` initial-notes timer.

## Notes for modders
- **Point it at an outpost** with config `uOutpostBldg` (the outpost building GUID) — without it, `Activated`
  registers nothing and the objective never completes on capture.
- Completion vs. failure is decided entirely by [`MrxOutpostManager`](mrxoutpostmanager)'s
  `knStatusCaptured` / `knStatusDestroyed`; this class just maps them to `CompletePart` / `CancelPart`.
- The outpost art overrides differ from the base action icons: radar `"objective_outpost"`, world
  `"HUD_objective_outpost"`, PDA `"icon_outpost_1_mc"` / `"icon_outpost_2_mc"`, inline
  `"[objoutpost]"` / `"[objoutpost2]"`.