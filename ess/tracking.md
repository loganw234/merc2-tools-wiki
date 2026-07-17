---
title: Tracking & Cleanup
parent: Essentials (Ess)
nav_order: 4
---

# Tracking & Cleanup

## Overview

Three namespaces united by one problem: this engine is full of `Add.../Remove...` pairs — spawn an object,
create an event, add a radar objective, add a PDA blip, add a quality ref, add to a disposer, add a context
action — and **none of them has a native "clear everything I made" call**. Every one of these leaks if you
forget to hand-track its return value and call the matching `Remove...` yourself.

- **`Ess.Track`** — a single registry that accepts any of those handle types (or a plain teardown function)
  and tears the whole batch down in one call.
- **`Ess.Event`** — a thin `Event.Create` wrapper that logs failures instead of silently handing back a
  broken handle, and can register itself with a tracker in one extra argument.
- **`Ess.Save`** — a different kind of shared gate: the one place that suppresses savegames/autosaves while
  an ephemeral mode (like a sandboxed arena) is active, so two independent subsystems can't clobber each
  other's gate.

## Ess.Track

`Ess.Track` is, per its own source header, "the single most leak-prone shape on this engine, repeated
everywhere." The Contract Framework's own `task = {events={}, guids={}, markers={}, marks={}}` plus
`cleanupTask` is exactly this pattern, hand-rolled once per framework instead of shared — `Ess.Track` is
that shared implementation, generalized to every leak-prone pair this project has found.

`Ess.Track.new()` returns a tracker object. Every `:xxx()` method both **registers** a teardown for that
thing and **returns the value you gave it**, so you can wrap a spawn/creation call inline without an extra
local variable.

| Method | Signature | Tracks | Teardown call |
|---|---|---|---|
| `:add(closeFn)` | `add(closeFn) -> closeFn` | Any zero-arg function — the generic escape hatch for anything not covered below. | Calls `closeFn()` directly. |
| `:event(handle)` | `event(handle) -> handle` | An `Event.Create` handle. | `Event.Delete(handle)` |
| `:guid(uGuid)` | `guid(uGuid) -> uGuid` | A spawned object. | `Object.Remove(uGuid)` |
| `:marker(handle)` | `marker(handle) -> handle` | A raw `Marker.Add*()` handle. | `Marker.Remove(handle)` |
| `:radar(sName)` | `radar(sName) -> sName` | A `Hud.Radar:AddObjective({sName=...})` registration. | `Hud.Radar:RemoveObjective({sName=sName})` |
| `:pda(sName)` | `pda(sName) -> sName` | A `Pda.Map:AddBlip({sName=...})` registration. | `Pda.Map:RemoveBlip({sName=sName})` |
| `:qualityRef(uGuid, nQuality)` | `qualityRef(uGuid, nQuality) -> ref \| nil` | Calls `Object.AddQualityRef(uGuid, nQuality)` itself and tracks the result. | `Object.RemoveQualityRef(ref)` |
| `:disposer(uGuid, sCategory)` | `disposer(uGuid, sCategory) -> uGuid` | Calls `Object.AddToDisposer(uGuid, sCategory)` itself. | `Object.RemoveFromDisposer(uGuid)` — note this takes the **same `uGuid`**, not a separately-returned handle. |
| `:contextAction(uGuid, sLabelOrKey, ...)` | `contextAction(uGuid, sLabelOrKey, ...) -> uGuid` | Calls `Pg.AddContextAction(uGuid, sLabelOrKey, ...)` itself; `...` passes through whatever trailing args that call wants (confirmed to vary 2-8 args across real call sites). | `Pg.RemoveContextAction(uGuid)` — again the same `uGuid`, not a returned handle. |
| `:closeAll()` | `closeAll()` | — | Runs every registered teardown in **reverse-registration order**, each `pcall`-guarded, then clears the tracker. Safe to call more than once, and safe to keep using the tracker afterward — a fresh `:add()` after `:closeAll()` just starts a new batch. |

Two methods — `:qualityRef` and `:disposer`/`:contextAction` — actually *make* the underlying call for you
(unlike `:event`/`:guid`/`:marker`/`:radar`/`:pda`, which only track a handle you already produced
elsewhere). Read the argument order carefully: `:disposer` and `:contextAction` track by re-using the
original `uGuid` on teardown, since their native `Remove...` calls don't hand back a separate handle to
begin with.

### Worked example

The full method surface, composed into one batch (grounded in the confirmed signatures above — not every
call in this snippet comes from a single existing recipe, but every call matches a real, documented method):

```lua
local tr = Ess.Track.new()

-- things you created elsewhere, tracked by their handle/guid:
local car    = tr:guid(Ess.Object.spawn("Veyron", x, y, z))
local evt    = tr:event(Event.Create(Event.TimerRelative, { 10 }, function() end))
local blip   = tr:marker(Marker.AddBlip(car, "HUD_objective_action", 32, 255, 200, 0, 255, 2, 5, 175))
local rName  = tr:radar(car)
local pName  = tr:pda(car)

-- things Track itself creates AND tracks in one call:
local qref   = tr:qualityRef(car, 5)
tr:disposer(car, "vehicles")
tr:contextAction(car, "Enter Vehicle")

-- a generic teardown for anything else:
tr:add(function() Ess.Log("cleaning up my batch") end)

-- ... later, one call tears everything above down, in reverse order:
tr:closeAll()
```

