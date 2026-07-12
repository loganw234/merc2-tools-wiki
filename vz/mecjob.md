---
title: MecJob
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskJob
tags: [job]
verified: false
---

# MecJob

## Overview
`MecJob` is a **local base class defined in this corpus, not a native engine class** — it's `mecjob.lua`'s
own shared template for "deliver a specific damaged vehicle to the mechanic's garage" side jobs, built on
top of the native [`MrxTaskJob`](../resident/mrxtaskjob). [`MecJob001`](mecjob001),
[`MecJob002`](mecjob002), and [`MecJob003`](mecjob003) all subclass this file directly, and each only
supplies a different target-vehicle label/image/VO/health threshold in its own `Activated` — almost all of
the actual job logic (finding the right vehicle, delivering it, garage-door choreography, low-health/
wrong-vehicle nagging, the completion/cancel fanfare) lives here in `MecJob` itself.

## Inheritance
- Inherits from: [`MrxTaskJob`](../resident/mrxtaskjob) (→ [`MrxTaskMission`](../resident/mrxtaskmission)
  → [`MrxTask`](../resident/mrxtask))
- Imports: [`MrxGuiHudMessage`](../resident/mrxguihudmessage),
  [`MrxSoundCategories`](../resident/mrxsoundcategories), [`MrxMusic`](../resident/mrxmusic),
  [`MrxVoSequence`](../resident/mrxvosequence)

## Instance pattern
Native task-framework subclass (`self`-based). Per-`self` fields fall into two groups: ones a subclass is
expected to set in its own `Activated` before calling `MecJob.Activated(self)` (`sVehImg`, `sVehLabel`,
`sObjText`, `iMinHealth`, `sIntro`, `sWrongVeh`, `sRightVeh`, and optionally `sPropVehTemplate`), and ones
`MecJob` itself manages (`inRegion`/`outRegion`/`garage`, `uVehicle` — the delivered vehicle once found,
`objFilterVehFound`, `bFirstWrongVehWarning`, `bPlayingVO`).

## Functions

### `LoadAssets(self, tSaveData)`
Adds `vz_state_gua_upperclass_pristine`/`Vz_State_MecJob` then calls `AssetsLoaded`.

### `AssetsLoaded(self)`
Overrides the framework default: calls `_IssueAssetsLoadedCallbacks()` itself (as the base
[`MrxTask`](../resident/mrxtask) version would), but instead of calling `Activated` immediately, delays it
2 seconds via `Event.TimerRelative`.

### `Activated(self)`
Sets the 4 stock wrong-vehicle/low-health VO line tables and messages, resolves the garage/in/out regions,
calls `MrxTaskJob.Activated(self)` (super call), removes and (if `sPropVehTemplate` is set) respawns a
"damaged vehicle" prop at `mc001.propVehicle`, watches the garage for death (→ `_GarageDestroyed`), then
closes the gate (`_PlayerOutside`) and calls `_SetupJob`.

### `_SetupJob(self)`
Displays the target-vehicle reference image to both players (`_DisplayVehicleImg`), creates the delivery
objective (`_CreateDeliverObjective`), and arms an `ObjectFilter` (matching `self.sVehLabel`) watching for
any vehicle with that label to be entered — the "wrong vehicle" detection hook (`_VehicleFound`).

### `_CreateDeliverObjective(self)`
Creates the `MrxTaskObjectiveDeliver` ([`MrxTaskObjectiveDeliver`](../resident/mrxtaskobjectivedeliver))
child (label-filtered, not GUID-filtered, so any vehicle matching `sVehLabel` counts) with
`fEvaluateTarget` wired to `_EvaluateDeliveryTarget`. On completion, plays the exit-garage VO, calls
`_ExitGarage`, and arms `_DeliveryTargetDestroyedBeforeExitingEvent`.

### `_EvaluateDeliveryTarget(self, uGuid)`
The delivery objective's target-acceptance gate: rejects AI-driven vehicles outright; for a
player-driven one, accepts it only if it both has the right label *and* meets `iMinHealth` (playing a
low-health VO otherwise), and plays a wrong-vehicle warning (first time a dedicated line, afterward a
random one from `tMsgWrongVeh`) if the label doesn't match at all.

