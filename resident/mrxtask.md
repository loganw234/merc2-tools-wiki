---
title: MrxTask
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [task, mission]
verified: true
verified_note: deeper pass -- re-confirmed every function/signature against source line-by-line (Create/Configure/Activate/Activated/Complete/Cancel/Cleanup, the dynamic_import->_ModuleLoaded->PreLoadAssets->LoadAssets->AssetsLoaded->Activated pipeline, and all child/state/save helpers); Instance pattern (class-factory by name/lineage, not per-uGuid), the identical cleanup of _CreateEvent/_CreatePersistentEvent handles, and the zero-argument fOnActivate/fOnComplete/fOnCancel call all still hold -- no changes needed. See the [Custom Contract deep dive](../deep-dives/custom-contract)
---

# MrxTask

*Module: mrxtask.lua*

## Overview
`MrxTask` is the base class nearly every mission/contract/objective in the
[Missions & Tasks](index) category builds on — [`MrxTaskMission`](mrxtaskmission) and
[`MrxTaskJob`](mrxtaskjob) both build on this directly. It provides a config-driven
latent→active→(completed|cancelled) state machine, parent/child task trees, dynamic module loading, and
automatic event cleanup.

**A working, confirmed-live example of using this API from outside a mission script**:
[`MrxCheatBootstrap`](mrxcheatbootstrap)'s `_DisplayTraverseDialog` walks the live task tree using exactly
the methods documented below (`:GetParent()`, `:GetChildren()`, `:IsActive()`, `:Complete()`, `:Cancel()`,
`:GetLineage()`) — read that function if you want to inspect or manipulate real mission state
programmatically rather than through the menu.

