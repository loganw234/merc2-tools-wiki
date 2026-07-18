---
title: "Objectives & Quests"
parent: Essentials (Ess)
nav_order: 16
---

# Objectives & Quests

## Overview

`Ess.Objective` and `Ess.Quest` (`src/59_objective.lua`) are the middle tier between two things `Ess`
already had and nothing in between: `Ess.Hud.objective("Kill 5 enemies")` — a bare text line, no state, no
counter, no completion — and `Ess.Contract` — a whole save-safe mission engine with 16 objective types,
overkill for "show a goal and know when it's met." This layer is a stateful counted goal that paints
`"label   3/5"` on the HUD objective line, ticks up as you advance it, and fires a callback at target —
built entirely out of pieces `Ess` already exposes elsewhere (`Ess.Hud.objective` for the line, `Ess.On` for
wiring completion to a world event, `Ess.Loop` underneath the ticking). No new engine calls.

Two Core-tier pieces, then the beginner-tier bundles built on them:

- **`Ess.Objective`** — one counted goal: create it, `:advance()` it, it paints the HUD line and calls
  `onComplete` at target.
- **`Ess.Quest`** — an ordered sequence of objectives shown one at a time on the same HUD line, each step
  either manual (you advance it) or auto-wired (it completes itself off a world event).
- **`Ess.Easy.Objective`** / **`Ess.Easy.Quest`** — the intent bundles: a goal already wired to a world
  event *and* its map marker, in one call — `.reach`, `.destroy`, `.clear`, `.survive`.

**Status:** this shipped in the same Unreleased batch as `Ess.On`, `Ess.Support`, and `Ess.Keys`. Per the
CHANGELOG, the state machine itself — counting, sequencing, auto-wiring, marker/watcher teardown, the
reload-safe id replace — is **execute-verified offline** (run against a stubbed loop, not just read and
believed correct), but the whole batch is explicitly flagged **not yet in-game smoke-run**. So: this is a
step above "written and internally consistent" — it has actually been executed and observed to behave —
but there is no recorded live-game pass for the Objective/Quest layer itself. The primitives it composes
(`Ess.Hud.objective`, `Ess.On.*`, `Ess.Probe.nearby`, `Ess.Mark`) are separately documented elsewhere as
already live-confirmed; this layer's own logic hasn't had that pass yet.

## Ess.Objective

```lua
local o = Ess.Objective.new{ label = "Collect intel", target = 5, onComplete = fn }
o:advance()   -- HUD shows "Collect intel   1/5", then 2/5... fires onComplete at 5
```

`Ess.Objective.new(opts) -> obj`:

| Option | Default | Notes |
|---|---|---|
| `label` | `"Objective"` | Coerced with `tostring`. |
| `target` | `1` | Coerced to a number and floored at `1` (`math.max(1, tonumber(...) or 1)`). |
| `slot` | `1` | The HUD objective-tray slot — `Ess.Hud.objective`'s newly-added second argument (see [Sound & HUD](sound-hud)); lets an objective live on a line other than a running `Ess.Contract`'s. |
| `show` | `true` | Pass `false` to keep the objective silent on the HUD (state/callbacks still work — see `:hide()`/`:show()`). |
| `onComplete` | — | Called (via `pcall`) when the goal is met or `:complete()` is forced. |
| `onProgress` | — | Called as `onProgress(count, target)` on every `:advance()`/`:set()`, including the one that completes it. |
| `onFail` | — | Called (via `pcall`) on `:fail()` only — never on `:complete()` or `:cancel()`. |
| `id` | — | A stable string makes construction **reload-safe** — see [Reload safety](#reload-safety-the-id-option). |

The HUD line is the bare label while `target <= 1`; once `target > 1` it's `"<label>   <count>/<target>"`
(three spaces). It's cleared (`Ess.Hud.objective(nil, slot)`) the moment the objective ends, matching the
base game's own objectives not lingering once met — celebrate from `onComplete` with a banner/toast if you
want the moment to land.

| Method | Signature | Notes |
|---|---|---|
| `:advance` | `obj:advance(n=1) -> obj` | Adds `n` (default `1`) to the count, clamped at `target`; repaints, fires `onProgress`, then `:complete()`s once `count >= target`. No-op once done. |
| `:set` | `obj:set(n) -> obj` | Sets the count to an absolute value, clamped to `[0, target]`; same repaint/`onProgress`/auto-complete as `:advance`. |
| `:progress` | `obj:progress() -> count, target` | Read the raw numbers. |
| `:isDone` | `obj:isDone() -> bool` | True once complete, failed, or cancelled. |
| `:label` | `obj:label(s) -> obj` | Replaces the label and repaints immediately. |
| `:complete` | `obj:complete() -> obj` | Forces the count to `target` and ends the objective, firing `onComplete`. |
| `:fail` | `obj:fail() -> obj` | Ends the objective **without** touching the count, firing `onFail`. |
| `:cancel` | `obj:cancel() -> obj` | Ends the objective silently — no `onComplete`/`onFail`. Used internally for reload-safe replace and manual abort. |
| `:hide` | `obj:hide() -> obj` | Clears the HUD line but leaves the objective live (counting/callbacks still work). |
| `:show` | `obj:show() -> obj` | Re-paints the HUD line after `:hide()`. |

`:complete()`, `:fail()`, and `:cancel()` are idempotent — each ends the objective's life exactly once; a
second call on an already-done objective is a no-op. Whichever one fires also runs teardown: any watcher or
marker the objective owns (see the `Ess.Easy.Objective` auto-wired constructors below) is torn down at that
point, not before.

## Ess.Quest

```lua
local quest = Ess.Quest.new{
    steps = {
        { reach = { 2700, -14, -780, 10 }, label = "Get to the docks" },      -- auto: arrival
        { destroy = uTowerGuid,           label = "Blow the tower" },        -- auto: it dies
        { clear = { 2700, -14, -780, 50, "VZ" }, label = "Clear them out" }, -- auto: area emptied
        "Escape",                                                            -- manual: call quest:advance()
    },
}
```

`Ess.Quest.new(opts) -> quest` sequences steps one at a time on the objective line — no manual event
wiring even for a whole linear mission. Each entry in `opts.steps` normalizes to one of four kinds:

| Step form | Kind | Behavior |
|---|---|---|
| `"some text"` (a bare string) | manual | `target = 1`; you call `quest:advance()` yourself. |
| `{ label=, target= }` | manual, counted | A manual goal with `target > 1`; advance it in increments. |
| `{ reach = {x,y,z,r}, label= }` | auto | Built through `Ess.Easy.Objective.reach` — completes on arrival, drops a ground ring. |
| `{ destroy = guid, label= }` | auto | Built through `Ess.Easy.Objective.destroy` — completes when that object dies, marks it. |
| `{ clear = {x,y,z,r,faction}, label= }` | auto | Built through `Ess.Easy.Objective.clear` — completes when the area's polled clear, marks the zone. |

| Option | Default | Notes |
|---|---|---|
| `steps` | `{}` | The list above. |
| `slot` | `1` | The HUD tray slot for **manual** steps only — see the gotcha below. |
| `showCounter` | `true` | With more than one step, prefixes the label `"(i/total) "`. |
| `onStep` | — | Called as `onStep(i, total)` each time a step completes and the quest advances. |
| `onComplete` | — | Called once the last step completes. |

| Method | Signature | Notes |
|---|---|---|
| `:advance` | `quest:advance(n) -> quest` | Forwards to the current step's `Ess.Objective:advance(n)`. |
| `:skip` | `quest:skip() -> quest` | Force-completes the current step regardless of kind (calls its `:complete()`), advancing to the next. |
| `:current` | `quest:current() -> obj \| nil` | The live `Ess.Objective` backing the current step. |
| `:step` | `quest:step() -> i, total` | Current step index and total step count. |
| `:isDone` | `quest:isDone() -> bool` | True once every step has resolved. |
| `:cancel` | `quest:cancel() -> quest` | Cancels the current step's objective (silent), marks the quest done, clears the HUD slot. |

**Gotcha: the auto step kinds (`reach`/`destroy`/`clear`) always land on HUD slot 1**, because they're
built through the `Ess.Easy.Objective` constructors, which don't take a slot argument — `opts.slot` on
`Ess.Quest.new` only applies to **manual** steps. A quest mixing manual and auto steps on a non-default
slot will see its manual steps move but its auto steps stay on slot 1.

## Ess.Easy.Objective

`Ess.Easy.Objective` is a **callable table**: calling it directly makes a plain manual goal, while its
`.reach`/`.destroy`/`.clear`/`.survive` fields are the auto-wired intent presets — the whole "show goal +
mark it + detect + clean up" loop in one call, no polling or event glue on the caller's side.

| Call | Signature | What it wires |
|---|---|---|
| (bare call) | `Ess.Easy.Objective(label, target, onComplete) -> obj` | A plain manual goal — `Ess.Objective.new{label=label, target=target, onComplete=onComplete}` verbatim. No `id`/`slot`/`show`/`onProgress`/`onFail` — use `Ess.Objective.new` directly if you need those. |
| `.reach` | `Ess.Easy.Objective.reach(x, y, z, r=8, label, onDone) -> obj` | Completes the instant the player comes within `r` of `(x,y,z)`. Drops a "go here" ground ring ([`Ess.Easy.Mark.zone`](mark)) and wires [`Ess.On.enterArea`](reactive-hotkeys) to call `:advance()` on entry. Default label `"Reach the marker"`. |
| `.destroy` | `Ess.Easy.Objective.destroy(guid, label, onDone) -> obj` | Completes when the object at `guid` dies. Marks it on radar + PDA + world icon ([`Ess.Easy.Mark.objective`](mark)) and wires [`Ess.On.death`](reactive-hotkeys). Default label `"Destroy the target"`. |
| `.clear` | `Ess.Easy.Objective.clear(x, y, z, r=40, faction, label, onDone) -> obj` | Completes once every matching unit in the zone is dead. Default label `"Clear the area"`. |
| `.survive` | `Ess.Easy.Objective.survive(seconds, label, onDone, onFail) -> obj` | A live countdown; completes after `seconds`, fails if the local player dies first. Default label `"Survive"`. |

**`.reach(x, y, z, r=8, label, onDone)`** — `r` defaults to `8` ("you're here"-comfortable). Under the hood
it's `Ess.Objective.new{label=..., target=1, onComplete=onDone}` plus a zone marker and an
[`Ess.On.enterArea`](reactive-hotkeys) watcher, both registered as teardown on the objective so they're torn
down the instant it resolves (complete, fail, or cancel).

**`.destroy(guid, label, onDone)`** — for a target you already hold the guid of (as opposed to `.clear`,
which has no target guid at all). Marks with `Ess.Easy.Mark.objective` (all three surfaces: radar, PDA,
floating world icon) and wires [`Ess.On.death(guid, ...)`](reactive-hotkeys).

**`.clear(x, y, z, r=40, faction, label, onDone)`** — "eliminate every `faction` unit in this area." The
engine has no clean per-kill event to hang this off of, so it **polls** instead: every second
([`Ess.On.tick(1, ...)`](reactive-hotkeys)) it re-runs [`Ess.Probe.nearby(x, y, z, r, "humans", faction)`](identity-query#ess-probe)
and completes the instant the count hits zero. The label live-updates to show the remaining count —
`"Clear the area   4 left"` — recomputed at construction time too, so the very first paint already shows
an accurate number. `faction` is an `Object.HasLabel` string (e.g. `"VZ"`); leave it `nil` to count *every*
human in the radius, not just one faction. Marks the zone with a ground ring only (`Ess.Easy.Mark.zone`) —
no radar/PDA clutter for what could be several targets.

**`.survive(seconds, label, onDone, onFail)`** — `seconds` is clamped to at least `1` (falls back to `30`
if not a number). The label counts down every second — `"Survive   12s"` — via the same `Ess.On.tick(1,...)`
pattern, and calls `:complete()` (firing `onDone`) when it reaches zero. Separately, it resolves
`Ess.Player.character(0)` once at construction and, **only if that resolves to a real guid**, wires
[`Ess.On.death`](reactive-hotkeys) on it to `:fail()` the objective (firing `onFail`) if the player dies
before the timer runs out. If the local character can't be resolved at construction, the fail-watcher is
silently never wired — the countdown still completes on schedule, it just has no fail condition. No map
marker is dropped (a "survive" goal has no single point to mark).

## Ess.Easy.Quest

`Ess.Easy.Quest(steps, onComplete) -> quest` — the one-liner form of `Ess.Quest.new{steps=steps,
onComplete=onComplete}`. No `slot`/`showCounter`/`onStep` control at this tier; reach for `Ess.Quest.new`
directly for those.

## Reload safety: the `id` option

`Ess.Objective.new{id="some_id", ...}` is **reload-safe**: re-creating an objective with an id already in
use silently `:cancel()`s the prior instance (no `onComplete`/`onFail`, teardown still runs — its watchers
and markers are torn down) before the replacement takes its place in `Ess.Objective._active`. This is the
same pattern `Ess.Loop.start`'s own `id` argument uses (see [Timing & Input](timing-input#ess-loop)) — it
matters because an `OnLoad`/`OnKey` script that re-runs its own setup (a save reload, a hotkey re-trigger)
would otherwise leave the *previous* objective's wired `Ess.On` watcher armed alongside a brand-new one,
double-firing `:advance()` on the same world event.

`Ess.Quest.new` has **no `id` option** in the current source — a quest itself isn't part of the reload-safe
registry, and neither are the individual step objectives it builds internally (they're constructed without
an `id`). If a quest needs to survive a reload cleanly, hold the `quest` reference in whatever reload-safe
state your script already keeps (`Ess.SaveVar`/a module-level guarded table — see
[Core Primitives](core)), and `:cancel()` the old one yourself before building a new one.

## Worked example

The real recipe, `samples/recipes/a_quick_mission.lua` (quoted verbatim) — a two-step quest: an auto
`reach` step, then a manual step, force-advanced with `:skip()` to prove the sequencer without having to
walk there:

```lua
-- RECIPE: a whole linear MISSION in one table -- no Contract, no manual event wiring. Each step shows on the
-- HUD objective line and (for the auto kinds) completes itself + drops its own marker. This is the light
-- middle tier: heavier than a single Ess.Objective, far lighter than a save-safe Ess.Contract.
-- Namespaces: Ess.Quest, Ess.Easy.Objective, Ess.Player, Ess.Math.

local Ess = _G.Ess
if not Ess then if Loader and Loader.Printf then Loader.Printf("[recipe] load Ess first") end return end

local x, y, z, yaw = Ess.Player.pose(0)
if not x then Ess.Log("[SMOKE] a_quick_mission: FAIL (no player position)") return end

-- a point ~25u ahead of you to walk to (the first step's destination)
local ax, az = Ess.Math.pointAhead(x, z, yaw or 0, 25)

-- a two-step quest: an AUTO "reach" step (completes when you arrive) then a MANUAL "return" step.
local quest = Ess.Quest.new{
    steps = {
        { reach = { ax, y, az, 8 }, label = "Advance to the marker" },   -- auto: fires on arrival
        "Return to safety",                                             -- manual: call quest:advance()
    },
    onStep = function(i, t) Ess.Log("[recipe] a_quick_mission: cleared step " .. i .. "/" .. t) end,
    onComplete = function() Ess.Easy.Toast("Mission complete!") end,
}

-- prove the sequencer works live without having to walk there: skip() force-completes the current step, which
-- should advance us from step 1 to step 2.
local i0 = select(1, quest:step())     -- 1
quest:skip()                           -- force step 1 done -> advances to step 2
local i1 = select(1, quest:step())     -- 2
local ok = (i0 == 1 and i1 == 2 and not quest:isDone())

-- tidy up after 20s (a real mod leaves the quest up until the player finishes it)
Ess.Easy.Triggers.after(20, function() pcall(function() quest:cancel() end) end)

Ess.Log("[recipe] a_quick_mission: quest advanced to step 2/2 ('Return to safety') on the HUD")
Ess.Log("[SMOKE] a_quick_mission: " .. (ok and "PASS" or "FAIL"))
```

## See also

- [Sound & HUD](sound-hud) — `Ess.Hud.objective`, the bare HUD primitive this layer builds on.
- [Markers](mark) — `Ess.Easy.Mark.zone`/`.objective`, what the auto-wired constructors drop and clear.
- [Reactive Hotkeys](reactive-hotkeys) — `Ess.On.enterArea`/`.death`/`.tick`, the world-event wiring behind
  `.reach`/`.destroy`/`.clear`/`.survive`.
- [Identity & World Query](identity-query#ess-probe) — `Ess.Probe.nearby`, what `.clear` polls in place of a
  per-kill event.
- [Objectives Reference](../contract-framework/objectives) — the older, heavier-weight objective system this
  sits below. It's a **different** system, not a replacement: that page covers the 16 objective types built
  into the standalone Contract Framework, and `Ess.Objective`/`Ess.Quest` don't touch or require a running
  `Ess.Contract` at all. `Ess.Contract` itself (the native port of that same engine) is documented separately
  on [Contract Engine](contract).