### `_VehicleFound(self)`
Plays the "right vehicle" VO line once the label-matching `ObjectFilter` sees a player enter a matching
vehicle (this fires independently of, and earlier than, the delivery objective's own acceptance check).

### `_GarageDestroyed(self)`
Plays the garage-destroyed VO and cancels the job.

### `_DeliveryTargetDestroyedBeforeExitingEvent(self)` / `_DeliveryTargetDestroyedBeforeExiting(self)`
Watches the found vehicle for death while the player is still inside the garage region; if it dies, tears
down the door-trigger event, plays a low-health VO line, and re-creates the delivery objective (the
vehicle's gone, so the player has to bring a fresh one).

### `_PlayerOutside(self)` / `_PlayerInside(self, uPCharacter)` / `_ExitGarage(self)` / `_VehicleDelivered(self)`
The same closed/open/closed gate choreography pattern used in [`MecCon001`](meccon001)'s delivery
objective, ending in `_VehicleDelivered`: if the vehicle is alive and actually inside the garage, closes
the gate and waits for `"gateFullyClosed"`/`"gateStuck"`/a `"MedevacComplete"` script event to clean up and
complete; otherwise re-arms the objective and re-opens for another attempt. `_PlayerOutside` also arms
`_CleanupVehicle` early if a vehicle was already found, in case it needs cleaning up before the player even
re-enters.

### `_CleanupVehicle(self, fCallback)`
Shared teardown: bails out (returns `false`) if the vehicle is outside the garage region or still has a
player-controlled rider aboard; otherwise removes it, clears `self.uVehicle`, and (if provided) runs
`fCallback`.

### `_PlayRandomVO(self, tVOs)` / `_PlayOneVO(self, sLine)`
`_PlayOneVO` guards against overlapping VO with `self.bPlayingVO` and clears the flag on completion;
`_PlayRandomVO` just picks a random entry from a table and defers to it.

### `_DisplayVehicleImg(sImg, uPlayer)`
Module-level (no `self`) one-line wrapper around `MrxGuiHudMessage.ShowMessage` showing the
target-vehicle reference photo at a fixed size/position.

### `Complete(self)`
Builds player-name strings, gets the job's reward config, and shows the `Hud.Fanfare` completion banner
(`sType = "mission"`), fading the fanfare sound category in/out around it; the actual completion
(`MrxTaskMission.Complete(self)`) only runs from the fanfare's own callback.

### `Cancel(self)`
Same fanfare pattern as `Complete`, but for cancellation — notably references a bare `bRetryable` that is
**never assigned anywhere in this file** (confirmed by direct search; a stray global, not a real
per-instance flag), so `bAllowRetry` in the fanfare config is effectively always `nil`/falsy here. Also
cancels the *parent* task (`self:GetParent():Cancel()`) from the fanfare callback, not just this job.

### `Cleanup(self)`
Closes the garage gate, clears `objFilterVehFound`, and calls `MrxTaskJob.Cleanup(self)`.

### `CreateChild(self, tConfig)`
Overrides the inherited `CreateChild` to call `MrxTaskMission.CreateChild(self, tConfig)` directly rather
than [`MrxTaskJob`](../resident/mrxtaskjob)'s own `CreateChild` (its immediate parent). Since
`MrxTaskMission` doesn't define its own `CreateChild`, this ends up resolving to the generic
[`MrxTask.CreateChild`](../resident/mrxtask) — effectively opting `MecJob`'s single delivery-objective
child out of whatever `MrxTaskJob`-specific child-creation behavior its direct parent would otherwise add.

## Events
- `Event.ObjectDeath` — garage destruction, and the found vehicle dying before the player exits with it.
- `Event.ObjectInSeat` — the label-matching `ObjectFilter` watch for "wrong/right vehicle entered".
- `Event.Boundary` — the garage in/out region door choreography.
- `Event.ObjectPhysicsEvent` — `"gateFullyClosed"`/`"gateStuck"` gate-state watches.
- `Event.ScriptEvent` — `"MedevacComplete"`, an alternate path to vehicle cleanup/completion.
- `Event.TimerRelative` — the 2-second `AssetsLoaded` → `Activated` delay.

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system (specifically the `MrxTaskJob`
  branch of it), not [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- **This is the file to read to understand any `MecJob00N` subclass** — the subclasses only ever set
  identity/config fields before calling `MecJob.Activated(self)`; every function above is shared.
- `Cancel`'s reference to an unassigned `bRetryable` global is worth knowing about if you're tracing why a
  cancelled mechanic job never seems to offer a retry option.
- `_EvaluateDeliveryTarget` and `_VehicleFound` are two independent checks on the same
  `ObjectFilter`/objective pair — a modder adding a 4th job on this template should keep both label checks
  (`sVehLabel`) consistent between them.
