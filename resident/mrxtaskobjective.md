---
title: MrxTaskObjective
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTask
tags: [task, objective]
verified: true
verified_note: deeper pass — REMOVED a fabricated Events list (ObjectHibernation/ObjectDeath/PlayerJoined/PlayerLeft/Awake/OnDeactivate none exist here; the only real subscription is Event.TimerRelative for the initial-notes delay); corrected imports (MrxUtil + MrxGuiInterface + MrxVoSequence, inherits MrxTask); surfaced the blip texture/size constants and message-type/icon strings; corrected that _compare is a real comparator (a[2] < b[2]), not a decompiler artifact
---

# MrxTaskObjective

*Module: mrxtaskobjective.lua*

## Overview
`MrxTaskObjective` is the base class for a single trackable objective inside a mission — the thing that
draws a blip on the radar/PDA/world, prints the "New objective / … / Complete" HUD messages, and counts
progress toward a quota. Every concrete objective type (`MrxTaskObjectiveDestroy`,
`…Deliver`, `…Protect`, `…Verify`, `…CaptureOutpost`, `…EnterVehicle`, `…Action` and its
`…Accept`/`…Release` subclasses) inherits from this and overrides a handful of hooks — see the
[Missions & Tasks](index) index. It extends [`MrxTask`](mrxtask) and leans heavily on
[`MrxGuiInterface`](mrxguiinterface) for the on-screen messages, the `Hud.Radar`/`Pda.Map`/`Marker`
namespaces for the three blip surfaces, and [`ObjectFilter`](../namespaces/object) to pick target objects.

<details class="lua101" markdown="1">
<summary>New to Lua? What is a "quota" here?</summary>
An objective can have several targets (e.g. "destroy 3 tanks"). `_nTotal` is how many targets it found,
`_nQuota` is how many you must finish (defaults to `_nTotal`, or a config `nQuota`), and `_nCompleted`
counts finished parts. Subclasses call `CompletePart`/`CancelPart` per target; when `_nCompleted`
reaches `_nQuota` the whole objective auto-`Complete`s.
</details>

