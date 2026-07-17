---
title: Contract Engine
parent: Essentials (Ess)
nav_order: 12
---

# Contract Engine

## Overview

`Ess.Contract` (`80_contract.lua` + `81_contract_objectives.lua` + `82_contract_encounter.lua`) is the native
port of the standalone [Contract Framework](../contract-framework/) — a save-safe, **ephemeral**
custom-mission engine. The source header states the modder API is "unchanged from ContractFramework.lua,
just under `Ess.Contract` now": the same `Register`/`Accept`/`Abort`/`Status` lifecycle, the same 16
objective builders, the same `def.support`/`def.triggers`/`def.relations`/`def.units`/`def.waypoints`
vocabulary. See [Contract Framework](../contract-framework/) and its children — in particular
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) and
[Objectives Reference](../contract-framework/objectives) — for the deep-dive on all of that; this page
focuses on what's the same at a glance, and calls out what's genuinely new or restructured under `Ess`.

**Why it's save-safe** (unchanged from the original): the native contract system corrupts saves because it
registers into `WifMissionData`, serializes `MrxTask` nodes *into* the save, and drives missions through
`dynamic_import` + `mrxbriefing` + the `MrxState` load gate. `Ess.Contract` touches none of that — a
contract is an ephemeral runtime object built only from safe primitives (`Pg.Spawn` / `Event.*` / `Object.*`
/ `MrxPmc`). It never writes to the save, so it can't corrupt one. The tradeoff, also unchanged: a contract
does not survive a save/reload — it's simply re-offered on the next level load.

The engine is split across three files:

- **`80_contract.lua`** — the registry, the runtime engine (task/instance bookkeeping, the sequential/
  parallel objective runner), `Register`/`Accept`/`Abort`/`Status`, and the objective builder functions
  (`.Destroy`, `.Reach`, etc. — friendly sugar over the internal objective shape).
- **`81_contract_objectives.lua`** — the 16 objective-type handlers (`C.tHandlers`).
- **`82_contract_encounter.lua`** — the relations/support-call-in/AI-order/trigger subsystem glue.

## Lifecycle: `Register` / `Accept` / `Abort` / `Status`

```lua
Ess.Contract.Register{
  id = "my_contract", title = "My Contract", briefing = "...",
  reward = { cash = 50000, fuel = 20 },
  start  = { x = 0, y = 0, z = 0, yaw = 0 },
  objectives = {
    Ess.Contract.Destroy{ desc = "Destroy 3 cars" },
    Ess.Contract.Reach{ desc = "Reach the drop-off", radius = 12 },
  },
  onComplete = function() end,
  onFail     = function() end,
}
Ess.Contract.Accept("my_contract")
```

`Ess.Contract.Register(def)`, `Ess.Contract.Accept(idOrDef)`, `Ess.Contract.Abort()`, and
`Ess.Contract.Status()` behave exactly as documented on
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) — same field set
(`id`/`title`/`briefing`/`category`/`reward`/`start`/`objectives`/`mode`/`timeLimit`/`fail`/`relations`/
`units`/`waypoints`/`support`/`triggers`/`intro`/`fanfareType`/`fanfare`/`onComplete`/`onFail`/`fResolve`/
`onBegin`/`hideTracker`), same `Status()` shape ({% raw %}`{ finished, progress, timeLeft, objectives = {{done=},
...} }`{% endraw %}), same co-op gate (`Accept` checks the **native** `Net.IsMultiplayer()`/`Net.IsClient()` directly,
not `Ess.Net`'s own `IsCoop`/`IsClient` helpers — see [Networking](net) for why that distinction matters:
`Net.IsClient()` can read `true` in single-player too, which would silently no-op every accept if gated on
that alone). `Ess.Contract.List()` returns the registry array; `Ess.Contract.All` is an alias of it kept
specifically for the [Contract Board](../contract-framework/contract-board)'s own detection convention.

Two `def` fields are **new**, not present in the original `ContractFramework.lua`:

| Field | Purpose |
|---|---|
| `def.sandbox` | `true` or `{ providers = {"layers", ...}, opts = {} }`. Wraps the whole contract in an [`Ess.Sandbox`](encounter-toolkit) for its duration: saves are gated and a layer snapshot/restore runs automatically, begun at `Accept` (before the intro) and finished in `_finish` (complete/fail/abort). Use it for a mission that destroys a major, persistent set piece — the destruction lives only in memory and never serializes. `true` defaults to the `"layers"` provider alone. |
| `def.cinematic` | Inline [`Ess.Cinematic`](cinematic) steps, `{ steps=, opts= }`, or a named-id string (`Ess.Cinematic.define`'d). Plays **after** heroes are placed (`def.start`) and relations are applied, **before** objectives begin — the objective list waits for it to finish (or be ESC-skipped). Fully guarded: if the cinematic can't start, the mission begins directly instead of hanging with no objectives running. A mid-mission cutscene is a `support` entry instead (`effect = "cinematic"`), not this field. |

## What else changed under the hood

The modder-facing objective builders and `def` shape are unchanged, but the implementation underneath picked
up several fixes and a structural rebuild on top of the now-standalone Encounter Toolkit namespaces:

- **Built on `Ess.AIOrders` / `Ess.Relations` / `Ess.Triggers` / `Ess.Sandbox`** instead of re-hand-rolling
  that logic a third time inside the contract engine — see [Encounter Toolkit](encounter-toolkit) below.
- **A CTD guard on every spawn.** A blank/whitespace `Pg.Spawn` template string hard-crashes the engine (an
  empty name resolves to a null asset in native C++), and `pcall` can't catch a native crash — only a Lua
  error. Every `Pg.Spawn` call site in the objective/support system now goes through an internal
  `safeSpawn()` that rejects a blank template before ever reaching `Pg.Spawn`. The original
  `ContractFramework.lua`'s own `Pg.Spawn` call sites never had this guard.
- **A tracker-compatible task object.** `Ess.Triggers.arm`/`armNamed`/`gate` and `Ess.AIOrders.command`'s
  `tracker` parameter both expect an object with real `:event(handle)`/`:guid(uGuid)` methods — a plain
  `{events={}, ...}` table literal crashes the moment a trigger actually schedules something. Every task
  bucket in the objective/support system is built through an internal constructor (`C._newTask()`) that
  returns a metatable-backed object satisfying both consumers, rather than an inline table literal.
- **A double-fire trigger bug is fixed.** In the original `ContractFramework.lua`, a support/waypoint entry
  wired to a trigger both via that trigger's own `fires={id}` list *and* via the entry's own
  `trigger={ref=id}` fired twice per activation — no deduplication between the two scan paths. `Ess.Contract`
  tracks what's already fired per trigger activation and skips a second hit.
- **Objective markers now go through `Ess.Mark.object`/`.zone`** (one combined handle covering radar + PDA +
  world-marker), replacing the original's own separately-tracked `marks`/`markers` arrays.
- **`Ess.Contract.UI.Panel`/`.Bar` are now real**, aliased straight to [`Ess.UI`](ui). The original
  `ContractFramework.lua` only ever stubbed these (`C.UI = C.UI or {}`, never implemented — its own README
  noted "need a `.gfx`; see README"). No separate `.gfx` authoring was needed here: `ui_panel.gfx`/
  `ui_bar.gfx` are the same movies `Ess.UI` itself already uses.
- **`{ onObjComplete = N }` is no longer a valid inline `trigger=` shape.** The standalone `Ess.Triggers.arm`
  vocabulary has no `onObjComplete` branch (deliberately — see the Encounter Toolkit page). Objective
  completion is now a top-level named `def.triggers` entry instead: `{ id = "...", kind = "objective", index
  = N }`, referenced from a support/waypoint entry the normal way via `trigger = { ref = "..." }`. A contract
  def authored against the original inline `{ onObjComplete = N }` shape needs updating to this form.
- **Three new support effects**: `shake` (camera shake via `Ess.Camera.shake`), `hint` (native tutorial-style
  HUD popup via `Ess.Hud.hint`), and `cinematic` (mid-mission `Ess.Cinematic` playback) — none of these
  existed in the original `ContractFramework.lua`'s effect catalog.

## The 16 objective types

The builder functions and their `def` shapes are unchanged from `ContractFramework.lua` — see
[Objectives Reference](../contract-framework/objectives) for the full depth (target sourcing, sequential vs.
parallel execution, nesting, and which of these are still flagged as draft/newer in the original source).
One-line summary of each:

| Builder | Type | Completes when |
|---|---|---|
| `Ess.Contract.Destroy{desc, spawns, objects, where, quota}` | `destroy` | `quota` (default: all) of the sourced targets are killed. |
| `Ess.Contract.Reach{desc, at, radius}` | `reach` | The player enters a radius around a point. |
| `Ess.Contract.Defend{desc, time, target}` | `defend` | `time` seconds elapse; fails immediately if `target` dies first. |
| `Ess.Contract.Collect{desc, items, quota, radius}` | `collect` | The player walks within `radius` of `quota` spawned pickup items. |
| `Ess.Contract.Escort{desc, spawn, to, radius}` | `escort` | A spawned unit/vehicle reaches the `to` zone; fails if it dies first. |
| `Ess.Contract.Enter{desc, target, spawn, seat}` | `enter` | The player boards the named/spawned vehicle's `seat` (default `"d"`). |
| `Ess.Contract.Hold{desc, at, radius, time}` | `hold` | `time` seconds accumulate inside the zone (leaving and returning keeps prior progress). |
| `Ess.Contract.Group{desc, mode, objectives}` | `group` | Its own nested objective list resolves in `mode` — full tree nesting for free. |
| `Ess.Contract.Interact{desc, target, spawn, at, radius, time}` | `interact` | The player stays within `radius` of a target/point for `time` seconds — one primitive for talk/plant/hack/sabotage. |
| `Ess.Contract.Verify{desc, target, spawn, capture, captureHealth, radius}` | `verify` | An HVT bounty: completes on kill, or (if `capture`) when adjacent while the target is at low health. |
| `Ess.Contract.Extract{desc, at, radius, boardTime, heli, victoryLap}` | `extract` | Reaching the LZ (instant if `boardTime <= 0`), or holding it `boardTime` seconds; optionally boards `heli` and flies a victory lap first. |
| `Ess.Contract.Race{desc, checkpoints, radius, time}` | `race` | Every checkpoint is reached in order; only the current one is marked. |
| `Ess.Contract.Survive{desc, time, target}` | `survive` | `time` seconds elapse (own HUD countdown); fails if the optional protected `target` dies first. |
| `Ess.Contract.Chase{desc, spawns, objects, where, escapeAt, escapeRadius, time, haste}` | `chase` | The inverse of `destroy` — sourced targets flee toward `escapeAt`; completes when all are killed, fails if any reach the escape zone. |
| `Ess.Contract.Protect{desc, target, spawn}` | `protect` | *(fail-condition only — `def.fail`, not `def.objectives`.)* Fails the contract if the target dies. |
| `Ess.Contract.StayInArea{desc, at, radius}` | `stay` | *(fail-condition only — `def.fail`.)* Fails the contract if the player leaves the radius. |

## Built on the Encounter Toolkit

`82_contract_encounter.lua`'s relations/support/AI-order/trigger subsystem — previously ~hand-rolled
contract-only internals — is now a thin layer over the standalone [Encounter Toolkit](encounter-toolkit)
namespaces (`Ess.AIOrders`, `Ess.Relations`, `Ess.Triggers`, `Ess.Sandbox`), the same machinery those
namespaces expose for use *outside* a running contract too:

- **`def.relations`** → `Ess.Relations.apply(def.relations, "Ess.Contract:<instanceId>")` /
  `.restore(handle)` — a two-line wrapper replacing what the source calls "the ~25-line hand-rolled
  snapshot/apply/restore pair this file used to carry independently."
- **`def.units`** → spawned and bucketed by group, each group registered via `Ess.AIOrders.setGroup(group,
  guids)` so `def.waypoints`/support `target=` lookups resolve. `Ess.AIOrders`' group registry is **global,
  not per-instance** — this relies on the existing "only one active contract at a time" invariant (`Accept`
  aborts any prior active instance) to avoid two contracts' groups colliding under the same name.
- **`def.waypoints`** → `Ess.AIOrders.command(guids, wp.behavior, wp, task)` per fired order.
- **`def.triggers` / `def.support[].trigger`** → each contract *instance* gets its **own**
  `Ess.Triggers.scope()`, so a trigger/gate id from a previous `Accept` (or a different instance) can never
  read as "already fired" to this one — isolation is structural now, not the string-prefix workaround
  (`ns .. t.id`) a shared global registry would otherwise need.
- **`def.sandbox`** → `Ess.Sandbox.begin(sbId, providers, opts)` / `.finish(sbId)`, keyed
  `"contract:" .. def.id`; a stale same-id sandbox from a previous accept is finished first so re-accepting
  the same contract can't strand a save-gate holder.

See [Encounter Toolkit](encounter-toolkit) for the full `AIOrders`/`Relations`/`Triggers`/`Sandbox` API —
this page only covers how `Ess.Contract` wires into it.

## `Ess.Easy.Contract`

For the common one-objective case, `Ess.Easy.Contract` (`83_contract_easy.lua`) skips `Register`+`Accept`
entirely:

```lua
Ess.Easy.Contract.destroy(sTitle, tSpawns, tOpts) -> sId
Ess.Easy.Contract.reach(sTitle, at, radius, tOpts) -> sId
-- tOpts (both) = { desc=, reward={cash=,fuel=} }
```

Each registers a throwaway single-objective contract under an auto-generated id (`"easy1"`, `"easy2"`, ...)
and accepts it immediately. See [Ess.Easy](easy) for the rest of the beginner-tier surface.

## See also

- [Contract Framework](../contract-framework/) and its children — the standalone predecessor's full
  reference (lifecycle, all 16 objectives in depth, support effects & triggers, units/AI orders/relations).
  The modder-facing shapes documented there carry over except where noted above.
- [Encounter Toolkit](encounter-toolkit) — the standalone `AIOrders`/`Relations`/`Triggers`/`Sandbox`
  namespaces `Ess.Contract` is now built on.
- [Networking](net) — why `Ess.Contract.Accept`'s co-op gate checks native `Net.*` directly.
- [Essentials (Ess)](index) — the framework index.
