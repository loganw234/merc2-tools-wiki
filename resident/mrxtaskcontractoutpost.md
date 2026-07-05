---
title: MrxTaskContractOutpost
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskContract
tags: [mission, outpost]
verified: true
verified_note: 'deeper pass: re-confirmed all functions against source; corrected Events (proximity range is
  100 units, tutorial re-arm is a distance-hysteresis pair, not a generic listener), surfaced the tutorial
  timing constants (6s/15s/29s waits, 4-message OutpostCapture sequence), the child MrxTaskObjectiveCaptureOutpost
  objective, and the Outpost:Create config fields; cross-linked Outpost/MrxFactionManager/MrxStatsManager/
  MrxLayerManager; replaced vacuous notes with real config levers.'
---

# MrxTaskContractOutpost

*Module: mrxtaskcontractoutpost.lua*

## Overview
The `MrxTaskContractOutpost` module is responsible for managing outpost-capture contracts in the game. It handles loading and switching between different layers (pristine, staging, defense, captured), setting up proximity tutorials, and tracking progress towards capturing an outpost. Upon completion, it updates statistics and swaps the relevant layers.

## Inheritance
- Inherits from: `MrxTaskContract`
- Imports: `Outpost`, `MrxFactionManager`, `MrxAchievements`, `MrxTutorialManager`, `MrxStatsManager`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskContract`](mrxtaskcontract)'s class-factory pattern** (itself
inherited from [`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general
mechanism), identified by name/lineage rather than a world-object GUID. Per-instance fields (on `self`):
- `bCompletedFirstTutorial`: whether the first full tutorial pass has finished (gates the "no progress" nag).
- `nTutorialText`: 1-based cursor into the 4-step OutpostCapture tutorial sequence.
- `_UpdatedTimer`, `_ShowOutpostTutorial`, `_Far`, `_Near`, `_TutorialTimer`: timer/event handles for
  tutorials and the "no progress" retrigger.

{: .warning }
> **Real bug — `_oOutpost` is a module-level global, not `self._oOutpost`.** In `Activated` it's assigned as
> a bare `_oOutpost = Outpost:Create(...)` (no `self.`), and `Complete`/`Cleanup` read the same bare global.
> Because the module table is shared across all instances of this class, **only one outpost-capture contract
> can be tracked at a time** — a second concurrent instance would clobber the first's `_oOutpost`. In the
> real game only one is ever active, so this never bites, but don't rely on `self._oOutpost` (it doesn't
> exist) and be aware of the limitation if you author overlapping outpost contracts.

## Functions
### `LoadAssets(self, tSaveData)`
Loads the necessary layers (pristine, staging, defense) based on the outpost configuration. It uses `MrxLayerManager.Add` to add these layers and calls `self.AssetsLoaded` when done.

