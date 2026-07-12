---
title: ChiCon002
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# ChiCon002

## Overview
A China story contract: a three-pronged siege of an Oil Company base near Maracaibo. The player can
destroy the OC headquarters building, an OC supply depot (fifteen named building pieces), and a
three-segment bridge in any order; each objective is tracked independently through its own save flag
(`HQDestroyed_New`, `DepotDestroyed_New`, `BridgeDestroyed_New`), so a contract resumed mid-siege skips
objectives already completed rather than restarting. Each objective has a "spotted" VO (plays once the
target becomes visible from a watch region) and, while partially destroyed, a "missed" VO that nags the
player with a random reminder line every 45 seconds. Completing all three ends the contract.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `DangerousBuilding`, `MrxVoSequence`, `MrxSubtitle`, `MrxSupportData`, `MrxUtil`,
  `MrxHQManager`

## Instance pattern
A native `MrxTaskContract` subclass. The three save flags above are the primary state; standing event
handles (`uBridgeMissedEvent`, `uDepotMissedEvent`) are module-level globals cleared/reset as each
objective's state changes.

## Functions
### `LoadAssets(self, tSaveData)`
Removes the pre-mission layers and adds the siege layers, branching per-objective on the three save flags
so a resumed contract loads the correct pristine/destroyed/hostile layer variant for each of HQ, depot,
and bridge independently.

### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, sets the region atmosphere to `"warzonemar"`, disables OC HQ
respawn, and creates whichever of the three `MrxTaskObjectiveDestroy` children aren't already flagged
complete; arms the three "spotted" boundary triggers regardless of completion state.

### `_SetupVehiclePatrol(self, sActor, sTarget, sPriority)`
Arms a hibernation trigger that starts a vehicle's driver on a `PathMove` goal once it wakes. **No call
site found anywhere in this file.**

### `_StartPatrol(self, uActor, uTarget, sPriority)`
Issues the actual `Ai.Goal` PathMove call, one second after being scheduled. Only reachable via
`_SetupVehiclePatrol`, so also effectively unused in this file.

### `_CheckObjectiveCompletion(self)`
Completes the contract once all three save flags are set.

### `_HQHealthBar(self)`
Shows a health bar over the OC HQ building once the player enters a traffic-watch region, hiding it again
(and re-arming itself) when they leave a separate attack-watch region.

### `_BridgeSpottedBoundary(self)` / `_HQSpottedBoundary(self)` / `_DepotSpottedBoundary(self)`
Each arms a boundary-enter trigger on its own watch region that fires the matching `*SpottedVO` function.

### `_BridgeSpottedVO(self)` / `_HQSpottedVO(self)` / `_DepotSpottedVO(self)`
If the objective isn't already destroyed, checks whether any of its key pieces are currently visible; if
so, plays a one-time VO line and raises the action-level music, otherwise re-polls one second later.

### `_BridgeMissedVO(self)` / `_DepotMissedVO(self)`
Picks a random VO line from a short list and schedules it 45 seconds out — the recurring "you left this
unfinished" nag while an objective is partially destroyed.

### `_BridgeDestroyedVO(self)` / `_HQDestroyedVO(self)` / `_DepotDestroyedVO(self)`
Disables the relevant road intersections (bridge only) or stops the health bar (HQ only), sets the
objective's save flag, plays a VO line that varies depending on which other objectives are already done,
and records a checkpoint.

### `Cleanup(self)`
Stops the HQ health bar, marks the siege layers for removal, and calls the base
`MrxTaskContract.Cleanup`.

## Events
- `Event.Boundary` — two triggers toggle the HQ health bar on/off; three "spotted" triggers arm the
  visibility checks for bridge/HQ/depot.
- `Event.TimerRelative` — one-second repoll loops for each `*SpottedVO` while not yet visible; 45-second
  repeating nag loops for `*MissedVO`.
- `Event.ObjectHibernation` — used by the (unwired) `_SetupVehiclePatrol` helper.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Possible case-mismatch bug**: the file imports `MrxHQManager` (capital Q) but `Activated` calls
  `MrxHqManager.SetHqRespawn("OilHq", false)` (lowercase q) — a different global name under Lua's
  case-sensitive rules. Unless some other already-loaded script also defines a lowercase-`q`
  `MrxHqManager` global, this call would attempt to index `nil` every time `Activated` runs. Flagged here
  as observed directly in the source; whether it actually errors in a live session isn't something this
  file alone can confirm.
- **The three-independent-save-flag pattern** (`HQDestroyed_New`/`DepotDestroyed_New`/
  `BridgeDestroyed_New`, each checked in both `LoadAssets` and `Activated`) is a concrete, worked example of
  how the native contract system threads objective progress through the save file via `_GetFlag`/
  `_SetFlag` — exactly the save-coupling behavior [Contract.Register &
  Lifecycle](../contract-framework/register-and-lifecycle) cites as the reason `ContractFramework.lua`
  keeps its own contracts ephemeral instead.
- `_SetupVehiclePatrol`/`_StartPatrol` are unused in this file — likely leftover from an earlier draft or
  a shared template.
