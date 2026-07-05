---
title: MrxTaskJobVerifySet
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [mission, task]
verified: true
verified_note: 'deeper pass: confirmed all functions; documented the HVT capture/kill fanfare + Net.SendEvent_HVTFanfare,
  the cash-halving-on-kill (MrxRewardData.EnableCashRewardHalving), the MrxTaskObjectiveVerify child config
  (icon_verify_3_mc), and the Fiona verification VO; flagged _bPlayedVerificationVO as a module-level global
  masquerading as per-instance state; corrected Events; cross-linked MrxTaskObjectiveVerify/MrxRewardData.'
---

# MrxTaskJobVerifySet

*Module: mrxtaskjobverifyset.lua*

## Overview
The `MrxTaskJobVerifySet` module is a subclass of `MrxTaskJob` designed to handle mission tasks where players need to verify or capture specific high-value targets (HVTs). It manages the lifecycle of these verification tasks, including adding targets, handling events, and updating player notifications.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `MrxFactionManager`, `MrxUtil`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskJob`](mrxtaskjob)'s class-factory pattern** (itself inherited from
[`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general mechanism),
identified by name/lineage rather than a world-object GUID. Key fields:
- `_oObjective`: The objective associated with the verification task (a
  [`MrxTaskObjectiveVerify`](mrxtaskobjectiveverify)).
- `_sFactionId`: The faction ID for the task (set by `_SetFactionId`).
- `self._bPlayedNearVO`: per-instance guard so a per-target near-VO plays only once.

{: .warning }
> **`_bPlayedVerificationVO` is a module-level global, not `self._bPlayedVerificationVO`.** It's declared at
> file scope (`_bPlayedVerificationVO = false`) and read/written bare in `_PlayVerificationVO`, `LoadAssets`,
> and `SaveInstance` — but the field-name typo means `LoadAssets`/`SaveInstance` read `tSaveData.bPlayedVerificationVO`
> into the *global*, while a per-instance `self._bPlayedVerificationVO` (mentioned nowhere in the setters) is
> never actually populated. In practice only one verify-set job runs at a time so the shared global is
> harmless, but don't expect per-instance isolation of the "played the Fiona verification line" flag.

## Functions
### `_AddTarget(self, ...)`
Adds a target to the verification set. If the first argument is a table, it configures the target with various layers and properties. Otherwise, it calls the base class's `_AddTarget` method.

### `_Go(self, fCallback, tCallbackArgs)`
Creates the child [`MrxTaskObjectiveVerify`](mrxtaskobjectiveverify) (named `"VerifySet"`) over the named HVT
list, PDA icon `"icon_verify_3_mc"`, default desc `"[GurJob002.Objectives.001]"`, passing through
`sFactionId`. `fOnActivate` arms proximity/VO via the inherited `_CreateNearbyEvent` then runs `fCallback`.
The interesting logic is in **`fOnPartComplete(uGuid, bKilled)`**:
- Layer swap: removes the target's `sStagingLayer`, adds its `sVerifiedLayer` (via
  [`MrxLayerManager`](mrxlayermanager)).
- Fanfare: `Hud.EventFanfare:Commence` with `sType = "hvtcapture"` or `"hvtkill"` depending on `bKilled`,
  text prefixed by the faction inline icon; on the server it also fires `Net.SendEvent_HVTFanfare(...)` so
  clients show the same HVT fanfare.
- **Cash halving on kill:** if `bKilled`, wraps the `_TargetComplete` call in
  [`MrxRewardData.EnableCashRewardHalving(true)`](mrxrewarddata) … `EnableCashRewardHalving(false)` — so
  *killing* an HVT (vs. capturing) awards half the cash. This is the concrete "capture is worth more than
  kill" reward lever.

`fOnComplete`/`fOnCancel` → `Complete`/`Cancel`.

### `_SetFactionId(self, sFactionId)`
Sets the faction ID for the task.

### `_GetPerTargetLayerKeys()`
Returns a list of layer keys associated with each target.

### `_GetNearRadius()`
Returns the radius within which nearby events are triggered (150 units).

### `_GetFarRadius()`
Returns the radius beyond which far events are triggered (200 units).

### `_GetNearbyVoPlaybackMode()`
Returns a boolean indicating whether nearby voice-over playback is enabled.

### `_PlayVerificationVO(self)`
Plays Fiona's verification lines (`"Fiona.Misc.Verification01"`, 0.5 s gap, `"Fiona.Misc.Verification02"`) via
[`MrxVoSequence.Start`](mrxvosequence) at `knPriorityBounties`, guarded by the module-level
`_bPlayedVerificationVO` so it fires only once per session (see the Instance-pattern warning).

### `_NearVoComplete(self)`
Overrides the base: clears `self._bNearVoInProgress`, then schedules `_PlayVerificationVO` `1` second later
via `Event.TimerRelative` — so the generic "target nearby" VO is followed by Fiona's verification prompt.

### `_TargetNearby(self, uGuid)`
Handles events for targets that are nearby. If the target has a near VO sequence, it plays it; otherwise, it calls the base class's method.

### `LoadAssets(self, tSaveData)`
Loads saved data, including whether the verification voice-over has been played.

### `SaveInstance(self)`
Saves the current state of the instance, including whether the verification voice-over has been played.

## Events
No `Event.*` subscriptions of its own. Proximity events come from the inherited
[`MrxTaskJob._CreateNearbyEvent`](mrxtaskjob) (this class's `150`/`200` radii and `_GetNearbyVoPlaybackMode()`
= `true`, so nearby VO plays even when not free-roaming). `_NearVoComplete` uses a one-shot
`Event.TimerRelative`. The HVT fanfare on kill/capture is a `Hud.EventFanfare` + `Net.SendEvent_HVTFanfare`
call inside the objective's `fOnPartComplete` config callback — not an event listener.

## Notes for modders
- **Per-target config via the table form of `_AddTarget`:** `{sTarget=, vNearVoSequence=, sStagingLayer=,
  sDefenseLayer=, sPristineLayer=, sVerifiedLayer=, sMilestoneKey=}`. On verify, `sStagingLayer` is removed
  and `sVerifiedLayer` added.
- **Capture pays more than kill:** killing an HVT halves the cash reward
  ([`MrxRewardData.EnableCashRewardHalving`](mrxrewarddata) around the completion). If you want kill and
  capture to pay equally, that's the call to remove/override.
- `vNearVoSequence` per target plays a bespoke line when the player first nears that HVT (once, guarded by
  `self._bPlayedNearVO`); absent that, the shared nearby-VO + Fiona verification prompt plays instead.