### `Activated(self)`
Calls `MrxTaskContract.Activated(self)` first, then builds the outpost via
[`Outpost:Create`](outpost) with config drawn from `GetOutpostConfig()`: `sOutpost`/`sBoundary`/`tCapturePts`
(the capture geometry), `sDefenders`/`sAttackers` (faction template names resolved via
[`MrxFactionManager.GetFactionTemplateName`](mrxfactionmanager) — defenders = the rival faction, attackers =
this contract's faction), `tDBSpawners` (dangerous-building spawners), `nStartingHealth`, `nRusherQuota`, and
an `fUpdatedCallback` that re-arms the "no progress" nag timers. It then `CreateChild`s a
[`MrxTaskObjectiveCaptureOutpost`](mrxtaskobjectivecaptureoutpost) objective (named `"Outpost"`) whose
`fOnComplete` bumps [`MrxStatsManager.IncreaseOutpostCapturedCounter`](mrxstatsmanager) then calls
`self:Complete()`, and whose `fOnCancel` cancels the contract (with an `OutpostDestroyed` cancel message if
the outpost was destroyed rather than lost). Finally it arms the first `Event.ObjectProximity` (`"<"` 100
units, player → outpost building) → `Near`.

### `NoProgressMade(self)`
Called when no progress is made on the outpost capture. It shows the tutorial if it hasn't been shown yet.

### `Near(self)`
Handles the player getting near the outpost. It removes any far proximity events, sets up new near proximity events, and starts the tutorial timers.

### `SetupTutorialTimers(self)`
Sets up the initial state for the tutorial, showing the first message and setting up a timer to show subsequent messages.

### `Far(self)`
Handles the player moving away from the outpost. It hides any tutorial messages and sets up new far proximity events.

### `ShowOutpostTutorial(self)`
Steps through the 4-message `"OutpostCapture"` custom tutorial keyed by `self.nTutorialText` (via
[`MrxTutorialManager`](mrxtutorialmanager)). Messages 1–4 use the localization keys
`[Tutorial.OutpostCapture.Key1..Key4]` (Key1–Key3 interpolate faction name / adjective / support name from
[`MrxFactionManager`](mrxfactionmanager)); each advances after a `6`-second `Event.TimerRelative`. After the
4th, it calls `EndCustomTutorial`, sets `bCompletedFirstTutorial = true`, resets `nTutorialText = 1`, and
schedules the next loop `29` seconds out.

### `Complete(self)`
Marks the outpost captured (`_oOutpost:Captured()` if not already captured/destroyed), then swaps layers via
[`MrxLayerManager`](mrxlayermanager): `MarkForRemoval` the staging and defense layers, `MarkForAddition` the
captured layer (each guarded by its config field being set). Ends with `MrxTaskContract.Complete(self)`.
(The stats increment happens in the objective's `fOnComplete`, not here.)

### `RemoveTutorialEvents(self)`
Removes all tutorial-related events and timers to clean up resources.

### `Cleanup(self)`
Cleans up the outpost contract task by deleting the outpost instance if it hasn't been captured or destroyed, removing tutorial events, and calling the base class's cleanup function.

### `GetOutpostConfig(self)`
Retrieves the outpost configuration from the task's config.

## Events
Real `Event.ObjectProximity` handles only — created via the inherited `_CreateEvent` (in `Activated`) and
bare `Event.Create` (in `Near`/`Far`), all against the outpost building GUID at **100 units**:
- `Activated` arms `"<" 100` (player enters range) → `Near`.
- `Near` arms `">" 100` (player leaves) → `Far` and starts the tutorial timers.
- `Far` arms `"<" 100` again → `Near` and hides the tutorial. This near/far pair is a hysteresis loop that
  shows the capture tutorial only while the player is within 100 units of the outpost.

`NoProgressMade` is **not** an event — it's a plain method retriggered by `Event.TimerRelative` (6 s) from the
outpost's `fUpdatedCallback`. `ShowOutpostTutorial`/subsequent messages are likewise `Event.TimerRelative`
scheduling, not subscriptions.

## Notes for modders
- **Tutorial timing knobs** (in `ShowOutpostTutorial`): the inter-message wait is `6` s, the "no progress"
  re-arm is `6` s, the re-show delay is `15` s, and the gap before the tutorial loops again after all 4
  messages is `29` s. The message count is fixed at 4 (`[Tutorial.OutpostCapture.Key1..Key4]`).
- **Proximity radius is hard-coded to `100`** in four places (`Activated`/`Near`/`Far`) — change all of them
  together if you want a different tutorial trigger distance.
- **Outpost tuning** is data-driven via `tOutpostConfig` (`GetOutpostConfig()` → `tConfig.tOutpostConfig`):
  `sOutpostBldg`, `sCapturePt`, `tCapturePts`, `sRivalFaction`, `nStartingHealth`, `nRusherQuota`,
  `tDangerousBldgs`, and the four layer names (`sPristineLayer`/`sStagingLayer`/`sDefenseLayer`/
  `sCapturedLayer`). These are the real levers — see [`Outpost`](outpost) for what each does.
- `Cleanup` deletes the outpost (`_oOutpost:Delete()`) only if it wasn't captured or destroyed, then removes
  all tutorial events before the base `MrxTaskContract.Cleanup`.