This is exactly the pattern the Contract Framework's own task cleanup uses internally, and it's the real,
confirmed shape of `samples/recipes/track_lifecycles.lua` (which exercises `:guid`, `:event`, and `:add`
end to end — two spawned cars, a 10s timer that never gets the chance to fire, and a closer flag — then
proves `:closeAll()` actually ran every one of them):

```lua
local tr = Ess.Track.new()

local a = tr:guid(Ess.Object.spawn("Veyron", px + 6, py, pz + 4))
local b = tr:guid(Ess.Object.spawn("Veyron", px + 6, py, pz - 4))

tr:event(Ess.Event.on(Event.TimerRelative, { 10 }, function() end))

local closerRan = false
tr:add(function() closerRan = true end)

-- ... later:
tr:closeAll()   -- cars removed, timer deleted, closer fired -- in one line
```

**A tracked `:marker(handle)` is not the same thing as an `Ess.Mark` handle.** `Ess.Raw.Mark.world(...)`
and `Ess.Raw.Mark.worldDisc(...)` (see [Markers](mark)) return a raw `Marker.Add*` handle that `:marker()`
tracks directly — but `Ess.Mark.object(...)`/`Ess.Mark.zone(...)` return a *compound table* covering several
surfaces at once, which has its own teardown call, `Ess.Mark.clear(handle)`. To fold an `Ess.Mark` handle
into a tracker's batch, wrap it with `:add`:

```lua
local m = Ess.Easy.Mark.objective(uGuid)
tr:add(function() Ess.Mark.clear(m) end)
```

## Ess.Event

A thin wrapper around `Event.Create` so a bad call logs instead of silently returning a broken handle, and
so registering the result with an `Ess.Track` tracker is one extra argument instead of a separate line.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Event.on(eventType, args, cb, tracker)` | `on(eventType, args, cb, tracker) -> handle \| nil` | Wraps `Event.Create(eventType, args, cb)` in a `pcall`. On failure, logs via `Ess.Log` and returns `nil` instead of a broken handle. If `tracker` is passed, the handle is registered on it (`tracker:event(handle)`) automatically. |
| `Ess.Event.off(handle)` | `off(handle) -> bool` | `pcall`-guarded `Event.Delete(handle)`; returns whether it succeeded. |

`args`' shape must match whatever `eventType` expects — getting that shape wrong doesn't error, it just
silently never fires. Double-check against the engine's own event reference if a handler seems dead.

## Ess.Save

The one shared save-gate. Any subsystem that needs to suppress savegames/autosaves for the duration of an
ephemeral mode routes through this instead of touching `Pg.SaveGame` itself.

| Function | Signature | Notes |
|---|---|---|
| `Ess.Save.gate(sHolderKey)` | `gate(sHolderKey)` | Adds a holder — saves are suppressed while at least one holder is active. `sHolderKey` defaults to `"default"` if omitted. Idempotent per key: gating twice with the same key is one holder, so a single matching `ungate()` clears it. |
| `Ess.Save.ungate(sHolderKey)` | `ungate(sHolderKey)` | Removes a holder — saves resume once the *last* holder is gone. |
| `Ess.Save.isGated()` | `isGated() -> bool` | Are saves currently suppressed by anyone? |
| `Ess.Save.holders()` | `holders() -> {keys}` | Which holder keys are currently active, for diagnostics. |

Give each caller a distinct key (e.g. `"Ess.Layers"`, `"sandbox:myArena"`) so independent gates never
collide.

**Why this exists (a real, confirmed bug it fixes structurally):** before `Ess.Save`, two different
subsystems each gated saves their own way — one by stashing and swapping `Pg.SaveGame` directly, the other
by lazily installing an `Ess.Override.wrap` on its own first use. A specific interleaving (one mode begins,
then the other begins while the first is still active, then the first finishes) had the first mode's
finish reassign `Pg.SaveGame` back to its pre-begin value — silently discarding the second mode's freshly
installed wrap, leaving its save-gate permanently ineffective for the rest of the session. Two independent
owners of `Pg.SaveGame` was the root cause. `Ess.Save` fixes it by construction: the wrap around
`Pg.SaveGame` (and, where present, `Sys.RequestAutosave`/`Sys.ForceNextAutosave`) is installed **once**,
never uninstalled, and simply passes through when no holders are active — nobody reassigns `Pg.SaveGame`
directly again, so one gate-user can't clobber another's.

The installed wrap survives a world reload (`_installed` persists); the holder set does **not** — it resets
to empty on every `OnLoad` re-run, since a reload ends any ephemeral mode that was mid-flight and saves must
resume rather than stay stuck gated forever.

## See also

- [Essentials (Ess)](index) — the framework index.
- [Markers](mark) — `Ess.Mark`'s compound handles are the one common case that doesn't plug directly into
  `Ess.Track` without a wrapping `:add()`, as noted above.
- [Timing & Input](timing-input) — `Ess.Loop`, the other reload-safe registry pattern in this framework
  (keyed by string id rather than a tracker instance).
- [Encounter Toolkit](encounter-toolkit) — `Ess.Sandbox`/`Ess.Layers`, the real consumers of `Ess.Save`'s
  gate for ephemeral, save-clean gameplay modes.
