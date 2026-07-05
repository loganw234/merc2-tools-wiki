---
title: MrxTaskObjectiveRelease
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjectiveAction
tags: [task, objective, release]
verified: true
verified_note: deeper pass — clarified this overrides MrxTaskObjectiveAction: _PrepTargets stubbed to no-op (prompts added on proximity instead), _TargetActioned chains to base then sets AI relations from parent tMaterielScale; noted _knTgtNearbyRadius=100 is a module constant; corrected the Events section (proximity events + inherited ContextAction, no "custom events")
---

# MrxTaskObjectiveRelease

*Module: mrxtaskobjectiverelease.lua*

## Overview
The `MrxTaskObjectiveRelease` module is a specific type of task objective that deals with the release of prisoners or controlled entities. It inherits from `MrxTaskObjectiveAction` and provides functionality to manage nearby targets, set their states, and adjust AI relations based on configuration settings.

## Inheritance
- Inherits from: `MrxTaskObjectiveAction`
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction)'s class-factory pattern**
(itself inherited from [`MrxTaskObjective`](mrxtaskobjective)/[`MrxTask`](mrxtask); see that page). Per-instance
field:
- `self._uFarTgtFilter` — a **copy** of the target filter (players removed) used to track which prisoners are
  currently *out of range*, so they can be re-armed with a release prompt when the player returns.

`_knTgtNearbyRadius = 100` is a **module-level constant** (the near/far proximity radius), not a per-instance
field.

## Functions
### `Activated(self)`
Called when the objective is activated. It calls the base class's `Activated` method and sets up a nearby event to monitor targets.

### `_PrepTargets(self)` *(override)*
**Overrides** [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction)'s version to an empty no-op — release
objectives do **not** slap a prompt on every target up front. Instead, prompts (`"[ContextAction.ReleasePrisoner]"`)
are added only to prisoners the player gets near, in `_TargetNearby`.

### `_TargetActioned(self, uActionerGuid, uActioneeGuid)` *(override)*
Chains to the base `MrxTaskObjectiveAction._TargetActioned` (which completes the part), then sets the freed
target `Human.SetState(..., "Upright", "Idle")` and, if the parent task's config has `tMaterielScale`, adds
an [`Ai`](../namespaces/ai) infraction against the relevant faction and turns that faction hostile toward the
freed prisoner — releasing prisoners has diplomatic consequences.

### `_GetShortDescription()`
Returns a short description of the objective, which is "[Generic.ObjectiveRelease]".

### `_CreateNearbyEvent(self)`
Creates an event that listens for nearby targets within a specified radius. It sets up a filter to exclude the player character and creates a persistent event to monitor proximity.

### `_TargetNearby(self, tGuids)`
Handles the detection of nearby targets. It adjusts AI relations, sets the target's state to "Subdued", adds a context action for releasing the prisoner, and removes the target from the nearby filter while setting up a faraway event.

### `_CreateFarawayEvent(self, uGuid)`
Creates an event that listens for targets moving beyond the specified radius. It adds the target back to the nearby filter when they move away.

### `_TargetFaraway(self, uGuid)`
Handles the detection of targets moving beyond the specified radius by adding them back to the nearby filter.

## Events
- **`Event.ObjectProximity`** — a **persistent** near event (`< _knTgtNearbyRadius`, i.e. 100) on
  `_uFarTgtFilter` → `_TargetNearby`, and a per-target far event (`> _knTgtNearbyRadius`) → `_TargetFaraway`.
  Together they toggle the release prompt as the player moves in and out of range.
- Plus the **inherited** `Event.ContextAction` / `Event.ObjectDeath` from
  [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction) — the release button press itself is that context
  action. There are no "custom events" here.

## Notes for modders
- **Release consequences come from the parent's `tMaterielScale`**, not this objective's own config — the
  faction relation/infraction changes in `_TargetActioned` read `self:GetConfig().oParent:GetConfig()`.
- Prisoners are set to `"Subdued"` on approach and `"Upright"` on release (`Human.SetState`); the prompt is
  `"[ContextAction.ReleasePrisoner]"`.
- Short description override: `"[Generic.ObjectiveRelease]"`. Icon/art are inherited from
  [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction) (action icons).