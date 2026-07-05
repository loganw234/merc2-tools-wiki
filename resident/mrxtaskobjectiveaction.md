---
title: MrxTaskObjectiveAction
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective]
verified: true
verified_note: deeper pass — re-confirmed both events are Event.CreatePersistent (ContextAction id 0 + filter, and ObjectDeath) stored in _tEvents.uActionEvent/uDeathEvent; surfaced the default action label "[ContextAction.Talk]", the icon override strings, and the Pg.AddContextAction call; documented this as the base for Accept/Release
---

# MrxTaskObjectiveAction

*Module: mrxtaskobjectiveaction.lua*

## Overview
`MrxTaskObjectiveAction` is a concrete [`MrxTaskObjective`](mrxtaskobjective) where the player completes each
target by walking up and pressing the context-action button on it (a "Talk"/interact prompt). It attaches a
context action to every target, completes the part when the action fires, and cancels the part when the
target is destroyed. It is also the **base class** for
[`MrxTaskObjectiveAccept`](mrxtaskobjectiveaccept) (adds a Yes/No confirmation) and
[`MrxTaskObjectiveRelease`](mrxtaskobjectiverelease) (prisoner release).

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `MrxUtil`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields:
- `_tEvents`: Stores event handles for action and death events.
- `_uTgtObjFilter`: Filter used to identify target objects.

## Functions
### `Activated(self)`
Called when the task objective is activated. It initializes the base class, prepares target objects by setting context actions, and sets up persistent events to handle target interactions (`_TargetActioned`) and destruction (`_TargetDestroyed`).

### `_PrepTargets(self)`
Adds a context action to every target via `Pg.AddContextAction(uGuid, sActionLabel, 2, 0, 200, 0, 2)`. The
label comes from config `sActionLabel`, defaulting to `"[ContextAction.Talk]"`. **Overridable** — 
[`MrxTaskObjectiveRelease`](mrxtaskobjectiverelease) overrides this to a no-op and adds its prompts on
proximity instead.

### `_TargetActioned(self, uActionerGuid, uActioneeGuid)`
Handles the event when a target object is interacted with. It removes the context action from the target, updates the task state by removing the target if necessary, and marks the part of the task as complete for both the actor and the target.

### `_TargetDestroyed(self, uGuid)`
Handles the event when a target object is destroyed. It removes the context action from the target, updates the task state by removing the target if necessary, and cancels the part of the task.

### `Cleanup(self)`
Cleans up any remaining context actions on the target objects and calls the base class's cleanup method to ensure proper resource management.

### Overridden base hooks (icons / text / validity)
Each of these overrides the neutral [`MrxTaskObjective`](mrxtaskobjective) default:
- `_GetShortDescription()` → `"[Generic.ObjectiveAction]"`
- `_GetTargetRadarIcon()` → `"objective_action"`
- `_GetTargetPdaIcon(bOptional)` → `"icon_action_1_mc"` / `"icon_action_2_mc"`
- `_GetTargetGameSpaceIcon()` → `"HUD_objective_action"`
- `_IsValidTarget(uGuid)` → any-player/all-player GUIDs, else `Object.IsAlive(uGuid)` (dead targets are
  filtered out at setup)

## Events
Both are `Event.CreatePersistent` (created in `Activated`, stashed in `_tEvents` and torn down by
`Cleanup`/the base):
- **`Event.ContextAction`** — args `{0, self._uTgtObjFilter}` → `_TargetActioned` when the player interacts
  with a target.
- **`Event.ObjectDeath`** — args `{self._uTgtObjFilter}` → `_TargetDestroyed` when a target dies (cancels
  that part).

## Notes for modders
- **Change the interact prompt** with config `sActionLabel` (default `"[ContextAction.Talk]"`); it is
  applied to every target by `_PrepTargets`.
- **This is the class to subclass for "go press-button on X" objectives.** Override the `_Get*` hooks for
  new art/text; override `_TargetActioned` to gate completion (see
  [`MrxTaskObjectiveAccept`](mrxtaskobjectiveaccept)) or run side effects (see
  [`MrxTaskObjectiveRelease`](mrxtaskobjectiverelease)).
- `Cleanup` explicitly `Pg.RemoveContextAction`s every remaining target before deferring to the base — so a
  cancelled objective won't leave a dangling interact prompt in the world.