## Inheritance
- Inherits from: [`MrxTask`](mrxtask)
- Imports: `MrxUtil`, [`MrxGuiInterface`](mrxguiinterface), [`MrxVoSequence`](mrxvosequence) (and, via
  `MrxTask`, `MrxGui`)

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTask`](mrxtask)'s class-factory pattern** (see that page), identified by
name/lineage rather than a world-object GUID. Per-instance fields, all initialized in `Activated`:
- `_tEvents` — event handles (inherited plumbing; subclasses stash their `Event.CreatePersistent` handles
  here by name).
- `_tTargets` — per-target display bookkeeping keyed by target `uGuid` (`bStatus`, `bSuppressDsp`,
  `bDisplay`, `sType`, `uMarkerGuid`, …).
- `_nCompleted` / `_nCancelled` / `_nQuota` / `_nTotal` — progress counters (see the quota box above).
- `_uTgtObjFilter` — the [`ObjectFilter`](../namespaces/object) that selects this objective's targets.
- `_bDspBlpRdr` / `_bDspBlpPda` / `_bDspBlpWld` — enable flags for the radar, PDA and world blip surfaces.
- `_bDspMsgAdd` / `_bDspMsgUpd` / `_bDspMsgCpl` / `_bDspMsgCcl` — enable flags for the add/update/complete/
  cancel HUD messages.
- `_bDspDescPda` — whether the PDA shows this objective's text description.
- `_bDspBlpSticky` — radar-blip "sticky" flag, seeded from config `bTrackOnActivate` (default `true`).

## Module constants & tunables
- `_knMarkerYClampDistance = 32` — **module-local** vertical clamp distance passed to `Marker.AddBlip` for
  every world blip (not a per-instance field).
- Default blip look, when a subclass/config doesn't override it (all confirmed in `_BuildRadarBlipConfig`
  / `_BuildPdaBlipConfig` / `_RefreshTargetDisplay`):
  - **Radar:** texture `"objective_action"` at `8`×`8` (or the icon returned by `_GetTargetRadarIcon` at
    `10.666667`×`10.666667`); sort order `5` (primary) / `6` (optional).
  - **PDA:** texture `"icon_yellow_mc"` fallback, or `_GetTargetPdaIcon` → `"icon_action_1_mc"` /
    `"icon_action_2_mc"`; sort order `2` (primary) / `3` (optional).
  - **World:** icon `"HUD_objective_action"`, size `32`, near/far draw distances default `5`/`175`
    (config `nDspBlpWldNearDist` / `nDspBlpWldFarDist`).
- `PulsateRadarBlip` animates a blip to `12`×`12` at speed `20`; `Activated` pulses for `5` s and schedules
  `_InitialNotesComplete` `5.5` s later.
- `GetInlineIcon` → `"[objaction]"` (primary) / `"[objaction2]"` (optional); `_GetShortDescription` →
  `"NULL"` (base placeholder, overridden by every real subclass).

## Functions

### `Activated(self)`
Resets the counters/tables, reads config, builds the `_uTgtObjFilter` (either taken from config or created
from `sTgtLabelFilter` + `vTgtInclude`/`vTgtExclude`), calls `_SetupTargets`, refreshes all displays, then
prints the "add" message (via `_PrintObjectiveMessage`, optionally after a `vVoSeqOnAdd` voice sequence).
Finally calls `MrxTask.Activated(self)` and, if targets were configured, registers
`DisplayTextInSatelliteMode` with `MrxGui`. The only event this base class itself creates is a
`Event.TimerRelative` (5.5 s) that fires `_InitialNotesComplete`.

### `_InitialNotesComplete(self)`
Fires the config's `tOnInitialNotesComplete` / `fOnInitialNotesComplete` callbacks once the opening
message/VO has finished. **Overridable hook** for a mod that wants to run logic only after the intro plays.

### `Complete(self)` / `Cancel(self)`
Overrides of [`MrxTask`](mrxtask)'s versions: same "already in that state?" guard, `Cleanup`, `_SetState`,
`_IssueStateChangeCallbacks` — **plus** a call to `GetMissionAncestor():RefreshPdaDisplay()` so the mission's
PDA entry updates when this objective finishes. Concrete subclasses do not usually override these; they call
`CompletePart`/`CancelPart` instead.

### `CompletePart(self, ...)` / `CancelPart(self, ...)`
The per-target progress API subclasses actually call. `CompletePart` increments `_nCompleted`, fires
`tOnPartComplete`/`fOnPartComplete`, optionally adds `nAddTime` to the timer, picks a message type
(`upd`/`cpl`, or the `bounty`/`bonus`/`collectible` variants), prints it, refreshes the PDA, and calls
`Complete()` once the quota is met. `CancelPart` increments `_nCancelled`, fires the part-cancel callbacks,
and calls `Cancel()` once the remaining live targets can no longer meet the quota
(`_nQuota > _nTotal - _nCancelled`).

### `IsQuotaMet(self)`
`self._nCompleted == self._nQuota`.

### `Cleanup(self)`
Stops an in-flight `vVoSeqOnAdd` sequence, drops the target filter, recursively clears `_tEvents` via
`_ClearEventTable`, turns off all target displays, removes the objective's GUI info, then defers to
`MrxTask.Cleanup(self)`.

### `_ClearEventTable(tEvents)`
Recursively `Event.Delete`s a (possibly nested) table of handles — subclasses store event handles both flat
and per-target, so this walks both.

### `IsLiveConfigureable(self, sConfigKey)`
Extends the base with display/quota/part-callback keys (`nQuota`, `bDsp*`, `tOnPartComplete`, …) that may be
changed on an already-active objective; falls back to `MrxTask.IsLiveConfigureable` for the rest.

### `ReinterpretConfig(self)`
Override of the base no-op: re-applies display settings from config and re-marks every included (non-player)
target as active, then refreshes displays. This is what makes a live `Configure` of an active objective take
visual effect.

### Target-set functions
- `_SetupTargets(self)` — counts targets from the filter (or `1` for a co-op player filter), marks each
  active, and sets `_nQuota` (config `nQuota` overrides).
- `RemoveTarget(self, uGuid)` — excludes a GUID from the filter and clears its status (how subclasses drop a
  finished/dead target).
- `_SetTargetStatus(self, uGuid, bOn, sType)` / `_SetAllTargetStatus(self, bOn)` — set a target's live
  status (and optional `sType`, e.g. `"destination"`) and refresh its blip.
- `GetTargetObjectFilter(self)` — returns `_uTgtObjFilter`.
- `EnableTracking(self, bEnable)` — toggles the sticky flag and, when enabling, re-pulses and re-prints the
  "add" message.

### Display functions
- `_SetDisplaySettingsFromConfig(self)` — reads `bDsp`/`bDspBlp`/`bDspMsg`/`bDspDescPda` (all default
  `true`) and pushes them into the blip/message/description toggles.
- `_ToggleBlipDisplay` / `_SetBlipDisplay` / `_ToggleMsgDisplay` / `_SetMsgDisplay` /
  `_SetDescPdaDisplay` — the low-level setters behind the `_bDsp*` flags.
- `_SetTargetDisplay(self, uGuid, bOn, bPulsate)` / `_SetAllTargetsDisplay(self, bOn)` — suppress/unsuppress
  a target's blip (optionally pulsing it).
- `_RefreshTargetDisplay(self, uGuid)` — the workhorse: adds/updates/removes the radar (`Hud.Radar`), world
  (`Marker.AddBlip`) and PDA (`Pda.Map`) blips for one target based on its status flags, and mirrors them to
  clients via `Net.SendEvent_*` when `Net.IsServer()`.
- `_BuildRadarBlipConfig(self, uGuid)` / `_BuildPdaBlipConfig(self, uGuid)` — build the arg tables (textures,
  colors, sort order) `_RefreshTargetDisplay` passes to the HUD/PDA (see constants above).
- `_RefreshAllTargetDisplay(self)` / `RefreshPdaDisplay(self)` — refresh every target's blip / re-add every
  PDA blip.
- `PulsateRadarBlips(self, nDuration)` / `PulsateRadarBlip(uGuid, nDuration)` — animate blip size to draw the
  eye (`Hud.Radar:AnimateObjectiveSize`).
- `_compare(a, b)` — a small sort comparator returning `a[2] < b[2]`. **Not a decompiler artifact** — it is a
  real function (though nothing in this file's visible logic calls it).

### Message / description functions
- `_PrintObjectiveMessage(self, sMsgType, fCallback, tCallbackArgs)` — routes an objective message
  (`add`/`upd`/`cpl`/`ccl` and their `bonus_`/`bty_`/`collectible_` variants) through
  `MrxGuiInterface.DisplayObjectiveMessage`, honoring the matching `_bDspMsg*` flag. **Overridable** — some
  subclasses (e.g. [`MrxTaskObjectiveAccept`](mrxtaskobjectiveaccept)) stub it to suppress messaging.
- `GetDescription(self, bPrependInlineIcon)` / `GetShortDescription(self)` /
  `GetObjectiveDescription(sObjDesc, nCompleted, nQuota, sMsgType)` — build the displayed text, appending an
  `(n/quota)` progress suffix.
- `GetDisplayDescription(self)` — returns `_bDspDescPda` (whether the PDA shows the description);
  [`MrxTaskMission`](mrxtaskmission)'s PDA walk checks this.
- `GetProgressQuota(self)` / `GetProgressCompleted(self)` — `_nQuota` / `_nCompleted`.
- `GetInlineIcon(self)` — inline-icon token (`"[objaction]"` / `"[objaction2]"`), overridden per subclass.

### `GetMissionAncestor(self)` / `_UpdateMissionInPda(self)`
`GetMissionAncestor` walks up `GetParent()` until it finds a task that has a `GetMissionId` method (i.e. a
[`MrxTaskMission`](mrxtaskmission)); `_UpdateMissionInPda` calls that ancestor's `RefreshPdaDisplay`. This is
how a leaf objective gets itself redrawn on the mission's PDA panel.

### Overridable "get" hooks (the subclass customization surface)
These plain (non-`local`) functions all return neutral base defaults and are the exact override points every
concrete objective uses to swap in its own icons/text/validation:
- `_GetShortDescription()` → `"NULL"`
- `_GetTargetBlipColor(bOptional)` → primary vs. secondary objective RGB (from `MrxUtil`)
- `_GetJust2DCheckNeeded()` → `false`
- `_GetTargetRadarIcon()` → `nil`; `_GetTargetPdaIcon(bOptional)` → `"icon_action_1_mc"`/`"icon_action_2_mc"`;
  `_GetTargetGameSpaceIcon()` → `nil`
- `_IsValidTarget(uGuid)` → `true`
- `DisplayTextInSatelliteMode(tObjectives, uGuid)` — returns the satellite-mode label for a target, prefixed
  `"[objt]"` / `"[2ndobjt]"`.

## Events
- **`Event.TimerRelative`** — the only subscription this base class creates itself: a `5.5`-second timer in
  `Activated` that calls `_InitialNotesComplete` after the opening message/VO. Registered via the inherited
  `_CreateEvent`, so it is cleaned up automatically.

Everything else driving an objective's progress is created by the **subclasses** (e.g.
`Event.ObjectDeath`, `Event.ContextAction`, `Event.ObjectProximity`) — see each subclass page. `Activated`
itself is an engine lifecycle call, **not** an event subscription.

{: .warning }
> A previous version of this page listed `Event.ObjectHibernation`, `Event.ObjectDeath`,
> `Event.PlayerJoined`/`Event.PlayerLeft`, and `Awake`/`OnDeactivate` callbacks here. **None of those exist
> in this file** — they were fabricated. Only `Event.TimerRelative` is real at this level.

## Notes for modders
- **The subclass customization surface is the `_Get*` hooks**, not the display machinery. To make a new
  objective type, inherit this and override `_GetShortDescription`, the three `_Get*Icon` functions,
  `GetInlineIcon`, and `_IsValidTarget` — then wire your own gameplay events in `Activated` and call
  `CompletePart`/`CancelPart`. Every shipped subclass follows exactly this shape.
- **Blip look is config-overridable without subclassing:** `sDspBlpRdrIcon` / `sDspBlpPdaIcon` /
  `sDspBlpWldIcon`, `nDspBlpWldNearDist` / `nDspBlpWldFarDist`, `nSortOrder`, and `bOptional` (which flips
  colors and sort order) all feed `_BuildRadarBlipConfig` / `_BuildPdaBlipConfig` / `_RefreshTargetDisplay`.
- **Suppress messaging/blips per objective** with the `bDsp` family (`bDsp`, `bDspBlp`, `bDspMsg`,
  `bDspBlpRdr`/`Pda`/`Wld`, `bDspMsgAdd`/`Upd`/`Cpl`/`Ccl`, `bDspDescPda`) — all default `true`, all
  live-configurable on an active objective.
- **Progress messages** come out as `[objt]…`-style tokens through `MrxGuiInterface.DisplayObjectiveMessage`;
  the `(n/quota)` suffix only appears when `nQuota > 1` or there's a positive count with an open-ended quota.
