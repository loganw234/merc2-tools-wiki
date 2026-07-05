---
title: MrxTaskObjectiveExtract
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, extraction]
verified: true
verified_note: deeper pass — flagged that the extraction event handles (eHeliClose/eHeliFar/uHeliHurt/eHeliFailsafe/eAIenter1/eAIenter2/_evClientJoined/tEnterGoal) are MODULE-LEVEL globals not per-instance fields (two concurrent extract objectives would collide); confirmed all events and the MrxSupportData "Extraction_AL" freebie; documented the fixed radii (40/70/150) and heli-abort thresholds
---

# MrxTaskObjectiveExtract

*Module: mrxtaskobjectiveextract.lua*

## Overview
The `MrxTaskObjectiveExtract` module is responsible for handling the extraction task objective in the game. It manages the extraction process, including setting up followers, checking for allied helicopters, and handling various events related to the target's proximity and health.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `MrxSupportData`, `MrxFollow`, `MrxUtil`, `MrxGui`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page). Genuine per-instance fields:
- `self._uTgtObjFilter` — the person to extract (inherited).
- `self.oFollower` — the [`MrxFollow`](mrxfollow) escort managing the prisoner while awaiting pickup.

{: .warning }
> **The extraction event handles are module-level globals, not per-instance fields:** `eHeliClose`,
> `eHeliFar`, `uHeliHurt`, `eHeliFailsafe`, `eAIenter1`, `eAIenter2`, `_evClientJoined`, and `tEnterGoal`
> are all assigned as bare globals (no `self.`/`local`). Two extract objectives running at the same time
> would overwrite each other's handles — this is a real latent bug in the corpus, not a per-instance design.

## Functions
### `Activated(self)`
Called when the task objective is activated. It sets default configuration values, retrieves target objects, and initializes a follower if necessary. It also creates events for object death and player join.

### `SendPlayerJoinEvents()`
Sends player join events to the server. This function ensures that the extraction process is properly synchronized with new players joining the game.

### `CheckForHeli(self, uGuid)`
Checks for allied helicopters in proximity to the target. If an allied helicopter is found, it sets up events for handling the extraction process.

### `TargetDestroyed(self, uGuid)`
Cancels the part of the task related to the destroyed target.

### `TargetStopsForHeli(self, uGuid, tHeliExt)`
Handles the scenario where the target stops for an allied helicopter. It activates the follower, sets up AI goals for entering the helicopter, and creates events for handling various extraction-related scenarios.

### `TargetRunsForHeli(self, uGuid, tHeliExt)`
Sets up AI goals for the target to run towards the helicopter.

### `CheckEnter(self, tHeliExt, uGuid, nState)`
Checks if the target has successfully entered the helicopter. If not, it retries entering after a short delay.

### `AbortExtract(self, uGuid)`
Aborts the extraction process due to various failure conditions, such as the destruction of the extraction heli or the target moving too far away. It resets the prisoner's AI goals and activates the follower again.

### `ResetPrisoner(self, uGuid)`
Resets the prisoner's AI goals and reactivates the follower. It also checks for allied helicopters again.

### `TargetIn(self, uGuid, tHeliExt, Guid, State)`
Handles the scenario where the target is inside the helicopter. It completes the part of the task related to the extraction process after a short delay.

### `Cleanup(self)`
Cleans up the module by removing the freebie associated with the extraction task and calling the base class's cleanup function.

## Events
- Listens for `Event.ObjectDeath` to call `TargetDestroyed` when the target object dies.
- Listens for custom event `mpPlayerJoin` to send player join events.
- Listens for `Event.ObjectProximity` to handle scenarios where the target is close or far from an allied helicopter.
- Listens for `Event.ObjectHealth` to handle scenarios where the extraction heli's health drops below a certain threshold.
- Listens for `Event.ObjectInSeat` to handle scenarios where the target enters the helicopter.

## Notes for modders
- **`Activated` grants a free extraction airstrike** via `MrxSupportData.AddFreebie("Extraction_AL")` (the
  Allied extraction heli), removed again in `Cleanup`. That is what makes the pickup chopper available while
  the objective is live.
- **Extraction geometry is hardcoded** (no config knobs): the heli must come within `40` m to trigger the
  run-for-it, the run aborts if it drifts past `70` m or loses `> 25` health, with a `50` s failsafe timer;
  entering the heli completes the part after a `4` s delay.
- Default config (via `MrxUtil.SetDefault`): `fDist = 40`, `bStop = false`, `bXZOnly = false`,
  `bHumansFollow = true`; pass `oFollower` to reuse an existing [`MrxFollow`](mrxfollow) instead of spawning
  one.
- **Don't run two extract objectives concurrently** — see the module-globals warning above; the second
  would clobber the first's heli event handles.