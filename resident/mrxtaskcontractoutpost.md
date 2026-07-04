---
title: MrxTaskContractOutpost
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskContract
tags: [mission, outpost]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskContract](mrxtaskcontract) for the general mechanism.
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
mechanism), identified by name/lineage rather than a world-object GUID. Key fields:
- `_oOutpost`: The outpost instance being managed.
- `bCompletedFirstTutorial`: Indicates whether the first tutorial has been completed.
- `_UpdatedTimer`, `_ShowOutpostTutorial`, `_Far`, `_Near`, `_TutorialTimer`: Timers and events related to tutorials and updates.

## Functions
### `LoadAssets(self, tSaveData)`
Loads the necessary layers (pristine, staging, defense) based on the outpost configuration. It uses `MrxLayerManager.Add` to add these layers and calls `self.AssetsLoaded` when done.

### `Activated(self)`
Activates the outpost contract task. It sets up the outpost instance with various parameters such as boundary points, defenders, attackers, and health settings. It also creates a child objective for capturing the outpost and sets up proximity events to trigger tutorials.

### `NoProgressMade(self)`
Called when no progress is made on the outpost capture. It shows the tutorial if it hasn't been shown yet.

### `Near(self)`
Handles the player getting near the outpost. It removes any far proximity events, sets up new near proximity events, and starts the tutorial timers.

### `SetupTutorialTimers(self)`
Sets up the initial state for the tutorial, showing the first message and setting up a timer to show subsequent messages.

### `Far(self)`
Handles the player moving away from the outpost. It hides any tutorial messages and sets up new far proximity events.

### `ShowOutpostTutorial(self)`
Displays the tutorial messages in sequence. It uses `MrxTutorialManager` to manage the display of each message and sets up a timer to show the next message.

### `Complete(self)`
Completes the outpost capture task. It marks the staging and defense layers for removal and adds the captured layer. It also updates statistics using `MrxStatsManager.IncreaseOutpostCapturedCounter`.

### `RemoveTutorialEvents(self)`
Removes all tutorial-related events and timers to clean up resources.

### `Cleanup(self)`
Cleans up the outpost contract task by deleting the outpost instance if it hasn't been captured or destroyed, removing tutorial events, and calling the base class's cleanup function.

### `GetOutpostConfig(self)`
Retrieves the outpost configuration from the task's config.

## Events
- Listens for `Event.ObjectProximity` to trigger proximity-based tutorials.
- Listens for custom event `NoProgressMade` to handle cases where no progress is made on the outpost capture.

## Notes for modders
- Ensure that `LoadAssets`, `Activated`, and `Cleanup` are called appropriately to manage the lifecycle of the outpost contract task.
- Customize outpost properties by modifying the configuration fields such as `sOutpostBldg`, `sCapturePt`, and `tDangerousBldgs`.
- Be aware of the tutorial sequence and adjust timing or messages if needed.
- Ensure that network synchronization is handled correctly for multiplayer scenarios.