**Not the `Inheritable`/per-`uGuid` pattern** — tasks are identified by name and parent/child lineage
(`GetName`/`GetLineage`/`GetParent`), not by a world-object GUID. `Create(mModule, self)` is a class-style
factory: `setmetatable(self, {__index = mModule})`, no `tInstance` registry.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxLayerManager`, `MrxTaskState`, `MrxTimer`, `MrxUtil`

## Instance pattern
Class-style object (see Overview), not per-`uGuid`. Key fields, all set/managed internally rather than
meant to be poked directly:
- `_tConfig` — the task's configuration table, read/written via `Configure`/`GetConfig`, not directly.
- `_tChildren` — child tasks keyed by name.
- `_nState` — one of `MrxTaskState`'s latent/active/completed/cancelled constants (default latent if unset).
- `_tEvents` — handles for **every** event this task registered via `_CreateEvent`/`_CreatePersistentEvent`
  (see the correction below — both kinds land in the same table).
- `_oTimer` — an `MrxTimer` instance, only set if the task's config included `tTimerParams`/`nTimeLimit`.
- `_tSaveData` — whatever was passed to `Activate`/`SaveInstance`, used to restore state across saves.
- `_bCleanedUp` — set once `Cleanup` has run, gating it from running twice.

## Functions

### `Create(mModule, self)`
Builds a task instance with `mModule` as its metatable `__index` fallback (mirroring the general
prototype-inheritance pattern used across `resident/`, just without a `uGuid` registry).

### `Configure(self, tConfig)`
Merges `tConfig` into `self._tConfig`. While the task is **latent**, any key can be set, and
`tConfig.oParent` (if present) automatically registers this task as that parent's child. While the task is
**active**, only keys where `IsLiveConfigureable` returns true (`tOnActivate`/`fOnActivate`/
`tOnComplete`/`fOnComplete`/`tOnCancel`/`fOnCancel`) can be changed — anything else is rejected with a
debug log message, not a silent no-op. Once the active-branch merge is done, `Configure` calls
`self:ReinterpretConfig()` — **another empty no-op hook in this base class**, a place for a subclass to
react to a live reconfiguration rather than just letting the config table change silently underneath it.

### `Activate(self, tSaveData)` / `Activated(self)`
`Activate` resets state to latent (via `_ResetState`, a one-line wrapper around `_SetState`), optionally
restores save data, then either dynamically imports a module (`dynamic_import`, if `tConfig.sModuleName` is
set) or goes straight to `LoadAssets`.
`Activated` (called once assets finish loading) is what actually flips the task to the active state,
issues activate callbacks, and starts a timer if `tTimerParams`/`nTimeLimit` was configured — the timer's
default behavior on expiry is to call `self:Cancel()`.

### `_ModuleLoaded(self, mModule)` / `PreLoadAssets(self)` / `LoadAssets(self, tSaveData)` / `AssetsLoaded(self)` / `_IssueAssetsLoadedCallbacks(self)`
The full pipeline between `Activate` and `Activated`, one previously-undocumented step at a time:
`_ModuleLoaded` is `Activate`'s `dynamic_import` callback (called synchronously in the no-`sModuleName`
case too) — it re-points the task's metatable at the freshly-loaded module (subclass overrides start
applying from here on), initializes `_tEvents`, then calls `PreLoadAssets` followed by `LoadAssets`.
**`PreLoadAssets` is an empty no-op in this base class** — a hook point for a subclass to do setup work
before layers load, the same override pattern as `_GetRewards`/`_CanCompleteViaCheatMenu` further down this
page. `LoadAssets` loads `tConfig.tLayers` (if any) via `MrxLayerManager.Add`, or calls `AssetsLoaded`
immediately if there are none. `AssetsLoaded` runs `_IssueAssetsLoadedCallbacks` — which fires
`tConfig.tOnAssetsLoaded`/`fOnAssetsLoaded`, a separate callback pair from the activate/complete/cancel ones
covered below — and only then finally calls `Activated`.

### `Complete(self)` / `Cancel(self)`
Both are no-ops (with a debug log) if the task is already in that state. Otherwise: run `Cleanup`, set the
new state, and issue the corresponding callbacks (`tOnComplete`/`fOnComplete` or `tOnCancel`/`fOnCancel`).
Completing or cancelling a task recursively propagates the same state to all its children
(`_SetChildrenState`).

### `IsLatent(self)` / `IsActive(self)` / `IsCompleted(self)` / `IsCancelled(self)`
Simple boolean accessors, each just comparing `_GetState()` (the raw `MrxTaskState` constant) against the
matching named state. `_SetState(self, nState)` is the underlying mutator these read back from — it
`ASSERT`s the new state is valid, bails out if it's unchanged, and is what actually triggers
`_SetChildrenState` on a completed/cancelled transition.

### `Cleanup(self)`
Only runs if the task isn't latent and hasn't already been cleaned up. Detaches from its parent, deletes
**every** event in `_tEvents` (see the correction below), stops any timer, marks configured layers for
removal, dynamically un-imports the module if one was loaded, then recursively cleans up every child.

### `_CreateEvent(self, nEventId, tEventArgs, fCallback, tCallbackArgs)` / `_CreatePersistentEvent(...)`
Both register an event (via `Event.Create`/`Event.CreatePersistent` respectively) and **both** insert the
resulting handle into the same `self._tEvents` table. **A previous version of this page claimed persistent
events aren't automatically cleaned up — that's incorrect.** `Cleanup` iterates `_tEvents` and calls
`Event.Delete` on every handle in it regardless of which of these two functions created it, so both kinds
get torn down together when the task cleans up. Use `_CreatePersistentEvent` for the usual reason
(something that needs to survive whatever `Event.Create` alone wouldn't — see the
[Snippets](../snippets)/[Glossary](../glossary) coverage of the persistent/non-persistent distinction
elsewhere on this wiki), not out of concern for manual cleanup — the task handles that for you either way.

### `AddCallback(self, sConfigKey, fCallback, tData)`
Appends `{fCallback, tData}` to a config key that holds a *list* of callbacks (`tOnActivate`/`tOnComplete`/
`tOnCancel`), rather than replacing the single-function `fOnActivate`-style key. Both mechanisms exist
side-by-side — see `_IssueStateChangeCallbacks` below for how they're both invoked.

### `_IssueStateChangeCallbacks(self)`
On any real state transition (not latent), calls every callback in the matching `tOnActivate`/
`tOnComplete`/`tOnCancel` list (via `MrxUtil.CallWithOptionalArgs`), then also calls the single
`fOnActivate`/`fOnComplete`/`fOnCancel` function if one was configured. Both the list-based and
single-function config keys fire on the same transition, not one or the other.

**Confirmed: the single `fOnActivate`/`fOnComplete`/`fOnCancel` callback is called with zero arguments —
literally `fCallback()`, not even `self`.** A mission/task built without a real subclass (e.g. a bare
`MrxTask` config'd with `fOnActivate` directly, skipping `MrxTaskMission`/`MrxTaskContract` entirely) can't
rely on receiving its own instance this way — it has to look itself up by name instead, e.g.
`WifMissionFlow._tActiveMissions.<sMissionName>.oMission` for a mission unlocked via
[`WifMissionFlow.UnlockMission`](mrxmissionflow), confirmed populated synchronously before activation ever
fires. Confirmed live while building a custom contract with no `sModuleName`/subclass — see the
[Custom Contract deep dive](../deep-dives/custom-contract).

### `GetName(self)` / `GetTitle(self)` / `GetParent(self)` / `GetLineage(self)`
Read `sName`/`sTitle`/`oParent` from config. `GetLineage` walks up through `GetParent` repeatedly,
building a dotted string like `"root.child.grandchild"` — this is what shows up in the `Debug.Printf`
messages throughout this module, and what `MrxCheatBootstrap`'s task-tree browser displays.

### `CreateChild(self, tConfig)`
Convenience: creates a new task from the same module (`_THIS:Create()`), configures it with `tConfig`,
sets its parent to `self`, and activates it immediately — a one-line way to spawn a child task rather than
doing `Create`/`Configure`/`Activate` yourself.

### `_AddChild(self, oChild)` / `_RemoveChild(self, sChildName)` / `_AddChildren(self, tChildren)` / `GetChild(self, sChildName)`
The lower-level child-table operations `Configure`/`Cleanup`/`CreateChild` build on: `_AddChild` (called
automatically by `Configure` when `tConfig.oParent` is set) `ASSERT`s the name isn't already taken,
`_RemoveChild` (called by `Cleanup`) just clears the slot, `_AddChildren` is a bulk-add helper, and
`GetChild` looks up one specific child by name, as opposed to `GetChildren` returning the whole table.

### `_GetRewards(self)`
Returns `{nCash = 0, nFuel = 0}` by default — a hook point for subclasses (like
[`MrxTaskMission`](mrxtaskmission)) to override with real reward values.

### `_CanCompleteViaCheatMenu()`
Returns `true` by default — a hook a subclass could override to hide itself from
`MrxCheatBootstrap`'s task-tree "Complete"/"Cancel" options if completing it via the cheat menu wouldn't
make sense.

### `SaveInstance(self)` / `_GetSaveData(self)` / `_SetSaveData(self, tSaveData)`
Save-game plumbing — `SaveInstance` returns a copy of whatever was last set via `_SetSaveData`, plus the
current state, ready to be persisted and later handed back to `Activate`.

### `GetStub(self)` / `_SetTask(self, oTask)` / `GetTask(self)`
`GetStub`/`GetTask` both just return `self` by default in this base class — these exist as override points
for a subclass that wraps or delegates to a *different* underlying task object rather than being one
itself (`_SetTask` sets what `GetTask` would return, if overridden to do so).

## Events
This file doesn't itself subscribe to persistent engine-level events beyond what `_CreateEvent`/
`_CreatePersistentEvent` set up on behalf of whoever configures a task with `tTimerParams`. The lifecycle
here is driven by direct calls (`Activate`/`Complete`/`Cancel`) and the config-driven callback lists
(`tOnActivate`/`tOnComplete`/`tOnCancel`), not by the task base class listening for anything on its own.

## Notes for modders
- **Read `MrxCheatBootstrap._DisplayTraverseDialog` for a real, confirmed-working example** of walking a
  live task tree with this exact API — the fastest way to understand this module in practice rather than
  in the abstract.
- **`_CreateEvent` vs `_CreatePersistentEvent` doesn't affect cleanup** — both get torn down together by
  `Cleanup`. Pick based on the actual persistent/non-persistent event semantics you need, not cleanup
  concerns.
- **`Configure` silently rejects unknown keys on an active task** (logged, not thrown) — if a live
  reconfiguration isn't taking effect, check `IsLiveConfigureable` for whether that key is even eligible
  while active, rather than assuming a bug elsewhere.
- **`Complete`/`Cancel` cascade to every child task** — cancelling a parent task cancels its whole subtree,
  not just itself.
